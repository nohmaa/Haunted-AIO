"""Negative tests for the signed Next.js -> FastAPI trust boundary."""

import hashlib
import hmac
import unittest

from api.proxy_auth import (
    ProxyAuthError,
    clear_nonce_cache_for_tests,
    enforce_user_rate_limit,
    ProxyRateLimitError,
    validate_proxy_scope,
    verify_proxy_signature,
    api_key_matches,
    canonical_request_target,
)


SECRET = "a-test-only-proxy-secret-at-least-32-bytes"
BODY = b'{"enabled":false}'
NOW = 1_800_000_000


def signed_headers(
    *,
    method: str = "PATCH",
    path: str = "/api/v1/guilds/123/modules/automod",
    body: bytes = BODY,
    timestamp: int = NOW,
    nonce: str = "A_valid_test_nonce_value_123456",
    user_id: str = "456",
    scope: str = "guild:123",
) -> dict[str, str]:
    digest = hashlib.sha256(body).hexdigest()
    message = "\n".join(
        (method, path, digest, str(timestamp), nonce, user_id, scope)
    )
    signature = hmac.new(SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    return {
        "X-Haunted-Proxy-User": user_id,
        "X-Haunted-Proxy-Scope": scope,
        "X-Haunted-Proxy-Timestamp": str(timestamp),
        "X-Haunted-Proxy-Nonce": nonce,
        "X-Haunted-Proxy-Signature": signature,
    }


class ProxySignatureTests(unittest.TestCase):
    def setUp(self):
        clear_nonce_cache_for_tests()

    def test_accepts_valid_signed_guild_request(self):
        identity = verify_proxy_signature(
            method="PATCH",
            path_and_query="/api/v1/guilds/123/modules/automod",
            body=BODY,
            headers=signed_headers(),
            secret=SECRET,
            now=NOW,
        )
        self.assertEqual(identity, ("456", "guild:123"))

    def test_rejects_absent_signature(self):
        with self.assertRaises(ProxyAuthError):
            verify_proxy_signature(
                method="GET", path_and_query="/api/v1/guilds/123", body=b"",
                headers={}, secret=SECRET, now=NOW,
            )

    def test_rejects_short_or_missing_shared_secret(self):
        for secret in ("", "short"):
            with self.subTest(secret_length=len(secret)):
                with self.assertRaises(ProxyAuthError):
                    verify_proxy_signature(
                        method="PATCH",
                        path_and_query="/api/v1/guilds/123/modules/automod",
                        body=BODY,
                        headers=signed_headers(),
                        secret=secret,
                        now=NOW,
                    )

    def test_rejects_expired_session_request(self):
        with self.assertRaisesRegex(ProxyAuthError, "expired"):
            verify_proxy_signature(
                method="PATCH",
                path_and_query="/api/v1/guilds/123/modules/automod",
                body=BODY,
                headers=signed_headers(timestamp=NOW - 61),
                secret=SECRET,
                now=NOW,
            )

    def test_rejects_overlong_path(self):
        path = "/api/v1/bot/info?" + ("q" * 4090)
        with self.assertRaisesRegex(ProxyAuthError, "too long"):
            verify_proxy_signature(
                method="GET",
                path_and_query=path,
                body=b"",
                headers=signed_headers(method="GET", path=path, body=b"", nonce="A_long_path_nonce_value_123456"),
                secret=SECRET,
                now=NOW,
            )

    def test_signature_binds_method_path_body_identity_and_scope(self):
        cases = (
            {"method": "GET"},
            {"path_and_query": "/api/v1/guilds/999/modules/automod"},
            {"body": b'{"enabled":true}'},
        )
        for change in cases:
            with self.subTest(change=change):
                with self.assertRaises(ProxyAuthError):
                    input_values = {
                        "method": "PATCH",
                        "path_and_query": "/api/v1/guilds/123/modules/automod",
                        "body": BODY,
                    }
                    input_values.update(change)
                    verify_proxy_signature(
                        **input_values,
                        headers=signed_headers(),
                        secret=SECRET,
                        now=NOW,
                    )

    def test_rejects_replayed_nonce(self):
        args = dict(
            method="PATCH",
            path_and_query="/api/v1/guilds/123/modules/automod",
            body=BODY,
            headers=signed_headers(),
            secret=SECRET,
            now=NOW,
        )
        verify_proxy_signature(**args)
        with self.assertRaisesRegex(ProxyAuthError, "already used"):
            verify_proxy_signature(**args)

    def test_nonce_cache_fails_closed_at_capacity(self):
        from api import proxy_auth

        old_limit = proxy_auth._MAX_NONCE_ENTRIES
        try:
            proxy_auth._MAX_NONCE_ENTRIES = 0
            with self.assertRaisesRegex(ProxyAuthError, "capacity"):
                verify_proxy_signature(
                    method="PATCH",
                    path_and_query="/api/v1/guilds/123/modules/automod",
                    body=BODY,
                    headers=signed_headers(),
                    secret=SECRET,
                    now=NOW,
                )
        finally:
            proxy_auth._MAX_NONCE_ENTRIES = old_limit

    def test_rate_limiter_bounds_tracked_user_state(self):
        from api import proxy_auth

        old_limit = proxy_auth._MAX_RATE_LIMIT_USERS
        try:
            proxy_auth._MAX_RATE_LIMIT_USERS = 1
            enforce_user_rate_limit("first-user", now=NOW)
            with self.assertRaises(ProxyRateLimitError):
                enforce_user_rate_limit("second-user", now=NOW)
        finally:
            proxy_auth._MAX_RATE_LIMIT_USERS = old_limit

    def test_rejects_guild_scope_mismatch_shape(self):
        self.assertFalse(validate_proxy_scope("/api/v1/guilds/123/modules", "guild:999"))

    def test_admin_scope_cannot_be_used_for_guild_or_bot_data(self):
        self.assertFalse(validate_proxy_scope("/api/v1/admin/config", "dashboard"))
        self.assertFalse(validate_proxy_scope("/api/v1/guilds/123/prefix", "admin"))
        self.assertTrue(validate_proxy_scope("/api/v1/admin/config", "admin"))
        self.assertTrue(validate_proxy_scope("/api/v1/bot/status", "dashboard"))

    def test_api_key_rotation_accepts_only_active_or_explicit_previous_value(self):
        self.assertTrue(api_key_matches("active-key", "active-key"))
        self.assertTrue(api_key_matches("old-key", "active-key", "old-key"))
        self.assertFalse(api_key_matches("old-key", "active-key"))
        self.assertFalse(api_key_matches("anything", None, None))

    def test_request_target_preserves_encoded_unicode_and_query(self):
        self.assertEqual(
            canonical_request_target(b"/api/v1/guilds/123/vanityroles/caf%C3%A9", b"page=1", "/decoded"),
            "/api/v1/guilds/123/vanityroles/caf%C3%A9?page=1",
        )

    def test_abusive_request_rate_is_limited_per_authenticated_user(self):
        for _ in range(120):
            enforce_user_rate_limit("456", now=NOW)
        with self.assertRaises(ProxyRateLimitError):
            enforce_user_rate_limit("456", now=NOW)
        # A separate authenticated identity has its own budget.
        enforce_user_rate_limit("789", now=NOW)
        # Requests older than a minute age out of the window.
        enforce_user_rate_limit("456", now=NOW + 60)

    def test_previous_hmac_key_can_verify_during_rotation(self):
        old_secret = "previous-test-secret-for-rotation-at-least-32-bytes"
        digest = hashlib.sha256(BODY).hexdigest()
        nonce = "A_previous_key_nonce_value_123456"
        message = "\n".join(
            ("PATCH", "/api/v1/guilds/123/modules/automod", digest, str(NOW), nonce, "456", "guild:123")
        )
        signature = hmac.new(old_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = signed_headers(nonce=nonce)
        headers["X-Haunted-Proxy-Signature"] = signature
        self.assertEqual(
            verify_proxy_signature(
                method="PATCH",
                path_and_query="/api/v1/guilds/123/modules/automod",
                body=BODY,
                headers=headers,
                secret=old_secret,
                now=NOW,
            ),
            ("456", "guild:123"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""FastAPI dependency authorization tests; no Discord connection is opened."""

import asyncio
import os
import pathlib
import sys
import unittest
from unittest.mock import patch
from unittest.mock import Mock

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials

BOT_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))

SECRET = "integration-test-hmac-secret-with-at-least-32-bytes"
API_KEY = "integration-test-api-key"
USER_ID = "456"
NOW = 1_800_000_000


def make_request(method: str, path: str, headers: dict[str, str] | None = None) -> Request:
    raw_headers = [(key.lower().encode(), value.encode()) for key, value in (headers or {}).items()]
    delivered = False

    async def receive():
        nonlocal delivered
        if delivered:
            return {"type": "http.disconnect"}
        delivered = True
        return {"type": "http.request", "body": b"", "more_body": False}

    return Request(
        {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1",
            "method": method,
            "scheme": "https",
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": b"",
            "root_path": "",
            "headers": raw_headers,
            "server": ("test", 443),
            "client": ("127.0.0.1", 12345),
        },
        receive=receive,
    )


def make_signed_headers(method: str, path: str, scope: str) -> dict[str, str]:
    import hashlib
    import hmac

    timestamp = str(NOW)
    nonce = "test-nonce-" + __import__("secrets").token_urlsafe(24)
    body_hash = hashlib.sha256(b"").hexdigest()
    canonical = "\n".join((method, path, body_hash, timestamp, nonce, USER_ID, scope))
    signature = hmac.new(SECRET.encode(), canonical.encode(), hashlib.sha256).hexdigest()
    return {
        "Authorization": f"Bearer {API_KEY}",
        "X-Haunted-Proxy-User": USER_ID,
        "X-Haunted-Proxy-Scope": scope,
        "X-Haunted-Proxy-Timestamp": timestamp,
        "X-Haunted-Proxy-Nonce": nonce,
        "X-Haunted-Proxy-Signature": signature,
    }


class ApiAuthDependencyTests(unittest.TestCase):
    def setUp(self):
        from api.proxy_auth import clear_nonce_cache_for_tests

        clear_nonce_cache_for_tests()
        self.env = patch.dict(
            os.environ,
            {
                "DASHBOARD_API_KEY": API_KEY,
                "DASHBOARD_API_KEY_PREVIOUS": "",
                "DASHBOARD_PROXY_SECRET": SECRET,
                "DASHBOARD_PROXY_SECRET_PREVIOUS": "",
            },
            clear=False,
        )
        self.env.start()
        self.now = patch("api.proxy_auth.time.time", return_value=NOW)
        self.now.start()

    def tearDown(self):
        from api.dependencies import set_bot

        set_bot(None)
        self.now.stop()
        self.env.stop()
        os.environ.pop("DASHBOARD_API_KEY_PREVIOUS", None)

    def _verify(self, method: str, path: str, headers: dict[str, str]):
        from api.dependencies import verify_api_key

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials=headers.get("Authorization", "").removeprefix("Bearer ")
        )
        return asyncio.run(verify_api_key(make_request(method, path, headers), credentials))

    def test_missing_bearer_key_is_rejected(self):
        with self.assertRaises(HTTPException) as raised:
            self._verify("GET", "/api/v1/bot/status", {})
        self.assertEqual(raised.exception.status_code, 401)

    def test_bearer_key_without_proxy_signature_is_rejected(self):
        with self.assertRaises(HTTPException) as raised:
            self._verify("GET", "/api/v1/bot/status", {"Authorization": f"Bearer {API_KEY}"})
        self.assertEqual(raised.exception.status_code, 401)

    def test_guild_scope_cannot_be_replayed_against_another_guild(self):
        path = "/api/v1/guilds/999/prefix"
        headers = make_signed_headers("GET", path, "guild:123")
        with self.assertRaises(HTTPException) as raised:
            self._verify("GET", path, headers)
        self.assertEqual(raised.exception.status_code, 403)

    def test_guild_route_requires_bot_presence(self):
        import api.dependencies as dependencies
        from api.dependencies import set_bot

        bot = Mock()
        bot.get_guild.return_value = None
        set_bot(bot)
        path = "/api/v1/guilds/123/prefix"
        with patch.object(dependencies, "get_bot", return_value=bot):
            with self.assertRaises(HTTPException) as raised:
                self._verify("GET", path, make_signed_headers("GET", path, "guild:123"))
        self.assertEqual(raised.exception.status_code, 404)

    def test_valid_scope_still_requires_bot_presence_and_accepts_present_bot(self):
        import api.dependencies as dependencies
        from api.dependencies import set_bot

        guild = object()
        bot = Mock()
        bot.get_guild.return_value = guild
        set_bot(bot)
        path = "/api/v1/guilds/123/prefix"
        with patch.object(dependencies, "get_bot", return_value=bot):
            self.assertEqual(
                self._verify("GET", path, make_signed_headers("GET", path, "guild:123")),
                USER_ID,
            )

    def test_admin_resource_rejects_dashboard_scope(self):
        path = "/api/v1/admin/config"
        with self.assertRaises(HTTPException) as raised:
            self._verify("GET", path, make_signed_headers("GET", path, "dashboard"))
        self.assertEqual(raised.exception.status_code, 403)

    def test_previous_bearer_key_without_signature_is_rejected(self):
        os.environ["DASHBOARD_API_KEY_PREVIOUS"] = "old-rotated-api-key"
        with self.assertRaises(HTTPException) as raised:
            self._verify(
                "GET",
                "/api/v1/bot/status",
                {"Authorization": "Bearer old-rotated-api-key"},
            )
        self.assertEqual(raised.exception.status_code, 401)


if __name__ == "__main__":
    unittest.main(verbosity=2)

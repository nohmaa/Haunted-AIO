"""Authentication for requests forwarded by the trusted Next.js dashboard."""

from __future__ import annotations

import hashlib
import hmac
import re
import threading
from collections import deque
import time
from typing import Mapping

_NONCE_TTL_SECONDS = 90
_NONCE_CACHE: dict[str, int] = {}
_NONCE_LOCK = threading.Lock()
_USER_REQUESTS: dict[str, deque[int]] = {}
_RATE_LIMIT_PER_MINUTE = 120
_MAX_NONCE_ENTRIES = 100_000
_MAX_RATE_LIMIT_USERS = 10_000


class ProxyAuthError(ValueError):
    """A signed dashboard request is missing, expired, or invalid."""


class ProxyRateLimitError(ValueError):
    """The authenticated dashboard identity exceeded its request budget."""


def verify_proxy_signature(
    *,
    method: str,
    path_and_query: str,
    body: bytes,
    headers: Mapping[str, str],
    secret: str,
    now: int | None = None,
) -> tuple[str, str]:
    """Verify a time-bounded HMAC and reject replayed nonces.

    The canonical format is shared with ``dashboard/lib/proxy-signature.ts``.
    This module uses only the standard library so its negative cases can be
    tested without starting Discord or FastAPI.
    """

    if len(secret.encode("utf-8")) < 32:
        raise ProxyAuthError("Dashboard proxy secret is not configured securely.")

    normalized = {str(key).lower(): str(value) for key, value in headers.items()}
    user_id = normalized.get("x-haunted-proxy-user", "")
    scope = normalized.get("x-haunted-proxy-scope", "")
    timestamp = normalized.get("x-haunted-proxy-timestamp", "")
    nonce = normalized.get("x-haunted-proxy-nonce", "")
    supplied_signature = normalized.get("x-haunted-proxy-signature", "")

    if not re.fullmatch(r"\d{1,20}", user_id):
        raise ProxyAuthError("Invalid proxy user.")
    if not re.fullmatch(r"(?:dashboard|admin|guild:\d{1,20})", scope):
        raise ProxyAuthError("Invalid proxy scope.")
    if not re.fullmatch(r"\d{1,10}", timestamp):
        raise ProxyAuthError("Invalid proxy timestamp.")
    if not re.fullmatch(r"[A-Za-z0-9_-]{20,64}", nonce):
        raise ProxyAuthError("Invalid proxy nonce.")
    if not re.fullmatch(r"[a-f0-9]{64}", supplied_signature):
        raise ProxyAuthError("Invalid proxy signature.")

    current_time = int(time.time()) if now is None else now
    if abs(current_time - int(timestamp)) > 60:
        raise ProxyAuthError("Proxy request expired.")

    # Periodically bound memory while keeping a nonce reserved for the entire
    # acceptance window. Requests run in one bot process in supported deploys.
    nonce_key = f"{user_id}:{nonce}"
    digest = hashlib.sha256(body).hexdigest()
    if len(path_and_query) > 4096:
        raise ProxyAuthError("Proxy request path is too long.")
    message = "\n".join(
        (method.upper(), path_and_query, digest, timestamp, nonce, user_id, scope)
    )
    expected_signature = hmac.new(
        secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(supplied_signature, expected_signature):
        raise ProxyAuthError("Invalid proxy signature.")

    with _NONCE_LOCK:
        for cached_nonce, expires_at in list(_NONCE_CACHE.items()):
            if expires_at < current_time:
                _NONCE_CACHE.pop(cached_nonce, None)
        if nonce_key in _NONCE_CACHE:
            raise ProxyAuthError("Proxy request was already used.")
        if len(_NONCE_CACHE) >= _MAX_NONCE_ENTRIES:
            raise ProxyAuthError("Proxy replay protection is temporarily at capacity.")
        _NONCE_CACHE[nonce_key] = current_time + _NONCE_TTL_SECONDS
    return user_id, scope


def validate_proxy_scope(path: str, scope: str) -> bool:
    """Bind the signed scope to the API resource being requested."""
    guild_match = re.match(r"^/api/v1/guilds/(\d+)(?:/|$)", path)
    if guild_match:
        return scope == f"guild:{guild_match.group(1)}"
    if path.startswith("/api/v1/admin/"):
        return scope == "admin"
    if (
        path.startswith("/api/v1/bot/")
        or path in ("/api/v1/guilds", "/api/v1/guilds/", "/api/v1/public/notification")
    ):
        return scope == "dashboard"
    return False


def api_key_matches(supplied: str, current: str | None, previous: str | None = None) -> bool:
    """Constant-time match against active and (during rotation) previous keys."""
    candidates = [key for key in (current, previous) if key]
    # Every accepted request must additionally carry a fresh HMAC signature;
    # the previous Bearer key is only a rotation aid, never sufficient alone.
    return bool(candidates) and any(hmac.compare_digest(supplied, key) for key in candidates)


def canonical_request_target(raw_path: bytes | None, raw_query: bytes, fallback_path: str) -> str:
    """Preserve percent-encoding so Next.js and ASGI sign the same request target."""
    path = raw_path.decode("ascii") if raw_path else fallback_path
    query = raw_query.decode("ascii")
    return f"{path}?{query}" if query else path


def enforce_user_rate_limit(user_id: str, *, now: int | None = None) -> None:
    """Allow at most 120 authenticated requests per user in a rolling minute."""
    current_time = int(time.time()) if now is None else now
    with _NONCE_LOCK:
        if len(_USER_REQUESTS) > 1024:
            for stale_user, timestamps in list(_USER_REQUESTS.items()):
                while timestamps and timestamps[0] <= current_time - 60:
                    timestamps.popleft()
                if not timestamps:
                    _USER_REQUESTS.pop(stale_user, None)
        if user_id not in _USER_REQUESTS and len(_USER_REQUESTS) >= _MAX_RATE_LIMIT_USERS:
            raise ProxyRateLimitError("Authenticated user rate-limit capacity reached.")
        timestamps = _USER_REQUESTS.setdefault(user_id, deque())
        while timestamps and timestamps[0] <= current_time - 60:
            timestamps.popleft()
        if len(timestamps) >= _RATE_LIMIT_PER_MINUTE:
            raise ProxyRateLimitError("Dashboard request rate limit exceeded.")
        timestamps.append(current_time)


def clear_nonce_cache_for_tests() -> None:
    """Reset replay state between isolated unit tests."""
    with _NONCE_LOCK:
        _NONCE_CACHE.clear()
        _USER_REQUESTS.clear()

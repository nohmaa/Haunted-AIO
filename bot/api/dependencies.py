# ╔══════════════════════════════════════════════════════════════════╗
# ║                                                                  ║
# ║   ░█▀▀░█▀█░█▀▄░█▀▀░█░█   ░█▀▄░█▀▀░█░█░█▀▀                     ║
# ║   ░█░░░█░█░█░█░█▀▀░▄▀▄   ░█░█░█▀▀░▀▄▀░▀▀█                     ║
# ║   ░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀░▀   ░▀▀░░▀▀▀░░▀░░▀▀▀                     ║
# ║                                                                  ║
# ║            © 2026 Arsonist   — All Rights Reserved              ║
# ║                                                                  ║
# ║   discord  ──  https://discord.gg/DvetGPq9q5                    ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

import os
import re
from typing import Optional, TYPE_CHECKING
from fastapi import HTTPException, Depends, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from slowapi import Limiter
from slowapi.util import get_remote_address
from api.proxy_auth import (
    ProxyAuthError,
    ProxyRateLimitError,
    api_key_matches,
    canonical_request_target,
    enforce_user_rate_limit,
    validate_proxy_scope,
    verify_proxy_signature,
)

if TYPE_CHECKING:
    from core.zyrox import zyrox

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["1000 per minute"])

# Global reference to the bot instance
_bot_instance: Optional["zyrox"] = None

# Security scheme
security = HTTPBearer()

async def verify_api_key(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """
    Dependency to verify the API key from the Authorization header.
    Expected: Authorization: Bearer <API_KEY>
    """
    api_key = os.getenv("DASHBOARD_API_KEY")
    previous_api_key = os.getenv("DASHBOARD_API_KEY_PREVIOUS")

    if not api_key and not previous_api_key:
        raise HTTPException(
            status_code=500,
            detail="DASHBOARD_API_KEY environment variable is not set."
        )

    if not api_key_matches(credentials.credentials, api_key, previous_api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key."
        )

    proxy_secret = os.getenv("DASHBOARD_PROXY_SECRET", "")
    if len(proxy_secret.encode("utf-8")) < 32:
        raise HTTPException(status_code=503, detail="Dashboard proxy signing is not configured.")
    previous_proxy_secret = os.getenv("DASHBOARD_PROXY_SECRET_PREVIOUS", "")
    if "x-haunted-proxy-signature" not in request.headers:
        raise HTTPException(status_code=401, detail="Signed dashboard proxy credentials required.")

    body = await request.body()
    signature_error = None
    for signing_secret in (proxy_secret, previous_proxy_secret):
        if len(signing_secret.encode("utf-8")) < 32:
            continue
        try:
            user_id, scope = verify_proxy_signature(
                method=request.method,
                path_and_query=canonical_request_target(
                    request.scope.get("raw_path"),
                    request.scope.get("query_string", b""),
                    request.url.path,
                ),
                body=body,
                headers=request.headers,
                secret=signing_secret,
            )
            break
        except ProxyAuthError as exc:
            signature_error = exc
    else:
        status_code = 503 if "capacity" in str(signature_error).lower() else 401
        raise HTTPException(status_code=status_code, detail="Invalid or expired dashboard proxy credentials.") from signature_error
    try:
        enforce_user_rate_limit(user_id)
    except ProxyRateLimitError as exc:
        raise HTTPException(status_code=429, detail="Trop de requêtes dashboard ; réessayez dans une minute.") from exc

    path = request.url.path
    guild_match = re.match(r"^/api/v1/guilds/(\d+)(?:/|$)", path)
    if not validate_proxy_scope(path, scope):
        raise HTTPException(status_code=403, detail="Dashboard proxy scope does not match this resource.")

    if guild_match:
        bot = get_bot()
        if bot.get_guild(int(guild_match.group(1))) is None:
            raise HTTPException(status_code=404, detail="Bot is not present in this guild.")

    # Keep the authenticated identity available for request-scoped auditing.
    request.state.dashboard_user_id = user_id
    request.state.dashboard_scope = scope
    return user_id

def set_bot(bot_instance: "zyrox"):
    """
    Sets the global bot instance. 
    This should be called in haunted.py during startup.
    """
    global _bot_instance
    _bot_instance = bot_instance

def get_bot() -> "zyrox":
    """
    FastAPI dependency to retrieve the Discord bot instance.
    Usage: bot: zyrox = Depends(get_bot)
    """
    if _bot_instance is None:
        raise HTTPException(
            status_code=503, 
            detail="Discord bot instance is not initialized yet."
        )
    return _bot_instance

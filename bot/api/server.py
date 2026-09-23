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

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import time
import json
import logging
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from utils.config import *


from api.routes import bot, guilds, admin, modules
from api.dependencies import verify_api_key, limiter
from api.db_manager import db_manager

# Configure logging
logger = logging.getLogger("api_request_logs")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: Nothing special needed for now
    yield
    # Shutdown: Close all shared database connections
    await db_manager.close_all()

def _expand_cors_origins(origins: list) -> list:
    """Ajoute automatiquement la variante www/apex de chaque origine.

    Évite l'erreur classique : dashboard sur `www.domaine.com` alors que
    seule `https://domaine.com` est dans CORS_ORIGINS (ou l'inverse).
    """
    from urllib.parse import urlsplit, urlunsplit

    expanded: list = []
    for origin in origins:
        origin = (origin or "").strip().rstrip("/")
        if not origin or origin in expanded:
            continue
        expanded.append(origin)
        try:
            parts = urlsplit(origin)
            host = parts.hostname or ""
            port = f":{parts.port}" if parts.port else ""
            if host.startswith("www."):
                alt_host = host[4:]
            elif host and "." in host and host != "localhost":
                alt_host = "www." + host
            else:
                alt_host = None
            if alt_host:
                alt = urlunsplit((parts.scheme, alt_host + port, "", "", ""))
                if alt not in expanded:
                    expanded.append(alt)
        except Exception:
            continue
    return expanded

def create_app() -> FastAPI:
    """
    Initializes the FastAPI application for the Haunted Bot Dashboard.
    The bot instance will be attached to app.state.bot in haunted.py at runtime.
    """
    # NOTE: auth moved from app-level to per-router so that / and /health stay
    # public — a health check must be reachable without a key to monitor the API
    # and distinguish "tunnel down" from "API broken".
    app = FastAPI(
        title=f"{BRAND_NAME} Bot API",
        description=f"REST API to manage the {BRAND_NAME} Discord Bot features",
        version="1.0",
        lifespan=lifespan
    )

    # Structured Logging Middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        log_data = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(process_time * 1000, 2),
            "client_ip": request.client.host if request.client else "unknown"
        }
        
        logger.info(json.dumps(log_data))
        return response

    # Attach limiter and handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    # Build allowed origins from env + hardcoded fallbacks
    _extra_origins = [
        o.strip()
        for o in os.getenv("CORS_ORIGINS", "").split(",")
        if o.strip()
    ]
    _allowed_origins = _expand_cors_origins([
        "http://localhost:3000",
        "https://localhost:3000",
        "https://dashboard.votredomaine.com",
        *_extra_origins,
    ])

    # Enable CORS for Next.js dashboard
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Routers (all require the Bearer API key)
    _auth = [Depends(verify_api_key)]
    app.include_router(bot.router, prefix="/api/v1/bot", tags=["Bot"], dependencies=_auth)
    app.include_router(guilds.router, prefix="/api/v1/guilds", tags=["Guilds"], dependencies=_auth)
    app.include_router(modules.router, prefix="/api/v1/guilds", tags=["Modules"], dependencies=_auth)
    app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"], dependencies=_auth)

    @app.get("/", summary="API Root", description="Returns basic API information and online status.")
    async def root():
        return {
            "status": "online",
            "bot_name": BRAND_NAME,
            "api_version": "1.0"
        }

    @app.get("/health", summary="Health Check", description="Performs a health check for container orchestration and uptime monitoring.")
    async def health():
        return {"status": "ok"}

    return app

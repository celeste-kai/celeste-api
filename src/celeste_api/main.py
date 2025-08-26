from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from fastapi.responses import ORJSONResponse as DefaultJSONResponse
except Exception:  # pragma: no cover - fallback if orjson is unavailable
    from fastapi.responses import JSONResponse as DefaultJSONResponse

from celeste_api import __version__
from celeste_api.routes import discovery, images, rerank, text, videos


@asynccontextmanager
async def lifespan(app: FastAPI):
    import httpx

    timeout = httpx.Timeout(60.0)
    limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
    client = httpx.AsyncClient(timeout=timeout, limits=limits, follow_redirects=True)
    app.state.httpx_client = client
    try:
        yield
    finally:
        await client.aclose()


app = FastAPI(
    title="Celeste API",
    version=__version__,
    default_response_class=DefaultJSONResponse,
    lifespan=lifespan,
)


origins_raw = os.getenv("CORS_ALLOW_ORIGINS", "*")
allow_origins = [o.strip() for o in origins_raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins if allow_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/v1/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Celeste API is running", "docs": "/docs", "health": "/v1/health"}


# Routers
app.include_router(discovery.router)
app.include_router(text.router)
app.include_router(images.router)
app.include_router(videos.router)
app.include_router(rerank.router)

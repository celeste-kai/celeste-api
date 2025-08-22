from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from celeste_api import __version__
from celeste_api.routes import discovery, images, rerank, text, videos

app = FastAPI(title="Celeste API", version=__version__)


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

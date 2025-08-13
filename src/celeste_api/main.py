from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from celeste_api.routes import discovery
from celeste_api.routes import text


def _get_version() -> str:
    try:
        return version("celeste-api")
    except PackageNotFoundError:
        return "0.1.0"


app = FastAPI(title="Celeste API", version=_get_version())


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
    return {"status": "ok", "version": _get_version()}


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Celeste API is running", "docs": "/docs", "health": "/v1/health"}


# Routers
app.include_router(discovery.router)
app.include_router(text.router)

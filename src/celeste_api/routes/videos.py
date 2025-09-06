from __future__ import annotations

from collections.abc import AsyncGenerator
from urllib.parse import quote

import httpx
from celeste_core.config.settings import settings
from celeste_core.types.video import VideoArtifact
from celeste_video_generation import create_video_client
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/v1", tags=["videos"])


def _add_api_key_if_needed(url: str) -> str:
    """Add Google API key to URL if it's a Google URL and doesn't have one."""
    if "generativelanguage.googleapis.com" in url and "key=" not in url:
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}key={settings.google.api_key}"
    return url


@router.get("/video/proxy")
async def proxy_video(url: str = Query(...)) -> StreamingResponse:
    async def stream_video() -> AsyncGenerator[bytes, None]:
        request_url = _add_api_key_if_needed(url)
        async with (
            httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client,
            client.stream("GET", request_url) as response,
        ):
            response.raise_for_status()
            async for chunk in response.aiter_bytes():
                yield chunk

    return StreamingResponse(stream_video(), media_type="video/mp4")


@router.post("/video/generate")
async def generate_video(payload: dict) -> dict:
    provider = payload["provider"]
    model = payload.get("model")
    prompt = payload["prompt"]
    options = payload.get("options", {})

    client = create_video_client(provider, model=model)
    response = await client.generate_content(prompt, **options)
    videos: list[VideoArtifact] = response.content
    return {
        "videos": [
            {
                "url": f"/v1/video/proxy?url={quote(v.url, safe='')}" if v.url else None,
                "path": v.path,
                "metadata": response.metadata,
            }
            for v in videos
        ]
    }

from __future__ import annotations

from urllib.parse import quote

from fastapi import APIRouter, Query, Request
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/v1", tags=["videos"])


def _add_api_key_if_needed(url: str) -> str:
    """Add Google API key to URL if it's a Google URL and doesn't have one."""
    from celeste_core.config.settings import settings  # lazy import to reduce import-time cost

    if "generativelanguage.googleapis.com" in url and "key=" not in url and settings.google.api_key:
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}key={settings.google.api_key}"
    return url


@router.get("/video/proxy")
async def proxy_video(request: Request, url: str = Query(...)):
    async def stream_video():
        request_url = _add_api_key_if_needed(url)
        client = request.app.state.httpx_client
        async with client.stream("GET", request_url) as response:
            response.raise_for_status()
            async for chunk in response.aiter_bytes():
                yield chunk

    return StreamingResponse(stream_video(), media_type="video/mp4")


@router.post("/video/generate")
async def generate_video(payload: dict):
    provider = payload["provider"]
    model = payload.get("model")
    prompt = payload["prompt"]
    options = payload.get("options", {})

    from celeste_video_generation import create_video_client  # lazy import

    client = create_video_client(provider, model=model)
    response = await client.generate_content(prompt, **options)
    videos = response.content
    return {
        "videos": [
            {
                "url": f"/v1/video/proxy?url={quote(v.url, safe='')}" if getattr(v, "url", None) else None,
                "path": getattr(v, "path", None),
                "metadata": response.metadata,
            }
            for v in videos
        ]
    }

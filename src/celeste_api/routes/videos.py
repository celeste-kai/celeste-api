from __future__ import annotations

from fastapi import APIRouter

from celeste_core.types.video import VideoArtifact
from celeste_video_generation import create_video_client


router = APIRouter(prefix="/v1", tags=["videos"])


@router.post("/video/generate")
async def generate_video(payload: dict):
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
                "url": v.url,
                "path": v.path,
                "metadata": response.metadata,
            }
            for v in videos
        ]
    }

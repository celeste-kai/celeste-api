from __future__ import annotations

from fastapi import APIRouter

from celeste_core.types.image import ImageArtifact
from celeste_image_generation.providers.google import GoogleImageGenerator
from celeste_image_generation.providers.openai import OpenAIImageGenerator


router = APIRouter(prefix="/v1", tags=["images"])


@router.post("/images/generate")
async def generate_images(payload: dict):
    provider = payload["provider"]
    model = payload.get("model")
    prompt = payload["prompt"]
    options = payload.get("options", {})

    if provider == "google":
        client = GoogleImageGenerator(model=model or "imagen-3.0-generate-002")
    else:
        client = OpenAIImageGenerator(model=model or "dall-e-3")

    images: list[ImageArtifact] = await client.generate_image(prompt, **options)
    return {
        "images": [
            {
                "data": (
                    img.data.decode("latin1")
                    if isinstance(img.data, (bytes, bytearray))
                    else img.data
                ),
                "path": img.path,
                "metadata": img.metadata,
            }
            for img in images
        ]
    }

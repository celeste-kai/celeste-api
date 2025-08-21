from __future__ import annotations

import base64

from celeste_core.types.image import ImageArtifact
from celeste_image_edit import create_image_editor
from celeste_image_generation import create_image_generator
from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["images"])


@router.post("/images/generate")
async def generate_images(payload: dict):
    provider = payload["provider"]
    model = payload.get("model")
    prompt = payload["prompt"]
    options = payload.get("options", {})

    client = create_image_generator(provider, model=model)

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


@router.post("/images/edit")
async def edit_image(payload: dict):
    # Parse request data - NO validation, let it fail
    provider = payload["provider"]
    model = payload.get("model")
    prompt = payload["prompt"]
    image_data = payload["image"]  # Base64 string
    options = payload.get("options", {})

    # Decode base64 to bytes - NO error handling
    image_bytes = base64.b64decode(image_data)

    # Create image artifact
    input_image = ImageArtifact(data=image_bytes)

    # Create editor and perform edit
    editor = create_image_editor(provider, model=model)
    result = await editor.edit_image(prompt=prompt, image=input_image, **options)

    # Return edited image as base64
    return {
        "image": {
            "data": base64.b64encode(result.data).decode("utf-8") if result.data else None,
            "path": result.path,
            "metadata": result.metadata,
        }
    }

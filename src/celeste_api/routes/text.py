from __future__ import annotations

from fastapi import APIRouter

from celeste_core import Capability
from celeste_client import create_client


router = APIRouter(prefix="/v1", tags=["text"])


@router.post("/text/generate")
async def generate_text(payload: dict):
    provider = payload["provider"]
    model = payload["model"]
    prompt = payload["prompt"]

    client = create_client(provider, model=model, capability=Capability.TEXT_GENERATION)
    response = await client.generate_content(prompt)
    return {
        "content": response.content,
        "provider": provider,
        "model": model,
        "metadata": response.metadata,
    }

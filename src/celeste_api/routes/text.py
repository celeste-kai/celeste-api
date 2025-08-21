from __future__ import annotations

import json

from celeste_client import create_client
from celeste_core import Capability
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

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


@router.post("/text/stream")
async def stream_text(payload: dict):
    provider = payload["provider"]
    model = payload["model"]
    prompt = payload["prompt"]

    client = create_client(provider, model=model, capability=Capability.TEXT_GENERATION)

    async def ndjson_generator():
        async for chunk in client.stream_generate_content(prompt):
            metadata = chunk.metadata or {}
            if not metadata.get("is_stream_chunk"):
                metadata = {**metadata, "is_stream_chunk": True}
            line = {
                "content": chunk.content,
                "provider": provider,
                "model": model,
                "metadata": metadata,
            }
            yield json.dumps(line, ensure_ascii=False) + "\n"

    return StreamingResponse(ndjson_generator(), media_type="application/x-ndjson")

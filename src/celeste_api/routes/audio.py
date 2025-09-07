from __future__ import annotations

import tempfile

from celeste_core.types.audio import AudioArtifact
from celeste_text_to_speech import GoogleTTSClient
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/v1", tags=["audio"])

# Simple in-memory storage for audio files (in production, use proper storage)
audio_storage: dict[str, bytes] = {}


@router.get("/audio/proxy/{audio_id}")
async def proxy_audio(audio_id: str) -> FileResponse:
    """Stream audio file."""
    if audio_id not in audio_storage:
        raise HTTPException(status_code=404, detail="Audio not found")

    # Write to temp file for streaming
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".wav", delete=False) as f:
        f.write(audio_storage[audio_id])
        temp_path = f.name

    return FileResponse(temp_path, media_type="audio/wav", filename="audio.wav")


@router.post("/audio/generate")
async def generate_audio(payload: dict) -> dict:
    """Generate audio/speech from text using TTS."""
    provider = payload["provider"]
    model = payload.get("model", "gemini-2.5-flash-preview-tts")
    text = payload["text"]
    options = payload.get("options", {})

    # Extract voice_name from options, default to a common voice
    voice_name = options.pop("voice", "Zephyr")

    # For now, we only support Google TTS
    if provider.lower() != "google":
        raise ValueError(f"Provider {provider} not yet supported for TTS")

    client = GoogleTTSClient(model=model)
    audio_artifact: AudioArtifact = await client.generate_speech(text=text, voice_name=voice_name, **options)

    # Store audio and return proxy URL (like video does)
    import uuid

    audio_id = str(uuid.uuid4())
    if audio_artifact.data:
        audio_storage[audio_id] = audio_artifact.data

    return {
        "audio": {
            "url": f"/v1/audio/proxy/{audio_id}" if audio_artifact.data else None,
            "format": audio_artifact.format or "wav",
            "sample_rate": audio_artifact.sample_rate,
            "metadata": {
                "model": model,
                "voice": voice_name,
            },
        }
    }

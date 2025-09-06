from __future__ import annotations

import base64

from celeste_core.types.audio import AudioArtifact
from celeste_text_to_speech import GoogleTTSClient
from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["audio"])


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

    # Convert audio bytes to base64
    audio_base64 = base64.b64encode(audio_artifact.data).decode("utf-8") if audio_artifact.data else None

    return {
        "audio": {
            "data": audio_base64,
            "format": audio_artifact.format or "wav",
            "sample_rate": audio_artifact.sample_rate,
            "metadata": {
                "model": model,
                "voice": voice_name,
            },
        }
    }

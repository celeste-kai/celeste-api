from __future__ import annotations

from celeste_core.enums.capability import Capability
from celeste_core.enums.providers import Provider
from celeste_core.models.registry import list_models
from fastapi import APIRouter, Query

router = APIRouter(prefix="/v1", tags=["discovery"])


@router.get("/capabilities")
async def get_capabilities() -> list[dict]:
    items: list[dict] = []
    for cap in Capability:
        if cap is Capability.NONE:
            continue
        items.append({"id": cap.name.lower(), "label": cap.name.lower()})
    return items


@router.get("/providers")
async def get_providers() -> list[dict]:
    return [{"id": p.value, "label": p.value} for p in Provider]


@router.get("/models")
async def get_models(
    capability: str | None = Query(default=None, description="Capability name (lowercase)"),
    provider: str | None = Query(default=None, description="Provider id (value)"),
) -> list[dict]:
    cap_enum: Capability | None = Capability[capability.upper()] if capability else None
    prov_enum: Provider | None = Provider(provider) if provider else None

    models = list_models(provider=prov_enum, capability=cap_enum)
    result: list[dict] = []
    for m in models:
        result.append(
            {
                "id": m.id,
                "provider": m.provider.value,
                "display_name": m.display_name,
                "capabilities": [c.name for c in Capability if c and (c & m.capabilities)],
            }
        )
    return result

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Query, Response

router = APIRouter(prefix="/v1", tags=["discovery"])


@router.get("/capabilities")
async def get_capabilities(response: Response) -> List[dict]:
    from celeste_core.enums.capability import Capability  # lazy import

    response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=3600"
    items: List[dict] = []
    for cap in Capability:
        if cap is Capability.NONE:
            continue
        items.append({"id": cap.name.lower(), "label": cap.name.lower()})
    return items


@router.get("/providers")
async def get_providers(response: Response) -> List[dict]:
    from celeste_core.enums.providers import Provider  # lazy import

    response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=3600"
    return [{"id": p.value, "label": p.value} for p in Provider]


@router.get("/models")
async def get_models(
    response: Response,
    capability: str | None = Query(default=None, description="Capability name (lowercase)"),
    provider: str | None = Query(default=None, description="Provider id (value)"),
) -> List[dict]:
    from celeste_core.enums.capability import Capability  # lazy import
    from celeste_core.enums.providers import Provider  # lazy import
    from celeste_core.models.registry import list_models  # lazy import

    response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=600"

    cap_enum: Capability | None = Capability[capability.upper()] if capability else None
    prov_enum: Provider | None = Provider(provider) if provider else None

    models = list_models(provider=prov_enum, capability=cap_enum)
    result: List[dict] = []
    for m in models:
        result.append(
            {
                "id": m.id,
                "provider": m.provider.value,
                "display_name": m.display_name,
                "capabilities": [c for c in m._serialize_capabilities(m.capabilities)],
            }
        )
    return result

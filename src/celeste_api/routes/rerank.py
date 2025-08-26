from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["rerank"])


@router.post("/rerank")
async def rerank_texts(payload: dict):
    """Rerank texts based on relevance to query."""
    from celeste_reranking import create_reranker  # lazy import

    provider = payload["provider"]
    model = payload.get("model")
    query = payload["query"]
    texts = payload["texts"]
    top_k = payload.get("top_k", 5)

    reranker = create_reranker(provider, model=model)
    response = await reranker.rerank(query, texts, top_k=top_k)

    return {
        "content": response.content,
        "provider": provider,
        "model": model,
        "metadata": response.metadata,
    }

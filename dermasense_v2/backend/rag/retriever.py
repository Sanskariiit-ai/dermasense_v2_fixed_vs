from config.settings import settings
from rag.chroma_manager import search


def retrieve(query: str, top_k: int = 3, min_score: float | None = None) -> list[dict]:
    """Return relevant chunks as [{text, source, score}], best first. Score is cosine similarity."""
    threshold = settings.rag_min_score if min_score is None else min_score
    raw = search(query, top_k)
    docs = raw["documents"][0]
    metas = raw["metadatas"][0]
    dists = raw["distances"][0]
    results = []
    for text, meta, dist in zip(docs, metas, dists):
        score = round(1 - float(dist), 3)
        if score >= threshold:
            results.append({"text": text, "source": (meta or {}).get("source", "unknown"), "score": score})
    return results

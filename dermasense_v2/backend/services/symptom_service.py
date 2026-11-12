import re

import numpy as np

from embeddings.encoder import encode, get_encoder
from embeddings.similarity import cosine_matrix
from services.symptom_registry import get_aliases, get_all_symptoms

SEMANTIC_THRESHOLD = 0.55
_embeddings = None


def _lexical(text: str) -> dict[str, float]:
    """Whole-word / phrase matches against each symptom's aliases (reliable and explainable)."""
    lowered = text.lower()
    found = {}
    for symptom, aliases in get_aliases().items():
        for alias in aliases:
            if re.search(rf"\b{re.escape(alias.lower())}\b", lowered):
                found[symptom] = 1.0
                break
    return found


def _semantic(text: str) -> dict[str, float]:
    """Embedding similarity to catch paraphrases. Only meaningful with a neural encoder."""
    global _embeddings
    if get_encoder().name != "st":  # the hashing fallback cannot judge meaning, so rely on aliases only
        return {}
    names = get_all_symptoms()
    if _embeddings is None:
        _embeddings = encode(names)
    scores = cosine_matrix(encode([text]), _embeddings)[0]
    return {n: float(s) for n, s in zip(names, scores) if s >= SEMANTIC_THRESHOLD}


def detect_symptoms(user_text: str) -> list[dict]:
    """Return [{symptom, confidence}] sorted by confidence. Lexical matches win over semantic ones."""
    combined = _semantic(user_text)
    combined.update(_lexical(user_text))
    return [
        {"symptom": s, "confidence": round(c, 3)}
        for s, c in sorted(combined.items(), key=lambda kv: -kv[1])
    ]

import hashlib
import logging
import re

import numpy as np

from config.settings import settings

log = logging.getLogger("dermasense")
DIM = 2048
STOP = {"the","a","an","and","or","of","in","on","to","is","are","it","my","i","with","for","as","at","be","can","that","this","by","from","you","your","have","has"}


class HashingEncoder:
    """Offline fallback: hashed word and bigram counts, L2-normalised.

    Much weaker than a neural model, but deterministic and dependency-free.
    Vectors are non-negative so cosine similarity measures shared vocabulary."""

    name = "hash"

    def encode(self, texts: list[str]) -> np.ndarray:
        out = np.zeros((len(texts), DIM), dtype=np.float32)
        for row, text in enumerate(texts):
            words = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]
            for gram in words + [" ".join(p) for p in zip(words, words[1:])]:
                h = int(hashlib.md5(gram.encode()).hexdigest(), 16)
                out[row, h % DIM] += 1.0
            out[row] = np.sqrt(out[row])  # damp repeated words
        norms = np.linalg.norm(out, axis=1, keepdims=True)
        return out / np.where(norms == 0, 1, norms)


class SentenceEncoder:
    name = "st"

    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        return np.asarray(self._model.encode(texts, normalize_embeddings=True), dtype=np.float32)


_encoder = None


def get_encoder():
    global _encoder
    if _encoder is None:
        backend = settings.embedding_backend.lower()
        if backend == "hash":
            _encoder = HashingEncoder()
        else:
            try:
                _encoder = SentenceEncoder(settings.embedding_model)
            except Exception as exc:
                if backend == "sentence-transformers":
                    raise
                log.warning("Neural embeddings unavailable (%s); using hashing fallback", exc)
                _encoder = HashingEncoder()
    return _encoder


def set_encoder(encoder) -> None:
    global _encoder
    _encoder = encoder


def encode(texts: list[str]) -> np.ndarray:
    return get_encoder().encode(list(texts))

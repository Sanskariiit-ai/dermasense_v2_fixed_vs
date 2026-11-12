import hashlib

from config.settings import settings
from embeddings.encoder import encode, get_encoder

_client = None


def _collection():
    """One collection per embedding backend, because vectors from different models are not comparable."""
    global _client
    import chromadb

    if _client is None:
        _client = chromadb.PersistentClient(path=settings.chroma_path)
    name = "medical_docs" if get_encoder().name == "st" else f"medical_docs_{get_encoder().name}"
    return _client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})


def reset_client() -> None:
    global _client
    _client = None


def add_documents(texts: list[str], source: str = "unknown") -> int:
    """Insert or update chunks. IDs are deterministic, so re-ingesting never duplicates."""
    if not texts:
        return 0
    ids = [hashlib.sha1(f"{source}:{i}:{t}".encode()).hexdigest()[:24] for i, t in enumerate(texts)]
    _collection().upsert(
        ids=ids,
        documents=texts,
        embeddings=encode(texts).tolist(),
        metadatas=[{"source": source, "chunk": i} for i in range(len(texts))],
    )
    return len(texts)


def count() -> int:
    return _collection().count()


def search(query: str, top_k: int = 3) -> dict:
    col = _collection()
    n = col.count()
    if n == 0:
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    return col.query(query_embeddings=encode([query]).tolist(), n_results=min(top_k, n))

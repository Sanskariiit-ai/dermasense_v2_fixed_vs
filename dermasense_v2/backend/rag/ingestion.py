from pathlib import Path

from rag.chroma_manager import add_documents
from rag.chunker import chunk_text


def ingest_document(path) -> int:
    path = Path(path)
    chunks = chunk_text(path.read_text(encoding="utf-8"))
    return add_documents(chunks, source=path.name)


def ingest_directory(directory) -> dict[str, int]:
    results = {}
    for file in sorted(Path(directory).glob("*.txt")):
        results[file.name] = ingest_document(file)
    return results

"""Background-job wrapper for (re)indexing documents. Run: python -m workers.embedding_worker"""
from pathlib import Path

from config.settings import settings
from rag.ingestion import ingest_directory


def reindex() -> dict[str, int]:
    return ingest_directory(Path(settings.data_dir) / "medical_docs")


if __name__ == "__main__":
    print(reindex())

"""Index the documents in data/medical_docs into the vector store (safe to re-run).

Run from the backend folder:  python -m scripts.load_docs
"""
from pathlib import Path

from config.settings import settings
from rag.ingestion import ingest_directory

if __name__ == "__main__":
    results = ingest_directory(Path(settings.data_dir) / "medical_docs")
    for name, chunks in results.items():
        print(f"{name}: {chunks} chunks")
    if not results:
        print("No .txt files found in data/medical_docs")

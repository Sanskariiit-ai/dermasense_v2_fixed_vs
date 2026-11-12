from pathlib import Path

import pytest

from rag.chunker import chunk_text
from rag.ingestion import ingest_directory
from rag.retriever import retrieve

DOCS = Path(__file__).resolve().parents[2] / "data" / "medical_docs"


def test_chunker_respects_size_words_and_overlap():
    text = " ".join(f"word{i}" for i in range(300))
    chunks = chunk_text(text, chunk_size=100, overlap=30)
    assert len(chunks) > 3 and all(len(c) <= 100 for c in chunks)
    assert chunks[0].split()[-1] in chunks[1].split()  # overlap carries context
    assert chunk_text("") == [] and chunk_text("short") == ["short"]


def test_chunker_never_cuts_words():
    for c in chunk_text("alpha beta gamma delta " * 50, 40, 10):
        assert all(w in {"alpha", "beta", "gamma", "delta"} for w in c.split())


@pytest.fixture(scope="module")
def indexed():
    return ingest_directory(DOCS)


def test_ingest_is_idempotent(indexed):
    from rag.chroma_manager import count

    before = count()
    assert indexed and all(n > 0 for n in indexed.values())
    ingest_directory(DOCS)
    assert count() == before


@pytest.mark.parametrize("query,source", [
    ("eczema itchy dry skin in children", "eczema.txt"),
    ("silvery scales plaques on elbows psoriasis", "psoriasis.txt"),
    ("rosacea facial flushing redness triggers", "rosacea.txt"),
    ("blackheads whiteheads acne pimples", "acne_vulgaris.txt"),
])
def test_retrieval_finds_the_right_document(indexed, query, source):
    results = retrieve(query, top_k=3, min_score=0.0)
    assert results and results[0]["source"] == source
    assert 0 <= results[0]["score"] <= 1

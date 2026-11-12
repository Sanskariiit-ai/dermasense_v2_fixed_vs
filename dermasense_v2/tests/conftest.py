import os
import tempfile

os.environ.setdefault("EMBEDDING_BACKEND", "hash")
os.environ.setdefault("JWT_SECRET", "test-secret-test-secret-test-secret-123456")
os.environ["CHROMA_PATH"] = tempfile.mkdtemp(prefix="chroma_test_")

import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from cache.memory_cache import TTLCache
from cache.redis_client import set_cache
from db.mongo import set_db


@pytest.fixture()
def client():
    set_db(AsyncMongoMockClient()["test"])
    set_cache(TTLCache())
    from main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def auth(client):
    r = client.post("/auth/register", json={"name": "Asha", "age": 30, "gender": "female",
                                            "phone_number": "9876543210", "password": "correct-horse"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}, r.json()["patient"]["id"]


@pytest.fixture(autouse=True)
def no_real_llm(monkeypatch):
    """Tests must never call a real model. Individual tests override this."""
    from services import llm_service

    def boom(messages):
        raise RuntimeError("model offline")

    monkeypatch.setattr(llm_service, "_chat_blocking", boom)

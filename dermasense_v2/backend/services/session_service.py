import json

from cache.redis_client import get_cache

TTL_SECONDS = 3600


def _key(patient_id: str, session_id: str) -> str:
    return f"session:{patient_id}:{session_id}"


def save_session(patient_id: str, session_id: str, data: dict) -> None:
    get_cache().setex(_key(patient_id, session_id), TTL_SECONDS, json.dumps(data))


def get_session(patient_id: str, session_id: str) -> dict:
    raw = get_cache().get(_key(patient_id, session_id))
    return json.loads(raw) if raw else {"symptoms": {}, "asked": []}

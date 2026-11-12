import re
import uuid
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def to_object_id(value: str) -> ObjectId | None:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


def new_session_id() -> str:
    return uuid.uuid4().hex


_SESSION_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")


def valid_session_id(value: str) -> bool:
    return bool(_SESSION_RE.match(value or ""))

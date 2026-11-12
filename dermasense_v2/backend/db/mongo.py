import logging

from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import settings

log = logging.getLogger("dermasense")
_db = None


def get_db():
    global _db
    if _db is None:
        client = AsyncIOMotorClient(settings.mongo_uri, serverSelectionTimeoutMS=3000)
        _db = client[settings.database_name]
    return _db


def set_db(db) -> None:
    """Swap the database (used by tests)."""
    global _db
    _db = db


def patients():
    return get_db()["patients"]


def chats():
    return get_db()["chat_history"]


async def ensure_indexes() -> None:
    try:
        await patients().create_index("phone_number", unique=True)
        await chats().create_index([("patient_id", 1), ("session_id", 1), ("created_at", 1)])
    except Exception as exc:  # database may be down at boot; requests will report it
        log.warning("Could not create indexes: %s", exc)

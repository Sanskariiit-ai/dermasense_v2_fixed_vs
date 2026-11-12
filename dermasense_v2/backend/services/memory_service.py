from db.mongo import chats
from utils.helpers import utcnow


async def save_message(patient_id: str, session_id: str, role: str, content: str) -> None:
    await chats().insert_one(
        {"patient_id": patient_id, "session_id": session_id, "role": role, "content": content, "created_at": utcnow()}
    )


async def get_conversation(patient_id: str, session_id: str | None = None, limit: int = 50) -> list[dict]:
    query = {"patient_id": patient_id}
    if session_id:
        query["session_id"] = session_id
    docs = await chats().find(query).sort("created_at", -1).to_list(limit)
    return [
        {"role": d["role"], "content": d["content"], "session_id": d["session_id"], "created_at": d["created_at"]}
        for d in reversed(docs)
    ]

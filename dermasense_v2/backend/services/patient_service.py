from pymongo.errors import DuplicateKeyError

from core.security import hash_password, verify_password
from db.mongo import patients
from db.schemas import serialize
from utils.helpers import to_object_id, utcnow


class PhoneAlreadyRegistered(Exception):
    pass


async def create_patient(data) -> dict:
    doc = {
        "name": data.name,
        "age": data.age,
        "gender": data.gender,
        "phone_number": data.phone_number,
        "password_hash": hash_password(data.password),
        "created_at": utcnow(),
    }
    if await patients().find_one({"phone_number": data.phone_number}):
        raise PhoneAlreadyRegistered()
    try:
        result = await patients().insert_one(doc)
    except DuplicateKeyError:
        raise PhoneAlreadyRegistered()
    doc["_id"] = result.inserted_id
    return serialize(doc)


async def authenticate(phone_number: str, password: str) -> dict | None:
    doc = await patients().find_one({"phone_number": phone_number})
    # Always run a hash comparison so response time does not reveal whether the phone number exists.
    stored = doc["password_hash"] if doc else "scrypt$00$00"
    ok = verify_password(password, stored)
    return serialize(doc) if doc and ok else None


async def get_patient(patient_id: str) -> dict | None:
    oid = to_object_id(patient_id)
    if oid is None:
        return None
    return serialize(await patients().find_one({"_id": oid}))

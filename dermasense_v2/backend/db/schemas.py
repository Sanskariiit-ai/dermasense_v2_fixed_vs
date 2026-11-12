from bson import ObjectId


def serialize(doc: dict | None) -> dict | None:
    """Convert a Mongo document into JSON-safe form and drop secrets."""
    if doc is None:
        return None
    out = {}
    for key, value in doc.items():
        if key == "password_hash":
            continue
        if key == "_id":
            out["id"] = str(value)
        elif isinstance(value, ObjectId):
            out[key] = str(value)
        else:
            out[key] = value
    return out

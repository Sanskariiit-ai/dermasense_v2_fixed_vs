from services.symptom_registry import get_symptom


def get_followups(detected_symptoms, already_asked: set[str] | None = None, limit: int = 3) -> list[str]:
    """Follow-up questions for detected symptoms, skipping questions already asked."""
    asked = already_asked or set()
    questions: list[str] = []
    for item in detected_symptoms:
        name = item["symptom"] if isinstance(item, dict) else item
        info = get_symptom(name)
        for q in (info or {}).get("followups", []):
            if q not in asked and q not in questions:
                questions.append(q)
    return questions[:limit]

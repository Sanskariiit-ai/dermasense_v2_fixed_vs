from reports.pdf_generator import create_report
from services.diagnosis_service import rank_conditions
from services.memory_service import get_conversation
from services.patient_service import get_patient
from services.session_service import get_session
from services.symptom_registry import get_symptom


async def generate_report(patient_id: str, session_id: str) -> bytes | None:
    patient = await get_patient(patient_id)
    if patient is None:
        return None
    session = get_session(patient_id, session_id)
    names = list(session["symptoms"].keys())
    symptoms = [{"symptom": n, "category": (get_symptom(n) or {}).get("category", "general")} for n in names]
    transcript = await get_conversation(patient_id, session_id)
    return create_report(patient, symptoms, rank_conditions(names), transcript)

import logging

from rag.retriever import retrieve
from services import llm_service, memory_service, session_service
from services.diagnosis_service import rank_conditions
from services.followup_service import get_followups
from services.safety_service import check_red_flags
from services.symptom_registry import get_symptom
from services.symptom_service import detect_symptoms

log = logging.getLogger("dermasense")


async def handle_message(patient_id: str, session_id: str, message: str) -> dict:
    """One chat turn. Safety rules run first and never depend on the language model."""
    history = await memory_service.get_conversation(patient_id, session_id, limit=12)
    await memory_service.save_message(patient_id, session_id, "user", message)

    flag = check_red_flags(message)
    if flag and flag["level"] in ("crisis", "emergency"):
        await memory_service.save_message(patient_id, session_id, "assistant", flag["reply"])
        return {"session_id": session_id, "response": flag["reply"], "urgent": flag["level"], "symptoms": [],
                "followups": [], "conditions": [], "disclaimer": llm_service.DISCLAIMER}

    session = session_service.get_session(patient_id, session_id)
    detected = detect_symptoms(message)
    for item in detected:
        session["symptoms"][item["symptom"]] = item["confidence"]
    names = list(session["symptoms"].keys())

    followups = get_followups(names, set(session["asked"]))
    session["asked"] = session["asked"] + followups
    conditions = rank_conditions(names)

    try:
        chunks = retrieve(message)
    except Exception as exc:  # vector store problems should not break the chat
        log.warning("Retrieval failed: %s", exc)
        chunks = []
    context = "\n\n".join(c["text"] for c in chunks)

    reply = await llm_service.generate_response(message, context, names, [c["condition"] for c in conditions], history)
    if reply is None:
        reply = llm_service.fallback_response(names, followups, conditions)
    if flag:  # urgent_review: attach the guidance to whatever the model said
        reply = f"{flag['reply']}\n\n{reply}"

    session_service.save_session(patient_id, session_id, session)
    await memory_service.save_message(patient_id, session_id, "assistant", reply)
    return {
        "session_id": session_id,
        "response": reply,
        "urgent": flag["level"] if flag else None,
        "symptoms": [{"symptom": n, "category": (get_symptom(n) or {}).get("category", "general"),
                      "confidence": session["symptoms"][n]} for n in names],
        "followups": followups,
        "conditions": [{k: c[k] for k in ("condition", "score", "matched_symptoms", "confidence_note")} for c in conditions],
        "sources": sorted({c["source"] for c in chunks}),
        "disclaimer": llm_service.DISCLAIMER,
    }

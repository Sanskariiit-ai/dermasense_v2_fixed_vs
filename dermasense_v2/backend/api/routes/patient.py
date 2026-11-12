from fastapi import APIRouter, Depends, HTTPException, Query

from core.security import current_patient_id
from models.patient import PatientResponse
from services.memory_service import get_conversation
from services.patient_service import get_patient

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/me", response_model=PatientResponse)
async def me(patient_id: str = Depends(current_patient_id)):
    patient = await get_patient(patient_id)
    if patient is None:
        raise HTTPException(404, "Patient not found")
    return patient


@router.get("/me/history")
async def history(session_id: str | None = Query(default=None, pattern=r"^[A-Za-z0-9_-]{8,64}$"),
                  patient_id: str = Depends(current_patient_id)):
    return {"messages": await get_conversation(patient_id, session_id)}

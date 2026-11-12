from fastapi import APIRouter, Depends

from core.security import current_patient_id
from models.chat import ChatRequest, ChatResponse
from services.chat_service import handle_message
from utils.helpers import new_session_id

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse, include_in_schema=False)
async def chat(request: ChatRequest, patient_id: str = Depends(current_patient_id)):
    return await handle_message(patient_id, request.session_id or new_session_id(), request.message)

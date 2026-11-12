from fastapi import APIRouter, HTTPException, status

from core.security import create_token
from models.patient import LoginRequest, PatientCreate, TokenResponse
from services.patient_service import PhoneAlreadyRegistered, authenticate, create_patient

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: PatientCreate):
    try:
        patient = await create_patient(data)
    except PhoneAlreadyRegistered:
        raise HTTPException(status.HTTP_409_CONFLICT, "This phone number is already registered")
    return {"access_token": create_token(patient["id"]), "patient": patient}


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    patient = await authenticate(data.phone_number, data.password)
    if patient is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect phone number or password")
    return {"access_token": create_token(patient["id"]), "patient": patient}

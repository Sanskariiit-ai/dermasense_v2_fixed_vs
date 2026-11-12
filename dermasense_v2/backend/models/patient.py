from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Gender = Literal["female", "male", "other", "prefer_not_to_say"]


class PatientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)
    gender: Gender
    phone_number: str = Field(pattern=r"^\+?[0-9]{10,15}$")
    password: str = Field(min_length=8, max_length=128)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name must not be blank")
        return v


class LoginRequest(BaseModel):
    phone_number: str = Field(pattern=r"^\+?[0-9]{10,15}$")
    password: str = Field(min_length=1, max_length=128)


class PatientResponse(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    phone_number: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    patient: PatientResponse

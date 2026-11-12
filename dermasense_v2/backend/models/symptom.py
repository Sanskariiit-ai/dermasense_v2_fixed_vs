from pydantic import BaseModel


class SymptomMatch(BaseModel):
    symptom: str
    confidence: float
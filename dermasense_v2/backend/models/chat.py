from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: str | None = Field(default=None, pattern=r"^[A-Za-z0-9_-]{8,64}$")


class ChatResponse(BaseModel):
    session_id: str
    response: str
    urgent: str | None = None
    symptoms: list[dict] = []
    followups: list[str] = []
    conditions: list[dict] = []
    sources: list[str] = []
    disclaimer: str

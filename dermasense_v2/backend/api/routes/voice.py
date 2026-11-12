import os
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from config.settings import settings
from core.security import current_patient_id
from voice.whisper_engine import SpeechUnavailable, transcribe

router = APIRouter(prefix="/voice", tags=["voice"])
ALLOWED = {".wav", ".mp3", ".m4a", ".webm", ".ogg", ".flac"}


@router.post("/transcribe")
async def transcribe_voice(file: UploadFile = File(...), patient_id: str = Depends(current_patient_id)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED:
        raise HTTPException(415, f"Unsupported audio type. Allowed: {', '.join(sorted(ALLOWED))}")
    limit = settings.max_audio_mb * 1024 * 1024
    data = await file.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(413, f"Audio is larger than {settings.max_audio_mb} MB")
    if not data:
        raise HTTPException(400, "Empty audio file")
    # Never use the client's filename on disk; use a private temp file and always remove it.
    fd, path = tempfile.mkstemp(suffix=ext)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(data)
        transcript = await transcribe(path)
    except SpeechUnavailable as exc:
        raise HTTPException(503, str(exc))
    finally:
        os.path.exists(path) and os.remove(path)
    return {"transcript": transcript}

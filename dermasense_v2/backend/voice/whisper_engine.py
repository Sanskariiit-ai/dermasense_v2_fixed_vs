import asyncio

from config.settings import settings

_model = None


class SpeechUnavailable(RuntimeError):
    pass


def _get_model():
    """Load Whisper on first use so the API starts fast and works without it."""
    global _model
    if _model is None:
        try:
            from faster_whisper import WhisperModel

            _model = WhisperModel(settings.whisper_model, device="cpu", compute_type="int8")
        except Exception as exc:
            raise SpeechUnavailable(f"Speech model could not be loaded: {exc}") from exc
    return _model


def set_model(model) -> None:
    global _model
    _model = model


def _transcribe_blocking(path: str) -> str:
    segments, _ = _get_model().transcribe(path)
    return " ".join(s.text.strip() for s in segments).strip()


async def transcribe(audio_path: str) -> str:
    return await asyncio.to_thread(_transcribe_blocking, audio_path)

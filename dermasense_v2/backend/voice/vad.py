import array
import math

try:
    import webrtcvad  # optional dependency

    _vad = webrtcvad.Vad(2)
except Exception:  # not installed or no compiler: use the energy fallback
    _vad = None


def is_speech(audio_bytes: bytes, sample_rate: int = 16000, threshold: float = 500.0) -> bool:
    """True if a 16-bit mono PCM frame contains speech. webrtcvad needs 10/20/30 ms frames."""
    if _vad is not None:
        try:
            return _vad.is_speech(audio_bytes, sample_rate)
        except Exception:
            pass
    samples = array.array("h")
    samples.frombytes(audio_bytes[: len(audio_bytes) - (len(audio_bytes) % 2)])
    if not samples:
        return False
    rms = math.sqrt(sum(s * s for s in samples) / len(samples))
    return rms > threshold

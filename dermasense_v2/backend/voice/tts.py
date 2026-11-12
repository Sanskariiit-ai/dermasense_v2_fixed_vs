class TTSUnavailable(RuntimeError):
    pass


def synthesize(text: str) -> bytes:
    """Server-side text-to-speech is optional. The web app uses the browser's speech synthesis instead.
    Plug a engine (for example Piper or pyttsx3) in here if you need server-side audio."""
    raise TTSUnavailable("No server-side TTS engine is configured")

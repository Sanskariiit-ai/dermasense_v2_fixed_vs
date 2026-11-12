from voice.whisper_engine import transcribe


async def process_audio(path: str) -> str:
    return await transcribe(path)

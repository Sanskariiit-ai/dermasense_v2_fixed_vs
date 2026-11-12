from realtime.manager import manager


async def stream_transcript(websocket, transcript: str) -> None:
    await manager.send_json(websocket, {"type": "transcript", "text": transcript})

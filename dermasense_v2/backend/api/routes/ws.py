import json

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from core.security import patient_id_from_token
from realtime.manager import manager
from services.chat_service import handle_message
from utils.helpers import new_session_id, valid_session_id

router = APIRouter()
MAX_LEN = 2000


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = ""):
    """Chat over WebSocket. Connect with ?token=<access token>. Send {"message": "...", "session_id": "..."}."""
    try:
        patient_id = patient_id_from_token(token)
    except HTTPException:
        await websocket.close(code=4401)
        return
    await manager.connect(websocket)
    session_id = new_session_id()
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                payload = json.loads(raw)
                message = str(payload["message"]).strip()
            except (ValueError, KeyError, TypeError):
                await manager.send_json(websocket, {"type": "error", "detail": "Send JSON like {\"message\": \"...\"}"})
                continue
            if not message or len(message) > MAX_LEN:
                await manager.send_json(websocket, {"type": "error", "detail": f"Message must be 1-{MAX_LEN} characters"})
                continue
            sid = payload.get("session_id")
            session_id = sid if isinstance(sid, str) and valid_session_id(sid) else session_id
            result = await handle_message(patient_id, session_id, message)
            await manager.send_json(websocket, {"type": "response", **result})
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)

import pytest
from starlette.websockets import WebSocketDisconnect


def test_report_is_pdf_with_escaped_user_text(client, auth):
    headers, _ = auth
    sid = client.post("/chat/", json={"message": "itching and dry skin"}, headers=headers).json()["session_id"]
    r = client.post("/reports/", json={"session_id": sid}, headers=headers)
    assert r.status_code == 200 and r.headers["content-type"] == "application/pdf"
    assert r.content.startswith(b"%PDF")


def test_report_survives_markup_in_name(client):
    reg = client.post("/auth/register", json={"name": "<b>Tom & <i>Jerry", "age": 22, "gender": "male",
                                              "phone_number": "9000000001", "password": "long-enough-pw"}).json()
    h = {"Authorization": f"Bearer {reg['access_token']}"}
    r = client.post("/reports/", json={"session_id": "abcdefgh12"}, headers=h)
    assert r.status_code == 200 and r.content.startswith(b"%PDF")


def test_websocket_requires_token_and_chats(client, auth):
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws/chat?token=bad") as ws:
            ws.receive_text()
    headers, _ = auth
    token = headers["Authorization"].split()[1]
    with client.websocket_connect(f"/ws/chat?token={token}") as ws:
        ws.send_text("not json")
        assert ws.receive_json()["type"] == "error"
        ws.send_json({"message": "my skin is itchy"})
        msg = ws.receive_json()
        assert msg["type"] == "response" and any(s["symptom"] == "itching" for s in msg["symptoms"])

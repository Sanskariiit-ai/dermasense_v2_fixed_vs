from services import llm_service


def test_chat_detects_symptoms_and_asks_followups(client, auth):
    headers, _ = auth
    r = client.post("/chat/", json={"message": "My skin is dry and itchy with red patches"}, headers=headers)
    assert r.status_code == 200
    data = r.json()
    names = {s["symptom"] for s in data["symptoms"]}
    assert {"dry skin", "itching", "red patches"} <= names
    assert data["followups"] and data["disclaimer"]
    assert data["conditions"][0]["condition"] in {"eczema", "psoriasis"}
    assert data["urgent"] is None
    assert data["response"]  # fallback reply when the model is offline


def test_session_accumulates_and_does_not_repeat_questions(client, auth):
    headers, _ = auth
    first = client.post("/chat/", json={"message": "I have itching"}, headers=headers).json()
    sid = first["session_id"]
    second = client.post("/chat/", json={"message": "also dry skin", "session_id": sid}, headers=headers).json()
    assert {"itching", "dry skin"} <= {s["symptom"] for s in second["symptoms"]}
    assert not set(first["followups"]) & set(second["followups"])


def test_uses_llm_when_available(client, auth, monkeypatch):
    monkeypatch.setattr(llm_service, "_chat_blocking", lambda m: "Model reply")
    headers, _ = auth
    assert client.post("/chat/", json={"message": "itchy rash"}, headers=headers).json()["response"] == "Model reply"


def test_red_flags_bypass_the_model(client, auth, monkeypatch):
    called = []
    monkeypatch.setattr(llm_service, "_chat_blocking", lambda m: called.append(1) or "x")
    headers, _ = auth
    r = client.post("/chat/", json={"message": "I have a rash and my lips are swelling, hard to breathe"}, headers=headers).json()
    assert r["urgent"] == "emergency" and "112" in r["response"] and not called
    c = client.post("/chat/", json={"message": "I want to die because of my skin"}, headers=headers).json()
    assert c["urgent"] == "crisis" and "14416" in c["response"] and not called


def test_urgent_review_prefixes_reply(client, auth):
    headers, _ = auth
    r = client.post("/chat/", json={"message": "my mole is bleeding and changing"}, headers=headers).json()
    assert r["urgent"] == "urgent_review" and "see a doctor" in r["response"].lower()


def test_chat_input_limits(client, auth):
    headers, _ = auth
    assert client.post("/chat/", json={"message": ""}, headers=headers).status_code == 422
    assert client.post("/chat/", json={"message": "x" * 2001}, headers=headers).status_code == 422
    assert client.post("/chat/", json={"message": "hi", "session_id": "../etc"}, headers=headers).status_code == 422


def test_history_is_private_to_each_patient(client, auth):
    headers, _ = auth
    sid = client.post("/chat/", json={"message": "itchy skin"}, headers=headers).json()["session_id"]
    mine = client.get(f"/patients/me/history?session_id={sid}", headers=headers).json()["messages"]
    assert [m["role"] for m in mine] == ["user", "assistant"]
    other = client.post("/auth/register", json={"name": "B", "age": 40, "gender": "male",
                                                "phone_number": "9123456780", "password": "another-pass"}).json()
    oh = {"Authorization": f"Bearer {other['access_token']}"}
    assert client.get(f"/patients/me/history?session_id={sid}", headers=oh).json()["messages"] == []

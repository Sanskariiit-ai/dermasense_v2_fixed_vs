def test_register_login_me(client):
    body = {"name": "Asha", "age": 30, "gender": "female", "phone_number": "9876543210", "password": "correct-horse"}
    r = client.post("/auth/register", json=body)
    assert r.status_code == 201
    token = r.json()["access_token"]
    assert "password" not in r.text and "password_hash" not in r.text
    me = client.get("/patients/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200 and me.json()["name"] == "Asha"
    ok = client.post("/auth/login", json={"phone_number": "9876543210", "password": "correct-horse"})
    assert ok.status_code == 200
    bad = client.post("/auth/login", json={"phone_number": "9876543210", "password": "wrong-password"})
    assert bad.status_code == 401


def test_duplicate_phone_rejected(client, auth):
    r = client.post("/auth/register", json={"name": "B", "age": 20, "gender": "male",
                                            "phone_number": "9876543210", "password": "another-pass"})
    assert r.status_code == 409


def test_validation(client):
    base = {"name": "A", "age": 30, "gender": "female", "phone_number": "9876543210", "password": "correct-horse"}
    for bad in ({"age": -1}, {"age": 200}, {"phone_number": "abc"}, {"password": "short"}, {"gender": "x"}, {"name": "  "}):
        assert client.post("/auth/register", json={**base, **bad}).status_code == 422, bad


def test_endpoints_require_auth(client):
    assert client.get("/patients/me").status_code == 401
    assert client.post("/chat/", json={"message": "hi"}).status_code == 401
    assert client.post("/reports/", json={"session_id": "abcdefgh"}).status_code == 401
    assert client.get("/patients/me", headers={"Authorization": "Bearer garbage"}).status_code == 401


def test_health(client):
    assert client.get("/").json()["status"] == "running"

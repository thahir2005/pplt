from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_signup_and_login_flow():
    email = f"test-{uuid.uuid4()}@test.com"

    # signup
    res = client.post(
        "/users/",
        json={
            "email": email,
            "password": "secret123"
        }
    )
    assert res.status_code in (200, 201)

    # login
    res = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "secret123"
        }
    )
    assert res.status_code == 200
    assert "access_token" in res.json()

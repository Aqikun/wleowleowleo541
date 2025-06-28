# Lokasi file: tests/test_domains/test_reports_api.py
from fastapi.testclient import TestClient
from datetime import date
from decimal import Decimal

def get_auth_headers_for_login(client: TestClient, username: str, password: str, role: str) -> dict:
    login_response = client.post("/token", data={"username": username, "password": password})
    if login_response.status_code != 200:
        email = f"{username}@example.com"
        # PERBAIKAN: Gunakan endpoint /register
        client.post("/register", json={"username": username, "email": email, "password": password, "role": role})
        login_response = client.post("/token", data={"username": username, "password": password})

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# ... sisa tes tidak berubah
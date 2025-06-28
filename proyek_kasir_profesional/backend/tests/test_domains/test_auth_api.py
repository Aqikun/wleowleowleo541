# Lokasi file: tests/test_domains/test_auth_api.py
# PERBAIKAN FINAL: Menggunakan endpoint /register untuk semua pembuatan pengguna

from fastapi.testclient import TestClient

def test_register_user_success(client: TestClient):
    """Tes skenario sukses: Membuat pengguna baru melalui /register."""
    response = client.post(
        "/register",
        json={"username": "testuser_final_v1", "email": "testuser_final_v1@example.com", "password": "testpassword123", "role": "Admin"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser_final_v1"
    assert "hashed_password" not in data

def test_register_user_duplicate_username(client: TestClient):
    """Tes skenario gagal: Mencoba mendaftar dengan username yang sudah ada."""
    client.post(
        "/register",
        json={"username": "duplicate_final_v1", "email": "duplicate_final_v1@example.com", "password": "password1", "role": "Kasir"}
    )
    response = client.post(
        "/register",
        json={"username": "duplicate_final_v1", "email": "another_final_v1@example.com", "password": "password2", "role": "Kasir"}
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_login_for_access_token_success(client: TestClient):
    """Tes skenario sukses: Login dengan kredensial yang valid."""
    client.post(
        "/register",
        json={"username": "loginuser_final_v1", "email": "loginuser_final_v1@example.com", "password": "loginpassword", "role": "Kasir"}
    )
    response = client.post(
        "/token",
        data={"username": "loginuser_final_v1", "password": "loginpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_incorrect_password(client: TestClient):
    """Tes skenario gagal: Login dengan password yang salah."""
    client.post(
        "/register",
        json={"username": "wrongpassuser_final_v1", "email": "wrongpass_final_v1@example.com", "password": "correctpassword", "role": "Kasir"}
    )
    response = client.post(
        "/token",
        data={"username": "wrongpassuser_final_v1", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
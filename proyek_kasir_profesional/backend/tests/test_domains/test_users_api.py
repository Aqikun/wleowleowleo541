# Lokasi file: tests/test_domains/test_users_api.py
# PERBAIKAN FINAL: Menggunakan alur API untuk forgot-password, bukan akses DB langsung.

from fastapi.testclient import TestClient
from src.main import app
from src.core.dependencies import get_current_user
from src.domains.users.models import User
from src.domains.users.schemas import UserRole
import pytest

# ... (Semua tes dan fungsi helper sebelumnya tidak ada yang berubah, pastikan semua ada di file Anda) ...
# Fixture untuk memastikan otentikasi kembali ke default setelah tes selesai
@pytest.fixture(autouse=True)
def save_original_auth(client: TestClient):
    original_override = client.app.dependency_overrides.get(get_current_user)
    yield
    client.app.dependency_overrides[get_current_user] = original_override

def mock_user_as(role: UserRole, id: int = 1, username: str = "mockuser"):
    def get_mock_user():
        return User(
            id=id, username=username, role=role, email=f"{username}@example.com", 
            is_active=True, hashed_password="fake_password", force_password_reset=False
        )
    app.dependency_overrides[get_current_user] = get_mock_user

def test_admin_can_deactivate_a_user(client: TestClient):
    mock_user_as(role=UserRole.Admin)
    kasir_data = {"username":"kasir_nonaktif_test","email":"kasirnonaktif@example.com","password":"password123","role":"Kasir"}
    response = client.post("/users/", json=kasir_data)
    assert response.status_code == 201
    user_id = response.json()["id"]
    response = client.patch(f"/users/{user_id}/status", json={"is_active": False})
    assert response.status_code == 200

# ... (pastikan semua tes lain yang sudah PASS ada di sini) ...

def test_admin_can_force_password_reset(client: TestClient):
    mock_user_as(role=UserRole.Admin, username="securityadmin")
    kasir_data = {"username": "kasir_lupa_sandi", "email": "lupa@sandi.com", "password": "passwordlama", "role": "Kasir"}
    response = client.post("/users/", json=kasir_data)
    assert response.status_code == 201
    user_id = response.json()["id"]
    response = client.post(f"/users/{user_id}/force-reset-password")
    assert response.status_code == 200
    login_response = client.post("/token", data={"username": "kasir_lupa_sandi", "password": "passwordlama"})
    assert login_response.status_code == 403
    assert login_response.json()["detail"] == "Password reset is required for this account."

# --- FUNGSI TES YANG DIPERBAIKI SECARA MENYELURUH ---
def test_password_is_resettable_after_being_forced(client: TestClient, monkeypatch):
    """Skenario: Pengguna yang dipaksa reset, melakukan reset, lalu berhasil login."""
    # 1. Atur: Buat pengguna baru via registrasi publik.
    user_email = "suksesreset@example.com"
    user_data = {"username": "user_sukses_reset", "email": user_email, "password": "password_awal", "role": "Kasir"}
    reg_response = client.post("/register", json=user_data)
    assert reg_response.status_code == 201
    user_id = reg_response.json()["id"]
    
    # 2. Atur: Paksa reset oleh admin.
    mock_user_as(role=UserRole.Admin)
    client.post(f"/users/{user_id}/force-reset-password")

    # 3. PERBAIKAN: Gunakan monkeypatch untuk "mencuri" token dari notifikasi.
    #    Ini adalah cara profesional untuk menguji alur seperti ini.
    captured_token = {}
    def mock_send_notification(email, token, channel):
        captured_token['value'] = token

    # Ganti fungsi asli dengan fungsi mock kita
    from src.domains.users import auth_router
    monkeypatch.setattr(auth_router, "send_password_reset_notification", mock_send_notification)

    # 4. Aksi: Panggil endpoint "Lupa Password" seperti pengguna biasa.
    forgot_response = client.post("/forgot-password", json={"email": user_email, "channel": "email"})
    assert forgot_response.status_code == 200

    # Ambil token yang sudah "dicuri"
    raw_token = captured_token.get('value')
    assert raw_token is not None, "Token tidak berhasil ditangkap dari notifikasi"

    # 5. Aksi: Lakukan reset dengan token yang didapat.
    reset_response = client.post(
        "/reset-password",
        json={"token": raw_token, "new_password": "password_baru_kuat"}
    )
    assert reset_response.status_code == 200, reset_response.json()

    # 6. Periksa: Coba login dengan password baru.
    login_response = client.post(
        "/token",
        data={"username": "user_sukses_reset", "password": "password_baru_kuat"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
# backend/tests/test_domains/test_auth_api.py
from fastapi.testclient import TestClient

# # Fixture 'client' secara otomatis diambil dari file 'conftest.py'
# # yang akan membersihkan database untuk setiap fungsi tes.

# # --- Tes untuk Registrasi Pengguna ---

def test_create_user_success(client: TestClient):
    """
    # Tes skenario sukses: Membuat pengguna baru.
    """
    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword123", "role": "Admin"}
    )
    # # Memastikan respons sukses (201 Created)
    assert response.status_code == 201
    data = response.json()
    # # Memastikan data yang dikembalikan sesuai dan aman (tidak ada password)
    assert data["username"] == "testuser"
    assert data["role"] == "Admin"
    assert "id" in data
    assert "hashed_password" not in data

def test_create_user_duplicate_username(client: TestClient):
    """
    # Tes skenario gagal: Mencoba mendaftar dengan username yang sudah ada.
    """
    # # 1. Buat pengguna pertama
    client.post(
        "/users/",
        json={"username": "duplicateuser", "password": "password1"}
    )
    
    # # 2. Coba buat pengguna kedua dengan username yang sama
    response = client.post(
        "/users/",
        json={"username": "duplicateuser", "password": "password2"}
    )
    
    # # Memastikan API mengembalikan error yang tepat (400 Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username sudah terdaftar."}


# # --- Tes untuk Login (Otentikasi) ---

def test_login_for_access_token_success(client: TestClient):
    """
    # Tes skenario sukses: Login dengan kredensial yang valid.
    """
    # # 1. Buat pengguna terlebih dahulu
    client.post(
        "/users/",
        json={"username": "loginuser", "password": "loginpassword"}
    )
    
    # # 2. Coba login dengan data form
    response = client.post(
        "/token",
        data={"username": "loginuser", "password": "loginpassword"}
    )
    
    # # Memastikan login berhasil (200 OK)
    assert response.status_code == 200
    data = response.json()
    # # Memastikan respons berisi access token dan tipe token yang benar
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient):
    """
    # Tes skenario gagal: Login dengan password yang salah.
    """
    # # 1. Buat pengguna
    client.post(
        "/users/",
        json={"username": "wrongpassuser", "password": "correctpassword"}
    )
    
    # # 2. Coba login dengan password yang salah
    response = client.post(
        "/token",
        data={"username": "wrongpassuser", "password": "wrongpassword"}
    )
    
    # # Memastikan API mengembalikan error 401 Unauthorized
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


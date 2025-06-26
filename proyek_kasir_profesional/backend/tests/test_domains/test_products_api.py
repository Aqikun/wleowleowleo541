# backend/tests/test_domains/test_products_api.py
from fastapi.testclient import TestClient
from decimal import Decimal # <-- Impor Decimal untuk perbandingan yang akurat

# Fungsi bantuan untuk mendapatkan header otentikasi
def get_auth_headers(client: TestClient) -> dict:
    """
    # Membuat user tes, login, dan mengembalikan header Authorization.
    """
    # # Coba cari user dulu, jika sudah ada, tidak perlu dibuat lagi
    # # Ini untuk menghindari error jika tes dijalankan berulang kali
    user_login_response = client.post("/token", data={"username": "testproduser", "password": "password"})
    if user_login_response.status_code != 200:
        client.post("/users/", json={"username": "testproduser", "password": "password"})
        user_login_response = client.post("/token", data={"username": "testproduser", "password": "password"})
    
    token = user_login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# # --- Tes Keamanan Endpoint ---

def test_create_product_unauthenticated(client: TestClient):
    """
    # Tes: Gagal membuat produk jika tidak login (tanpa token).
    """
    response = client.post(
        "/products/", 
        json={"name": "Produk Gagal", "description": "Tes", "price": 100, "stock": 10}
    )
    # # Mengharapkan error 401 Unauthorized
    assert response.status_code == 401


# # --- Tes Fungsionalitas CRUD Produk (Telah Terotentikasi) ---

def test_create_and_read_product(client: TestClient):
    """
    # Tes: Berhasil membuat dan membaca satu produk.
    """
    headers = get_auth_headers(client)
    product_data = {"name": "Laptop Gaming", "description": "ROG Zephyrus", "price": 25000000.50, "stock": 15}

    # # 1. Buat produk baru
    create_response = client.post("/products/", json=product_data, headers=headers)
    assert create_response.status_code == 201
    created_product = create_response.json()
    assert created_product["name"] == product_data["name"]
    assert "id" in created_product

    product_id = created_product["id"]

    # # 2. Baca kembali produk yang baru dibuat
    read_response = client.get(f"/products/{product_id}", headers=headers)
    assert read_response.status_code == 200
    read_product = read_response.json()
    assert read_product["name"] == product_data["name"]
    
    # # FIX: Bandingkan dengan mengonversi keduanya ke tipe data yang sama (Decimal)
    assert Decimal(read_product["price"]) == Decimal("25000000.50")


def test_read_all_products(client: TestClient):
    """
    # Tes: Berhasil membaca daftar semua produk.
    """
    headers = get_auth_headers(client)
    # # Buat beberapa produk
    client.post("/products/", json={"name": "Mouse", "price": 150000, "stock": 100}, headers=headers)
    client.post("/products/", json={"name": "Keyboard", "price": 350000, "stock": 50}, headers=headers)

    # # Ambil daftar produk
    response = client.get("/products/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2 # # Gunakan >= untuk mengakomodasi tes sebelumnya


def test_update_product(client: TestClient):
    """
    # Tes: Berhasil memperbarui produk yang ada.
    """
    headers = get_auth_headers(client)
    # # Buat produk awal
    product_data = {"name": "Buku Tulis", "price": 5000, "stock": 200}
    created_product = client.post("/products/", json=product_data, headers=headers).json()
    product_id = created_product["id"]
    
    # # Perbarui produk
    update_data = {"price": 4500.00, "stock": 190}
    response = client.put(f"/products/{product_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_product = response.json()

    # # FIX: Bandingkan dengan mengonversi keduanya ke tipe data yang sama (Decimal)
    assert Decimal(updated_product["price"]) == Decimal("4500.00")
    assert updated_product["stock"] == 190


def test_delete_product(client: TestClient):
    """
    # Tes: Berhasil menghapus produk.
    """
    headers = get_auth_headers(client)
    # # Buat produk untuk dihapus
    product_data = {"name": "Produk Hapus", "price": 1000, "stock": 10}
    created_product = client.post("/products/", json=product_data, headers=headers).json()
    product_id = created_product["id"]

    # # Hapus produk
    delete_response = client.delete(f"/products/{product_id}", headers=headers)
    assert delete_response.status_code == 200

    # # Coba akses lagi, seharusnya 404 Not Found
    get_response = client.get(f"/products/{product_id}", headers=headers)
    assert get_response.status_code == 404

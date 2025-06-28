# Lokasi file: tests/test_domains/test_products_api.py
# PERBAIKAN TUNTAS: Helper menggunakan alur yang benar (Register -> Login)

from fastapi.testclient import TestClient
from decimal import Decimal

def get_auth_headers(client: TestClient) -> dict:
    username = "testproduser_tuntas"
    password = "password"
    email = f"{username}@example.com"
    
    # Alur yang Benar: Selalu buat user baru untuk memastikan tes terisolasi
    create_response = client.post(
        "/register", 
        json={"username": username, "email": email, "password": password, "role": "Admin"}
    )
    if create_response.status_code != 201 and create_response.status_code != 400:
         assert False, f"Pembuatan pengguna tes gagal dengan status tak terduga: {create_response.status_code} - {create_response.json()}"

    # Setelah registrasi, selalu login untuk mendapatkan token baru
    login_response = client.post("/token", data={"username": username, "password": password})
    assert login_response.status_code == 200, f"Login gagal setelah registrasi: {login_response.json()}"
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- Tes Keamanan Endpoint ---
def test_create_product_unauthenticated(client: TestClient):
    response = client.post("/products/", json={"name": "Produk Gagal Tuntas", "price": 100, "stock": 10})
    assert response.status_code == 401

# --- Tes Fungsionalitas CRUD Produk ---
def test_create_and_read_product(client: TestClient):
    headers = get_auth_headers(client)
    product_data = {"name": "Laptop Gaming Tuntas", "price": 25000000.50, "stock": 15}
    create_response = client.post("/products/", json=product_data, headers=headers)
    assert create_response.status_code == 201
    created_product = create_response.json()
    assert created_product["name"] == product_data["name"]
    product_id = created_product["id"]
    read_response = client.get(f"/products/{product_id}", headers=headers)
    assert read_response.status_code == 200
    read_product = read_response.json()
    assert read_product["name"] == product_data["name"]

def test_read_all_products(client: TestClient):
    headers = get_auth_headers(client)
    client.post("/products/", json={"name": "Mouse Tuntas", "price": 150000, "stock": 100}, headers=headers)
    client.post("/products/", json={"name": "Keyboard Tuntas", "price": 350000, "stock": 50}, headers=headers)
    response = client.get("/products/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_product(client: TestClient):
    headers = get_auth_headers(client)
    product_data = {"name": "Buku Tulis Tuntas", "price": 5000, "stock": 200}
    created_product = client.post("/products/", json=product_data, headers=headers).json()
    product_id = created_product["id"]
    update_data = {"price": 4500.00, "stock": 190}
    response = client.put(f"/products/{product_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_product = response.json()
    assert Decimal(updated_product["price"]) == Decimal("4500.00")

def test_delete_product(client: TestClient):
    headers = get_auth_headers(client)
    product_data = {"name": "Produk Hapus Tuntas", "price": 1000, "stock": 10}
    created_product = client.post("/products/", json=product_data, headers=headers).json()
    product_id = created_product["id"]
    delete_response = client.delete(f"/products/{product_id}", headers=headers)
    assert delete_response.status_code == 200
    get_response = client.get(f"/products/{product_id}", headers=headers)
    assert get_response.status_code == 404
# Lokasi file: tests/test_domains/test_transactions_api.py
# PERBAIKAN TUNTAS: Menggunakan helper terpusat dengan alur yang benar

from fastapi.testclient import TestClient
from decimal import Decimal

# --- Fungsi Bantuan (Helpers) ---
def get_auth_headers(client: TestClient, role: str) -> dict:
    username = f"transaction_user_tuntas_{role.lower()}"
    password = "password"
    email = f"{username}@example.com"

    # Alur yang Benar: Selalu buat user baru untuk memastikan tes terisolasi
    create_response = client.post(
        "/register",
        json={"username": username, "email": email, "password": password, "role": role}
    )
    if create_response.status_code != 201 and create_response.status_code != 400:
         assert False, f"Pembuatan pengguna tes gagal dengan status tak terduga: {create_response.status_code} - {create_response.json()}"

    # Setelah registrasi, selalu login untuk mendapatkan token baru
    login_response = client.post("/token", data={"username": username, "password": password})
    assert login_response.status_code == 200, f"Login gagal setelah registrasi: {login_response.json()}"
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- Tes Fungsionalitas Transaksi ---
def test_create_transaction_success(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    kasir_headers = get_auth_headers(client, role="Kasir")

    product1_res = client.post("/products/", json={"name": "Kopi Tuntas", "price": "15000.00", "stock": 50}, headers=admin_headers)
    product2_res = client.post("/products/", json={"name": "Teh Tuntas", "price": "10000.00", "stock": 30}, headers=admin_headers)
    assert product1_res.status_code == 201
    assert product2_res.status_code == 201
    product1 = product1_res.json()
    product2 = product2_res.json()

    transaction_payload = {
        "details": [
            {"product_id": product1["id"], "quantity": 2, "price_at_transaction": product1["price"]},
            {"product_id": product2["id"], "quantity": 1, "price_at_transaction": product2["price"]},
        ]
    }
    response = client.post("/transactions/", json=transaction_payload, headers=kasir_headers)
    assert response.status_code == 201
    
def test_create_transaction_insufficient_stock(client: TestClient):
    admin_headers = get_auth_headers(client, "Admin")
    kasir_headers = get_auth_headers(client, "Kasir")

    product_res = client.post("/products/", json={"name": "Barang Langka Tuntas", "price": "100000.00", "stock": 5}, headers=admin_headers)
    assert product_res.status_code == 201
    product = product_res.json()

    transaction_payload = { "details": [{"product_id": product["id"], "quantity": 6, "price_at_transaction": product["price"]}] }
    response = client.post("/transactions/", json=transaction_payload, headers=kasir_headers)
    assert response.status_code == 400

def test_create_transaction_product_not_found(client: TestClient):
    kasir_headers = get_auth_headers(client, "Kasir")
    transaction_payload = { "details": [{"product_id": 99999, "quantity": 1, "price_at_transaction": "1.00"}] }
    response = client.post("/transactions/", json=transaction_payload, headers=kasir_headers)
    assert response.status_code == 404

def test_read_transaction_history(client: TestClient):
    admin_headers = get_auth_headers(client, "Admin")
    
    product_res = client.post("/products/", json={"name": "Roti Tuntas", "price": "5000.00", "stock": 10}, headers=admin_headers)
    assert product_res.status_code == 201
    product = product_res.json()
    
    client.post("/transactions/", json={"details": [{"product_id": product["id"], "quantity": 1, "price_at_transaction": product["price"]}]}, headers=admin_headers)
    
    response = client.get("/transactions/", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
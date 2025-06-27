# nama file: tests/test_domains/test_transactions_api.py

from fastapi.testclient import TestClient
from decimal import Decimal

# Fungsi bantuan untuk pengguna dengan peran KASIR
def get_kasir_auth_headers(client: TestClient) -> dict:
    username = "testcashier_for_pos"
    password = "password"
    # Coba login dulu
    user_login_response = client.post("/token", data={"username": username, "password": password})
    if user_login_response.status_code != 200:
        client.post("/users/", json={"username": username, "password": password, "role": "Kasir"})
        user_login_response = client.post("/token", data={"username": username, "password": password})
    token = user_login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Fungsi bantuan untuk pengguna dengan peran ADMIN
def get_admin_auth_headers(client: TestClient) -> dict:
    username = "testadmin_for_history"
    password = "password"
    user_login_response = client.post("/token", data={"username": username, "password": password})
    if user_login_response.status_code != 200:
        client.post("/users/", json={"username": username, "password": password, "role": "Admin"})
        user_login_response = client.post("/token", data={"username": username, "password": password})
    token = user_login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_transaction_success(client: TestClient):
    """ Tes skenario sukses: Membuat transaksi valid. """
    headers = get_kasir_auth_headers(client)
    product1_res = client.post("/products/", json={"name": "Kopi", "price": "15000.00", "stock": 50}, headers=headers)
    product2_res = client.post("/products/", json={"name": "Teh", "price": "10000.00", "stock": 30}, headers=headers)
    product1 = product1_res.json()
    product2 = product2_res.json()

    transaction_payload = {
        "details": [
            {"product_id": product1["id"], "quantity": 2, "price_at_transaction": product1["price"]},
            {"product_id": product2["id"], "quantity": 1, "price_at_transaction": product2["price"]},
        ]
    }
    response = client.post("/transactions/", json=transaction_payload, headers=headers)
    assert response.status_code == 201
    
def test_create_transaction_insufficient_stock(client: TestClient):
    """ Tes skenario gagal: Stok produk tidak mencukupi. """
    headers = get_kasir_auth_headers(client)
    product_res = client.post("/products/", json={"name": "Barang Langka", "price": "100000.00", "stock": 5}, headers=headers)
    product = product_res.json()
    transaction_payload = { "details": [{"product_id": product["id"], "quantity": 6, "price_at_transaction": product["price"]}] }
    response = client.post("/transactions/", json=transaction_payload, headers=headers)
    assert response.status_code == 400

def test_create_transaction_product_not_found(client: TestClient):
    """ Tes skenario gagal: Produk yang dibeli tidak ada. """
    headers = get_kasir_auth_headers(client)
    transaction_payload = { "details": [{"product_id": 99999, "quantity": 1, "price_at_transaction": "1.00"}] }
    response = client.post("/transactions/", json=transaction_payload, headers=headers)
    assert response.status_code == 404

def test_read_transaction_history(client: TestClient):
    """ Tes skenario sukses: Melihat daftar riwayat transaksi. """
    # PERBAIKAN: Gunakan admin untuk membuat data dan melihat riwayat
    admin_headers = get_admin_auth_headers(client)
    product_res = client.post("/products/", json={"name": "Roti", "price": "5000.00", "stock": 10}, headers=admin_headers)
    product = product_res.json()
    
    client.post("/transactions/", json={"details": [{"product_id": product["id"], "quantity": 1, "price_at_transaction": product["price"]}]}, headers=admin_headers)
    
    # PERBAIKAN: Gunakan header admin untuk mengambil riwayat
    response = client.get("/transactions/", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
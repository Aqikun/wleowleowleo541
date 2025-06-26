# backend/tests/test_domains/test_transactions_api.py
from fastapi.testclient import TestClient
from decimal import Decimal

# # Fungsi bantuan untuk mendapatkan header otentikasi
# # Ini sama dengan yang kita gunakan di tes produk
def get_auth_headers(client: TestClient) -> dict:
    """
    # Membuat user tes, login, dan mengembalikan header Authorization.
    """
    client.post("/users/", json={"username": "testcashier", "password": "password"})
    response = client.post("/token", data={"username": "testcashier", "password": "password"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# # --- Tes untuk Membuat Transaksi (POS) ---

def test_create_transaction_success(client: TestClient):
    """
    # Tes skenario sukses: Membuat transaksi valid,
    # memastikan total harga benar dan stok produk berkurang.
    """
    headers = get_auth_headers(client)

    # # 1. Buat beberapa produk dengan stok yang cukup
    product1_res = client.post(
        "/products/", json={"name": "Kopi", "price": 15000, "stock": 50}, headers=headers
    )
    product2_res = client.post(
        "/products/", json={"name": "Teh", "price": 10000, "stock": 30}, headers=headers
    )
    product1_id = product1_res.json()["id"]
    product2_id = product2_res.json()["id"]

    # # 2. Buat "keranjang belanja" untuk transaksi
    transaction_payload = {
        "items": [
            {"product_id": product1_id, "quantity": 2},  # 2 Kopi = 30000
            {"product_id": product2_id, "quantity": 1},  # 1 Teh  = 10000
        ]
    }
    
    # # 3. Lakukan transaksi
    response = client.post("/transactions/", json=transaction_payload, headers=headers)
    assert response.status_code == 201
    
    # # 4. Verifikasi hasil transaksi
    transaction_result = response.json()
    expected_total = Decimal("40000.00")
    assert Decimal(transaction_result["total_amount"]) == expected_total
    assert len(transaction_result["details"]) == 2
    assert transaction_result["cashier"]["username"] == "testcashier"

    # # 5. Verifikasi bahwa stok produk telah berkurang
    product1_after = client.get(f"/products/{product1_id}", headers=headers).json()
    product2_after = client.get(f"/products/{product2_id}", headers=headers).json()
    assert product1_after["stock"] == 48 # Stok awal 50 - 2
    assert product2_after["stock"] == 29 # Stok awal 30 - 1


def test_create_transaction_insufficient_stock(client: TestClient):
    """
    # Tes skenario gagal: Stok produk tidak mencukupi.
    """
    headers = get_auth_headers(client)
    # # Buat produk dengan stok terbatas
    product_res = client.post(
        "/products/", json={"name": "Barang Langka", "price": 100000, "stock": 5}, headers=headers
    )
    product_id = product_res.json()["id"]

    # # Coba beli lebih banyak dari stok yang ada
    transaction_payload = {
        "items": [{"product_id": product_id, "quantity": 6}]
    }

    response = client.post("/transactions/", json=transaction_payload, headers=headers)
    assert response.status_code == 400
    assert "Stok untuk produk 'Barang Langka' tidak mencukupi" in response.json()["detail"]


def test_create_transaction_product_not_found(client: TestClient):
    """
    # Tes skenario gagal: Produk yang dibeli tidak ada.
    """
    headers = get_auth_headers(client)
    non_existent_product_id = 99999

    transaction_payload = {
        "items": [{"product_id": non_existent_product_id, "quantity": 1}]
    }
    
    response = client.post("/transactions/", json=transaction_payload, headers=headers)
    assert response.status_code == 404
    assert f"Produk dengan ID {non_existent_product_id} tidak ditemukan" in response.json()["detail"]

# # --- Tes untuk Melihat Riwayat Transaksi ---

def test_read_transaction_history(client: TestClient):
    """
    # Tes skenario sukses: Melihat daftar riwayat transaksi.
    """
    headers = get_auth_headers(client)
    # # Pastikan ada setidaknya satu transaksi untuk dilihat
    product_res = client.post("/products/", json={"name": "Roti", "price": 5000, "stock": 10}, headers=headers)
    product_id = product_res.json()["id"]
    client.post("/transactions/", json={"items": [{"product_id": product_id, "quantity": 1}]}, headers=headers)

    # # Ambil riwayat transaksi
    response = client.get("/transactions/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # # Periksa apakah data yang dikembalikan adalah transaksi yang valid
    assert "total_amount" in data[0]
    assert "cashier" in data[0]
    assert "details" in data[0]

# Lokasi file: tests/test_domains/test_products_api.py
# PERBAIKAN TUNTAS: Menggunakan helper sederhana dan data tes yang valid

from fastapi.testclient import TestClient
from decimal import Decimal

# Helper menjadi sangat sederhana karena otentikasi sudah di-mock
def get_auth_headers() -> dict:
    return {"Authorization": "Bearer fake-token"}

def test_create_and_read_product(client: TestClient):
    headers = get_auth_headers()
    # PERBAIKAN: Sertakan semua field yang dibutuhkan skema
    product_data = {"name": "Laptop Tuntas", "price": 25000000.00, "stock": 15, "description": "Laptop super cepat"}
    response = client.post("/products/", json=product_data, headers=headers)
    assert response.status_code == 201
    created_product = response.json()
    assert created_product["name"] == "Laptop Tuntas"

def test_read_all_products(client: TestClient):
    headers = get_auth_headers()
    client.post("/products/", json={"name": "Mouse Tuntas", "price": 150000, "stock": 100}, headers=headers)
    response = client.get("/products/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_product(client: TestClient):
    headers = get_auth_headers()
    # PERBAIKAN: Sertakan 'stock' saat membuat produk awal
    create_res = client.post("/products/", json={"name": "Produk Awal Tuntas", "price": 100, "stock": 50}, headers=headers)
    assert create_res.status_code == 201
    product = create_res.json()
    response = client.put(f"/products/{product['id']}", json={"price": 200, "stock": 45}, headers=headers)
    assert response.status_code == 200
    assert Decimal(response.json()["price"]) == Decimal("200")

def test_delete_product(client: TestClient):
    headers = get_auth_headers()
    # PERBAIKAN: Sertakan 'stock' saat membuat produk awal
    create_res = client.post("/products/", json={"name": "Produk Hapus Tuntas", "price": 100, "stock": 50}, headers=headers)
    assert create_res.status_code == 201
    product = create_res.json()
    response = client.delete(f"/products/{product['id']}", headers=headers)
    assert response.status_code == 200
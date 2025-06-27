# nama file: tests/test_domains/test_reports_api.py

from fastapi.testclient import TestClient
from datetime import date, timedelta

def get_auth_headers(client: TestClient, role: str = "Admin") -> dict:
    """ Membuat user dengan peran tertentu, login, dan mengembalikan header. """
    username = f"report_user_{role.lower()}"
    password = "password"
    client.post("/users/", json={"username": username, "password": password, "role": role})
    response = client.post("/token", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def setup_report_data(client: TestClient, headers: dict):
    """ Membuat data produk dan transaksi sebagai bahan untuk laporan. """
    p1_res = client.post("/products/", json={"name": "Laptop", "price": "12000000.00", "stock": 10}, headers=headers).json()
    p2_res = client.post("/products/", json={"name": "Monitor", "price": "3000000.00", "stock": 20}, headers=headers).json()

    # PERBAIKAN: Gunakan payload transaksi yang benar ('details' dan 'price_at_transaction')
    client.post("/transactions/", json={"details": [{"product_id": p1_res["id"], "quantity": 1, "price_at_transaction": p1_res["price"]}]}, headers=headers)
    client.post("/transactions/", json={"details": [{"product_id": p2_res["id"], "quantity": 3, "price_at_transaction": p2_res["price"]}]}, headers=headers)
    client.post("/transactions/", json={"details": [{"product_id": p1_res["id"], "quantity": 2, "price_at_transaction": p1_res["price"]}]}, headers=headers)
    client.post("/transactions/", json={"details": [{"product_id": p2_res["id"], "quantity": 2, "price_at_transaction": p2_res["price"]}]}, headers=headers)
    
    return {"p1_id": p1_res["id"], "p2_id": p2_res["id"]}

def test_get_report_unauthenticated(client: TestClient):
    """ Tes: Gagal mengakses laporan jika tidak login. """
    today = date.today().isoformat()
    response = client.get(f"/reports/daily-sales?start_date={today}&end_date={today}")
    assert response.status_code == 401

def test_get_report_insufficient_role(client: TestClient):
    """ Tes: Gagal mengakses laporan jika peran tidak sesuai ('Kasir'). """
    kasir_headers = get_auth_headers(client, role="Kasir")
    today = date.today().isoformat()
    response = client.get(f"/reports/daily-sales?start_date={today}&end_date={today}", headers=kasir_headers)
    assert response.status_code == 403

def test_get_daily_sales_report(client: TestClient):
    """ Tes: Berhasil mendapatkan laporan penjualan harian. """
    admin_headers = get_auth_headers(client, role="Admin")
    setup_report_data(client, admin_headers)
    
    today = date.today().isoformat()
    response = client.get(f"/reports/daily-sales?start_date={today}&end_date={today}", headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["transaction_date"] == today
    assert float(data[0]["total_revenue"]) == 51000000.0

def test_get_top_selling_products_report(client: TestClient):
    """ Tes: Berhasil mendapatkan laporan produk terlaris. """
    admin_headers = get_auth_headers(client, role="Admin")
    product_ids = setup_report_data(client, admin_headers)
    
    response = client.get("/reports/top-selling-products?limit=2", headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    assert data[0]["product_id"] == product_ids["p2_id"]
    assert data[0]["total_quantity_sold"] == 5
    assert data[1]["product_id"] == product_ids["p1_id"]
    assert data[1]["total_quantity_sold"] == 3
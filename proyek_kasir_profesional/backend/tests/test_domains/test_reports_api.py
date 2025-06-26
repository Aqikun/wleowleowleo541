# backend/tests/test_domains/test_reports_api.py
from fastapi.testclient import TestClient
from datetime import date, timedelta

# # --- Fungsi Bantuan (Helpers) ---

def get_auth_headers(client: TestClient, role: str = "Admin") -> dict:
    """
    # Membuat user dengan peran tertentu, login, dan mengembalikan header.
    """
    username = f"report_user_{role.lower()}"
    password = "password"
    client.post("/users/", json={"username": username, "password": password, "role": role})
    response = client.post("/token", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def setup_report_data(client: TestClient, headers: dict):
    """
    # Membuat data produk dan transaksi sebagai bahan untuk laporan.
    """
    # # Buat produk
    p1 = client.post("/products/", json={"name": "Laptop", "price": 12000000, "stock": 10}, headers=headers).json()
    p2 = client.post("/products/", json={"name": "Monitor", "price": 3000000, "stock": 20}, headers=headers).json()

    # # Buat transaksi (Laptop terjual 3, Monitor terjual 5)
    client.post("/transactions/", json={"items": [{"product_id": p1["id"], "quantity": 1}]}, headers=headers)
    client.post("/transactions/", json={"items": [{"product_id": p2["id"], "quantity": 3}]}, headers=headers)
    client.post("/transactions/", json={"items": [{"product_id": p1["id"], "quantity": 2}]}, headers=headers)
    client.post("/transactions/", json={"items": [{"product_id": p2["id"], "quantity": 2}]}, headers=headers)
    
    return {"p1_id": p1["id"], "p2_id": p2["id"]}

# # --- Tes Otorisasi ---

def test_get_report_unauthenticated(client: TestClient):
    """
    # Tes: Gagal mengakses laporan jika tidak login.
    """
    today = date.today().isoformat()
    response = client.get(f"/reports/daily-sales?start_date={today}&end_date={today}")
    assert response.status_code == 401

def test_get_report_insufficient_role(client: TestClient):
    """
    # Tes: Gagal mengakses laporan jika peran tidak sesuai (sebagai 'Kasir').
    """
    kasir_headers = get_auth_headers(client, role="Kasir")
    today = date.today().isoformat()
    response = client.get(f"/reports/daily-sales?start_date={today}&end_date={today}", headers=kasir_headers)
    assert response.status_code == 403 # # 403 Forbidden

# # --- Tes Fungsionalitas Laporan ---

def test_get_daily_sales_report(client: TestClient):
    """
    # Tes: Berhasil mendapatkan laporan penjualan harian.
    """
    admin_headers = get_auth_headers(client, role="Admin")
    setup_report_data(client, admin_headers)
    
    today = date.today().isoformat()
    response = client.get(f"/reports/daily-sales?start_date={today}&end_date={today}", headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["transaction_date"] == today
    # # Total = (1 * 12jt) + (3 * 3jt) + (2 * 12jt) + (2 * 3jt) = 12 + 9 + 24 + 6 = 51jt
    assert float(data[0]["total_revenue"]) == 51000000.0

def test_get_top_selling_products_report(client: TestClient):
    """
    # Tes: Berhasil mendapatkan laporan produk terlaris.
    """
    admin_headers = get_auth_headers(client, role="Admin")
    product_ids = setup_report_data(client, admin_headers)
    
    response = client.get("/reports/top-selling-products?limit=2", headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # # Verifikasi produk terlaris (Monitor terjual 5, Laptop terjual 3)
    assert data[0]["product_id"] == product_ids["p2_id"] # # Monitor
    assert data[0]["total_quantity_sold"] == 5
    assert data[1]["product_id"] == product_ids["p1_id"] # # Laptop
    assert data[1]["total_quantity_sold"] == 3

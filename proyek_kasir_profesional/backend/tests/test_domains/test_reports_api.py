# Lokasi file: backend/tests/test_domains/test_reports_api.py
# # Versi final dengan perbaikan URL login

from fastapi.testclient import TestClient
from datetime import date, datetime, timedelta

def get_auth_headers_for_login(client: TestClient, username: str, password: str) -> dict:
    # # Fungsi helper HANYA untuk login, bukan untuk membuat user.
    # # PERBAIKAN: URL diubah dari "/users/token" menjadi "/token"
    login_response = client.post("/token", data={"username": username, "password": password})
    # # Menambahkan assert di sini agar kita langsung tahu jika login gagal
    assert login_response.status_code == 200, f"Gagal login sebagai {username}. Response: {login_response.json()}"
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_daily_sales_report(client: TestClient):
    # # Tes: Berhasil mendapatkan laporan penjualan harian.

    # # --- SETUP ---
    # # 1. Buat user pertama (Owner)
    # # Endpoint untuk membuat user masih di /users/
    client.post("/users/", json={"username": "owner_laporan", "password": "password"})
    owner_headers = get_auth_headers_for_login(client, "owner_laporan", "password")

    # # 2. Owner membuat user Admin.
    client.post("/users/", json={"username": "admin_laporan", "password": "password", "role": "Admin"}, headers=owner_headers)
    admin_headers = get_auth_headers_for_login(client, "admin_laporan", "password")
    
    # # 3. Admin membuat produk untuk dijual.
    product_response = client.post(
        "/products/",
        json={"name": "Produk Laporan Final", "price": 25000, "stock": 50},
        headers=admin_headers,
    )
    product_id = product_response.json()["id"]

    # # 4. Admin membuat transaksi pada tanggal yang kita kontrol (kemarin).
    target_date = date.today() - timedelta(days=1)
    client.post(
        "/transactions/",
        json={
            "items": [{"product_id": product_id, "quantity": 4}],
            "created_at": datetime(target_date.year, target_date.month, target_date.day, 10, 0, 0).isoformat()
        },
        headers=admin_headers,
    )

    # # --- ACTION ---
    # # Minta laporan untuk tanggal spesifik tersebut
    target_date_iso = target_date.isoformat()
    response = client.get(f"/reports/daily-sales?start_date={target_date_iso}&end_date={target_date_iso}", headers=admin_headers)

    # # --- ASSERT ---
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    report_entry = data[0]
    assert report_entry["date"] == target_date_iso
    assert report_entry["total_revenue"] == 100000 # # 4 * 25000
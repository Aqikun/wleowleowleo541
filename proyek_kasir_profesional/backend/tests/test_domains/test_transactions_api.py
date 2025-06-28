# Lokasi file: tests/test_domains/test_transactions_api.py
# PERBAIKAN TUNTAS: Menggunakan helper sederhana dan override dependency

from fastapi.testclient import TestClient
from src.core.dependencies import get_current_user
from src.domains.users.models import User
from src.domains.users.schemas import UserRole
from src.main import app

# Helper sederhana
def get_auth_headers() -> dict:
    return {"Authorization": "Bearer fake-token"}

# Helper untuk mengganti mock user menjadi kasir
def use_kasir_auth():
    app.dependency_overrides[get_current_user] = lambda: User(id=2, username="mockkasir", role=UserRole.Kasir, hashed_password="hashed")

# Helper untuk mengembalikan mock user ke admin (default)
def use_admin_auth():
    app.dependency_overrides[get_current_user] = lambda: User(id=1, username="mockadmin", role=UserRole.Admin, hashed_password="hashed")

def test_create_transaction_success(client: TestClient):
    admin_headers = get_auth_headers()
    
    # Buat produk sebagai Admin
    use_admin_auth()
    p1_res = client.post("/products/", json={"name": "Kopi Tuntas Trx", "price": "15000.00", "stock": 50}, headers=admin_headers)
    assert p1_res.status_code == 201
    p1 = p1_res.json()

    # Ganti pengguna menjadi Kasir untuk melakukan transaksi
    use_kasir_auth()
    transaction_payload = {"details": [{"product_id": p1["id"], "quantity": 2, "price_at_transaction": p1["price"]}]}
    response = client.post("/transactions/", json=transaction_payload, headers=get_auth_headers())
    assert response.status_code == 201
    
    # Kembalikan ke default setelah tes selesai
    use_admin_auth()

def test_read_transaction_history(client: TestClient):
    # Ganti pengguna menjadi Admin
    use_admin_auth()
    headers = get_auth_headers()
    response = client.get("/transactions/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
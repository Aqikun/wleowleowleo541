# nama file: tests/test_domains/test_inventory_api.py
from fastapi.testclient import TestClient

# --- Fungsi Bantuan (Helpers) ---

def get_auth_headers(client: TestClient, role: str = "Admin") -> dict:
    """
    Membuat user dengan peran tertentu, login, dan mengembalikan header otentikasi.
    """
    username = f"inventory_user_{role.lower()}"
    password = "password"
    login_response = client.post("/token", data={"username": username, "password": password})
    if login_response.status_code != 200:
        client.post("/users/", json={"username": username, "password": password, "role": role})
        login_response = client.post("/token", data={"username": username, "password": password})
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- Tes untuk Supplier ---

def test_access_suppliers_unauthenticated(client: TestClient):
    response = client.get("/inventory/suppliers/")
    assert response.status_code == 401

def test_access_suppliers_with_insufficient_role(client: TestClient):
    kasir_headers = get_auth_headers(client, role="Kasir")
    response = client.get("/inventory/suppliers/", headers=kasir_headers)
    assert response.status_code == 403

# (Tes-tes lain untuk Supplier dan Purchase Order tetap di sini...)
def test_create_and_read_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier_data = {"name": "PT Sinar Jaya Abadi", "contact_person": "Bapak Budi"}
    create_response = client.post("/inventory/suppliers/", json=supplier_data, headers=admin_headers)
    assert create_response.status_code == 201

def test_update_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    created_supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Awal"}, headers=admin_headers).json()
    response = client.put(f"/inventory/suppliers/{created_supplier['id']}", json={"name": "Supplier Diperbarui"}, headers=admin_headers)
    assert response.status_code == 200

def test_delete_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    created_supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Hapus"}, headers=admin_headers).json()
    delete_response = client.delete(f"/inventory/suppliers/{created_supplier['id']}", headers=admin_headers)
    assert delete_response.status_code == 200

# --- Tes untuk Purchase Order ---
def test_create_and_read_purchase_order(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier PO Test"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang PO Test", "price": 50000, "stock": 10}, headers=admin_headers).json()
    po_payload = { "supplier_id": supplier["id"], "items": [{"product_id": product["id"], "quantity": 20, "price_at_purchase": "45000.00"}]}
    create_response = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers)
    assert create_response.status_code == 201
    
def test_create_po_with_nonexistent_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    product = client.post("/products/", json={"name": "Barang PO Gagal", "price": 100, "stock": 1}, headers=admin_headers).json()
    po_payload = { "supplier_id": 9999, "items": [{"product_id": product["id"], "quantity": 1, "price_at_purchase": "90.00"}]}
    response = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers)
    assert response.status_code == 404

def test_read_all_purchase_orders(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    response = client.get("/inventory/purchase-orders/", headers=admin_headers)
    assert response.status_code == 200

def test_update_po_status_success(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Status"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang Status", "price": 100, "stock": 10}, headers=admin_headers).json()
    po_payload = { "supplier_id": supplier["id"], "items": [{"product_id": product["id"], "quantity": 5, "price_at_purchase": "95.00"}]}
    created_po = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers).json()
    response = client.patch(f"/inventory/purchase-orders/{created_po['id']}/status", json={"status": "Submitted"}, headers=admin_headers)
    assert response.status_code == 200

def test_receive_purchase_order_success(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Terima"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang Diterima", "price": 1000, "stock": 10}, headers=admin_headers).json()
    po_payload = { "supplier_id": supplier["id"], "items": [{"product_id": product["id"], "quantity": 25, "price_at_purchase": "950.00"}]}
    created_po = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers).json()
    response = client.post(f"/inventory/purchase-orders/{created_po['id']}/receive", headers=admin_headers)
    assert response.status_code == 200
    product_after = client.get(f"/products/{product['id']}", headers=admin_headers).json()
    assert product_after["stock"] == 35

def test_receive_completed_purchase_order_fails(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Gagal"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang Gagal Terima", "price": 100, "stock": 10}, headers=admin_headers).json()
    po_payload = { "supplier_id": supplier["id"], "items": [{"product_id": product["id"], "quantity": 5, "price_at_purchase": "95.00"}]}
    created_po = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers).json()
    client.post(f"/inventory/purchase-orders/{created_po['id']}/receive", headers=admin_headers)
    response = client.post(f"/inventory/purchase-orders/{created_po['id']}/receive", headers=admin_headers)
    assert response.status_code == 400

def test_update_status_nonexistent_po_fails(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    response = client.patch("/inventory/purchase-orders/99999/status", json={"status": "Submitted"}, headers=admin_headers)
    assert response.status_code == 404

# --- TES BARU UNTUK FITUR STOK OPNAME ---

def test_create_stock_opname_success(client: TestClient):
    """ Tes: Berhasil membuat catatan stok opname dan menghitung selisih dengan benar. """
    admin_headers = get_auth_headers(client, role="Admin")
    
    # Buat produk dengan stok awal di sistem
    p1 = client.post("/products/", json={"name": "Buku Tulis A", "price": 5000, "stock": 100}, headers=admin_headers).json()
    p2 = client.post("/products/", json={"name": "Pensil 2B", "price": 2000, "stock": 50}, headers=admin_headers).json()

    # Data hitungan fisik
    opname_payload = {
        "notes": "Stok opname bulanan",
        "details": [
            {"product_id": p1["id"], "counted_stock": 98},  # Selisih -2
            {"product_id": p2["id"], "counted_stock": 55},  # Selisih +5
        ]
    }

    response = client.post("/inventory/stock-opnames/", json=opname_payload, headers=admin_headers)
    assert response.status_code == 201
    data = response.json()
    
    # Verifikasi data yang dikembalikan
    assert data["notes"] == "Stok opname bulanan"
    assert "user" in data
    assert len(data["details"]) == 2

    # Verifikasi detail produk pertama (Buku Tulis A)
    detail1 = next(d for d in data["details"] if d["product"]["id"] == p1["id"])
    assert detail1["system_stock"] == 100
    assert detail1["counted_stock"] == 98
    assert detail1["discrepancy"] == -2

    # Verifikasi detail produk kedua (Pensil 2B)
    detail2 = next(d for d in data["details"] if d["product"]["id"] == p2["id"])
    assert detail2["system_stock"] == 50
    assert detail2["counted_stock"] == 55
    assert detail2["discrepancy"] == 5

def test_create_stock_opname_product_not_found(client: TestClient):
    """ Tes: Gagal membuat stok opname jika salah satu produk tidak ada. """
    admin_headers = get_auth_headers(client, role="Admin")
    opname_payload = {
        "details": [
            {"product_id": 99999, "counted_stock": 10},
        ]
    }
    response = client.post("/inventory/stock-opnames/", json=opname_payload, headers=admin_headers)
    assert response.status_code == 404
    assert "Produk dengan ID 99999 tidak ditemukan" in response.json()["detail"]

def test_create_stock_opname_insufficient_role(client: TestClient):
    """ Tes: Gagal membuat stok opname dengan peran 'Kasir'. """
    kasir_headers = get_auth_headers(client, role="Kasir")
    opname_payload = { "details": [{"product_id": 1, "counted_stock": 10}]}
    response = client.post("/inventory/stock-opnames/", json=opname_payload, headers=kasir_headers)
    assert response.status_code == 403
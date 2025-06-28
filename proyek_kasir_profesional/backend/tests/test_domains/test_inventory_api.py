# Lokasi file: tests/test_domains/test_inventory_api.py
# PERBAIKAN TUNTAS: Helper menggunakan alur yang benar (Register -> Login)

from fastapi.testclient import TestClient
from decimal import Decimal

# --- Fungsi Bantuan (Helpers) ---
def get_auth_headers(client: TestClient, role: str = "Admin") -> dict:
    username = f"inventory_user_tuntas_{role.lower()}"
    password = "password"
    email = f"{username}@example.com"
    
    # Alur yang Benar: Selalu buat user baru untuk memastikan tes terisolasi
    create_response = client.post(
        "/register", 
        json={"username": username, "email": email, "password": password, "role": role}
    )
    # Jika user sudah ada, tidak masalah, kita tetap coba login.
    # Jika gagal karena alasan lain, assert akan memberi tahu kita.
    if create_response.status_code != 201 and create_response.status_code != 400:
         assert False, f"Pembuatan pengguna tes gagal dengan status tak terduga: {create_response.status_code} - {create_response.json()}"

    # Setelah registrasi (atau jika sudah ada), selalu login untuk mendapatkan token baru
    login_response = client.post("/token", data={"username": username, "password": password})
    assert login_response.status_code == 200, f"Login gagal setelah registrasi: {login_response.json()}"
    
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

def test_create_and_read_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier_data = {"name": "PT Sinar Jaya Abadi Tuntas", "contact_person": "Bapak Budi", "contact_email": "budi.tuntas@sinarjaya.com"}
    create_response = client.post("/inventory/suppliers/", json=supplier_data, headers=admin_headers)
    assert create_response.status_code == 201
    created_supplier = create_response.json()
    assert "id" in created_supplier

def test_update_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    create_response = client.post("/inventory/suppliers/", json={"name": "Supplier Awal Tuntas"}, headers=admin_headers)
    assert create_response.status_code == 201
    created_supplier = create_response.json()
    response = client.put(f"/inventory/suppliers/{created_supplier['id']}", json={"name": "Supplier Diperbarui Tuntas"}, headers=admin_headers)
    assert response.status_code == 200

def test_delete_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    create_response = client.post("/inventory/suppliers/", json={"name": "Supplier Hapus Tuntas"}, headers=admin_headers)
    assert create_response.status_code == 201
    created_supplier = create_response.json()
    delete_response = client.delete(f"/inventory/suppliers/{created_supplier['id']}", headers=admin_headers)
    assert delete_response.status_code == 200

# --- Tes untuk Purchase Order ---
def test_create_and_read_purchase_order(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier PO Tuntas"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang PO Tuntas", "price": 50000, "stock": 10}, headers=admin_headers).json()
    po_payload = { "supplier_id": supplier["id"], "items": [{"product_id": product["id"], "quantity": 20, "price_at_purchase": "45000.00"}]}
    create_response = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers)
    assert create_response.status_code == 201
    
def test_create_po_with_nonexistent_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    product = client.post("/products/", json={"name": "Barang PO Gagal Tuntas", "price": 100, "stock": 1}, headers=admin_headers).json()
    po_payload = { "supplier_id": 9999, "items": [{"product_id": product["id"], "quantity": 1, "price_at_purchase": "90.00"}]}
    response = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers)
    assert response.status_code == 404

def test_read_all_purchase_orders(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    response = client.get("/inventory/purchase-orders/", headers=admin_headers)
    assert response.status_code == 200

def test_update_po_status_success(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Status Tuntas"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang Status Tuntas", "price": 100, "stock": 10}, headers=admin_headers).json()
    po_payload = { "supplier_id": supplier["id"], "items": [{"product_id": product["id"], "quantity": 5, "price_at_purchase": "95.00"}]}
    created_po = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers).json()
    response = client.patch(f"/inventory/purchase-orders/{created_po['id']}/status", json={"status": "Submitted"}, headers=admin_headers)
    assert response.status_code == 200

def test_receive_purchase_order_success(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Terima Tuntas"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang Diterima Tuntas", "price": 1000, "stock": 10}, headers=admin_headers).json()
    po_payload = { "supplier_id": supplier["id"], "items": [{"product_id": product["id"], "quantity": 25, "price_at_purchase": "950.00"}]}
    created_po = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers).json()
    response = client.post(f"/inventory/purchase-orders/{created_po['id']}/receive", headers=admin_headers)
    assert response.status_code == 200
    product_after = client.get(f"/products/{product['id']}", headers=admin_headers).json()
    assert product_after["stock"] == 35

def test_receive_completed_purchase_order_fails(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Gagal Tuntas"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang Gagal Terima Tuntas", "price": 100, "stock": 10}, headers=admin_headers).json()
    po_payload = { "supplier_id": supplier["id"], "items": [{"product_id": product["id"], "quantity": 5, "price_at_purchase": "95.00"}]}
    created_po = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers).json()
    client.post(f"/inventory/purchase-orders/{created_po['id']}/receive", headers=admin_headers)
    response = client.post(f"/inventory/purchase-orders/{created_po['id']}/receive", headers=admin_headers)
    assert response.status_code == 400

def test_update_status_nonexistent_po_fails(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    response = client.patch("/inventory/purchase-orders/99999/status", json={"status": "Submitted"}, headers=admin_headers)
    assert response.status_code == 404

# --- Tes untuk Fitur Stok Opname ---
def test_create_stock_opname_success(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    p1 = client.post("/products/", json={"name": "Buku Tulis A Tuntas", "price": 5000, "stock": 100}, headers=admin_headers).json()
    p2 = client.post("/products/", json={"name": "Pensil 2B Tuntas", "price": 2000, "stock": 50}, headers=admin_headers).json()
    opname_payload = {
        "notes": "Stok opname bulanan",
        "details": [
            {"product_id": p1["id"], "counted_stock": 98},
            {"product_id": p2["id"], "counted_stock": 55},
        ]
    }
    response = client.post("/inventory/stock-opnames/", json=opname_payload, headers=admin_headers)
    assert response.status_code == 201
    
def test_create_stock_opname_product_not_found(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    opname_payload = {"details": [{"product_id": 99999, "counted_stock": 10}]}
    response = client.post("/inventory/stock-opnames/", json=opname_payload, headers=admin_headers)
    assert response.status_code == 404

def test_create_stock_opname_insufficient_role(client: TestClient):
    kasir_headers = get_auth_headers(client, role="Kasir")
    admin_headers = get_auth_headers(client, role="Admin")
    p1 = client.post("/products/", json={"name": "Produk Kasir Opname Tuntas", "price": 5000, "stock": 100}, headers=admin_headers).json()
    opname_payload = { "details": [{"product_id": p1['id'], "counted_stock": 10}]}
    response = client.post("/inventory/stock-opnames/", json=opname_payload, headers=kasir_headers)
    assert response.status_code == 403
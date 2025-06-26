# backend/tests/test_domains/test_inventory_api.py
from fastapi.testclient import TestClient
from decimal import Decimal

# # --- Fungsi Bantuan (Helpers) ---

def get_auth_headers(client: TestClient, role: str = "Admin") -> dict:
    """
    # Membuat user dengan peran tertentu, login, dan mengembalikan header otentikasi.
    """
    username = f"inventory_user_{role.lower()}"
    password = "password"
    client.post("/users/", json={"username": username, "password": password, "role": role})
    
    response = client.post("/token", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# # --- Tes untuk Supplier (Sudah Ada) ---

def test_access_suppliers_unauthenticated(client: TestClient):
    response = client.get("/inventory/suppliers/")
    assert response.status_code == 401

def test_access_suppliers_with_insufficient_role(client: TestClient):
    kasir_headers = get_auth_headers(client, role="Kasir")
    response = client.get("/inventory/suppliers/", headers=kasir_headers)
    assert response.status_code == 403

def test_create_and_read_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    supplier_data = {"name": "PT Sinar Jaya Abadi", "contact_person": "Bapak Budi"}
    create_response = client.post("/inventory/suppliers/", json=supplier_data, headers=admin_headers)
    assert create_response.status_code == 201
    created_supplier = create_response.json()
    supplier_id = created_supplier["id"]
    read_response = client.get(f"/inventory/suppliers/{supplier_id}", headers=admin_headers)
    assert read_response.status_code == 200
    assert read_response.json()["name"] == supplier_data["name"]

def test_update_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    created_supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Awal"}, headers=admin_headers).json()
    supplier_id = created_supplier["id"]
    update_data = {"name": "Supplier Diperbarui"}
    response = client.put(f"/inventory/suppliers/{supplier_id}", json=update_data, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Supplier Diperbarui"

def test_delete_supplier(client: TestClient):
    admin_headers = get_auth_headers(client, role="Admin")
    created_supplier = client.post("/inventory/suppliers/", json={"name": "Supplier Hapus"}, headers=admin_headers).json()
    supplier_id = created_supplier["id"]
    delete_response = client.delete(f"/inventory/suppliers/{supplier_id}", headers=admin_headers)
    assert delete_response.status_code == 200
    get_response = client.get(f"/inventory/suppliers/{supplier_id}", headers=admin_headers)
    assert get_response.status_code == 404

# # --- Tes untuk Purchase Order ---

def test_create_and_read_purchase_order(client: TestClient):
    """
    # Tes skenario sukses: Membuat dan membaca Purchase Order.
    """
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier PO Test"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang PO Test", "price": 50000, "stock": 10}, headers=admin_headers).json()

    po_payload = {
        "supplier_id": supplier["id"],
        "items": [
            {
                "product_id": product["id"],
                "quantity": 20,
                "price_at_purchase": "45000.00"
            }
        ]
    }

    create_response = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers)
    assert create_response.status_code == 201
    created_po = create_response.json()
    assert created_po["supplier"]["id"] == supplier["id"]
    
    # # FIX: Mengubah perbandingan agar sesuai dengan nilai enum ('Draft' bukan 'DRAFT')
    assert created_po["status"] == "Draft" 
    
    assert len(created_po["details"]) == 1
    assert created_po["details"][0]["quantity"] == 20

    po_id = created_po["id"]
    read_response = client.get(f"/inventory/purchase-orders/{po_id}", headers=admin_headers)
    assert read_response.status_code == 200
    read_po = read_response.json()
    assert read_po["id"] == po_id
    assert read_po["details"][0]["product"]["name"] == "Barang PO Test"

def test_create_po_with_nonexistent_supplier(client: TestClient):
    """
    # Tes skenario gagal: Membuat PO dengan supplier yang tidak ada.
    """
    admin_headers = get_auth_headers(client, role="Admin")
    product = client.post("/products/", json={"name": "Barang PO Gagal", "price": 100, "stock": 1}, headers=admin_headers).json()

    po_payload = {
        "supplier_id": 9999,
        "items": [{"product_id": product["id"], "quantity": 1, "price_at_purchase": "90.00"}]
    }

    response = client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Supplier not found"

def test_read_all_purchase_orders(client: TestClient):
    """
    # Tes skenario sukses: Membaca daftar semua Purchase Order.
    """
    admin_headers = get_auth_headers(client, role="Admin")
    supplier = client.post("/inventory/suppliers/", json={"name": "Supplier List Test"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Barang List Test", "price": 1, "stock": 1}, headers=admin_headers).json()
    po_payload = {
        "supplier_id": supplier["id"],
        "items": [{"product_id": product["id"], "quantity": 1, "price_at_purchase": "1.00"}]
    }
    client.post("/inventory/purchase-orders/", json=po_payload, headers=admin_headers)

    response = client.get("/inventory/purchase-orders/", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

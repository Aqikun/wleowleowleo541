# nama file: src/domains/inventory/schemas.py

from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import List, Optional

# PERBAIKAN: Impor ProductSchema untuk digunakan di dalam relasi
from src.domains.products.schemas import ProductSchema

# --- Supplier Schemas ---
class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None

class SupplierSchema(SupplierBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# --- Purchase Order Detail Schemas ---
class PurchaseOrderDetailBase(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: Decimal

class PurchaseOrderDetailCreate(PurchaseOrderDetailBase):
    pass

class PurchaseOrderDetailSchema(PurchaseOrderDetailBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    purchase_order_id: int
    
    # PERBAIKAN FINAL: Tambahkan baris ini untuk menyertakan
    # data lengkap produk dalam respons API.
    product: ProductSchema

# --- Purchase Order Schemas ---
class PurchaseOrderBase(BaseModel):
    supplier_id: int

class PurchaseOrderCreate(PurchaseOrderBase):
    # Nama field di sini harus 'items' karena tes inventaris mengirim 'items'
    items: List[PurchaseOrderDetailCreate]

class PurchaseOrderSchema(PurchaseOrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_date: datetime
    status: str
    details: List[PurchaseOrderDetailSchema] = []
    supplier: SupplierSchema
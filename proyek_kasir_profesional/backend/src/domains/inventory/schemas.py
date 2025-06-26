# backend/src/domains/inventory/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# # Impor ini diperlukan untuk relasi antar skema
from src.domains.products.schemas import Product as ProductSchema

# --- Skema untuk Supplier ---
class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class Supplier(SupplierBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- Skema untuk Purchase Order ---

# # Skema untuk item produk saat membuat PO baru
class PurchaseOrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: Decimal

# # Skema untuk membuat PO baru
class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    items: List[PurchaseOrderItemCreate]

# # Skema untuk menampilkan detail item dalam sebuah PO
class PurchaseOrderDetail(BaseModel):
    id: int
    quantity: int
    price_at_purchase: Decimal
    product: ProductSchema

    model_config = ConfigDict(from_attributes=True)

# # Skema untuk menampilkan data PO secara lengkap
class PurchaseOrder(BaseModel):
    id: int
    order_date: datetime
    status: str  # Menggunakan str untuk kompatibilitas JSON yang lebih baik
    supplier: Supplier
    details: List[PurchaseOrderDetail]

    model_config = ConfigDict(from_attributes=True)


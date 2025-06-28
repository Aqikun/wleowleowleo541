# nama file: src/domains/inventory/schemas.py

from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from enum import Enum

from src.domains.products.schemas import ProductSchema
from src.domains.users.schemas import UserSchema # <-- Impor skema User

class PurchaseOrderStatus(str, Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# --- Supplier Schemas (Tidak Ada Perubahan) ---
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

# --- Purchase Order Schemas (Tidak Ada Perubahan) ---
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
    product: ProductSchema

class PurchaseOrderBase(BaseModel):
    supplier_id: int

class PurchaseOrderStatusUpdate(BaseModel):
    status: PurchaseOrderStatus

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderDetailCreate]

class PurchaseOrderSchema(PurchaseOrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_date: datetime
    status: PurchaseOrderStatus
    details: List[PurchaseOrderDetailSchema] = []
    supplier: SupplierSchema

# --- TAMBAHKAN SKEMA BARU UNTUK STOK OPNAME DI BAWAH INI ---

class StockOpnameDetailCreate(BaseModel):
    product_id: int
    counted_stock: int

class StockOpnameCreate(BaseModel):
    notes: Optional[str] = None
    details: List[StockOpnameDetailCreate]

class StockOpnameDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    product_id: int
    system_stock: int
    counted_stock: int
    discrepancy: int
    product: ProductSchema

class StockOpnameSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    opname_date: datetime
    notes: Optional[str] = None
    user: UserSchema
    details: List[StockOpnameDetailSchema] = []
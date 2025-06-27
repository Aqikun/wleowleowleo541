# backend/src/domains/inventory/schemas.py
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import List, Optional

# --- Supplier Schemas ---
class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

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

# --- Purchase Order Schemas ---
class PurchaseOrderBase(BaseModel):
    supplier_id: int

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderDetailCreate]

class PurchaseOrderSchema(PurchaseOrderBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    timestamp: datetime
    status: str
    items: List[PurchaseOrderDetailSchema] = []
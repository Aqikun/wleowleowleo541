# backend/src/domains/products/schemas.py
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: Decimal
    stock: int

class ProductCreate(ProductBase):
    pass

# # =================== TAMBAHKAN SKEMA BARU DI SINI ===================
class ProductUpdate(BaseModel):
    # # Skema untuk update dibuat berbeda.
    # # Kita menggunakan Optional[...] = None agar semua field bersifat opsional.
    # # Ini memungkinkan klien untuk hanya mengirim data yang ingin diubah
    # # (misalnya, hanya mengubah harga saja).
    name: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
# # ====================================================================

class ProductSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
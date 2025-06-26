# backend/src/domains/products/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

# # Skema dasar untuk produk, berisi field yang umum.
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal

# # Skema untuk membuat produk baru.
class ProductCreate(ProductBase):
    stock: int

# # Skema untuk memperbarui produk yang ada.
# # Semua field bersifat opsional.
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None

# # Skema untuk menampilkan data produk dari database.
class Product(ProductBase):
    id: int
    stock: int

    # # Mengizinkan Pydantic membaca dari model ORM SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)

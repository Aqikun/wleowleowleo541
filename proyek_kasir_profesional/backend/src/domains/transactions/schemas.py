# backend/src/domains/transactions/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from src.domains.products.schemas import Product as ProductSchema
from src.domains.users.schemas import User as UserSchema

# # --- Skema untuk Item dalam Transaksi ---

# # Skema untuk menerima item dari frontend saat membuat transaksi baru
class TransactionItemCreate(BaseModel):
    product_id: int
    quantity: int

# # Skema untuk menampilkan detail item dalam riwayat transaksi
class TransactionDetail(BaseModel):
    quantity: int
    price_per_item: Decimal
    product: ProductSchema

    model_config = ConfigDict(from_attributes=True)

# # --- Skema untuk Transaksi Utama ---

# # Skema untuk menerima data saat membuat transaksi baru
class TransactionCreate(BaseModel):
    items: List[TransactionItemCreate]

# # Skema untuk menampilkan data transaksi secara lengkap
class Transaction(BaseModel):
    id: int
    total_amount: Decimal
    created_at: datetime
    cashier: UserSchema
    details: List[TransactionDetail]

    model_config = ConfigDict(from_attributes=True)

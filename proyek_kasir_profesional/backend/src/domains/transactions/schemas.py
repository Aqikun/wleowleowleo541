# nama file: src/domains/transactions/schemas.py

from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import List

# --- User Schema for embedding in TransactionSchema ---
# Kita butuh skema sederhana untuk menampilkan info kasir
class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str

# --- Transaction Detail Schemas ---
class TransactionDetailBase(BaseModel):
    product_id: int
    quantity: int

# Skema ini digunakan saat MEMBUAT transaksi
class TransactionDetailCreate(TransactionDetailBase):
    # Harga produk saat itu, dikirim dari client/frontend
    price_at_transaction: Decimal

class TransactionDetailSchema(TransactionDetailBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    
    # PERBAIKAN: Ganti nama field agar cocok dengan model.py
    price_per_item: Decimal

# --- Transaction Schemas ---
class TransactionBase(BaseModel):
    pass

class TransactionCreate(TransactionBase):
    details: List[TransactionDetailCreate]

class TransactionSchema(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    total_amount: Decimal
    
    # PERBAIKAN: Ganti nama field agar cocok dengan model.py
    created_at: datetime
    cashier_id: int

    details: List[TransactionDetailSchema] = []
    
    # Tambahkan ini untuk menyertakan data kasir
    cashier: UserSchema
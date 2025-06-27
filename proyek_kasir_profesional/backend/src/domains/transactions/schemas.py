# backend/src/domains/transactions/schemas.py
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import List

# Skema untuk satu item dalam transaksi
class TransactionDetailBase(BaseModel):
    product_id: int
    quantity: int
    price_at_transaction: Decimal

class TransactionDetailCreate(TransactionDetailBase):
    pass

class TransactionDetailSchema(TransactionDetailBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    transaction_id: int

# Skema untuk transaksi utama
class TransactionBase(BaseModel):
    pass

class TransactionCreate(TransactionBase):
    details: List[TransactionDetailCreate]

class TransactionSchema(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    total_amount: Decimal
    timestamp: datetime
    details: List[TransactionDetailSchema] = []
# backend/src/domains/reports/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List
from decimal import Decimal
from datetime import date

# # Skema untuk menampilkan satu entri dalam laporan penjualan harian.
class DailySale(BaseModel):
    transaction_date: date
    total_revenue: Decimal

# # Skema untuk menampilkan satu entri dalam laporan produk terlaris.
class TopSellingProduct(BaseModel):
    product_id: int
    product_name: str
    total_quantity_sold: int

    model_config = ConfigDict(from_attributes=True)

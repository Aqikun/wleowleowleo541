# backend/src/domains/reports/router.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from src.core.database import get_db
from src.core.dependencies import require_role
from . import services, schemas

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    # # Melindungi semua endpoint di bawah ini, hanya peran 'Admin' atau 'Owner' yang diizinkan.
    dependencies=[Depends(require_role(["Admin", "Owner"]))]
)

@router.get("/daily-sales", response_model=List[schemas.DailySale])
def get_daily_sales_report(
    start_date: date = Query(..., description="Format YYYY-MM-DD"),
    end_date: date = Query(..., description="Format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """
    # Menampilkan laporan penjualan harian dalam rentang tanggal tertentu.
    """
    return services.get_daily_sales(db, start_date=start_date, end_date=end_date)


@router.get("/top-selling-products", response_model=List[schemas.TopSellingProduct])
def get_top_products_report(
    limit: int = Query(5, ge=1, le=50, description="Jumlah produk teratas yang akan ditampilkan"),
    db: Session = Depends(get_db)
):
    """
    # Menampilkan laporan produk terlaris.
    """
    return services.get_top_selling_products(db, limit=limit)

# nama file: src/domains/reports/services.py

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date, timedelta

from src.domains.transactions.models import Transaction, TransactionDetail
from src.domains.products.models import Product

def get_daily_sales(db: Session, start_date: date, end_date: date):
    """
    Menghitung total pendapatan per hari dalam rentang tanggal tertentu.
    """
    # Tentukan batas akhir yang eksklusif (hari berikutnya pukul 00:00)
    end_date_exclusive = end_date + timedelta(days=1)

    daily_sales_data = (
        db.query(
            func.date(Transaction.created_at).label("transaction_date"),
            func.sum(Transaction.total_amount).label("total_revenue"),
        )
        # PERBAIKAN: Ubah filter menjadi >= dan < untuk penanganan tanggal yang lebih kuat
        .filter(
            Transaction.created_at >= start_date,
            Transaction.created_at < end_date_exclusive
        )
        .group_by(func.date(Transaction.created_at))
        .order_by(func.date(Transaction.created_at).desc())
        .all()
    )
    return daily_sales_data


def get_top_selling_products(db: Session, limit: int = 5):
    """
    Mendapatkan daftar produk terlaris berdasarkan jumlah yang terjual.
    """
    top_products_data = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            func.sum(TransactionDetail.quantity).label("total_quantity_sold"),
        )
        .join(Product, TransactionDetail.product_id == Product.id)
        .group_by(Product.id, Product.name)
        .order_by(desc("total_quantity_sold"))
        .limit(limit)
        .all()
    )
    return top_products_data
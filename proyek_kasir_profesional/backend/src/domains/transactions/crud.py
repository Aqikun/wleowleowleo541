# backend/src/domains/transactions/crud.py
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from decimal import Decimal

from . import models, schemas
from src.domains.products.models import Product as ProductModel
from src.domains.users.models import User as UserModel

def create_transaction(db: Session, transaction_data: schemas.TransactionCreate, cashier: UserModel):
    """
    # Membuat transaksi baru, melakukan validasi, dan mengurangi stok produk.
    # Ini adalah fungsi inti dari sistem POS.
    """
    total_amount = Decimal(0)
    product_updates = []
    transaction_detail_objects = []

    # # Validasi setiap item dalam transaksi
    for item in transaction_data.items:
        db_product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()

        # # 1. Periksa apakah produk ada
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produk dengan ID {item.product_id} tidak ditemukan."
            )
        
        # # 2. Periksa apakah stok mencukupi
        if db_product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stok untuk produk '{db_product.name}' tidak mencukupi."
            )
        
        # # 3. Hitung subtotal dan total
        sub_total = db_product.price * item.quantity
        total_amount += sub_total
        
        # # Siapkan data untuk mengurangi stok dan membuat detail transaksi
        product_updates.append({"product": db_product, "new_stock": db_product.stock - item.quantity})
        transaction_detail_objects.append(
            models.TransactionDetail(
                product_id=item.product_id,
                quantity=item.quantity,
                price_per_item=db_product.price
            )
        )

    # # Jika validasi berhasil, buat transaksi utama
    db_transaction = models.Transaction(
        total_amount=total_amount,
        cashier_id=cashier.id,
        details=transaction_detail_objects
    )
    db.add(db_transaction)
    
    # # Kurangi stok produk
    for update in product_updates:
        update["product"].stock = update["new_stock"]
        db.add(update["product"])
        
    # # Commit semua perubahan ke database
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    """
    # Mengambil riwayat transaksi.
    # Menggunakan joinedload untuk efisiensi query (mirip JOIN di SQL).
    """
    return (
        db.query(models.Transaction)
        .options(joinedload(models.Transaction.details).joinedload(models.TransactionDetail.product))
        .options(joinedload(models.Transaction.cashier))
        .order_by(models.Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

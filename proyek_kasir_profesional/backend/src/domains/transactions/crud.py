# Lokasi file: src/domains/transactions/crud.py
# PERBAIKAN BUG FINAL: Memuat ulang relasi 'cashier' setelah transaksi dibuat

from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from decimal import Decimal

from . import models, schemas
from src.domains.products.models import Product as ProductModel
from src.domains.users.models import User as UserModel

def create_transaction(db: Session, transaction_data: schemas.TransactionCreate, cashier: UserModel):
    """
    Membuat transaksi baru, melakukan validasi, dan mengurangi stok produk.
    """
    total_amount = Decimal(0)
    product_updates = []
    transaction_detail_objects = []

    for item in transaction_data.details:
        db_product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        if not db_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produk dengan ID {item.product_id} tidak ditemukan.")
        if db_product.stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Stok untuk produk '{db_product.name}' tidak mencukupi.")
        
        sub_total = db_product.price * item.quantity
        total_amount += sub_total
        
        product_updates.append({"product": db_product, "new_stock": db_product.stock - item.quantity})
        transaction_detail_objects.append(
            models.TransactionDetail(product_id=item.product_id, quantity=item.quantity, price_per_item=item.price_at_transaction)
        )

    db_transaction = models.Transaction(total_amount=total_amount, cashier_id=cashier.id, details=transaction_detail_objects)
    db.add(db_transaction)
    
    for update in product_updates:
        update["product"].stock = update["new_stock"]
        db.add(update["product"])
        
    db.commit()
    
    # PERBAIKAN KUNCI: Tambahkan 'cashier' ke attribute_names agar relasinya ikut dimuat untuk respons API.
    db.refresh(db_transaction, attribute_names=["details", "cashier"])
    return db_transaction

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    """
    Mengambil riwayat transaksi.
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
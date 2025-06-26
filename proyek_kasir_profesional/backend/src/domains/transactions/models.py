# backend/src/domains/transactions/models.py
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # # Foreign Key untuk menghubungkan dengan user (kasir)
    cashier_id = Column(Integer, ForeignKey("users.id"))

    # # Hubungan (Relationship) dengan tabel lain
    cashier = relationship("User")
    details = relationship("TransactionDetail", back_populates="transaction")


class TransactionDetail(Base):
    __tablename__ = "transaction_details"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(Numeric(10, 2), nullable=False)

    # # Foreign Key untuk menghubungkan dengan transaksi dan produk
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    # # Hubungan (Relationship) dengan tabel lain
    transaction = relationship("Transaction", back_populates="details")
    product = relationship("Product")

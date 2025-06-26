# backend/src/domains/products/models.py
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship

from src.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    # # Menambahkan hubungan ke PurchaseOrderDetail
    purchase_order_details = relationship("PurchaseOrderDetail", back_populates="product")

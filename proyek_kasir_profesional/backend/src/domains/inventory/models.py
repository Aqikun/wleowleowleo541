# backend/src/domains/inventory/models.py
from sqlalchemy import Column, Integer, String, Enum, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from src.core.database import Base

# # --- Model yang sudah ada ---
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    contact_person = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)

    # # Menambahkan hubungan ke PurchaseOrder
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

# # --- Model BARU untuk Purchase Order ---

# # Definisikan status untuk PO menggunakan Enum Python
class PurchaseOrderStatus(enum.Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(PurchaseOrderStatus), nullable=False, default=PurchaseOrderStatus.DRAFT)
    
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    supplier = relationship("Supplier", back_populates="purchase_orders")
    details = relationship("PurchaseOrderDetail", back_populates="purchase_order", cascade="all, delete-orphan")


class PurchaseOrderDetail(Base):
    __tablename__ = "purchase_order_details"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Numeric(10, 2), nullable=False)

    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    purchase_order = relationship("PurchaseOrder", back_populates="details")
    product = relationship("Product", back_populates="purchase_order_details")

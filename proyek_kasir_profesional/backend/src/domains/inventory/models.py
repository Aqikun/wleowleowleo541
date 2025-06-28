# nama file: src/domains/inventory/models.py

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum as DBEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base
# PERBARUAN: Impor Enum status yang baru kita buat dari skema
from .schemas import PurchaseOrderStatus

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    contact_person = Column(String)
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # PERBARUAN: Ubah tipe kolom status menjadi Enum
    # Nilai default untuk setiap PO baru adalah 'Draft'
    status = Column(DBEnum(PurchaseOrderStatus), nullable=False, default=PurchaseOrderStatus.DRAFT)
    
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
    product = relationship("Product")

# --- TAMBAHKAN DUA MODEL BARU DI BAWAH INI ---

class StockOpname(Base):
    __tablename__ = "stock_opnames"

    id = Column(Integer, primary_key=True, index=True)
    opname_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(String, nullable=True)

    # Foreign Key untuk mencatat siapa yang melakukan stok opname
    user_id = Column(Integer, ForeignKey("users.id"))

    # Hubungan dengan tabel lain
    user = relationship("User")
    details = relationship("StockOpnameDetail", back_populates="stock_opname", cascade="all, delete-orphan")

class StockOpnameDetail(Base):
    __tablename__ = "stock_opname_details"

    id = Column(Integer, primary_key=True, index=True)
    
    # Kuantitas menurut sistem saat opname dilakukan
    system_stock = Column(Integer, nullable=False)
    # Kuantitas menurut hitungan fisik
    counted_stock = Column(Integer, nullable=False)
    # Selisih (bisa positif atau negatif)
    discrepancy = Column(Integer, nullable=False)

    # Foreign Key
    stock_opname_id = Column(Integer, ForeignKey("stock_opnames.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    # Hubungan dengan tabel lain
    stock_opname = relationship("StockOpname", back_populates="details")
    product = relationship("Product")
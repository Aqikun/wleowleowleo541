# nama file: src/domains/inventory/crud.py

from sqlalchemy.orm import Session, joinedload
from . import models, schemas

# --- CRUD untuk Supplier ---
def get_supplier(db: Session, supplier_id: int):
    return db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()

def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Supplier).offset(skip).limit(limit).all()

def create_supplier(db: Session, supplier: schemas.SupplierCreate):
    db_supplier = models.Supplier(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def update_supplier(db: Session, db_supplier: models.Supplier, supplier_update: schemas.SupplierUpdate):
    update_data = supplier_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_supplier, key, value)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session, db_supplier: models.Supplier):
    db.delete(db_supplier)
    db.commit()
    return db_supplier

# --- CRUD untuk Purchase Order ---
def create_purchase_order(db: Session, po_data: schemas.PurchaseOrderCreate):
    """
    # Membuat Purchase Order baru beserta detail itemnya.
    """
    po_detail_objects = [
        models.PurchaseOrderDetail(**item.model_dump()) for item in po_data.items
    ]

    db_po = models.PurchaseOrder(
        supplier_id=po_data.supplier_id,
        details=po_detail_objects
    )
    
    db.add(db_po)
    db.commit()
    
    # # PERBAIKAN: Alih-alih hanya me-refresh, kita ambil kembali PO yang baru dibuat
    # # dengan semua relasinya (supplier dan details) sudah dimuat.
    # # Ini memastikan respons API berisi semua data yang diharapkan oleh tes.
    return get_purchase_order(db, po_id=db_po.id)

def get_purchase_order(db: Session, po_id: int):
    """
    # Mengambil satu Purchase Order berdasarkan ID, termasuk detailnya.
    """
    return (
        db.query(models.PurchaseOrder)
        .options(joinedload(models.PurchaseOrder.details).joinedload(models.PurchaseOrderDetail.product))
        .options(joinedload(models.PurchaseOrder.supplier))
        .filter(models.PurchaseOrder.id == po_id)
        .first()
    )

def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100):
    """
    # Mengambil daftar semua Purchase Order.
    """
    return (
        db.query(models.PurchaseOrder)
        .options(joinedload(models.PurchaseOrder.supplier))
        .order_by(models.PurchaseOrder.order_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
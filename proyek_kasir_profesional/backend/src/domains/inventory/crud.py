# nama file: src/domains/inventory/crud.py

from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from . import models, schemas
from src.domains.products.models import Product as ProductModel
from src.domains.users.models import User as UserModel

# --- CRUD untuk Supplier (Tidak ada perubahan) ---
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

# --- CRUD untuk Purchase Order (Tidak ada perubahan) ---
def create_purchase_order(db: Session, po_data: schemas.PurchaseOrderCreate):
    po_detail_objects = [
        models.PurchaseOrderDetail(**item.model_dump()) for item in po_data.items
    ]
    db_po = models.PurchaseOrder(
        supplier_id=po_data.supplier_id,
        details=po_detail_objects
    )
    db.add(db_po)
    db.commit()
    return get_purchase_order(db, po_id=db_po.id)

def get_purchase_order(db: Session, po_id: int):
    return (
        db.query(models.PurchaseOrder)
        .options(joinedload(models.PurchaseOrder.details).joinedload(models.PurchaseOrderDetail.product))
        .options(joinedload(models.PurchaseOrder.supplier))
        .filter(models.PurchaseOrder.id == po_id)
        .first()
    )

def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.PurchaseOrder)
        .options(joinedload(models.PurchaseOrder.supplier))
        .order_by(models.PurchaseOrder.order_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def receive_purchase_order(db: Session, po: models.PurchaseOrder):
    if po.status in [schemas.PurchaseOrderStatus.COMPLETED, schemas.PurchaseOrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Purchase Order dengan status '{po.status.value}' tidak dapat diterima lagi."
        )
    for detail in po.details:
        db_product = db.query(ProductModel).filter(ProductModel.id == detail.product_id).first()
        if db_product:
            db_product.stock += detail.quantity
            db.add(db_product)
    po.status = schemas.PurchaseOrderStatus.COMPLETED
    db.add(po)
    db.commit()
    db.refresh(po)
    return po

def update_purchase_order_status(db: Session, po: models.PurchaseOrder, new_status: schemas.PurchaseOrderStatus):
    po.status = new_status
    db.add(po)
    db.commit()
    db.refresh(po)
    return po

# --- FUNGSI LOGIKA BARU UNTUK STOK OPNAME ---

def create_stock_opname(db: Session, opname_data: schemas.StockOpnameCreate, user: UserModel):
    """
    Membuat catatan Stok Opname baru.
    1. Validasi setiap produk yang dihitung.
    2. Hitung selisih antara stok sistem dan hitungan fisik.
    3. Simpan catatan ke database.
    PENTING: Fungsi ini HANYA MENCATAT, tidak mengubah stok produk secara otomatis.
    """
    opname_detail_objects = []

    for detail in opname_data.details:
        db_product = db.query(ProductModel).filter(ProductModel.id == detail.product_id).first()
        
        # Pastikan produk yang dihitung ada di database
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produk dengan ID {detail.product_id} tidak ditemukan."
            )
        
        # Hitung selisih
        discrepancy = detail.counted_stock - db_product.stock
        
        opname_detail_objects.append(
            models.StockOpnameDetail(
                product_id=detail.product_id,
                system_stock=db_product.stock,
                counted_stock=detail.counted_stock,
                discrepancy=discrepancy
            )
        )

    # Buat entri utama untuk sesi stok opname ini
    db_opname = models.StockOpname(
        notes=opname_data.notes,
        user_id=user.id,
        details=opname_detail_objects
    )
    
    db.add(db_opname)
    db.commit()
    db.refresh(db_opname)
    
    # Ambil kembali data yang sudah lengkap dengan relasinya untuk dikembalikan
    return (
        db.query(models.StockOpname)
        .options(joinedload(models.StockOpname.details).joinedload(models.StockOpnameDetail.product))
        .options(joinedload(models.StockOpname.user))
        .filter(models.StockOpname.id == db_opname.id)
        .first()
    )
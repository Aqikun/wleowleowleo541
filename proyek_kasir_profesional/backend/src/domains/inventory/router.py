# nama file: src/domains/inventory/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.dependencies import require_role, get_current_user
from src.domains.users.models import User
from . import crud, schemas

# Membuat satu instance APIRouter untuk seluruh domain inventory
router = APIRouter(
    # Semua endpoint di file ini akan diawali dengan /inventory
    prefix="/inventory",
    # Semua endpoint di file ini akan dilindungi oleh otentikasi
    dependencies=[Depends(require_role(["Admin", "Owner"]))],
    # Pengelompokan di dokumentasi API
    tags=["Inventory Management"]
)

# --- Endpoint untuk Supplier ---
@router.post("/suppliers/", response_model=schemas.SupplierSchema, status_code=status.HTTP_201_CREATED)
def create_new_supplier(
    supplier: schemas.SupplierCreate,
    db: Session = Depends(get_db)
):
    return crud.create_supplier(db=db, supplier=supplier)

@router.get("/suppliers/", response_model=List[schemas.SupplierSchema])
def read_all_suppliers(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_suppliers(db, skip=skip, limit=limit)

@router.get("/suppliers/{supplier_id}", response_model=schemas.SupplierSchema)
def read_supplier_by_id(
    supplier_id: int, db: Session = Depends(get_db)
):
    db_supplier = crud.get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.put("/suppliers/{supplier_id}", response_model=schemas.SupplierSchema)
def update_existing_supplier(
    supplier_id: int, supplier_update: schemas.SupplierUpdate,
    db: Session = Depends(get_db)
):
    db_supplier = crud.get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.update_supplier(db=db, db_supplier=db_supplier, supplier_update=supplier_update)

@router.delete("/suppliers/{supplier_id}", response_model=schemas.SupplierSchema)
def delete_existing_supplier(
    supplier_id: int, db: Session = Depends(get_db)
):
    db_supplier = crud.get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.delete_supplier(db=db, db_supplier=db_supplier)

# --- Endpoint untuk Purchase Order ---
@router.post("/purchase-orders/", response_model=schemas.PurchaseOrderSchema, status_code=status.HTTP_201_CREATED)
def create_new_purchase_order(
    po_data: schemas.PurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    supplier = crud.get_supplier(db, supplier_id=po_data.supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.create_purchase_order(db, po_data=po_data)

@router.get("/purchase-orders/", response_model=List[schemas.PurchaseOrderSchema])
def read_all_purchase_orders(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_purchase_orders(db, skip=skip, limit=limit)

@router.get("/purchase-orders/{po_id}", response_model=schemas.PurchaseOrderSchema)
def read_purchase_order_by_id(
    po_id: int, db: Session = Depends(get_db)
):
    db_po = crud.get_purchase_order(db, po_id=po_id)
    if db_po is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return db_po

@router.patch("/purchase-orders/{po_id}/status", response_model=schemas.PurchaseOrderSchema)
def update_po_status(
    po_id: int,
    status_update: schemas.PurchaseOrderStatusUpdate, 
    db: Session = Depends(get_db)
):
    db_po = crud.get_purchase_order(db, po_id=po_id)
    if db_po is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return crud.update_purchase_order_status(db, po=db_po, new_status=status_update.status)

@router.post("/purchase-orders/{po_id}/receive", response_model=schemas.PurchaseOrderSchema)
def receive_po_items(
    po_id: int,
    db: Session = Depends(get_db)
):
    db_po = crud.get_purchase_order(db, po_id=po_id)
    if db_po is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    try:
        return crud.receive_purchase_order(db, po=db_po)
    except HTTPException as e:
        raise e

# --- ENDPOINT BARU UNTUK STOK OPNAME ---

@router.post("/stock-opnames/", response_model=schemas.StockOpnameSchema, status_code=status.HTTP_201_CREATED)
def create_new_stock_opname(
    opname_data: schemas.StockOpnameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Membuat sebuah sesi Stok Opname baru.
    Endpoint ini akan menerima daftar produk beserta jumlah hitungan fisiknya,
    lalu menyimpan catatan stok opname beserta selisihnya ke database.
    """
    try:
        return crud.create_stock_opname(db=db, opname_data=opname_data, user=current_user)
    except HTTPException as e:
        # Teruskan error dari CRUD (misal: jika produk tidak ditemukan)
        raise e
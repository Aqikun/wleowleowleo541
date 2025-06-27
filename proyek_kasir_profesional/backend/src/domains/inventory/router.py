# nama file: src/domains/inventory/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.dependencies import require_role
from . import crud, schemas

# # Membuat satu instance APIRouter untuk seluruh domain inventory
router = APIRouter()

# # --- Endpoint untuk Supplier ---
@router.post("/suppliers/", response_model=schemas.SupplierSchema, status_code=status.HTTP_201_CREATED, tags=["Inventory - Suppliers"])
def create_new_supplier(
    supplier: schemas.SupplierCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Owner"]))
):
    return crud.create_supplier(db=db, supplier=supplier)

@router.get("/suppliers/", response_model=List[schemas.SupplierSchema], tags=["Inventory - Suppliers"])
def read_all_suppliers(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Owner"]))
):
    return crud.get_suppliers(db, skip=skip, limit=limit)

@router.get("/suppliers/{supplier_id}", response_model=schemas.SupplierSchema, tags=["Inventory - Suppliers"])
def read_supplier_by_id(
    supplier_id: int, db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Owner"]))
):
    db_supplier = crud.get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.put("/suppliers/{supplier_id}", response_model=schemas.SupplierSchema, tags=["Inventory - Suppliers"])
def update_existing_supplier(
    supplier_id: int, supplier_update: schemas.SupplierUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Owner"]))
):
    db_supplier = crud.get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.update_supplier(db=db, db_supplier=db_supplier, supplier_update=supplier_update)

@router.delete("/suppliers/{supplier_id}", response_model=schemas.SupplierSchema, tags=["Inventory - Suppliers"])
def delete_existing_supplier(
    supplier_id: int, db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Owner"]))
):
    db_supplier = crud.get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.delete_supplier(db=db, db_supplier=db_supplier)

# # --- Endpoint untuk Purchase Order ---
@router.post("/purchase-orders/", response_model=schemas.PurchaseOrderSchema, status_code=status.HTTP_201_CREATED, tags=["Inventory - Purchase Orders"])
def create_new_purchase_order(
    po_data: schemas.PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Owner"]))
):
    # # Periksa apakah supplier ada
    supplier = crud.get_supplier(db, supplier_id=po_data.supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.create_purchase_order(db, po_data=po_data)

@router.get("/purchase-orders/", response_model=List[schemas.PurchaseOrderSchema], tags=["Inventory - Purchase Orders"])
def read_all_purchase_orders(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Owner"]))
):
    return crud.get_purchase_orders(db, skip=skip, limit=limit)

@router.get("/purchase-orders/{po_id}", response_model=schemas.PurchaseOrderSchema, tags=["Inventory - Purchase Orders"])
def read_purchase_order_by_id(
    po_id: int, db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Owner"]))
):
    db_po = crud.get_purchase_order(db, po_id=po_id)
    if db_po is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return db_po
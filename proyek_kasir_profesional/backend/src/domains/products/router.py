# -- KODE UNTUK INTERAKSI LANJUTAN --
# -- FILE: backend/src/domains/products/router.py --

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from . import crud, schemas
from src.domains.users.auth_service import require_role

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(require_role(["owner", "admin"]))]
)

# === PERBAIKAN DI SEMUA `response_model` DI BAWAH ===
@router.post("/", response_model=schemas.ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Membuat produk baru (Hanya Owner/Admin).
    """
    return crud.create_product(db=db, product=product)

@router.get("/", response_model=List[schemas.ProductSchema])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Membaca daftar produk (Hanya Owner/Admin).
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Membaca satu produk berdasarkan ID (Hanya Owner/Admin).
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.ProductSchema)
def update_product(
    product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    """
    Memperbarui produk yang ada (Hanya Owner/Admin).
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db=db, db_product=db_product, product_update=product_update)

@router.delete("/{product_id}", response_model=schemas.ProductSchema)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Menghapus produk (Hanya Owner/Admin).
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.delete_product(db=db, db_product=db_product)
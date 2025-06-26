# backend/src/domains/products/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.dependencies import get_current_user
from src.domains.users.models import User
from . import crud, schemas

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    # # Menambahkan dependensi otentikasi ke semua endpoint di router ini.
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_new_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # # Di sini Anda bisa menambahkan logika otorisasi,
    # # misalnya, hanya 'Admin' yang boleh membuat produk.
    return crud.create_product(db=db, product=product)

@router.get("/", response_model=List[schemas.Product])
def read_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_existing_product(
    product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db=db, db_product=db_product, product_update=product_update)

@router.delete("/{product_id}", response_model=schemas.Product)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.delete_product(db=db, db_product=db_product)

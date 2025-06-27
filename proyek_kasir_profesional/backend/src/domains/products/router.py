# backend/src/domains/products/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from . import crud, schemas

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

# # PERBAIKAN: Mengganti response_model dari schemas.Product menjadi schemas.ProductSchema
@router.post("/", response_model=schemas.ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)


# # PERBAIKAN: Mengganti response_model dari schemas.Product menjadi schemas.ProductSchema
@router.get("/", response_model=List[schemas.ProductSchema])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


# # PERBAIKAN: Mengganti response_model dari schemas.Product menjadi schemas.ProductSchema
@router.get("/{product_id}", response_model=schemas.ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# # PERBAIKAN: Mengganti response_model dari schemas.Product menjadi schemas.ProductSchema
@router.put("/{product_id}", response_model=schemas.ProductSchema)
def update_product(
    product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db=db, db_product=db_product, product_update=product_update)
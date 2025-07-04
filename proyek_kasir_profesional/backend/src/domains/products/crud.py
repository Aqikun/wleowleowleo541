# backend/src/domains/products/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def get_product(db: Session, product_id: int):
    """
    # Mengambil satu produk berdasarkan ID-nya.
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    # Mengambil daftar semua produk dengan paginasi.
    """
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    """
    # Membuat produk baru di database.
    """
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(
    db: Session, db_product: models.Product, product_update: schemas.ProductUpdate
):
    """
    # Memperbarui data produk di database.
    """
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: models.Product):
    """
    # Menghapus produk dari database.
    """
    db.delete(db_product)
    db.commit()
    return db_product

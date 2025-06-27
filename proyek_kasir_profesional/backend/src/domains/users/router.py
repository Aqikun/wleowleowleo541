# nama file: src/domains/users/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
# # PERBAIKAN: Hapus import get_password_hash karena tidak lagi digunakan di sini
# from src.core.security import get_password_hash 
from . import crud, schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terdaftar.")
    
    # # PERBAIKAN: Hapus baris hashing password dari router
    # # hashed_password = get_password_hash(user.password) 
    
    # # PERBAIKAN: Panggil crud.create_user hanya dengan 'db' dan 'user'
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # # Catatan: Anda belum membuat fungsi crud.get_users dan crud.get_user
    # # Ini akan menjadi error berikutnya jika tidak diperbaiki.
    # # Untuk sementara, saya akan berikan placeholder.
    # users = crud.get_users(db, skip=skip, limit=limit)
    return [] # Placeholder


@router.get("/{user_id}", response_model=schemas.UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # db_user = crud.get_user(db, user_id=user_id)
    db_user = None # Placeholder
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
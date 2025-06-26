# backend/src/domains/users/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from . import crud, schemas

# # Ini adalah baris yang paling penting.
# # Pastikan variabel bernama 'router' ada dan merupakan sebuah APIRouter.
router = APIRouter(
    prefix="/users",
    tags=["Users"], # # Memberi tag pada dokumentasi Swagger UI
)

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    # Endpoint untuk membuat (registrasi) pengguna baru.
    """
    # # Periksa apakah username sudah ada.
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah terdaftar.",
        )
    # # Jika belum ada, buat pengguna baru.
    return crud.create_user(db=db, user=user)

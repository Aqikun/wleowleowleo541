# Lokasi file: src/domains/users/users_router.py
# # Berisi semua endpoint manajemen user yang memerlukan otentikasi.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.dependencies import get_current_user, require_role
from . import crud, models, schemas

# # Definisi router khusus untuk manajemen pengguna
users_router = APIRouter(prefix="/users", tags=["Users Management"], dependencies=[Depends(get_current_user)])


@users_router.post("/", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(["Admin", "Owner"]))])
def create_new_user_by_admin(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Endpoint terproteksi untuk membuat pengguna baru (hanya Admin/Owner)."""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@users_router.get("/", response_model=List[schemas.UserSchema], dependencies=[Depends(require_role(["Admin", "Owner"]))])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Melihat daftar semua pengguna."""
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@users_router.patch("/{user_id}/status", response_model=schemas.UserSchema, dependencies=[Depends(require_role(["Admin", "Owner"]))])
def update_user_active_status(
    user_id: int,
    status_update: schemas.UserStatusUpdate,
    db: Session = Depends(get_db)
):
    """Mengaktifkan atau menonaktifkan akun pengguna."""
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.update_user_status(db=db, db_user=db_user, status_update=status_update)

@users_router.patch("/{user_id}/role", response_model=schemas.UserSchema, dependencies=[Depends(require_role(["Admin", "Owner"]))])
def update_user_role(
    user_id: int,
    role_update: schemas.UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Mengubah peran seorang pengguna."""
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if role_update.role == schemas.UserRole.Owner and current_user.role != schemas.UserRole.Owner:
        raise HTTPException(status_code=403, detail="Only an Owner can assign the Owner role.")
    
    if db_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot change your own role via this endpoint.")

    return crud.update_user_role(db=db, db_user=db_user, role_update=role_update)

@users_router.post("/{user_id}/force-reset-password", status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["Admin", "Owner"]))])
def force_user_password_reset(user_id: int, db: Session = Depends(get_db)):
    """
    Menandai seorang pengguna agar mereka dipaksa untuk mereset password
    saat mencoba login berikutnya.
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    crud.set_force_password_reset(db=db, db_user=db_user, status=True)
    return {"message": f"User '{db_user.username}' is now required to reset their password upon next login."}
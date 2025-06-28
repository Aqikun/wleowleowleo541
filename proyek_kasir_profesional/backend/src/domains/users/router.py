# Lokasi file: src/domains/users/router.py
# PERBAIKAN FINAL: Memperbaiki struktur router dan endpoint registrasi

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.security import create_access_token, create_reset_token, get_reset_token_hash, verify_password
from src.core.dependencies import get_current_user, require_role
from . import crud, models, schemas

def send_password_reset_notification(email: str, token: str, channel: str):
    reset_link = f"http://localhost:3000/reset-password?token={token}"
    print(f"---- SENDING NOTIFICATION to {email} via {channel} ----\n{reset_link}\n----------------------------")

# Router untuk endpoint yang TIDAK memerlukan otentikasi
auth_router = APIRouter(tags=["Authentication"])

# Router untuk endpoint MANAJEMEN PENGGUNA yang MEMERLUKAN otentikasi
users_router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)])

# --- Endpoint Publik di AUTH_ROUTER ---

@auth_router.post("/register", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def register_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Endpoint publik untuk registrasi pengguna baru."""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@auth_router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint untuk login dan mendapatkan JWT."""
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(request: schemas.ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=request.email)
    if user:
        raw_token = create_reset_token()
        hashed_token = get_reset_token_hash(raw_token)
        crud.set_password_reset_token(db=db, user=user, token=hashed_token)
        background_tasks.add_task(send_password_reset_notification, user.email, raw_token, request.channel)
    return {"message": "If an account with that email exists, a password reset link has been sent."}

@auth_router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(request: schemas.ResetPassword, db: Session = Depends(get_db)):
    hashed_token = get_reset_token_hash(request.token)
    user = crud.get_user_by_reset_token(db, token=hashed_token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    crud.update_user_password(db=db, user=user, new_password=request.new_password)
    return {"message": "Password has been reset successfully."}

# --- Endpoint Terproteksi di USERS_ROUTER ---

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
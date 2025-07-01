# Lokasi file: src/domains/users/auth_router.py
# PERBAIKAN FINAL: Menghilangkan logika hashing untuk reset token.

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core import security
from . import crud, schemas

auth_router = APIRouter(tags=["Authentication"])

def send_password_reset_notification(email: str, token: str, channel: str):
    reset_link = f"http://localhost:3000/reset-password?token={token}"
    print(f"---- SENDING NOTIFICATION to {email} via {channel} ----\n{reset_link}\n----------------------------")

@auth_router.post("/register", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def register_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_by_name = crud.get_user_by_username(db, username=user.username)
    if db_user_by_name:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@auth_router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not user.is_active: raise HTTPException(status_code=400, detail="Inactive user")
    if user.force_password_reset: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password reset is required for this account.")
    access_token = security.create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(request: schemas.ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=request.email)
    if user:
        raw_token = security.create_reset_token()
        # Langsung simpan token asli, tanpa hash
        crud.set_password_reset_token(db=db, user=user, token=raw_token)
        background_tasks.add_task(send_password_reset_notification, user.email, raw_token, request.channel)
    return {"message": "If an account with that email exists, a password reset link has been sent."}

@auth_router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(request: schemas.ResetPassword, db: Session = Depends(get_db)):
    # Langsung cari pengguna dengan token asli dari request
    user = crud.get_user_by_reset_token(db, token=request.token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    crud.update_user_password(db=db, user=user, new_password=request.new_password)
    return {"message": "Password has been reset successfully."}
# backend/src/domains/auth/router.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.config import settings
from src.core.security import create_access_token, verify_password
from src.domains.users import crud as users_crud
from . import schemas

# # Membuat instance APIRouter untuk domain otentikasi.
router = APIRouter(
    tags=["Authentication"], # # Memberi tag pada dokumentasi Swagger UI
)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    # Endpoint untuk login.
    # Menerima username dan password dari form, lalu mengembalikan token.
    """
    # # Cari user di database.
    user = users_crud.get_user_by_username(db, username=form_data.username)
    
    # # Jika user tidak ada atau password salah, kirim error.
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # # Jika berhasil, buat access token.
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # # Kirim kembali tokennya.
    return {"access_token": access_token, "token_type": "bearer"}

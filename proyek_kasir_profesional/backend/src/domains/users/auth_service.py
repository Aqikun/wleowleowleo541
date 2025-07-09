# -- KODE UNTUK INTERAKSI LANJUTAN --
# -- FILE: backend/src/domains/users/auth_service.py (VERSI FINAL) --

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import List

# Impor dari dalam proyek
from src.core.database import get_db
from src.core import security
from . import crud, models, schemas

# Skema ini akan mencari token di header permintaan
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Mendekode token JWT untuk mendapatkan data pengguna yang sedang login.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def require_role(allowed_roles: List[str]):
    """
    Dependency 'penjaga gerbang' yang memeriksa apakah peran (role) pengguna
    diizinkan untuk mengakses sebuah endpoint.
    """
    def role_checker(current_user: models.User = Depends(get_current_user)):
        
        # === PERBAIKAN FINAL DI SINI ===
        # Ubah peran pengguna menjadi huruf kecil sebelum membandingkan
        user_role = current_user.role.value.lower()
        
        if user_role not in allowed_roles:
        # ===============================
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with role '{current_user.role.value}' does not have access to this resource."
            )
        return current_user
    return role_checker
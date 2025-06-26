# backend/src/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.config import settings
from src.domains.users import crud as users_crud
from src.domains.users import models as user_models
from src.domains.auth import schemas as auth_schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> user_models.User:
    """
    # Dependensi untuk mendapatkan pengguna saat ini dari token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth_schemas.TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = users_crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# # FUNGSI BARU UNTUK OTORISASI BERBASIS PERAN
def require_role(allowed_roles: List[str]):
    """
    # Pabrik dependensi yang membuat dependensi untuk memeriksa peran pengguna.
    """
    def get_current_user_with_role(current_user: user_models.User = Depends(get_current_user)) -> user_models.User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user does not have access to this resource"
            )
        return current_user
    return get_current_user_with_role

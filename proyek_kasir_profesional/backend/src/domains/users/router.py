# backend/src/domains/users/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.security import get_password_hash
from . import crud, schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# # PERBAIKAN: Mengganti response_model dari schemas.User menjadi schemas.UserSchema
@router.post("/", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)


# # PERBAIKAN: Mengganti response_model dari schemas.User menjadi schemas.UserSchema
@router.get("/", response_model=List[schemas.UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# # PERBAIKAN: Mengganti response_model dari schemas.User menjadi schemas.UserSchema
@router.get("/{user_id}", response_model=schemas.UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
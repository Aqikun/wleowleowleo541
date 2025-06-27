# backend/src/domains/transactions/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.domains.users.models import User
from src.core.dependencies import get_current_user
from . import crud, schemas

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)

# # PERBAIKAN: Mengganti response_model dari schemas.Transaction menjadi schemas.TransactionSchema
@router.post("/", response_model=schemas.TransactionSchema, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return crud.create_transaction(
            db=db, transaction=transaction, user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# # PERBAIKAN: Mengganti response_model dari schemas.Transaction menjadi schemas.TransactionSchema
@router.get("/", response_model=List[schemas.TransactionSchema])
def read_transactions(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions


# # PERBAIKAN: Mengganti response_model dari schemas.Transaction menjadi schemas.TransactionSchema
@router.get("/{transaction_id}", response_model=schemas.TransactionSchema)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction
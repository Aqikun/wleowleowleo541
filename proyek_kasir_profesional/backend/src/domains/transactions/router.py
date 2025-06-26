# backend/src/domains/transactions/router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.core.dependencies import get_current_user
from src.domains.users.models import User as UserModel
from . import crud, schemas

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def create_new_transaction(
    transaction_data: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    # Endpoint untuk membuat transaksi baru.
    # Menerima daftar belanjaan, memvalidasi, dan mengembalikan detail transaksi.
    """
    return crud.create_transaction(db=db, transaction_data=transaction_data, cashier=current_user)

@router.get("/", response_model=List[schemas.Transaction])
def read_transaction_history(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    # Endpoint untuk melihat riwayat semua transaksi.
    """
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions

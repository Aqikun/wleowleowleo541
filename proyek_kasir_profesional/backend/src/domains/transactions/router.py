# nama file: src/domains/transactions/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.domains.users.models import User
from src.core.dependencies import get_current_user, require_role
from . import crud, schemas

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    # Lindungi semua endpoint transaksi, hanya user yang login bisa akses
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.TransactionSchema, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_payload: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # PERBAIKAN: Sesuaikan nama argumen menjadi 'transaction_data' dan 'cashier'
        return crud.create_transaction(
            db=db, transaction_data=transaction_payload, cashier=current_user
        )
    except HTTPException as e:
        # Teruskan HTTP Exception dari CRUD
        raise e
    except Exception as e:
        # Tangani error tak terduga lainnya
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.TransactionSchema], dependencies=[Depends(require_role(["Admin", "Owner"]))])
def read_transactions(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions
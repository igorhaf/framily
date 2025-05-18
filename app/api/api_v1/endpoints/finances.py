from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/transactions", response_model=List[schemas.Transaction])
def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve transactions.
    """
    transactions = crud.transaction.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return transactions

@router.post("/transactions", response_model=schemas.Transaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: schemas.TransactionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create new transaction.
    """
    transaction = crud.transaction.create_with_user(
        db=db, obj_in=transaction_in, user_id=current_user.id
    )
    return transaction 
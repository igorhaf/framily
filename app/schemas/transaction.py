from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class TransactionBase(BaseModel):
    amount: Decimal
    description: str
    category: str
    transaction_date: datetime
    is_expense: bool = True


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    user_id: int
    family_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 
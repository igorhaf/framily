from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date
from app.models.finance import TransactionType

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: TransactionType

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    family_id: int

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    date: date
    category_id: int
    type: TransactionType

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    family_id: int

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    amount: float = Field(..., gt=0)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000)
    category_id: int

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    family_id: int

    class Config:
        from_attributes = True

class CategorySummary(BaseModel):
    budget: float
    income: float
    expense: float
    type: TransactionType

class MonthlyBudget(BaseModel):
    categories: Dict[int, CategorySummary]
    month: int
    year: int

class FinancialSummary(BaseModel):
    total_income: float
    total_expenses: float
    balance: float
    category_summary: Dict[int, CategorySummary]
    monthly_budget: MonthlyBudget 
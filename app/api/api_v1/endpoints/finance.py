from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from app.api import deps
from app.crud.crud_finance import category, transaction, budget
from app.schemas.finance import (
    Category,
    CategoryCreate,
    Transaction,
    TransactionCreate,
    Budget,
    BudgetCreate,
    FinancialSummary
)
from app.models.finance import TransactionType

router = APIRouter()

# Categorias
@router.get("/categories/", response_model=List[Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    family_id: int = 1,  # Temporariamente fixo
    type: Optional[TransactionType] = None
):
    if type:
        return category.get_by_type(db, family_id=family_id, type=type)
    return category.get_by_family(db, family_id=family_id)

@router.post("/categories/", response_model=Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate,
    family_id: int = 1  # Temporariamente fixo
):
    category_obj = category.create_with_family(db, obj_in=category_in, family_id=family_id)
    return category_obj

# Transações
@router.get("/transactions/", response_model=List[Transaction])
def read_transactions(
    db: Session = Depends(deps.get_db),
    family_id: int = 1,  # Temporariamente fixo
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    type: Optional[TransactionType] = None
):
    return transaction.get_by_family(
        db,
        family_id=family_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id,
        type=type
    )

@router.post("/transactions/", response_model=Transaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: TransactionCreate,
    family_id: int = 1  # Temporariamente fixo
):
    transaction_obj = transaction.create_with_family(db, obj_in=transaction_in, family_id=family_id)
    return transaction_obj

# Orçamentos
@router.get("/budgets/", response_model=List[Budget])
def read_budgets(
    db: Session = Depends(deps.get_db),
    family_id: int = 1,  # Temporariamente fixo
    month: Optional[int] = None,
    year: Optional[int] = None
):
    return budget.get_by_family(db, family_id=family_id, month=month, year=year)

@router.post("/budgets/", response_model=Budget)
def create_budget(
    *,
    db: Session = Depends(deps.get_db),
    budget_in: BudgetCreate,
    family_id: int = 1  # Temporariamente fixo
):
    budget_obj = budget.create_with_family(db, obj_in=budget_in, family_id=family_id)
    return budget_obj

# Resumos
@router.get("/summary/", response_model=FinancialSummary)
def get_financial_summary(
    db: Session = Depends(deps.get_db),
    family_id: int = 1,  # Temporariamente fixo
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    try:
        # Obtém resumo de transações
        transaction_summary = transaction.get_summary(
            db,
            family_id=family_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Obtém resumo de orçamentos
        current_date = date.today()
        budget_summary = budget.get_monthly_summary(
            db,
            family_id=family_id,
            month=current_date.month,
            year=current_date.year
        )
        
        return {
            "total_income": transaction_summary["total_income"],
            "total_expenses": transaction_summary["total_expenses"],
            "balance": transaction_summary["balance"],
            "category_summary": budget_summary["categories"],
            "monthly_budget": budget_summary
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar resumo financeiro: {str(e)}"
        ) 
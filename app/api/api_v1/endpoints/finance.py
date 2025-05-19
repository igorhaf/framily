from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.api import deps
from app.crud.crud_finance import category, transaction, budget
from app.models.finance import FinanceCategory, FinanceTransaction, TransactionType
from app.schemas.finance import (
    Category,
    CategoryCreate,
    Transaction,
    TransactionCreate,
    Budget,
    BudgetCreate,
    FinancialSummary
)

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
        # Define as datas do período
        current_date = date.today()
        if not start_date:
            start_date = date(current_date.year, current_date.month, 1)
        if not end_date:
            if current_date.month == 12:
                end_date = date(current_date.year + 1, 1, 1)
            else:
                end_date = date(current_date.year, current_date.month + 1, 1)
        
        # Obtém resumo de transações
        transaction_summary = transaction.get_summary(
            db,
            family_id=family_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Obtém resumo de orçamentos
        budget_summary = budget.get_monthly_summary(
            db,
            family_id=family_id,
            month=current_date.month,
            year=current_date.year
        )
        
        # Garante que os totais sejam consistentes
        total_income = transaction_summary["total_income"]
        total_expenses = transaction_summary["total_expenses"]
        balance = total_income - total_expenses
        
        # Agrupa categorias por tipo e soma os valores
        category_summary = {}
        
        # Primeiro, vamos buscar todas as categorias
        categories = db.query(FinanceCategory).filter(
            FinanceCategory.family_id == family_id
        ).all()
        
        # Inicializa o dicionário com as categorias
        for cat in categories:
            category_summary[cat.id] = {
                'budget': 0.0,
                'income': 0.0,
                'expense': 0.0,
                'type': cat.type
            }
        
        # Busca totais de receitas por categoria
        income_totals = db.query(
            FinanceTransaction.category_id,
            func.sum(FinanceTransaction.amount).label('total')
        ).filter(
            FinanceTransaction.family_id == family_id,
            FinanceTransaction.date >= start_date,
            FinanceTransaction.date < end_date,
            FinanceTransaction.type == TransactionType.INCOME
        ).group_by(
            FinanceTransaction.category_id
        ).all()
        
        # Busca totais de despesas por categoria
        expense_totals = db.query(
            FinanceTransaction.category_id,
            func.sum(FinanceTransaction.amount).label('total')
        ).filter(
            FinanceTransaction.family_id == family_id,
            FinanceTransaction.date >= start_date,
            FinanceTransaction.date < end_date,
            FinanceTransaction.type == TransactionType.EXPENSE
        ).group_by(
            FinanceTransaction.category_id
        ).all()
        
        # Atualiza os totais por categoria
        for category_id, total in income_totals:
            if category_id in category_summary:
                category_summary[category_id]['income'] = float(total)
        
        for category_id, total in expense_totals:
            if category_id in category_summary:
                category_summary[category_id]['expense'] = float(total)
                category_summary[category_id]['budget'] = float(total)  # Orçamento igual à despesa
        
        # Remove categorias sem valores
        category_summary = {
            cat_id: data for cat_id, data in category_summary.items()
            if data['income'] > 0 or data['expense'] > 0
        }
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "category_summary": category_summary,
            "monthly_budget": total_expenses  # Orçamento mensal é igual ao total de despesas
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar resumo financeiro: {str(e)}"
        ) 
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date, datetime
from app.crud.base import CRUDBase
from app.models.finance import FinanceCategory, FinanceTransaction, FinanceBudget, TransactionType
from app.schemas.finance import CategoryCreate, TransactionCreate, BudgetCreate

class CRUDCategory(CRUDBase[FinanceCategory, CategoryCreate, CategoryCreate]):
    def get_by_family(self, db: Session, *, family_id: int) -> List[FinanceCategory]:
        return db.query(self.model).filter(self.model.family_id == family_id).all()

    def get_by_type(self, db: Session, *, family_id: int, type: TransactionType) -> List[FinanceCategory]:
        return db.query(self.model).filter(
            self.model.family_id == family_id,
            self.model.type == type
        ).all()
        
    def create_with_family(self, db: Session, *, obj_in: CategoryCreate, family_id: int) -> FinanceCategory:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, family_id=family_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDTransaction(CRUDBase[FinanceTransaction, TransactionCreate, TransactionCreate]):
    def get_by_family(
        self, 
        db: Session, 
        *, 
        family_id: int,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category_id: Optional[int] = None,
        type: Optional[TransactionType] = None
    ) -> List[FinanceTransaction]:
        query = db.query(self.model).filter(self.model.family_id == family_id)
        
        if start_date:
            query = query.filter(self.model.date >= start_date)
        if end_date:
            query = query.filter(self.model.date <= end_date)
        if category_id:
            query = query.filter(self.model.category_id == category_id)
        if type:
            query = query.filter(self.model.type == type)
            
        return query.offset(skip).limit(limit).all()

    def create_with_family(self, db: Session, *, obj_in: TransactionCreate, family_id: int) -> FinanceTransaction:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, family_id=family_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_summary(
        self,
        db: Session,
        *,
        family_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict:
        # Se não houver data de início, usa o primeiro dia do mês atual
        if not start_date:
            current_date = date.today()
            start_date = date(current_date.year, current_date.month, 1)
        
        # Se não houver data de fim, usa o último dia do mês atual
        if not end_date:
            current_date = date.today()
            if current_date.month == 12:
                end_date = date(current_date.year + 1, 1, 1)
            else:
                end_date = date(current_date.year, current_date.month + 1, 1)
        
        # Busca todas as transações do período
        transactions = db.query(self.model).filter(
            self.model.family_id == family_id,
            self.model.date >= start_date,
            self.model.date < end_date
        ).all()
        
        # Calcula totais
        total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
        total_expenses = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': total_income - total_expenses
        }

class CRUDBudget(CRUDBase[FinanceBudget, BudgetCreate, BudgetCreate]):
    def get_by_family(
        self,
        db: Session,
        *,
        family_id: int,
        month: Optional[int] = None,
        year: Optional[int] = None
    ) -> List[FinanceBudget]:
        query = db.query(self.model).filter(self.model.family_id == family_id)
        
        if month:
            query = query.filter(self.model.month == month)
        if year:
            query = query.filter(self.model.year == year)
            
        return query.all()

    def create_with_family(self, db: Session, *, obj_in: BudgetCreate, family_id: int) -> FinanceBudget:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, family_id=family_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_monthly_summary(
        self,
        db: Session,
        *,
        family_id: int,
        month: int,
        year: int
    ) -> Dict:
        # Busca orçamentos do mês
        budgets = self.get_by_family(db, family_id=family_id, month=month, year=year)
        
        # Busca transações do mês
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
            
        # Busca categorias
        categories = db.query(FinanceCategory).filter(
            FinanceCategory.family_id == family_id
        ).all()
        category_types = {cat.id: cat.type for cat in categories}
            
        # Busca transações do mês
        transactions = db.query(FinanceTransaction).filter(
            FinanceTransaction.family_id == family_id,
            FinanceTransaction.date >= start_date,
            FinanceTransaction.date < end_date
        ).all()
        
        # Calcula totais por categoria
        category_totals = {}
        
        # Inicializa todas as categorias
        for cat in categories:
            category_totals[cat.id] = {
                'budget': 0.0,
                'income': 0.0,
                'expense': 0.0,
                'type': cat.type
            }
        
        # Adiciona orçamentos
        for budget in budgets:
            if budget.category_id in category_totals:
                category_totals[budget.category_id]['budget'] = budget.amount
        
        # Soma transações
        for transaction in transactions:
            if transaction.category_id in category_totals:
                if transaction.type == TransactionType.INCOME:
                    category_totals[transaction.category_id]['income'] += transaction.amount
                else:
                    category_totals[transaction.category_id]['expense'] += transaction.amount
        
        return {
            'categories': category_totals,
            'month': month,
            'year': year
        }

category = CRUDCategory(FinanceCategory)
transaction = CRUDTransaction(FinanceTransaction)
budget = CRUDBudget(FinanceBudget) 
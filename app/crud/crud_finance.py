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
        
        # Busca totais de receitas
        income_total = db.query(
            func.sum(FinanceTransaction.amount)
        ).filter(
            FinanceTransaction.family_id == family_id,
            FinanceTransaction.date >= start_date,
            FinanceTransaction.date < end_date,
            FinanceTransaction.type == TransactionType.INCOME
        ).scalar() or 0
        
        # Busca totais de despesas
        expense_total = db.query(
            func.sum(FinanceTransaction.amount)
        ).filter(
            FinanceTransaction.family_id == family_id,
            FinanceTransaction.date >= start_date,
            FinanceTransaction.date < end_date,
            FinanceTransaction.type == TransactionType.EXPENSE
        ).scalar() or 0
        
        return {
            'total_income': float(income_total),
            'total_expenses': float(expense_total),
            'balance': float(income_total - expense_total)
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
        
        # Inicializa o dicionário de totais por categoria
        category_totals = {}
        for cat in categories:
            category_totals[cat.id] = {
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
        
        # Calcula totais
        total_income = 0
        total_expenses = 0
        
        # Atualiza totais de receitas
        for category_id, total in income_totals:
            if category_id in category_totals:
                category_totals[category_id]['income'] = float(total)
                total_income += float(total)
        
        # Atualiza totais de despesas
        for category_id, total in expense_totals:
            if category_id in category_totals:
                category_totals[category_id]['expense'] = float(total)
                category_totals[category_id]['budget'] = float(total)  # Orçamento igual à despesa
                total_expenses += float(total)
        
        # O orçamento mensal total é igual ao total de despesas
        monthly_budget = total_expenses
        
        return {
            'categories': category_totals,
            'month': month,
            'year': year,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': total_income - total_expenses,
            'monthly_budget': monthly_budget
        }

category = CRUDCategory(FinanceCategory)
transaction = CRUDTransaction(FinanceTransaction)
budget = CRUDBudget(FinanceBudget) 
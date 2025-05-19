from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class TransactionType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class FinanceCategory(Base):
    __tablename__ = "finance_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(Enum(TransactionType), nullable=False)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    
    # Relacionamentos
    transactions = relationship("FinanceTransaction", back_populates="category")
    budgets = relationship("FinanceBudget", back_populates="category")
    family = relationship("Family", back_populates="finance_categories")

class FinanceTransaction(Base):
    __tablename__ = "finance_transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String)
    date = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("finance_categories.id"), nullable=False)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    
    # Relacionamentos
    category = relationship("FinanceCategory", back_populates="transactions")
    family = relationship("Family", back_populates="finance_transactions")

    # Garante que o valor seja positivo para receitas e negativo para despesas
    __table_args__ = (
        CheckConstraint(
            "(type = 'INCOME' AND amount > 0) OR (type = 'EXPENSE' AND amount > 0)",
            name="check_amount_type"
        ),
    )

class FinanceBudget(Base):
    __tablename__ = "finance_budgets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("finance_categories.id"), nullable=False)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    
    # Relacionamentos
    category = relationship("FinanceCategory", back_populates="budgets")
    family = relationship("Family", back_populates="finance_budgets") 
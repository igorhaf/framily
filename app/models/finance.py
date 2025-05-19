from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class FinanceCategory(Base):
    __tablename__ = "finance_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    
    # Relacionamentos
    family = relationship("Family", back_populates="finance_categories")
    transactions = relationship("FinanceTransaction", back_populates="category")

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

class FinanceBudget(Base):
    __tablename__ = "finance_budgets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("finance_categories.id"), nullable=False)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    
    # Relacionamentos
    category = relationship("FinanceCategory")
    family = relationship("Family", back_populates="finance_budgets") 
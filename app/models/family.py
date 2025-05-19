from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = relationship("FamilyMember", back_populates="family")
    tasks = relationship("Task", back_populates="family")
    events = relationship("Event", back_populates="family")
    finance_categories = relationship("FinanceCategory", back_populates="family")
    finance_transactions = relationship("FinanceTransaction", back_populates="family")
    finance_budgets = relationship("FinanceBudget", back_populates="family")

class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    kinship = Column(String, nullable=False)  # Renomeado de 'relationship' para 'kinship'
    notes = Column(Text)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)

    # Relacionamentos
    family = relationship("Family", back_populates="members")
    tasks = relationship("Task", back_populates="family_member")
    events = relationship("Event", back_populates="family_member")
    appointments = relationship("HealthAppointment", back_populates="family_member")
    medications = relationship("HealthMedication", back_populates="family_member")
    exams = relationship("HealthExam", back_populates="family_member") 
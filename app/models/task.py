from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys - tornando opcionais
    family_id = Column(Integer, ForeignKey("families.id"), nullable=True)
    family_member_id = Column(Integer, ForeignKey("family_members.id"), nullable=True)
    
    # Relationships
    family = relationship("Family", back_populates="tasks")
    family_member = relationship("FamilyMember", back_populates="tasks") 
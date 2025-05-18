from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Family relationships
    family_id = Column(Integer, ForeignKey("families.id"))
    family = relationship("Family", back_populates="members")
    
    # User's items
    tasks = relationship("Task", back_populates="user")
    events = relationship("Event", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    health_records = relationship("HealthRecord", back_populates="user") 
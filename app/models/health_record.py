from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    record_type = Column(String, index=True)  # e.g., weight, blood_pressure, medication
    value = Column(String, nullable=False)  # Store as string to handle different formats
    unit = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    record_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"))
    family_id = Column(Integer, ForeignKey("families.id"))
    
    # Relationships
    user = relationship("User", back_populates="health_records")
    family = relationship("Family", back_populates="health_records") 
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class HealthRecordBase(BaseModel):
    record_type: str  # e.g., "weight", "blood_pressure", "medication"
    value: str
    unit: Optional[str] = None
    notes: Optional[str] = None
    record_date: datetime


class HealthRecordCreate(HealthRecordBase):
    pass


class HealthRecordUpdate(HealthRecordBase):
    pass


class HealthRecord(HealthRecordBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 
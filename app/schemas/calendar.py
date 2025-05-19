from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class CalendarEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    event_type: str  # Mudando para str para corresponder ao modelo
    family_member_id: int
    location: Optional[str] = None
    is_all_day: bool = False
    color: Optional[str] = None

    # Removendo validador restritivo para permitir novos tipos de eventos
    # Os tipos no banco incluem: trabalho, aniversario, saude, escola, lazer, esporte

class CalendarEventCreate(CalendarEventBase):
    pass

class CalendarEventUpdate(CalendarEventBase):
    title: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    event_type: Optional[str] = None
    family_member_id: Optional[int] = None

class CalendarEvent(CalendarEventBase):
    id: int

    class Config:
        from_attributes = True 
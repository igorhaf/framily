from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from app.db.base_class import Base
import enum

# Tipos de evento existentes na base de dados:
# trabalho, aniversario, saude, escola, lazer, esporte

class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    event_type = Column(String, nullable=False)  # Mudando para String para evitar problemas com o Enum
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    location = Column(String)
    is_all_day = Column(Boolean, default=False)
    color = Column(String)  # Para personalização visual 
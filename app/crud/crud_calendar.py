from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.calendar import CalendarEvent
from app.schemas.calendar import CalendarEventCreate, CalendarEventUpdate

class CRUDCalendar(CRUDBase[CalendarEvent, CalendarEventCreate, CalendarEventUpdate]):
    def get_events(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        family_member_id: Optional[int] = None,
        event_type: Optional[str] = None
    ) -> List[CalendarEvent]:
        query = db.query(self.model).filter(
            self.model.start_date <= end_date,
            self.model.end_date >= start_date
        )
        
        if family_member_id:
            query = query.filter(self.model.family_member_id == family_member_id)
        if event_type:
            query = query.filter(self.model.event_type == event_type)
            
        return query.all()

    def create_event(self, db: Session, *, obj_in: CalendarEventCreate) -> CalendarEvent:
        db_obj = CalendarEvent(
            title=obj_in.title,
            description=obj_in.description,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            event_type=obj_in.event_type,
            family_member_id=obj_in.family_member_id,
            location=obj_in.location,
            is_all_day=obj_in.is_all_day,
            color=obj_in.color
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_event(
        self,
        db: Session,
        *,
        db_obj: CalendarEvent,
        obj_in: CalendarEventUpdate
    ) -> CalendarEvent:
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

calendar = CRUDCalendar(CalendarEvent) 
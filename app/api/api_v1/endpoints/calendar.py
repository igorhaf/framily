from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app import crud, models, schemas
from app.api import deps
from app.crud.crud_calendar import calendar
from app.schemas.calendar import CalendarEvent, CalendarEventCreate, CalendarEventUpdate

router = APIRouter()

@router.get("/events/", response_model=List[CalendarEvent])
def get_events(
    db: Session = Depends(deps.get_db),
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    family_member_id: Optional[int] = None,
    event_type: Optional[str] = None
):
    """
    Retorna eventos do calendário dentro de um período específico.
    """
    return calendar.get_events(
        db=db,
        start_date=start_date,
        end_date=end_date,
        family_member_id=family_member_id,
        event_type=event_type
    )

@router.post("/events/", response_model=CalendarEvent)
def create_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: CalendarEventCreate
):
    """
    Cria um novo evento no calendário.
    """
    try:
        return calendar.create_event(db=db, obj_in=event_in)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar evento: {str(e)}"
        )

@router.put("/events/{event_id}", response_model=CalendarEvent)
def update_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int,
    event_in: CalendarEventUpdate
):
    """
    Atualiza um evento existente.
    """
    event = calendar.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return calendar.update_event(db=db, db_obj=event, obj_in=event_in)

@router.delete("/events/{event_id}")
def delete_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int
):
    """
    Remove um evento do calendário.
    """
    event = calendar.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return calendar.remove(db=db, id=event_id) 
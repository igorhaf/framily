from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/events", response_model=List[schemas.Event])
def read_events(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve events.
    """
    events = crud.event.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return events

@router.post("/events", response_model=schemas.Event)
def create_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: schemas.EventCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create new event.
    """
    event = crud.event.create_with_user(db=db, obj_in=event_in, user_id=current_user.id)
    return event 
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/records", response_model=List[schemas.HealthRecord])
def read_health_records(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve health records.
    """
    records = crud.health_record.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return records

@router.post("/records", response_model=schemas.HealthRecord)
def create_health_record(
    *,
    db: Session = Depends(deps.get_db),
    record_in: schemas.HealthRecordCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create new health record.
    """
    record = crud.health_record.create_with_user(
        db=db, obj_in=record_in, user_id=current_user.id
    )
    return record 
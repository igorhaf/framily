from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app import crud
from app.schemas.education import *
import logging

router = APIRouter()

# Instituições
@router.get("/institutions/", response_model=List[EducationInstitutionInDB])
def list_institutions(db: Session = Depends(deps.get_db)):
    return crud.education_institution.get_multi(db)

@router.post("/institutions/", response_model=EducationInstitutionInDB)
def create_institution(obj_in: EducationInstitutionCreate, db: Session = Depends(deps.get_db)):
    return crud.education_institution.create(db, obj_in=obj_in)

# Eventos
@router.get("/events/", response_model=List[EducationEventInDB])
def list_events(db: Session = Depends(deps.get_db)):
    try:
        return crud.education_event.get_multi(db)
    except Exception as e:
        logging.exception("Erro ao buscar eventos de educação")
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar eventos de educação: {str(e)}")

@router.post("/events/", response_model=EducationEventInDB)
def create_event(obj_in: EducationEventCreate, db: Session = Depends(deps.get_db)):
    return crud.education_event.create(db, obj_in=obj_in)

# Certificações
@router.get("/certifications/", response_model=List[CertificationInDB])
def list_certifications(db: Session = Depends(deps.get_db)):
    return crud.certification.get_multi(db)

@router.post("/certifications/", response_model=CertificationInDB)
def create_certification(obj_in: CertificationCreate, db: Session = Depends(deps.get_db)):
    return crud.certification.create(db, obj_in=obj_in)

# Recursos de Aprendizagem
@router.get("/resources/", response_model=List[LearningResourceInDB])
def list_resources(db: Session = Depends(deps.get_db)):
    return crud.learning_resource.get_multi(db)

@router.post("/resources/", response_model=LearningResourceInDB)
def create_resource(obj_in: LearningResourceCreate, db: Session = Depends(deps.get_db)):
    return crud.learning_resource.create(db, obj_in=obj_in)

# Metas de Aprendizagem
@router.get("/goals/", response_model=List[LearningGoalInDB])
def list_goals(db: Session = Depends(deps.get_db)):
    return crud.learning_goal.get_multi(db)

@router.post("/goals/", response_model=LearningGoalInDB)
def create_goal(obj_in: LearningGoalCreate, db: Session = Depends(deps.get_db)):
    return crud.learning_goal.create(db, obj_in=obj_in)

# Despesas Educacionais
@router.get("/expenses/", response_model=List[EducationExpenseInDB])
def list_expenses(db: Session = Depends(deps.get_db)):
    return crud.education_expense.get_multi(db)

@router.post("/expenses/", response_model=EducationExpenseInDB)
def create_expense(obj_in: EducationExpenseCreate, db: Session = Depends(deps.get_db)):
    return crud.education_expense.create(db, obj_in=obj_in) 
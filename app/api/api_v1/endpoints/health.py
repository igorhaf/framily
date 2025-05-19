from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_health import health_appointment, health_medication, health_exam
from app.schemas.health import (
    HealthAppointment,
    HealthAppointmentCreate,
    HealthAppointmentUpdate,
    HealthMedication,
    HealthMedicationCreate,
    HealthMedicationUpdate,
    HealthExam,
    HealthExamCreate,
    HealthExamUpdate
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Endpoints para Consultas
@router.get("/appointments/", response_model=List[HealthAppointment])
def read_appointments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    family_member_id: Optional[int] = None
):
    """
    Retorna lista de consultas médicas.
    Se family_member_id for fornecido, retorna apenas as consultas daquele membro.
    """
    if family_member_id:
        return health_appointment.get_by_family_member(
            db=db, family_member_id=family_member_id, skip=skip, limit=limit
        )
    return health_appointment.get_multi(db, skip=skip, limit=limit)

@router.post("/appointments/", response_model=HealthAppointment)
def create_appointment(
    *,
    db: Session = Depends(deps.get_db),
    appointment_in: HealthAppointmentCreate
):
    """
    Cria nova consulta médica.
    """
    return health_appointment.create(db=db, obj_in=appointment_in)

@router.put("/appointments/{appointment_id}", response_model=HealthAppointment)
def update_appointment(
    *,
    db: Session = Depends(deps.get_db),
    appointment_id: int,
    appointment_in: HealthAppointmentUpdate
):
    """
    Atualiza uma consulta médica existente.
    """
    appointment = health_appointment.get(db=db, id=appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return health_appointment.update(db=db, db_obj=appointment, obj_in=appointment_in)

@router.delete("/appointments/{appointment_id}")
def delete_appointment(
    *,
    db: Session = Depends(deps.get_db),
    appointment_id: int
):
    """
    Remove uma consulta médica.
    """
    appointment = health_appointment.get(db=db, id=appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return health_appointment.remove(db=db, id=appointment_id)

# Endpoints para Medicamentos
@router.get("/medications/", response_model=List[HealthMedication])
def read_medications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    family_member_id: Optional[int] = None
):
    """
    Retorna lista de medicamentos.
    Se family_member_id for fornecido, retorna apenas os medicamentos daquele membro.
    """
    if family_member_id:
        return health_medication.get_by_family_member(
            db=db, family_member_id=family_member_id, skip=skip, limit=limit
        )
    return health_medication.get_multi(db, skip=skip, limit=limit)

@router.post("/medications/", response_model=HealthMedication)
def create_medication(
    *,
    db: Session = Depends(deps.get_db),
    medication_in: HealthMedicationCreate
):
    """
    Cria novo registro de medicamento.
    """
    try:
        return health_medication.create(db=db, obj_in=medication_in)
    except Exception as e:
        logger.error(f"Erro ao criar medicamento: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar medicamento: {str(e)}"
        )

@router.put("/medications/{medication_id}", response_model=HealthMedication)
def update_medication(
    *,
    db: Session = Depends(deps.get_db),
    medication_id: int,
    medication_in: HealthMedicationUpdate
):
    """
    Atualiza um registro de medicamento existente.
    """
    medication = health_medication.get(db=db, id=medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return health_medication.update(db=db, db_obj=medication, obj_in=medication_in)

@router.delete("/medications/{medication_id}")
def delete_medication(
    *,
    db: Session = Depends(deps.get_db),
    medication_id: int
):
    """
    Remove um registro de medicamento.
    """
    medication = health_medication.get(db=db, id=medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return health_medication.remove(db=db, id=medication_id)

# Endpoints para Exames
@router.get("/exams/", response_model=List[HealthExam])
def read_exams(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    family_member_id: Optional[int] = None
):
    """
    Retorna lista de exames.
    Se family_member_id for fornecido, retorna apenas os exames daquele membro.
    """
    if family_member_id:
        return health_exam.get_by_family_member(
            db=db, family_member_id=family_member_id, skip=skip, limit=limit
        )
    return health_exam.get_multi(db, skip=skip, limit=limit)

@router.post("/exams/", response_model=HealthExam)
def create_exam(
    *,
    db: Session = Depends(deps.get_db),
    exam_in: HealthExamCreate
):
    """
    Cria novo registro de exame.
    """
    return health_exam.create(db=db, obj_in=exam_in)

@router.put("/exams/{exam_id}", response_model=HealthExam)
def update_exam(
    *,
    db: Session = Depends(deps.get_db),
    exam_id: int,
    exam_in: HealthExamUpdate
):
    """
    Atualiza um registro de exame existente.
    """
    exam = health_exam.get(db=db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exame não encontrado")
    return health_exam.update(db=db, db_obj=exam, obj_in=exam_in)

@router.delete("/exams/{exam_id}")
def delete_exam(
    *,
    db: Session = Depends(deps.get_db),
    exam_id: int
):
    """
    Remove um registro de exame.
    """
    exam = health_exam.get(db=db, id=exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exame não encontrado")
    return health_exam.remove(db=db, id=exam_id) 
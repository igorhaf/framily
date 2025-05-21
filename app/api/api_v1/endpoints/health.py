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
import traceback

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
    try:
        logger.info("Iniciando busca de consultas médicas...")
        logger.info(f"Parâmetros: skip={skip}, limit={limit}, family_member_id={family_member_id}")
        
        if family_member_id:
            appointments = health_appointment.get_by_family_member(
                db=db, family_member_id=family_member_id, skip=skip, limit=limit
            )
        else:
            appointments = health_appointment.get_multi(db, skip=skip, limit=limit)
            
        logger.info(f"Consultas encontradas: {len(appointments)}")
        for appointment in appointments:
            logger.info(f"Consulta ID: {appointment.id}, Data: {appointment.date}, Médico: {appointment.doctor}")
        
        return appointments
    except Exception as e:
        logger.error(f"Erro ao buscar consultas: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar consultas: {str(e)}"
        )

@router.post("/appointments/", response_model=HealthAppointment)
def create_appointment(
    *,
    db: Session = Depends(deps.get_db),
    appointment_in: HealthAppointmentCreate
):
    """
    Cria nova consulta médica.
    """
    try:
        logger.info("Iniciando criação de consulta médica...")
        logger.info(f"Dados da consulta: {appointment_in.dict()}")
        
        appointment = health_appointment.create(db=db, obj_in=appointment_in)
        logger.info(f"Consulta criada com ID: {appointment.id}")
        
        return appointment
    except Exception as e:
        logger.error(f"Erro ao criar consulta: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao criar consulta: {str(e)}"
        )

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
    try:
        logger.info(f"Iniciando atualização da consulta ID: {appointment_id}")
        logger.info(f"Novos dados: {appointment_in.dict()}")
        
        appointment = health_appointment.get(db=db, id=appointment_id)
        if not appointment:
            logger.warning(f"Consulta ID {appointment_id} não encontrada")
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
            
        updated_appointment = health_appointment.update(db=db, db_obj=appointment, obj_in=appointment_in)
        logger.info(f"Consulta ID {appointment_id} atualizada com sucesso")
        
        return updated_appointment
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar consulta: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao atualizar consulta: {str(e)}"
        )

@router.delete("/appointments/{appointment_id}")
def delete_appointment(
    *,
    db: Session = Depends(deps.get_db),
    appointment_id: int
):
    """
    Remove uma consulta médica.
    """
    try:
        logger.info(f"Iniciando remoção da consulta ID: {appointment_id}")
        
        appointment = health_appointment.get(db=db, id=appointment_id)
        if not appointment:
            logger.warning(f"Consulta ID {appointment_id} não encontrada")
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
            
        health_appointment.remove(db=db, id=appointment_id)
        logger.info(f"Consulta ID {appointment_id} removida com sucesso")
        
        return {"message": "Consulta removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover consulta: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao remover consulta: {str(e)}"
        )

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
    try:
        logger.info("Iniciando busca de medicamentos...")
        logger.info(f"Parâmetros: skip={skip}, limit={limit}, family_member_id={family_member_id}")
        
        if family_member_id:
            medications = health_medication.get_by_family_member(
                db=db, family_member_id=family_member_id, skip=skip, limit=limit
            )
        else:
            medications = health_medication.get_multi(db, skip=skip, limit=limit)
            
        logger.info(f"Medicamentos encontrados: {len(medications)}")
        for medication in medications:
            logger.info(f"Medicamento ID: {medication.id}, Nome: {medication.name}, Dosagem: {medication.dosage}")
        
        return medications
    except Exception as e:
        logger.error(f"Erro ao buscar medicamentos: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar medicamentos: {str(e)}"
        )

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
        logger.info("Iniciando criação de medicamento...")
        logger.info(f"Dados do medicamento: {medication_in.dict()}")
        
        medication = health_medication.create(db=db, obj_in=medication_in)
        logger.info(f"Medicamento criado com ID: {medication.id}")
        
        return medication
    except Exception as e:
        logger.error(f"Erro ao criar medicamento: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao criar medicamento: {str(e)}"
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
    try:
        logger.info(f"Iniciando atualização do medicamento ID: {medication_id}")
        logger.info(f"Novos dados: {medication_in.dict()}")
        
        medication = health_medication.get(db=db, id=medication_id)
        if not medication:
            logger.warning(f"Medicamento ID {medication_id} não encontrado")
            raise HTTPException(status_code=404, detail="Medicamento não encontrado")
            
        updated_medication = health_medication.update(db=db, db_obj=medication, obj_in=medication_in)
        logger.info(f"Medicamento ID {medication_id} atualizado com sucesso")
        
        return updated_medication
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar medicamento: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao atualizar medicamento: {str(e)}"
        )

@router.delete("/medications/{medication_id}")
def delete_medication(
    *,
    db: Session = Depends(deps.get_db),
    medication_id: int
):
    """
    Remove um registro de medicamento.
    """
    try:
        logger.info(f"Iniciando remoção do medicamento ID: {medication_id}")
        
        medication = health_medication.get(db=db, id=medication_id)
        if not medication:
            logger.warning(f"Medicamento ID {medication_id} não encontrado")
            raise HTTPException(status_code=404, detail="Medicamento não encontrado")
            
        health_medication.remove(db=db, id=medication_id)
        logger.info(f"Medicamento ID {medication_id} removido com sucesso")
        
        return {"message": "Medicamento removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover medicamento: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao remover medicamento: {str(e)}"
        )

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
    try:
        logger.info("Iniciando busca de exames...")
        logger.info(f"Parâmetros: skip={skip}, limit={limit}, family_member_id={family_member_id}")
        
        if family_member_id:
            exams = health_exam.get_by_family_member(
                db=db, family_member_id=family_member_id, skip=skip, limit=limit
            )
        else:
            exams = health_exam.get_multi(db, skip=skip, limit=limit)
            
        logger.info(f"Exames encontrados: {len(exams)}")
        for exam in exams:
            logger.info(f"Exame ID: {exam.id}, Nome: {exam.name}, Data: {exam.date}")
        
        return exams
    except Exception as e:
        logger.error(f"Erro ao buscar exames: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao buscar exames: {str(e)}"
        )

@router.post("/exams/", response_model=HealthExam)
def create_exam(
    *,
    db: Session = Depends(deps.get_db),
    exam_in: HealthExamCreate
):
    """
    Cria novo registro de exame.
    """
    try:
        logger.info("Iniciando criação de exame...")
        logger.info(f"Dados do exame: {exam_in.dict()}")
        
        exam = health_exam.create(db=db, obj_in=exam_in)
        logger.info(f"Exame criado com ID: {exam.id}")
        
        return exam
    except Exception as e:
        logger.error(f"Erro ao criar exame: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao criar exame: {str(e)}"
        )

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
    try:
        logger.info(f"Iniciando atualização do exame ID: {exam_id}")
        logger.info(f"Novos dados: {exam_in.dict()}")
        
        exam = health_exam.get(db=db, id=exam_id)
        if not exam:
            logger.warning(f"Exame ID {exam_id} não encontrado")
            raise HTTPException(status_code=404, detail="Exame não encontrado")
            
        updated_exam = health_exam.update(db=db, db_obj=exam, obj_in=exam_in)
        logger.info(f"Exame ID {exam_id} atualizado com sucesso")
        
        return updated_exam
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar exame: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao atualizar exame: {str(e)}"
        )

@router.delete("/exams/{exam_id}")
def delete_exam(
    *,
    db: Session = Depends(deps.get_db),
    exam_id: int
):
    """
    Remove um registro de exame.
    """
    try:
        logger.info(f"Iniciando remoção do exame ID: {exam_id}")
        
        exam = health_exam.get(db=db, id=exam_id)
        if not exam:
            logger.warning(f"Exame ID {exam_id} não encontrado")
            raise HTTPException(status_code=404, detail="Exame não encontrado")
            
        health_exam.remove(db=db, id=exam_id)
        logger.info(f"Exame ID {exam_id} removido com sucesso")
        
        return {"message": "Exame removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover exame: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao remover exame: {str(e)}"
        ) 
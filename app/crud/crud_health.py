from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.crud.base import CRUDBase
from app.models.health import HealthAppointment, HealthMedication, HealthExam
from app.schemas.health import HealthAppointmentCreate, HealthAppointmentUpdate
from app.schemas.health import HealthMedicationCreate, HealthMedicationUpdate
from app.schemas.health import HealthExamCreate, HealthExamUpdate

class CRUDHealthAppointment(CRUDBase[HealthAppointment, HealthAppointmentCreate, HealthAppointmentUpdate]):
    def get_by_family_member(
        self, db: Session, *, family_member_id: int, skip: int = 0, limit: int = 100
    ) -> List[HealthAppointment]:
        return (
            db.query(self.model)
            .filter(HealthAppointment.family_member_id == family_member_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_upcoming(
        self, db: Session, *, family_member_id: int, days: int = 30
    ) -> List[HealthAppointment]:
        today = date.today()
        return (
            db.query(self.model)
            .filter(
                HealthAppointment.family_member_id == family_member_id,
                HealthAppointment.date >= today,
                HealthAppointment.date <= today + datetime.timedelta(days=days)
            )
            .order_by(HealthAppointment.date, HealthAppointment.time)
            .all()
        )

class CRUDHealthMedication(CRUDBase[HealthMedication, HealthMedicationCreate, HealthMedicationUpdate]):
    def get_by_family_member(
        self, db: Session, *, family_member_id: int, skip: int = 0, limit: int = 100
    ) -> List[HealthMedication]:
        return (
            db.query(self.model)
            .filter(HealthMedication.family_member_id == family_member_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active(
        self, db: Session, *, family_member_id: int
    ) -> List[HealthMedication]:
        return (
            db.query(self.model)
            .filter(
                HealthMedication.family_member_id == family_member_id,
                HealthMedication.status == "ativo"
            )
            .all()
        )

class CRUDHealthExam(CRUDBase[HealthExam, HealthExamCreate, HealthExamUpdate]):
    def get_by_family_member(
        self, db: Session, *, family_member_id: int, skip: int = 0, limit: int = 100
    ) -> List[HealthExam]:
        return (
            db.query(self.model)
            .filter(HealthExam.family_member_id == family_member_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_upcoming(
        self, db: Session, *, family_member_id: int, days: int = 30
    ) -> List[HealthExam]:
        today = date.today()
        return (
            db.query(self.model)
            .filter(
                HealthExam.family_member_id == family_member_id,
                HealthExam.date >= today,
                HealthExam.date <= today + datetime.timedelta(days=days)
            )
            .order_by(HealthExam.date)
            .all()
        )

health_appointment = CRUDHealthAppointment(HealthAppointment)
health_medication = CRUDHealthMedication(HealthMedication)
health_exam = CRUDHealthExam(HealthExam) 
from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models.health import AppointmentType, MedicationStatus

class HealthAppointmentBase(BaseModel):
    family_member_id: int
    date: date
    time: str
    type: AppointmentType
    doctor: str
    specialty: str
    location: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = "agendado"

class HealthAppointmentCreate(HealthAppointmentBase):
    pass

class HealthAppointmentUpdate(HealthAppointmentBase):
    pass

class HealthAppointment(HealthAppointmentBase):
    id: int

    class Config:
        from_attributes = True

class HealthMedicationBase(BaseModel):
    family_member_id: int
    name: str
    dosage: str
    frequency: str
    start_date: date
    end_date: Optional[date] = None
    status: Optional[MedicationStatus] = MedicationStatus.ATIVO
    notes: Optional[str] = None

class HealthMedicationCreate(HealthMedicationBase):
    pass

class HealthMedicationUpdate(HealthMedicationBase):
    pass

class HealthMedication(HealthMedicationBase):
    id: int

    class Config:
        from_attributes = True

class HealthExamBase(BaseModel):
    family_member_id: int
    name: str
    date: date
    location: Optional[str] = None
    doctor: Optional[str] = None
    notes: Optional[str] = None
    result: Optional[str] = None
    status: Optional[str] = "agendado"

class HealthExamCreate(HealthExamBase):
    pass

class HealthExamUpdate(HealthExamBase):
    pass

class HealthExam(HealthExamBase):
    id: int

    class Config:
        from_attributes = True 
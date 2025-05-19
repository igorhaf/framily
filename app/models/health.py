from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class AppointmentType(str, enum.Enum):
    CONSULTA = "consulta"
    RETORNO = "retorno"
    EMERGENCIA = "emergencia"
    EXAME = "exame"
    VACINA = "vacina"

class HealthAppointment(Base):
    __tablename__ = "health_appointments"

    id = Column(Integer, primary_key=True, index=True)
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    date = Column(Date, nullable=False)
    time = Column(String, nullable=False)
    type = Column(Enum(AppointmentType), nullable=False)
    doctor = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    location = Column(String)
    notes = Column(Text)
    status = Column(String, default="agendado")

    family_member = relationship("FamilyMember", back_populates="appointments")

class HealthMedication(Base):
    __tablename__ = "health_medications"

    id = Column(Integer, primary_key=True, index=True)
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(String, default="ativo")
    notes = Column(Text)

    family_member = relationship("FamilyMember", back_populates="medications")

class HealthExam(Base):
    __tablename__ = "health_exams"

    id = Column(Integer, primary_key=True, index=True)
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String)
    doctor = Column(String)
    notes = Column(Text)
    result = Column(Text)
    status = Column(String, default="agendado")

    family_member = relationship("FamilyMember", back_populates="exams") 
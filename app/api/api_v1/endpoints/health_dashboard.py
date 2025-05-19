from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.api import deps
from app.models import HealthAppointment, HealthMedication, HealthExam, FamilyMember

router = APIRouter()

@router.get("/summary")
def health_summary(db: Session = Depends(deps.get_db)):
    today = date.today()
    next_30 = today + timedelta(days=30)
    # Próximas consultas
    upcoming_appointments = db.query(HealthAppointment).filter(
        HealthAppointment.date >= today,
        HealthAppointment.date <= next_30
    ).order_by(HealthAppointment.date).all()
    # Medicamentos ativos
    active_medications = db.query(HealthMedication).filter(
        HealthMedication.status == "ativo"
    ).all()
    # Exames agendados
    pending_exams = db.query(HealthExam).filter(
        HealthExam.status == "agendado"
    ).all()
    # Quantidade por membro
    members = db.query(FamilyMember).all()
    member_stats = []
    for m in members:
        member_stats.append({
            "id": m.id,
            "name": m.name,
            "consultas": db.query(HealthAppointment).filter(HealthAppointment.family_member_id==m.id).count(),
            "medicamentos": db.query(HealthMedication).filter(HealthMedication.family_member_id==m.id).count(),
            "exames": db.query(HealthExam).filter(HealthExam.family_member_id==m.id).count(),
        })
    return {
        "upcoming_appointments": [
            {"id": a.id, "date": a.date, "type": a.type, "member_id": a.family_member_id} for a in upcoming_appointments
        ],
        "active_medications": [
            {"id": m.id, "name": m.name, "member_id": m.family_member_id} for m in active_medications
        ],
        "pending_exams": [
            {"id": e.id, "name": e.name, "date": e.date, "member_id": e.family_member_id} for e in pending_exams
        ],
        "member_stats": member_stats
    }

@router.get("/stats")
def health_stats(db: Session = Depends(deps.get_db)):
    today = date.today()
    first_day = today.replace(day=1)
    # Consultas
    total_appointments = db.query(HealthAppointment).filter(HealthAppointment.date >= first_day).count()
    done_appointments = db.query(HealthAppointment).filter(HealthAppointment.date >= first_day, HealthAppointment.status=="realizado").count()
    scheduled_appointments = db.query(HealthAppointment).filter(HealthAppointment.date >= first_day, HealthAppointment.status=="agendado").count()
    canceled_appointments = db.query(HealthAppointment).filter(HealthAppointment.date >= first_day, HealthAppointment.status=="cancelado").count()
    # Exames
    done_exams = db.query(HealthExam).filter(HealthExam.date >= first_day, HealthExam.status=="realizado").count()
    pending_exams = db.query(HealthExam).filter(HealthExam.date >= first_day, HealthExam.status=="agendado").count()
    # Top membros
    top_members = db.query(FamilyMember).all()
    top = sorted([
        {"id": m.id, "name": m.name, "consultas": db.query(HealthAppointment).filter(HealthAppointment.family_member_id==m.id, HealthAppointment.date >= first_day).count(), "exames": db.query(HealthExam).filter(HealthExam.family_member_id==m.id, HealthExam.date >= first_day).count()} for m in top_members
    ], key=lambda x: (x["consultas"]+x["exames"]), reverse=True)[:3]
    return {
        "total_appointments": total_appointments,
        "done_appointments": done_appointments,
        "scheduled_appointments": scheduled_appointments,
        "canceled_appointments": canceled_appointments,
        "done_exams": done_exams,
        "pending_exams": pending_exams,
        "top_members": top
    }

@router.get("/timeline")
def health_timeline(db: Session = Depends(deps.get_db)):
    today = date.today()
    start = today - timedelta(days=90)
    # Consultas
    appointments = db.query(HealthAppointment).filter(HealthAppointment.date >= start).all()
    # Exames
    exams = db.query(HealthExam).filter(HealthExam.date >= start).all()
    # Medicamentos (início)
    medications = db.query(HealthMedication).filter(HealthMedication.start_date >= start).all()
    timeline = []
    for a in appointments:
        timeline.append({"type": "consulta", "date": a.date, "member_id": a.family_member_id, "id": a.id})
    for e in exams:
        timeline.append({"type": "exame", "date": e.date, "member_id": e.family_member_id, "id": e.id})
    for m in medications:
        timeline.append({"type": "medicamento", "date": m.start_date, "member_id": m.family_member_id, "id": m.id})
    timeline = sorted(timeline, key=lambda x: x["date"], reverse=True)
    return {"timeline": timeline} 
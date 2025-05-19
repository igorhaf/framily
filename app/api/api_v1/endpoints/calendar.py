from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import traceback
from app import crud, models, schemas
from app.api import deps
from app.crud.crud_calendar import calendar
from app.schemas.calendar import CalendarEvent, CalendarEventCreate, CalendarEventUpdate
from app.models.calendar import CalendarEvent as CalendarEventModel

router = APIRouter()


@router.get("/events/", response_model=List[CalendarEvent])
def get_events(
    db: Session = Depends(deps.get_db),
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    family_member_id: Optional[int] = None,
    event_type: Optional[str] = None
):
    """
    Retorna eventos do calendário dentro de um período específico.
    """
    try:
        print(f"Solicitação de eventos: start_date={start_date}, end_date={end_date}")
        
        # Converter strings para datas
        try:
            # Tenta primeiro o formato completo
            if "T" in start_date:
                start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            else:
                # Formato simples (YYYY-MM-DD)
                start = datetime.strptime(start_date, "%Y-%m-%d")
                
            if "T" in end_date:
                end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            else:
                # Formato simples (YYYY-MM-DD)
                end = datetime.strptime(end_date, "%Y-%m-%d")
                # Se for só a data, considerar o fim do dia
                end = end.replace(hour=23, minute=59, second=59)
                
            print(f"Datas convertidas: start={start}, end={end}")
        except Exception as date_error:
            print(f"Erro ao converter datas: {start_date} - {end_date}, Erro: {str(date_error)}")
            # Usar datas padrão em caso de erro
            start = datetime.now()
            end = start + timedelta(days=30)
            print(f"Usando datas padrão: start={start}, end={end}")
        
        # Consulta no banco
        try:
            print("Executando consulta no banco...")
            # Verificar quantos eventos existem no total
            total_events = db.query(CalendarEventModel).count()
            print(f"Total de eventos no banco: {total_events}")
            
            query = db.query(CalendarEventModel).filter(
                CalendarEventModel.start_date <= end,
                CalendarEventModel.end_date >= start
            )
            
            # Aplicar filtros adicionais
            if family_member_id:
                query = query.filter(CalendarEventModel.family_member_id == family_member_id)
            if event_type:
                query = query.filter(CalendarEventModel.event_type == event_type)
            
            # Executar a consulta
            events = query.all()
            print(f"Encontrados {len(events)} eventos de {start} até {end}")
            
            # Verificar se a serialização funciona
            try:
                # Testar a serialização de cada evento
                for i, event in enumerate(events):
                    print(f"Evento {i+1}: {event.id} - {event.title} - {event.start_date}")
            except Exception as serialize_error:
                print(f"Erro ao serializar eventos: {str(serialize_error)}")
                print(traceback.format_exc())
            
            return events
        except Exception as db_error:
            print(f"Erro na consulta ao banco: {str(db_error)}")
            print(traceback.format_exc())
            raise
        
    except Exception as e:
        print(f"Erro ao buscar eventos: {str(e)}")
        print(traceback.format_exc())
        # Retornar lista vazia em vez de erro para não quebrar a UI
        return []

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
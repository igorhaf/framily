#!/usr/bin/env python
import os
import sys
from datetime import datetime

# Adicionar o diretório raiz ao PYTHONPATH
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

from app.db.session import SessionLocal
from app.models.calendar import CalendarEvent

def check_events():
    """Verifica os eventos do calendário no banco de dados"""
    print("=== Verificando eventos do calendário ===")
    db = SessionLocal()
    
    try:
        # Contagem total de eventos
        total_events = db.query(CalendarEvent).count()
        print(f"Total de eventos no banco de dados: {total_events}")
        
        if total_events == 0:
            print("Não há eventos cadastrados.")
            return
        
        # Obter todos os eventos
        events = db.query(CalendarEvent).all()
        
        # Mostrar detalhes dos eventos
        print("\nDetalhes dos eventos:")
        for i, event in enumerate(events, 1):
            print(f"\nEvento {i}:")
            print(f"  ID: {event.id}")
            print(f"  Título: {event.title}")
            print(f"  Tipo: {event.event_type}")
            print(f"  Data início: {event.start_date}")
            print(f"  Data fim: {event.end_date}")
            print(f"  Membro da família: {event.family_member_id}")
            print(f"  Local: {event.location}")
            print(f"  Dia inteiro: {event.is_all_day}")
            print(f"  Cor: {event.color}")
            
        # Verificar eventos em um período específico
        start_date = datetime(2025, 5, 19)
        end_date = datetime(2025, 6, 18)
        
        filtered_events = db.query(CalendarEvent).filter(
            CalendarEvent.start_date <= end_date,
            CalendarEvent.end_date >= start_date
        ).all()
        
        print(f"\nEventos no período de {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}: {len(filtered_events)}")
        
        # Mostrar tipos de eventos existentes
        event_types = set(event.event_type for event in events)
        print(f"\nTipos de eventos existentes: {event_types}")
        
    except Exception as e:
        print(f"Erro ao consultar eventos: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_events() 
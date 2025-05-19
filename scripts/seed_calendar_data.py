import os
import sys
from datetime import datetime, timedelta
import requests

# Adicionar o diretório raiz ao PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# URL base da API
BASE_URL = "http://localhost:8000/api/v1"

def create_calendar_event(event_data):
    """Cria um evento no calendário."""
    response = requests.post(f"{BASE_URL}/calendar/events/", json=event_data)
    if response.status_code == 200:
        print(f"Evento criado: {event_data['title']}")
    else:
        print(f"Erro ao criar evento {event_data['title']}: {response.text}")

def seed_calendar_data():
    """Adiciona dados de exemplo ao calendário."""
    print("Iniciando seed do calendário...")

    # Data base para os eventos
    base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Lista de eventos de exemplo
    events = [
        {
            "title": "Consulta Médica - João",
            "description": "Consulta de rotina com Dr. Silva",
            "start_date": (base_date + timedelta(days=2)).isoformat(),
            "end_date": (base_date + timedelta(days=2, hours=1)).isoformat(),
            "event_type": "consulta",
            "family_member_id": 1,
            "location": "Clínica Saúde",
            "is_all_day": False
        },
        {
            "title": "Reunião de Pais",
            "description": "Reunião na escola dos filhos",
            "start_date": (base_date + timedelta(days=5, hours=19)).isoformat(),
            "end_date": (base_date + timedelta(days=5, hours=21)).isoformat(),
            "event_type": "evento",
            "family_member_id": 1,
            "location": "Escola Municipal",
            "is_all_day": False
        },
        {
            "title": "Pagamento de Contas",
            "description": "Pagar contas do mês",
            "start_date": (base_date + timedelta(days=7)).isoformat(),
            "end_date": (base_date + timedelta(days=7, hours=1)).isoformat(),
            "event_type": "tarefa",
            "family_member_id": 1,
            "is_all_day": False
        },
        {
            "title": "Aniversário Maria",
            "description": "Aniversário de 10 anos",
            "start_date": (base_date + timedelta(days=10)).isoformat(),
            "end_date": (base_date + timedelta(days=10, hours=4)).isoformat(),
            "event_type": "evento",
            "family_member_id": 1,
            "location": "Casa",
            "is_all_day": True
        },
        {
            "title": "Consulta Dentista",
            "description": "Limpeza semestral",
            "start_date": (base_date + timedelta(days=12, hours=14)).isoformat(),
            "end_date": (base_date + timedelta(days=12, hours=15)).isoformat(),
            "event_type": "consulta",
            "family_member_id": 1,
            "location": "Clínica Dental",
            "is_all_day": False
        },
        {
            "title": "Lembrete: Comprar Presente",
            "description": "Comprar presente para aniversário",
            "start_date": (base_date + timedelta(days=8)).isoformat(),
            "end_date": (base_date + timedelta(days=8)).isoformat(),
            "event_type": "lembrete",
            "family_member_id": 1,
            "is_all_day": True
        }
    ]

    # Criar eventos
    for event in events:
        create_calendar_event(event)

    print("Seed do calendário concluído!")

if __name__ == "__main__":
    seed_calendar_data() 
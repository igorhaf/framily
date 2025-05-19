import os
import sys
import requests
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

BASE_URL = "http://localhost:8000/api/v1"

def test_create_event():
    # Criar um evento de teste
    event = {
        "title": "Teste de Evento",
        "description": "Este é um evento de teste",
        "start_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=1, hours=1)).isoformat(),
        "event_type": "consulta",  # Usando o valor do enum
        "family_member_id": 1,
        "location": "Local de Teste",
        "is_all_day": False,
        "color": "#FF5733"
    }

    # Fazer a requisição POST
    response = requests.post(
        "http://localhost:8000/api/v1/calendar/events/",
        json=event
    )

    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")

if __name__ == "__main__":
    test_create_event() 
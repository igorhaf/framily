import os
import sys
import requests
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

def seed_health_data():
    base_url = "http://localhost:8000"
    
    # Dados de teste para consultas
    appointments = [
        {
            "type": "consulta",
            "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "time": "14:00",
            "family_member_id": 1,
            "doctor": "Dr. João Silva",
            "specialty": "Clínico Geral",
            "notes": "Check-up anual"
        },
        {
            "type": "consulta",
            "date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "time": "15:30",
            "family_member_id": 1,
            "doctor": "Dra. Maria Santos",
            "specialty": "Cardiologia",
            "notes": "Avaliação cardiológica"
        }
    ]

    # Dados de teste para medicamentos
    medications = [
        {
            "name": "Paracetamol",
            "dosage": "500mg",
            "frequency": "8/8 horas",
            "family_member_id": 1,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "status": "ativo"
        },
        {
            "name": "Vitamina C",
            "dosage": "1g",
            "frequency": "1 vez ao dia",
            "family_member_id": 1,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "status": "ativo"
        }
    ]

    # Dados de teste para exames
    exams = [
        {
            "name": "Hemograma Completo",
            "date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "family_member_id": 1,
            "notes": "Exame de sangue de rotina"
        },
        {
            "name": "Eletrocardiograma",
            "date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "family_member_id": 1,
            "notes": "Avaliação cardíaca"
        }
    ]

    # Adiciona as consultas
    print("\nAdicionando consultas...")
    for appointment in appointments:
        try:
            response = requests.post(f"{base_url}/api/v1/health/appointments/", json=appointment)
            print(f"Status: {response.status_code}")
            print(f"Resposta: {response.json()}")
        except Exception as e:
            print(f"Erro ao adicionar consulta: {str(e)}")

    # Adiciona os medicamentos
    print("\nAdicionando medicamentos...")
    for medication in medications:
        try:
            response = requests.post(f"{base_url}/api/v1/health/medications/", json=medication)
            print(f"Status: {response.status_code}")
            print(f"Resposta: {response.json()}")
        except Exception as e:
            print(f"Erro ao adicionar medicamento: {str(e)}")

    # Adiciona os exames
    print("\nAdicionando exames...")
    for exam in exams:
        try:
            response = requests.post(f"{base_url}/api/v1/health/exams/", json=exam)
            print(f"Status: {response.status_code}")
            print(f"Resposta: {response.json()}")
        except Exception as e:
            print(f"Erro ao adicionar exame: {str(e)}")

if __name__ == "__main__":
    seed_health_data() 
import os
import sys
import requests
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

def test_health_endpoints():
    base_url = "http://localhost:8000"
    
    # Testa o endpoint de consultas
    print("\nTestando endpoint de consultas...")
    try:
        response = requests.get(f"{base_url}/api/v1/health/appointments/")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"Erro ao testar consultas: {str(e)}")

    # Testa o endpoint de medicamentos
    print("\nTestando endpoint de medicamentos...")
    try:
        response = requests.get(f"{base_url}/api/v1/health/medications/")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"Erro ao testar medicamentos: {str(e)}")

    # Testa o endpoint de exames
    print("\nTestando endpoint de exames...")
    try:
        response = requests.get(f"{base_url}/api/v1/health/exams/")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"Erro ao testar exames: {str(e)}")

if __name__ == "__main__":
    test_health_endpoints() 
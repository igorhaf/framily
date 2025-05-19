import os
import sys
import requests
from bs4 import BeautifulSoup
import json

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

def check_health_page():
    base_url = "http://localhost:8000"
    
    print("\nVerificando página de saúde...")
    
    # Verifica a página HTML
    try:
        response = requests.get(f"{base_url}/health")
        print(f"\nStatus da página: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Verifica se há mensagem de erro
            error_div = soup.find('div', {'id': 'error-message'})
            if error_div and not error_div.get('class', []).count('hidden'):
                print("\nErro encontrado na página:")
                print(error_div.text.strip())
            
            # Verifica os contadores
            total_appointments = soup.find('p', {'id': 'total-appointments'})
            total_medications = soup.find('p', {'id': 'total-medications'})
            total_exams = soup.find('p', {'id': 'total-exams'})
            
            print("\nContadores:")
            print(f"Consultas: {total_appointments.text if total_appointments else 'N/A'}")
            print(f"Medicamentos: {total_medications.text if total_medications else 'N/A'}")
            print(f"Exames: {total_exams.text if total_exams else 'N/A'}")
            
            # Verifica as listas
            appointments_list = soup.find('div', {'id': 'appointments'})
            medications_list = soup.find('div', {'id': 'medications'})
            exams_list = soup.find('div', {'id': 'exams'})
            
            print("\nConteúdo das listas:")
            print(f"Consultas: {appointments_list.text.strip() if appointments_list else 'N/A'}")
            print(f"Medicamentos: {medications_list.text.strip() if medications_list else 'N/A'}")
            print(f"Exames: {exams_list.text.strip() if exams_list else 'N/A'}")
            
    except Exception as e:
        print(f"\nErro ao acessar a página: {str(e)}")
    
    # Verifica as APIs
    print("\nVerificando APIs...")
    
    # Consultas
    try:
        response = requests.get(f"{base_url}/api/v1/health/appointments/")
        print(f"\nAPI de Consultas - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Dados: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Erro na API de consultas: {str(e)}")
    
    # Medicamentos
    try:
        response = requests.get(f"{base_url}/api/v1/health/medications/")
        print(f"\nAPI de Medicamentos - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Dados: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Erro na API de medicamentos: {str(e)}")
    
    # Exames
    try:
        response = requests.get(f"{base_url}/api/v1/health/exams/")
        print(f"\nAPI de Exames - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Dados: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Erro na API de exames: {str(e)}")

if __name__ == "__main__":
    check_health_page() 
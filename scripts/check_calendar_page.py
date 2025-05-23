import os
import sys
import requests
from bs4 import BeautifulSoup
import json

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

BASE_URL = "http://localhost:8000"

ERROR_MSG = "Erro ao carregar eventos, tarefas, exames de saúde e consultas: Erro HTTP ao buscar eventos de educação! status: 500"


def check_calendar_page():
    print("\nVerificando página de calendário...")
    try:
        response = requests.get(f"{BASE_URL}/calendar")
        print(f"\nStatus da página: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Verifica se há mensagem de erro
            error_div = soup.find('div', {'id': 'error-message'})
            if error_div and not error_div.get('class', []).count('hidden'):
                error_text = error_div.text.strip()
                print("\nErro encontrado na página:")
                print(error_text)
                if ERROR_MSG in error_text:
                    print("\n>>> O ERRO 500 DE EVENTOS DE EDUCAÇÃO PERSISTE! <<<")
                else:
                    print("\n>>> Outro erro encontrado! <<<")
                return
            # Verifica se o calendário está sendo exibido
            calendar_div = soup.find('div', {'id': 'calendar'})
            if calendar_div:
                print("\nO calendário está sendo exibido normalmente!")
            else:
                print("\nO calendário NÃO está sendo exibido!")
        else:
            print(f"\nErro ao acessar a página: {response.status_code}")
    except Exception as e:
        print(f"\nErro ao acessar a página: {str(e)}")

    # Checa a API de eventos de educação
    print("\nVerificando API de eventos de educação...")
    try:
        api_resp = requests.get(f"{BASE_URL}/api/v1/education/events/")
        print(f"Status da API: {api_resp.status_code}")
        if api_resp.status_code == 200:
            print(f"Eventos de educação retornados: {len(api_resp.json())}")
        else:
            print(f"Resposta da API: {api_resp.text}")
    except Exception as e:
        print(f"Erro ao acessar a API de eventos de educação: {str(e)}")

if __name__ == "__main__":
    check_calendar_page() 
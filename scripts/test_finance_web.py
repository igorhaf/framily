import requests
from bs4 import BeautifulSoup
import json
import time
import sys

def test_finance_web_page():
    base_url = "http://localhost:8000"
    print("Testando página web de finanças...")
    print("-" * 50)
    
    try:
        # Testa a página principal de finanças
        print("\nTestando página principal de finanças...")
        response = requests.get(f"{base_url}/finances")
        
        if response.status_code == 200:
            print("✅ Página carregada com sucesso!")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Verifica se há elementos importantes na página
            error_div = soup.find('div', {'id': 'error-message'})
            if error_div and error_div.text.strip():
                print(f"❌ Erro encontrado na página: {error_div.text.strip()}")
            else:
                print("✅ Nenhum erro visível na página")
            
            # Verifica se os dados foram carregados
            data_div = soup.find('div', {'id': 'finance-data'})
            if data_div:
                print("✅ Dados financeiros encontrados na página")
            else:
                print("⚠️ Div de dados financeiros não encontrada")
                
        else:
            print(f"❌ Erro ao carregar página! Status: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {str(e)}")
    
    # Testa os endpoints da API que a página usa
    print("\nTestando endpoints da API usados pela página...")
    endpoints = [
        "/api/v1/finance/summary/",
        "/api/v1/finance/categories/",
        "/api/v1/finance/transactions/"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\nTestando {endpoint}")
            response = requests.get(f"{base_url}{endpoint}")
            
            if response.status_code == 200:
                print(f"✅ Sucesso! Status: {response.status_code}")
                try:
                    data = response.json()
                    print(f"Dados recebidos: {json.dumps(data, indent=2, ensure_ascii=False)}")
                except json.JSONDecodeError:
                    print("⚠️ Resposta não é um JSON válido")
            else:
                print(f"❌ Erro! Status: {response.status_code}")
                print(f"Resposta: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {str(e)}")
        
        # Pequena pausa entre as requisições
        time.sleep(1)

if __name__ == "__main__":
    print("Iniciando testes da página web de finanças...")
    test_finance_web_page() 
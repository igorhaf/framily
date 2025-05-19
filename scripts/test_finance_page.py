import requests
import json
from datetime import date
import sys

def test_finance_endpoints():
    base_url = "http://localhost:8000"
    endpoints = [
        "/api/v1/finance/summary/",
        "/api/v1/finance/categories/",
        "/api/v1/finance/transactions/",
        "/api/v1/finance/budgets/"
    ]
    
    print("Testando endpoints de finanças...")
    print("-" * 50)
    
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
    
    print("\nTestando resumo financeiro com parâmetros...")
    try:
        today = date.today()
        params = {
            "start_date": today.replace(day=1).isoformat(),
            "end_date": today.replace(month=today.month + 1, day=1).isoformat() if today.month < 12 else today.replace(year=today.year + 1, month=1, day=1).isoformat()
        }
        
        response = requests.get(f"{base_url}/api/v1/finance/summary/", params=params)
        
        if response.status_code == 200:
            print("✅ Sucesso no resumo financeiro!")
            try:
                data = response.json()
                print(f"Dados do resumo: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print("⚠️ Resposta do resumo não é um JSON válido")
        else:
            print(f"❌ Erro no resumo financeiro! Status: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição do resumo: {str(e)}")

if __name__ == "__main__":
    print("Iniciando testes da página de finanças...")
    test_finance_endpoints() 
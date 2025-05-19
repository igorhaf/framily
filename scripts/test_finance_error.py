import requests
import json
from datetime import date
import sys
import traceback

def test_finance_error():
    base_url = "http://localhost:8000"
    print("Testando erro de carregamento de transações...")
    print("-" * 50)
    
    try:
        # Testa o endpoint de resumo financeiro
        print("\nTestando endpoint de resumo financeiro...")
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
            
    except Exception as e:
        print(f"❌ Erro ao testar resumo financeiro:")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem do erro: {str(e)}")
        print("\nTraceback completo:")
        traceback.print_exc()
    
    try:
        # Testa o endpoint de transações
        print("\nTestando endpoint de transações...")
        response = requests.get(f"{base_url}/api/v1/finance/transactions/")
        
        if response.status_code == 200:
            print("✅ Sucesso nas transações!")
            try:
                data = response.json()
                print(f"Dados das transações: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print("⚠️ Resposta das transações não é um JSON válido")
        else:
            print(f"❌ Erro nas transações! Status: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar transações:")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem do erro: {str(e)}")
        print("\nTraceback completo:")
        traceback.print_exc()

if __name__ == "__main__":
    print("Iniciando testes de erro de finanças...")
    test_finance_error() 
#!/usr/bin/env python
import os
import sys
import requests
import json
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao PYTHONPATH
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

def test_calendar_api():
    """Testa diretamente a API de eventos do calendário"""
    print("=== Testando API de eventos do calendário ===")
    
    # URL base da API (supondo que esteja rodando localmente)
    base_url = "http://127.0.0.1:8000"
    
    # Definir período para a consulta (próximos 30 dias)
    today = datetime.now()
    end_date = today + timedelta(days=30)
    
    # Formatar as datas no formato esperado pela API
    start_str = today.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    # Construir a URL da requisição
    api_url = f"{base_url}/api/v1/calendar/events/?start_date={start_str}&end_date={end_str}"
    print(f"URL da API: {api_url}")
    
    # Fazer a requisição
    try:
        print("Enviando requisição...")
        response = requests.get(api_url)
        print(f"Status da resposta: {response.status_code}")
        
        # Se a resposta for bem-sucedida, mostrar os eventos
        if response.status_code == 200:
            data = response.json()
            print(f"Eventos encontrados: {len(data)}")
            
            # Mostrar detalhes dos eventos
            for i, event in enumerate(data, 1):
                print(f"\nEvento {i}:")
                print(f"  ID: {event['id']}")
                print(f"  Título: {event['title']}")
                print(f"  Tipo: {event['event_type']}")
                print(f"  Data início: {event['start_date']}")
                print(f"  Data fim: {event['end_date']}")
                print(f"  Membro: {event.get('family_member_id', 'Não informado')}")
                
            # Verificar se há dados inconsistentes
            print("\nVerificando inconsistências...")
            for event in data:
                if 'id' not in event:
                    print(f"ERRO: Evento sem ID: {event}")
                if 'start_date' not in event or 'end_date' not in event:
                    print(f"ERRO: Evento sem datas: {event}")
                    
            # Validar se as datas estão em formato ISO
            for event in data:
                try:
                    start = datetime.fromisoformat(event['start_date'].replace('Z', '+00:00'))
                    end = datetime.fromisoformat(event['end_date'].replace('Z', '+00:00'))
                except Exception as e:
                    print(f"ERRO: Formato de data inválido em {event['id']}: {str(e)}")
            
            return True
        else:
            # Se houver erro, mostrar os detalhes
            print("Erro na resposta:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(response.text)
            return False
    except Exception as e:
        print(f"Erro ao fazer requisição: {str(e)}")
        return False

if __name__ == "__main__":
    test_calendar_api() 
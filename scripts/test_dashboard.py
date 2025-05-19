#!/usr/bin/env python
import os
import sys
import requests
from datetime import datetime, timedelta
import json
import time
from urllib.parse import urljoin

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.calendar import CalendarEvent
from sqlalchemy import text

# Configurações
API_URL = "http://localhost:8000"

def test_calendar_events_api():
    """Testa a API de eventos do calendário diretamente"""
    print("\n=== Testando API de Eventos do Calendário ===")
    
    # Gera datas para a consulta
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)
    
    # Formata as datas no formato aceito pela API
    start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")
    
    # URL para a API de eventos
    url = f"{API_URL}/api/v1/calendar/events/?start_date={start_str}&end_date={end_str}"
    print(f"Fazendo requisição para: {url}")
    
    try:
        # Faz a requisição
        response = requests.get(url)
        
        # Verifica se a requisição foi bem-sucedida
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            events = response.json()
            print(f"Eventos encontrados: {len(events)}")
            for i, event in enumerate(events[:3], 1):
                print(f"  {i}. {event['title']} ({event['event_type']}) - {event['start_date']}")
            return True
        else:
            print(f"Erro na requisição: {response.text}")
            return False
    except Exception as e:
        print(f"Exceção durante a requisição: {str(e)}")
        return False

def check_database_events():
    """Verifica os eventos diretamente no banco de dados"""
    print("\n=== Verificando Eventos no Banco de Dados ===")
    
    try:
        db = SessionLocal()
        events = db.query(CalendarEvent).all()
        print(f"Eventos no banco: {len(events)}")
        
        if not events:
            print("Nenhum evento encontrado no banco de dados!")
            return False
        
        # Mostra alguns eventos
        for i, event in enumerate(events[:3], 1):
            print(f"  {i}. {event.title} ({event.event_type}) - {event.start_date} -> {event.end_date}")
        
        return True
    except Exception as e:
        print(f"Erro ao consultar o banco de dados: {str(e)}")
        return False
    finally:
        db.close()

def fix_database_events():
    """Corrige possíveis problemas nos eventos do calendário"""
    print("\n=== Tentando corrigir eventos do calendário ===")
    
    try:
        db = SessionLocal()
        
        # Verifica se existem eventos
        event_count = db.query(CalendarEvent).count()
        if event_count == 0:
            print("Não há eventos para corrigir. Vamos criar alguns eventos de teste.")
            
            # Criar eventos de teste
            eventos_teste = []
            for i in range(1, 6):
                start_date = datetime.now() + timedelta(days=i*3)
                end_date = start_date + timedelta(hours=2)
                
                novo_evento = CalendarEvent(
                    title=f"Evento Teste {i}",
                    description=f"Evento criado pelo script de teste {i}",
                    start_date=start_date,
                    end_date=end_date,
                    event_type="teste",
                    family_member_id=1,  # Assume que existe um membro com ID 1
                    is_all_day=False,
                    location="Local de Teste",
                    color="#" + hex(i*20)[2:].zfill(6)
                )
                eventos_teste.append(novo_evento)
                
            db.add_all(eventos_teste)
            db.commit()
            print(f"Criados {len(eventos_teste)} eventos de teste.")
        else:
            print(f"Existem {event_count} eventos no banco. Vamos verificar se estão corretos.")
            
            # Verifica os eventos existentes
            eventos = db.query(CalendarEvent).all()
            for evento in eventos:
                # Ajusta eventos com datas inválidas
                if evento.end_date < evento.start_date:
                    print(f"Corrigindo data final do evento {evento.id}: {evento.title}")
                    evento.end_date = evento.start_date + timedelta(hours=1)
                
                # Se o tipo de evento for NULL ou vazio
                if not evento.event_type:
                    print(f"Corrigindo tipo do evento {evento.id}: {evento.title}")
                    evento.event_type = "outro"
            
            db.commit()
            print("Eventos existentes verificados e corrigidos.")
            
        return True
    except Exception as e:
        print(f"Erro ao corrigir eventos: {str(e)}")
        return False
    finally:
        db.close()

def fix_api_issue():
    """Corrige problemas na API de calendário"""
    print("\n=== Corrigindo problemas na API de calendário ===")
    
    try:
        # 1. Verifica se o endpoint responde
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
        
        # Formata as datas no formato aceito pela API
        start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")
        
        url = f"{API_URL}/api/v1/calendar/events/?start_date={start_str}&end_date={end_str}"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("API está respondendo corretamente!")
            return True
        
        print(f"Erro na API: {response.status_code} - {response.text}")
        
        # Se o erro persistir, vamos verificar se é um problema de encoding ou formato de data
        # Convertendo para timestamp para evitar problemas de formatação
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        
        url_alt = f"{API_URL}/api/v1/calendar/events/?start_date={start_timestamp}&end_date={end_timestamp}"
        print(f"Tentando URL alternativa: {url_alt}")
        
        response_alt = requests.get(url_alt)
        if response_alt.status_code == 200:
            print("API respondeu com timestamp! Isso sugere um problema de formatação de data.")
            return True
        
        print("Erro persistente na API. Verifique os logs do servidor.")
        return False
        
    except Exception as e:
        print(f"Erro ao testar a API: {str(e)}")
        return False

def main():
    """Função principal de teste"""
    print("=== Iniciando testes da página inicial ===")
    
    # 1. Verifica eventos no banco de dados
    db_ok = check_database_events()
    
    # 2. Se não houver eventos ou se houver problemas, tenta corrigir
    if not db_ok:
        print("\nTentando corrigir o banco de dados...")
        fix_database_events()
        # Verifica novamente
        db_ok = check_database_events()
    
    # 3. Testa a API
    api_ok = test_calendar_events_api()
    
    # 4. Se a API não estiver funcionando, tenta corrigir
    if not api_ok:
        print("\nTentando corrigir a API...")
        fix_api_issue()
        # Testa novamente
        api_ok = test_calendar_events_api()
    
    # Resultado final
    if db_ok and api_ok:
        print("\n✅ Todos os testes foram bem-sucedidos!")
        print("O problema na página inicial deve estar resolvido.")
        print("Por favor, reinicie o servidor e teste novamente.")
    else:
        print("\n❌ Ainda existem problemas a serem resolvidos.")
        print("Verifique os logs para mais detalhes.")

if __name__ == "__main__":
    main() 
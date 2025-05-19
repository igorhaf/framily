#!/usr/bin/env python
import os
import sys
import traceback
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao PYTHONPATH
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

from app.db.session import SessionLocal
from app.models.calendar import CalendarEvent
from app.models.family import Family, FamilyMember

def check_family_members(db):
    """Verifica se existem membros da família no banco de dados"""
    count = db.query(FamilyMember).count()
    if count == 0:
        print("Não há membros da família cadastrados. Criando família e membros...")
        
        # Criar uma família
        family = Family(
            name="Família Teste",
            description="Família criada para testes"
        )
        db.add(family)
        db.flush()  # Para obter o ID da família
        
        # Criar membros da família
        members = [
            FamilyMember(
                name="João",
                birth_date=datetime.now() - timedelta(days=365*40),  # 40 anos
                kinship="Pai",
                family_id=family.id
            ),
            FamilyMember(
                name="Maria",
                birth_date=datetime.now() - timedelta(days=365*38),  # 38 anos
                kinship="Mãe",
                family_id=family.id
            ),
            FamilyMember(
                name="Pedro",
                birth_date=datetime.now() - timedelta(days=365*10),  # 10 anos
                kinship="Filho",
                family_id=family.id
            )
        ]
        db.add_all(members)
        db.commit()
        
        # Recarregar do banco para confirmar
        members = db.query(FamilyMember).all()
        print(f"Família e {len(members)} membros criados com sucesso:")
        for member in members:
            print(f"  - ID: {member.id}, Nome: {member.name}, Parentesco: {member.kinship}")
    else:
        members = db.query(FamilyMember).all()
        print(f"Já existem {count} membros da família cadastrados:")
        for member in members:
            print(f"  - ID: {member.id}, Nome: {member.name}, Parentesco: {member.kinship}")
    
    return db.query(FamilyMember).all()

def create_sample_events():
    """Cria eventos de amostra no banco de dados"""
    print("=== Criando eventos de amostra ===")
    db = SessionLocal()
    
    try:
        # Verificar se existem membros da família
        members = check_family_members(db)
        if not members:
            print("Erro: Não foi possível criar ou encontrar membros da família")
            return False
            
        # Usar IDs dos membros existentes
        member_ids = [member.id for member in members]
        
        # Verificar se já existem eventos
        count = db.query(CalendarEvent).count()
        print(f"Total de eventos existentes: {count}")
        
        # Criar eventos para os próximos dias
        today = datetime.now()
        
        # Dados dos eventos
        events_data = [
            {
                "title": "Reunião de Trabalho",
                "description": "Reunião com a equipe de desenvolvimento",
                "start_date": today + timedelta(days=1, hours=10),
                "end_date": today + timedelta(days=1, hours=11),
                "event_type": "trabalho",
                "family_member_id": member_ids[0],  # Primeiro membro
                "location": "Escritório",
                "is_all_day": False,
                "color": "#4285F4"
            },
            {
                "title": "Consulta Médica",
                "description": "Exame de rotina",
                "start_date": today + timedelta(days=3, hours=14),
                "end_date": today + timedelta(days=3, hours=15),
                "event_type": "saude",
                "family_member_id": member_ids[0],  # Primeiro membro
                "location": "Hospital",
                "is_all_day": False,
                "color": "#34A853"
            },
            {
                "title": "Aniversário da Maria",
                "description": "Festa de aniversário",
                "start_date": today + timedelta(days=5),
                "end_date": today + timedelta(days=5),
                "event_type": "aniversario",
                "family_member_id": member_ids[1] if len(member_ids) > 1 else member_ids[0],  # Segundo membro ou primeiro
                "location": "Casa",
                "is_all_day": True,
                "color": "#EA4335"
            },
            {
                "title": "Feira de Ciências",
                "description": "Apresentação do projeto escolar",
                "start_date": today + timedelta(days=7, hours=13),
                "end_date": today + timedelta(days=7, hours=16),
                "event_type": "escola",
                "family_member_id": member_ids[2] if len(member_ids) > 2 else member_ids[0],  # Terceiro membro ou primeiro
                "location": "Escola",
                "is_all_day": False,
                "color": "#FBBC05"
            },
            {
                "title": "Futebol",
                "description": "Jogo no clube",
                "start_date": today + timedelta(days=10, hours=16),
                "end_date": today + timedelta(days=10, hours=18),
                "event_type": "esporte",
                "family_member_id": member_ids[0],  # Primeiro membro
                "location": "Clube",
                "is_all_day": False,
                "color": "#4285F4"
            }
        ]
        
        # Criar os eventos no banco
        events = []
        for event_data in events_data:
            print(f"Criando evento: {event_data['title']}")
            event = CalendarEvent(**event_data)
            events.append(event)
        
        # Adicionar ao banco de dados
        try:
            db.add_all(events)
            db.commit()
            print(f"Foram criados {len(events)} eventos de amostra.")
        except Exception as commit_error:
            db.rollback()
            print(f"Erro ao salvar eventos no banco: {str(commit_error)}")
            traceback.print_exc()
            return False
        
        # Exibir os eventos criados
        all_events = db.query(CalendarEvent).all()
        print(f"\nTotal de eventos no banco: {len(all_events)}")
        for i, event in enumerate(all_events[-5:], 1):  # Mostrar os 5 últimos eventos
            print(f"{i}. {event.title} ({event.event_type}) - {event.start_date.strftime('%Y-%m-%d %H:%M')} -> {event.end_date.strftime('%Y-%m-%d %H:%M')}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar eventos: {str(e)}")
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_events() 
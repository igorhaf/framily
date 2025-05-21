import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

import sqlalchemy
from sqlalchemy import create_engine, text
from app.core.config import settings

def check_tasks_data():
    # Criar engine
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Verificar dados
    with engine.connect() as conn:
        # Verificar se há tarefas
        result = conn.execute(text("SELECT COUNT(*) FROM tasks"))
        count = result.scalar()
        print(f"\nTotal de tarefas: {count}")
        
        # Listar tarefas
        if count > 0:
            result = conn.execute(text("SELECT * FROM tasks"))
            tasks = result.fetchall()
            print("\nTarefas:")
            for task in tasks:
                print(f"ID: {task.id}")
                print(f"Título: {task.title}")
                print(f"Status: {task.status}")
                print(f"Família ID: {task.family_id}")
                print(f"Membro ID: {task.family_member_id}")
                print("---")

if __name__ == "__main__":
    check_tasks_data() 
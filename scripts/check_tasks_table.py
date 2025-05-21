import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

import sqlalchemy
from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

def check_tasks_table():
    # Criar engine
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    inspector = inspect(engine)
    
    # Verificar se a tabela existe
    if "tasks" not in inspector.get_table_names():
        print("A tabela 'tasks' não existe!")
        return
    
    # Obter informações das colunas
    columns = inspector.get_columns("tasks")
    print("\nTasks Columns:")
    for column in columns:
        print(f"{column['name']}: {column['type']}")

if __name__ == "__main__":
    check_tasks_table() 
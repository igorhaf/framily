import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

import sqlalchemy
from sqlalchemy import create_engine, text
from app.core.config import settings

print("Verificando registros na tabela 'tasks'...")
print(f"URL do banco de dados: {settings.SQLALCHEMY_DATABASE_URI}")

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM tasks"))
    count = result.scalar()
    print(f"Total de registros na tabela 'tasks': {count}")

    if count > 0:
        result = conn.execute(text("SELECT * FROM tasks LIMIT 5"))
        rows = result.fetchall()
        print("\nPrimeiros 5 registros:")
        for row in rows:
            print(row) 
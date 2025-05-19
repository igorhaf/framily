import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

import sqlalchemy
from sqlalchemy import create_engine, text
from app.core.config import settings

print("Criando tabela 'tasks' diretamente no banco de dados...")
print(f"URL do banco de dados: {settings.SQLALCHEMY_DATABASE_URI}")

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            description VARCHAR,
            due_date TIMESTAMP,
            completed BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            family_id INTEGER NOT NULL REFERENCES families(id),
            family_member_id INTEGER REFERENCES family_members(id)
        )
    """))
    conn.commit()
print("Tabela 'tasks' criada com sucesso!") 
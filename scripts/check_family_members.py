import os
import sys
import sqlalchemy
from sqlalchemy import create_engine, text

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost/family_dashboard"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Membros da família cadastrados:")
    try:
        result = conn.execute(text("SELECT id, name FROM family_members"))
        rows = result.fetchall()
        if not rows:
            print("Nenhum membro encontrado.")
        for row in rows:
            print(f"id={row[0]}, nome={row[1]}")
    except Exception as e:
        print(f"Erro ao consultar membros da família: {e}") 
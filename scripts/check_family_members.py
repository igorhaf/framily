import os
import sys
from sqlalchemy import create_engine, text

# Adicionar o diretório raiz ao PYTHONPATH antes de qualquer import do app
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from app.core.config import settings

# Conectar ao banco de dados
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

with engine.connect() as conn:
    print("Membros de família disponíveis:")
    result = conn.execute(text("SELECT id, name, family_id FROM family_members"))
    for row in result:
        print(f"ID: {row.id} | Nome: {row.name} | family_id: {row.family_id}") 
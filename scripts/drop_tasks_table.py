import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

import sqlalchemy
from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS tasks"))
    conn.commit()
print("Tabela tasks foi dropada. Agora rodando alembic upgrade head...")

import subprocess
subprocess.run(["alembic", "upgrade", "head"], check=True)
print("Migration aplicada com sucesso. Tabela tasks recriada com family_member_id.") 
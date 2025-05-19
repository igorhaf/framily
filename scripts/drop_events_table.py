import sqlalchemy
from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS events"))
    conn.commit()
print("Tabela events foi dropada. Agora rodando alembic upgrade head...")

import subprocess
subprocess.run(["alembic", "upgrade", "head"], check=True)
print("Migration aplicada com sucesso. Tabela events recriada com family_member_id.") 
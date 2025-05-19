import sqlalchemy
from sqlalchemy import create_engine, text
from datetime import date

DATABASE_URL = "postgresql://postgres:postgres@localhost/family_dashboard"

print("Adicionando membro de família de teste...")
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text("""
        INSERT INTO family_members (name, birth_date, kinship, family_id)
        VALUES ('Membro Teste', :birth_date, 'Responsável', 1)
    """), {"birth_date": date(1990, 1, 1)})
    conn.commit()
print("Membro de família de teste adicionado com sucesso!") 
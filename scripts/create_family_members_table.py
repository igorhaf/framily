import sqlalchemy
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:postgres@localhost/family_dashboard"

print("Dropando e recriando a tabela family_members...")
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS family_members CASCADE"))
    conn.execute(text("""
        CREATE TABLE family_members (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            birth_date DATE,
            kinship VARCHAR,
            family_id INTEGER REFERENCES families(id) ON DELETE CASCADE
        )
    """))
    conn.commit()
print("Tabela family_members recriada com sucesso!") 
import sqlalchemy
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:postgres@localhost/family_dashboard"

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    print("--- Family Members (columns) ---")
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'family_members'"))
    columns = [row[0] for row in result]
    print(columns)
    print("\n--- Family Members (records) ---")
    result = conn.execute(text(f"SELECT * FROM family_members"))
    for row in result:
        print(tuple(row)) 
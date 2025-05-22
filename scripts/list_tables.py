from app.db.session import SessionLocal
from sqlalchemy import inspect

db = SessionLocal()
inspector = inspect(db.bind)
print('Tabelas no banco de dados:')
for table_name in inspector.get_table_names():
    print('-', table_name)
db.close() 
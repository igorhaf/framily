from app.db.session import SessionLocal
from sqlalchemy import text

def clear_shopping_tables():
    db = SessionLocal()
    try:
        db.execute(text('DELETE FROM shopping_items;'))
        db.execute(text('DELETE FROM shopping_lists;'))
        db.commit()
        print('Tabelas de compras limpas com sucesso!')
    finally:
        db.close()

if __name__ == "__main__":
    clear_shopping_tables() 
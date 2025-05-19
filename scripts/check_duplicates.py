import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.models.finance import FinanceCategory, FinanceTransaction
from app.core.config import settings

# Criar conexão com o banco
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Verificar categorias duplicadas
    print("\nVerificando categorias duplicadas:")
    categories = db.query(FinanceCategory).all()
    category_names = {}
    for cat in categories:
        if cat.name in category_names:
            print(f"Categoria duplicada encontrada: {cat.name}")
            print(f"  ID 1: {category_names[cat.name]}")
            print(f"  ID 2: {cat.id}")
        else:
            category_names[cat.name] = cat.id

    # Verificar transações por categoria
    print("\nVerificando transações por categoria:")
    transactions = db.query(
        FinanceTransaction.category_id,
        FinanceCategory.name,
        func.count(FinanceTransaction.id).label('count'),
        func.sum(FinanceTransaction.amount).label('total')
    ).join(
        FinanceCategory,
        FinanceTransaction.category_id == FinanceCategory.id
    ).group_by(
        FinanceTransaction.category_id,
        FinanceCategory.name
    ).all()

    for cat_id, name, count, total in transactions:
        print(f"\nCategoria: {name} (ID: {cat_id})")
        print(f"  Número de transações: {count}")
        print(f"  Valor total: R$ {total:.2f}")

    # Verificar transações duplicadas
    print("\nVerificando transações duplicadas:")
    duplicate_transactions = db.query(
        FinanceTransaction.category_id,
        FinanceTransaction.date,
        FinanceTransaction.amount,
        FinanceTransaction.description,
        func.count(FinanceTransaction.id).label('count')
    ).group_by(
        FinanceTransaction.category_id,
        FinanceTransaction.date,
        FinanceTransaction.amount,
        FinanceTransaction.description
    ).having(
        func.count(FinanceTransaction.id) > 1
    ).all()

    if duplicate_transactions:
        print("\nTransações duplicadas encontradas:")
        for cat_id, date, amount, description, count in duplicate_transactions:
            print(f"\nDescrição: {description}")
            print(f"  Data: {date}")
            print(f"  Valor: R$ {amount:.2f}")
            print(f"  Categoria ID: {cat_id}")
            print(f"  Número de duplicatas: {count}")
    else:
        print("\nNenhuma transação duplicada encontrada.")

finally:
    db.close() 
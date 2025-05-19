import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.finance import FinanceCategory, FinanceTransaction, FinanceBudget
from app.core.config import settings

# Criar conexão com o banco
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Dicionário para mapear categorias duplicadas para suas originais
    category_mapping = {
        # Receitas
        'Salário': 1,
        'Freelance': 2,
        'Investimentos': 3,
        # Despesas
        'Moradia': 4,
        'Alimentação': 5,
        'Transporte': 6,
        'Saúde': 7,
        'Educação': 8,
        'Lazer': 9
    }

    # Atualizar transações e orçamentos para usar as categorias originais
    for category_name, original_id in category_mapping.items():
        # Encontrar todas as categorias com este nome
        duplicate_categories = db.query(FinanceCategory).filter(
            FinanceCategory.name == category_name,
            FinanceCategory.id != original_id
        ).all()

        for duplicate in duplicate_categories:
            # Atualizar todas as transações desta categoria duplicada
            db.query(FinanceTransaction).filter(
                FinanceTransaction.category_id == duplicate.id
            ).update({
                FinanceTransaction.category_id: original_id
            })
            
            # Atualizar todos os orçamentos desta categoria duplicada
            db.query(FinanceBudget).filter(
                FinanceBudget.category_id == duplicate.id
            ).update({
                FinanceBudget.category_id: original_id
            })
            
            # Remover a categoria duplicada
            db.delete(duplicate)
            
            print(f"Movidas transações e orçamentos da categoria {category_name} (ID: {duplicate.id}) para ID: {original_id}")

    # Commit das alterações
    db.commit()
    print("\nCategorias duplicadas removidas com sucesso!")

finally:
    db.close() 
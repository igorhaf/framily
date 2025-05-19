import sys
import os
from datetime import date, timedelta
import random

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.finance import FinanceCategory, FinanceTransaction, TransactionType
from app.crud.crud_finance import category, transaction
from app.schemas.finance import CategoryCreate, TransactionCreate

def seed_finance_data():
    db = SessionLocal()
    
    # Categorias de receitas
    income_categories = [
        CategoryCreate(name="Salário", description="Salário mensal", type=TransactionType.INCOME),
        CategoryCreate(name="Freelance", description="Trabalhos extras", type=TransactionType.INCOME),
        CategoryCreate(name="Investimentos", description="Rendimentos de investimentos", type=TransactionType.INCOME),
    ]
    
    # Categorias de despesas
    expense_categories = [
        CategoryCreate(name="Moradia", description="Aluguel e contas da casa", type=TransactionType.EXPENSE),
        CategoryCreate(name="Alimentação", description="Compras e refeições", type=TransactionType.EXPENSE),
        CategoryCreate(name="Transporte", description="Combustível e manutenção", type=TransactionType.EXPENSE),
        CategoryCreate(name="Saúde", description="Plano de saúde e medicamentos", type=TransactionType.EXPENSE),
        CategoryCreate(name="Educação", description="Mensalidades e material escolar", type=TransactionType.EXPENSE),
        CategoryCreate(name="Lazer", description="Entretenimento e diversão", type=TransactionType.EXPENSE),
    ]
    
    # Cria as categorias
    categories = []
    for cat_data in income_categories + expense_categories:
        category_obj = category.create_with_family(
            db,
            obj_in=cat_data,
            family_id=1  # Usando a família 1 como exemplo
        )
        categories.append(category_obj)
    
    # Gera transações aleatórias
    today = date.today()
    for _ in range(30):  # 30 transações
        # Escolhe uma categoria aleatória
        cat = random.choice(categories)
        
        # Gera um valor aleatório
        if cat.type == TransactionType.INCOME:
            amount = random.uniform(100, 5000)
        else:
            amount = random.uniform(10, 1000)
        
        # Gera uma data aleatória nos últimos 30 dias
        transaction_date = today - timedelta(days=random.randint(0, 30))
        
        # Cria a transação
        transaction.create_with_family(
            db,
            obj_in=TransactionCreate(
                amount=round(amount, 2),
                description=f"Transação {cat.name}",
                date=transaction_date,
                category_id=cat.id,
                type=cat.type
            ),
            family_id=1
        )
    
    db.close()

if __name__ == "__main__":
    print("Criando dados de exemplo para finanças...")
    seed_finance_data()
    print("Dados criados com sucesso!") 
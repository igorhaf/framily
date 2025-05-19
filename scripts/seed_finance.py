import sys
import os
from datetime import date, timedelta
import random

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.finance import FinanceCategory, FinanceTransaction, TransactionType
from app.crud.crud_finance import category, transaction, budget
from app.schemas.finance import CategoryCreate, TransactionCreate, BudgetCreate

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
    total_income = 0
    total_expenses = 0
    
    # Primeiro, gera as receitas
    income_cats = [cat for cat in categories if cat.type == TransactionType.INCOME]
    for cat in income_cats:
        # Gera 2-3 transações de receita por categoria
        for _ in range(random.randint(2, 3)):
            amount = random.uniform(1000, 5000)
            transaction_date = today - timedelta(days=random.randint(0, 30))
            transaction.create_with_family(
                db,
                obj_in=TransactionCreate(
                    amount=round(amount, 2),
                    description=f"Receita {cat.name}",
                    date=transaction_date,
                    category_id=cat.id,
                    type=cat.type
                ),
                family_id=1
            )
            total_income += amount
    
    # Depois, gera as despesas (total não deve exceder 70% da receita)
    expense_cats = [cat for cat in categories if cat.type == TransactionType.EXPENSE]
    max_expenses = total_income * 0.7  # Limita despesas a 70% da receita
    current_expenses = 0
    
    for cat in expense_cats:
        # Gera 3-5 transações de despesa por categoria
        for _ in range(random.randint(3, 5)):
            if current_expenses >= max_expenses:
                break
                
            # Calcula o valor máximo possível para esta transação
            remaining = max_expenses - current_expenses
            max_amount = min(remaining, 1000)  # Limita a 1000 por transação
            
            if max_amount <= 0:
                break
                
            amount = random.uniform(50, max_amount)
            transaction_date = today - timedelta(days=random.randint(0, 30))
            transaction.create_with_family(
                db,
                obj_in=TransactionCreate(
                    amount=round(amount, 2),
                    description=f"Despesa {cat.name}",
                    date=transaction_date,
                    category_id=cat.id,
                    type=cat.type
                ),
                family_id=1
            )
            current_expenses += amount
    
    # Cria orçamentos para o mês atual
    current_month = today.month
    current_year = today.year
    
    # Primeiro, cria orçamentos para receitas (total não deve exceder a receita atual)
    income_budget_total = 0
    for cat in income_cats:
        # Calcula o valor máximo possível para este orçamento
        remaining = total_income - income_budget_total
        if remaining <= 0:
            break
            
        # Distribui o orçamento proporcionalmente (90-100% do restante)
        budget_amount = remaining * random.uniform(0.9, 1.0)
        budget.create_with_family(
            db,
            obj_in=BudgetCreate(
                amount=round(budget_amount, 2),
                month=current_month,
                year=current_year,
                category_id=cat.id
            ),
            family_id=1
        )
        income_budget_total += budget_amount
    
    # Depois, cria orçamentos para despesas (total não deve exceder 70% da receita)
    expense_budget_total = 0
    max_expense_budget = total_income * 0.7  # Limita orçamento de despesas a 70% da receita
    
    # Distribui o orçamento de despesas proporcionalmente entre as categorias
    expense_cats_count = len(expense_cats)
    base_budget = max_expense_budget / expense_cats_count
    
    for cat in expense_cats:
        # Varia o orçamento em ±5% do valor base
        budget_amount = base_budget * random.uniform(0.95, 1.05)
        
        # Garante que não ultrapasse o limite total
        if expense_budget_total + budget_amount > max_expense_budget:
            budget_amount = max_expense_budget - expense_budget_total
        
        if budget_amount <= 0:
            break
            
        budget.create_with_family(
            db,
            obj_in=BudgetCreate(
                amount=round(budget_amount, 2),
                month=current_month,
                year=current_year,
                category_id=cat.id
            ),
            family_id=1
        )
        expense_budget_total += budget_amount
    
    db.close()

if __name__ == "__main__":
    print("Criando dados de exemplo para finanças...")
    seed_finance_data()
    print("Dados criados com sucesso!") 
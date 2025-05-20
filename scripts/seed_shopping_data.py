import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud import shopping_list, shopping_item
from app.schemas.shopping import ShoppingListCreate, ShoppingItemCreate
from app.models.shopping import CategoryEnum, PriorityEnum, StatusEnum

def create_shopping_lists(db: Session):
    # Lista de Compras do Mês
    lista_mes = shopping_list.create(
        db=db,
        obj_in=ShoppingListCreate(
            name="Compras do Mês",
            description="Lista de compras mensais para a casa"
        )
    )
    
    # Itens para a Lista do Mês
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Arroz",
            quantity=2,
            category=CategoryEnum.MARKET,
            priority=PriorityEnum.HIGH,
            status=StatusEnum.PENDING,
            notes="Arroz integral",
            shopping_list_id=lista_mes.id
        )
    )
    
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Feijão",
            quantity=2,
            category=CategoryEnum.MARKET,
            priority=PriorityEnum.HIGH,
            status=StatusEnum.PENDING,
            notes="Feijão carioca",
            shopping_list_id=lista_mes.id
        )
    )
    
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Óleo de Cozinha",
            quantity=1,
            category=CategoryEnum.MARKET,
            priority=PriorityEnum.MEDIUM,
            status=StatusEnum.PENDING,
            notes="Óleo de soja",
            shopping_list_id=lista_mes.id
        )
    )
    
    # Lista de Compras da Semana
    lista_semana = shopping_list.create(
        db=db,
        obj_in=ShoppingListCreate(
            name="Compras da Semana",
            description="Lista de compras semanais"
        )
    )
    
    # Itens para a Lista da Semana
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Pão",
            quantity=2,
            category=CategoryEnum.MARKET,
            priority=PriorityEnum.HIGH,
            status=StatusEnum.PENDING,
            notes="Pão francês",
            shopping_list_id=lista_semana.id
        )
    )
    
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Leite",
            quantity=2,
            category=CategoryEnum.MARKET,
            priority=PriorityEnum.HIGH,
            status=StatusEnum.PENDING,
            notes="Leite integral",
            shopping_list_id=lista_semana.id
        )
    )
    
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Queijo",
            quantity=1,
            category=CategoryEnum.MARKET,
            priority=PriorityEnum.MEDIUM,
            status=StatusEnum.PENDING,
            notes="Queijo muçarela",
            shopping_list_id=lista_semana.id
        )
    )
    
    # Lista de Compras Pessoais
    lista_pessoal = shopping_list.create(
        db=db,
        obj_in=ShoppingListCreate(
            name="Compras Pessoais",
            description="Lista de compras pessoais"
        )
    )
    
    # Itens para a Lista Pessoal
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Shampoo",
            quantity=1,
            category=CategoryEnum.PERSONAL,
            priority=PriorityEnum.MEDIUM,
            status=StatusEnum.PENDING,
            notes="Shampoo para cabelos oleosos",
            shopping_list_id=lista_pessoal.id
        )
    )
    
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Desodorante",
            quantity=1,
            category=CategoryEnum.PERSONAL,
            priority=PriorityEnum.MEDIUM,
            status=StatusEnum.PENDING,
            notes="Desodorante roll-on",
            shopping_list_id=lista_pessoal.id
        )
    )
    
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Creme Dental",
            quantity=1,
            category=CategoryEnum.PERSONAL,
            priority=PriorityEnum.LOW,
            status=StatusEnum.PENDING,
            notes="Creme dental com flúor",
            shopping_list_id=lista_pessoal.id
        )
    )
    
    # Lista de Compras da Casa
    lista_casa = shopping_list.create(
        db=db,
        obj_in=ShoppingListCreate(
            name="Compras da Casa",
            description="Lista de compras para a casa"
        )
    )
    
    # Itens para a Lista da Casa
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Detergente",
            quantity=2,
            category=CategoryEnum.HOME,
            priority=PriorityEnum.HIGH,
            status=StatusEnum.PENDING,
            notes="Detergente líquido",
            shopping_list_id=lista_casa.id
        )
    )
    
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Papel Higiênico",
            quantity=4,
            category=CategoryEnum.HOME,
            priority=PriorityEnum.HIGH,
            status=StatusEnum.PENDING,
            notes="Pacote com 4 rolos",
            shopping_list_id=lista_casa.id
        )
    )
    
    shopping_item.create(
        db=db,
        obj_in=ShoppingItemCreate(
            name="Sabão em Pó",
            quantity=1,
            category=CategoryEnum.HOME,
            priority=PriorityEnum.MEDIUM,
            status=StatusEnum.PENDING,
            notes="Sabão em pó para roupas",
            shopping_list_id=lista_casa.id
        )
    )

def main():
    db = SessionLocal()
    try:
        create_shopping_lists(db)
        print("Dados de exemplo criados com sucesso!")
    finally:
        db.close()

if __name__ == "__main__":
    main() 
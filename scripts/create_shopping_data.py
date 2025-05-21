import os
import sys
import logging

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.shopping import ShoppingList, ShoppingItem, CategoryEnum, PriorityEnum, StatusEnum
from app.db.session import SessionLocal

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_shopping_data():
    logger.info("Iniciando criação de dados de compras...")
    db = SessionLocal()
    try:
        # Testar conexão com o banco
        logger.info("Testando conexão com o banco de dados...")
        db.execute(text("SELECT 1"))
        logger.info("Conexão com o banco de dados estabelecida com sucesso!")

        # Criar lista de compras do mês
        logger.info("Criando lista de compras do mês...")
        monthly_list = ShoppingList(
            name="Compras do Mês",
            description="Lista de compras mensais para a família"
        )
        db.add(monthly_list)
        db.flush()
        logger.info(f"Lista mensal criada com ID: {monthly_list.id}")

        # Adicionar itens à lista mensal
        logger.info("Adicionando itens à lista mensal...")
        monthly_items = [
            ShoppingItem(
                name="Arroz",
                quantity=2,
                category=CategoryEnum.FOOD,
                priority=PriorityEnum.HIGH,
                status=StatusEnum.PENDING,
                notes="Preferência: tipo agulhinha",
                shopping_list_id=monthly_list.id
            ),
            ShoppingItem(
                name="Feijão",
                quantity=2,
                category=CategoryEnum.FOOD,
                priority=PriorityEnum.HIGH,
                status=StatusEnum.PENDING,
                shopping_list_id=monthly_list.id
            ),
            ShoppingItem(
                name="Óleo de Cozinha",
                quantity=1,
                category=CategoryEnum.FOOD,
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.PENDING,
                shopping_list_id=monthly_list.id
            ),
            ShoppingItem(
                name="Detergente",
                quantity=2,
                category=CategoryEnum.CLEANING,
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.PENDING,
                shopping_list_id=monthly_list.id
            ),
            ShoppingItem(
                name="Papel Higiênico",
                quantity=4,
                category=CategoryEnum.HYGIENE,
                priority=PriorityEnum.HIGH,
                status=StatusEnum.PENDING,
                shopping_list_id=monthly_list.id
            )
        ]
        db.add_all(monthly_items)
        logger.info(f"Adicionados {len(monthly_items)} itens à lista mensal")

        # Criar lista de compras da semana
        logger.info("Criando lista de compras da semana...")
        weekly_list = ShoppingList(
            name="Compras da Semana",
            description="Lista de compras semanais para a família"
        )
        db.add(weekly_list)
        db.flush()
        logger.info(f"Lista semanal criada com ID: {weekly_list.id}")

        # Adicionar itens à lista semanal
        logger.info("Adicionando itens à lista semanal...")
        weekly_items = [
            ShoppingItem(
                name="Leite",
                quantity=6,
                category=CategoryEnum.FOOD,
                priority=PriorityEnum.HIGH,
                status=StatusEnum.PENDING,
                shopping_list_id=weekly_list.id
            ),
            ShoppingItem(
                name="Pão",
                quantity=2,
                category=CategoryEnum.FOOD,
                priority=PriorityEnum.HIGH,
                status=StatusEnum.PENDING,
                shopping_list_id=weekly_list.id
            ),
            ShoppingItem(
                name="Frutas",
                quantity=1,
                category=CategoryEnum.FOOD,
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.PENDING,
                notes="Maçã, banana e laranja",
                shopping_list_id=weekly_list.id
            ),
            ShoppingItem(
                name="Sabão em Pó",
                quantity=1,
                category=CategoryEnum.CLEANING,
                priority=PriorityEnum.LOW,
                status=StatusEnum.PENDING,
                shopping_list_id=weekly_list.id
            )
        ]
        db.add_all(weekly_items)
        logger.info(f"Adicionados {len(weekly_items)} itens à lista semanal")

        # Criar lista de compras para festa
        logger.info("Criando lista de compras para festa...")
        party_list = ShoppingList(
            name="Compras para Festa",
            description="Lista de compras para a festa de aniversário"
        )
        db.add(party_list)
        db.flush()
        logger.info(f"Lista de festa criada com ID: {party_list.id}")

        # Adicionar itens à lista de festa
        logger.info("Adicionando itens à lista de festa...")
        party_items = [
            ShoppingItem(
                name="Bolo",
                quantity=1,
                category=CategoryEnum.FOOD,
                priority=PriorityEnum.HIGH,
                status=StatusEnum.PENDING,
                notes="Sabor chocolate",
                shopping_list_id=party_list.id
            ),
            ShoppingItem(
                name="Refrigerantes",
                quantity=6,
                category=CategoryEnum.FOOD,
                priority=PriorityEnum.HIGH,
                status=StatusEnum.PENDING,
                shopping_list_id=party_list.id
            ),
            ShoppingItem(
                name="Salgadinhos",
                quantity=4,
                category=CategoryEnum.FOOD,
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.PENDING,
                shopping_list_id=party_list.id
            ),
            ShoppingItem(
                name="Pratos Descartáveis",
                quantity=2,
                category=CategoryEnum.HOUSEHOLD,
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.PENDING,
                shopping_list_id=party_list.id
            ),
            ShoppingItem(
                name="Guardanapos",
                quantity=2,
                category=CategoryEnum.HOUSEHOLD,
                priority=PriorityEnum.LOW,
                status=StatusEnum.PENDING,
                shopping_list_id=party_list.id
            )
        ]
        db.add_all(party_items)
        logger.info(f"Adicionados {len(party_items)} itens à lista de festa")

        db.commit()
        logger.info("Dados de compras criados com sucesso!")

    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar dados de compras: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_shopping_data() 
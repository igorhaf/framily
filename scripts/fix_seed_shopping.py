import sys
import os
from pathlib import Path
from sqlalchemy import text
from datetime import datetime

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def create_shopping_lists():
    db = SessionLocal()
    try:
        # Limpar tabelas existentes
        db.execute(text('TRUNCATE TABLE shopping_items CASCADE; TRUNCATE TABLE shopping_lists CASCADE;'))
        db.commit()
        
        # Criar listas de compras
        result = db.execute(
            text("""
            INSERT INTO shopping_lists (name, description, created_at, updated_at) 
            VALUES 
                ('Compras do Mês', 'Lista de compras mensais para a casa', NOW(), NOW()),
                ('Compras da Semana', 'Lista de compras semanais', NOW(), NOW()),
                ('Compras Pessoais', 'Lista de compras pessoais', NOW(), NOW()),
                ('Compras da Casa', 'Lista de compras para a casa', NOW(), NOW())
            RETURNING id, name;
            """)
        )
        
        # Mapear os IDs das listas criadas
        lists = {name: id for id, name in result.fetchall()}
        print("Listas criadas:", lists)
        
        # Ver os tipos enums disponíveis
        result = db.execute(text("""
            SELECT t.typname, e.enumlabel
            FROM pg_type t
            JOIN pg_enum e ON t.oid = e.enumtypid
            ORDER BY t.typname, e.enumsortorder
        """))
        
        enums = {}
        for row in result:
            enum_type = row[0]
            enum_value = row[1]
            if enum_type not in enums:
                enums[enum_type] = []
            enums[enum_type].append(enum_value)
        
        print("\nEnum Types:")
        for enum_type, values in enums.items():
            print(f"{enum_type}: {', '.join(values)}")
        
        # Tentar criar alguns itens para a primeira lista
        try:
            db.execute(
                text("""
                INSERT INTO shopping_items 
                    (name, quantity, category, priority, status, notes, shopping_list_id, created_at, updated_at)
                VALUES
                    ('Arroz', 2, 'FOOD', 'HIGH', 'PENDING', 'Arroz integral', :list_id, NOW(), NOW())
                """),
                {"list_id": lists["Compras do Mês"]}
            )
            db.commit()
            print("Item adicionado com sucesso!")
            
            # Adicionar mais itens à Lista do Mês
            db.execute(
                text("""
                INSERT INTO shopping_items 
                    (name, quantity, category, priority, status, notes, shopping_list_id, created_at, updated_at)
                VALUES
                    ('Feijão', 2, 'FOOD', 'HIGH', 'PENDING', 'Feijão carioca', :list_id, NOW(), NOW()),
                    ('Óleo de Cozinha', 1, 'FOOD', 'MEDIUM', 'PENDING', 'Óleo de soja', :list_id, NOW(), NOW())
                """),
                {"list_id": lists["Compras do Mês"]}
            )
            db.commit()
            
            # Adicionar itens à Lista da Semana
            db.execute(
                text("""
                INSERT INTO shopping_items 
                    (name, quantity, category, priority, status, notes, shopping_list_id, created_at, updated_at)
                VALUES
                    ('Pão', 2, 'FOOD', 'HIGH', 'PENDING', 'Pão francês', :list_id, NOW(), NOW()),
                    ('Leite', 2, 'FOOD', 'HIGH', 'PENDING', 'Leite integral', :list_id, NOW(), NOW()),
                    ('Queijo', 1, 'FOOD', 'MEDIUM', 'PENDING', 'Queijo muçarela', :list_id, NOW(), NOW())
                """),
                {"list_id": lists["Compras da Semana"]}
            )
            db.commit()
            
            # Adicionar itens à Lista Pessoal
            db.execute(
                text("""
                INSERT INTO shopping_items 
                    (name, quantity, category, priority, status, notes, shopping_list_id, created_at, updated_at)
                VALUES
                    ('Shampoo', 1, 'HYGIENE', 'MEDIUM', 'PENDING', 'Shampoo para cabelos oleosos', :list_id, NOW(), NOW()),
                    ('Desodorante', 1, 'HYGIENE', 'MEDIUM', 'PENDING', 'Desodorante roll-on', :list_id, NOW(), NOW()),
                    ('Creme Dental', 1, 'HYGIENE', 'LOW', 'PENDING', 'Creme dental com flúor', :list_id, NOW(), NOW())
                """),
                {"list_id": lists["Compras Pessoais"]}
            )
            db.commit()
            
            # Adicionar itens à Lista da Casa
            db.execute(
                text("""
                INSERT INTO shopping_items 
                    (name, quantity, category, priority, status, notes, shopping_list_id, created_at, updated_at)
                VALUES
                    ('Detergente', 2, 'CLEANING', 'HIGH', 'PENDING', 'Detergente líquido', :list_id, NOW(), NOW()),
                    ('Papel Higiênico', 4, 'HOUSEHOLD', 'HIGH', 'PENDING', 'Pacote com 4 rolos', :list_id, NOW(), NOW()),
                    ('Sabão em Pó', 1, 'CLEANING', 'MEDIUM', 'PENDING', 'Sabão em pó para roupas', :list_id, NOW(), NOW())
                """),
                {"list_id": lists["Compras da Casa"]}
            )
            db.commit()
            
            print("Todos os itens adicionados com sucesso!")
            
        except Exception as e:
            db.rollback()
            print(f"Erro ao adicionar itens: {e}")
                
        print("Listas de compras criadas com sucesso!")
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar listas de compras: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_shopping_lists() 
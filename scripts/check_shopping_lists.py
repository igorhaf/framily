import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal
from app.crud.crud_shopping import shopping_list

def check_shopping_lists():
    db = SessionLocal()
    try:
        lists = shopping_list.get_multi(db)
        print(f"Total de listas: {len(lists)}")
        
        for lst in lists:
            print(f"Lista: {lst.name}")
            print(f"  ID: {lst.id}")
            print(f"  Descrição: {lst.description}")
            print(f"  Total de itens: {len(lst.items) if hasattr(lst, 'items') and lst.items is not None else 0}")
            
            if hasattr(lst, 'items') and lst.items:
                for item in lst.items:
                    print(f"    - Item: {item.name}, Categoria: {item.category}, Status: {item.status}")
            else:
                print("    Nenhum item encontrado")
            print()
    finally:
        db.close()

if __name__ == "__main__":
    check_shopping_lists() 
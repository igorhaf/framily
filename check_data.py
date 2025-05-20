import sys
import os
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud.crud_shopping import shopping_list, shopping_item

def check_data():
    db = SessionLocal()
    try:
        print("Verificando listas de compras:")
        lists = shopping_list.get_multi(db)
        print(f"Total de listas: {len(lists)}")
        
        for lst in lists:
            print(f"\nLista: {lst.name} (ID: {lst.id})")
            print(f"Descrição: {lst.description}")
            print(f"Possui atributo 'items'? {hasattr(lst, 'items')}")
            if hasattr(lst, 'items'):
                print(f"Tipo de lst.items: {type(lst.items)}")
                print(f"lst.items é None? {lst.items is None}")
                print(f"Total de itens: {len(lst.items) if lst.items is not None else 0}")
                
                if lst.items:
                    print("\nItens nesta lista:")
                    for item in lst.items:
                        print(f"  - {item.name} (ID: {item.id}, Categoria: {item.category}, Status: {item.status})")
                else:
                    print("Não há itens nesta lista (lst.items está vazio)")
            else:
                print("ERRO: O objeto lista não possui o atributo 'items'")
    finally:
        db.close()

if __name__ == "__main__":
    check_data() 
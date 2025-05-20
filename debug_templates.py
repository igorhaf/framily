import sys
import os
from app.db.session import SessionLocal
from app.crud.crud_shopping import shopping_list
from app.models.shopping import StatusEnum, CategoryEnum

# Simula o filtro enum_value do Jinja2
def enum_value(enum_obj):
    if hasattr(enum_obj, "value"):
        return enum_obj.value
    return enum_obj

def debug_templates():
    db = SessionLocal()
    try:
        lists = shopping_list.get_multi(db)
        print(f"Total de listas: {len(lists)}")
        
        for lst in lists:
            print(f"\nLista: {lst.name} (ID: {lst.id})")
            print(f"Total de itens: {len(lst.items) if hasattr(lst, 'items') and lst.items is not None else 0}")
            
            if hasattr(lst, 'items') and lst.items:
                print("\nTestando acesso aos itens da lista como feito no template:")
                
                # Simulando o uso de categoria|enum_value como no template
                for item in lst.items:
                    item_category = item.category
                    item_status = item.status
                    
                    print(f"  - Item: {item.name}")
                    print(f"    Categoria original: {item_category}, Tipo: {type(item_category)}")
                    print(f"    Categoria com enum_value: {enum_value(item_category)}")
                    print(f"    Status original: {item_status}, Tipo: {type(item_status)}")
                    print(f"    Status com enum_value: {enum_value(item_status)}")
                    
                    # Simulando as condições usadas no template
                    is_food = enum_value(item_category) == 'FOOD'
                    is_bought = enum_value(item_status) == 'BOUGHT'
                    
                    print(f"    É do tipo FOOD? {is_food}")
                    print(f"    Está com status BOUGHT? {is_bought}")
                    
                    # Verificar se categoria é realmente um enum
                    if not isinstance(item_category, CategoryEnum):
                        print(f"    ALERTA: item.category não é uma instância de CategoryEnum!")
                    
                    # Verificar se status é realmente um enum  
                    if not isinstance(item_status, StatusEnum):
                        print(f"    ALERTA: item.status não é uma instância de StatusEnum!")
            else:
                print("Não há itens nesta lista")
    finally:
        db.close()

if __name__ == "__main__":
    debug_templates() 
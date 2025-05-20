from app.db.session import SessionLocal
from app.models.shopping import ShoppingItem, StatusEnum

def check_status_values():
    db = SessionLocal()
    try:
        print("Valores de StatusEnum:")
        print(f"PENDING = {StatusEnum.PENDING.value}")
        print(f"BOUGHT = {StatusEnum.BOUGHT.value}")
        print(f"CANCELLED = {StatusEnum.CANCELLED.value}")
        
        print("\nVerificando itens no banco de dados:")
        items = db.query(ShoppingItem).all()
        print(f"Total de itens: {len(items)}")
        
        for item in items:
            print(f"Item: {item.name}")
            print(f"  Status (objeto): {item.status}")
            print(f"  Status (valor): {item.status.value}")
            print(f"  Status (nome): {item.status.name}")
            print(f"  Status == StatusEnum.PENDING? {item.status == StatusEnum.PENDING}")
            print(f"  Status == StatusEnum.BOUGHT? {item.status == StatusEnum.BOUGHT}")
            print(f"  Status.value == 'PENDING'? {item.status.value == 'PENDING'}")
            print(f"  Status.value == 'BOUGHT'? {item.status.value == 'BOUGHT'}")
    finally:
        db.close()

if __name__ == "__main__":
    check_status_values() 
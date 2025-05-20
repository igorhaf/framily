from app.models.shopping import StatusEnum, CategoryEnum
from app.routes import get_enum_value
import enum

def check_enum_values():
    print("Testando filtro enum_value com enums:")
    
    # Verificar enum StatusEnum
    print("\nStatusEnum:")
    for status in StatusEnum:
        print(f"{status.name} = {status.value}, enum_value: {get_enum_value(status)}")
    
    # Verificar enum CategoryEnum
    print("\nCategoryEnum:")
    for category in CategoryEnum:
        print(f"{category.name} = {category.value}, enum_value: {get_enum_value(category)}")
    
    # Testar comparações
    print("\nComparações:")
    print(f"StatusEnum.PURCHASED.value == 'BOUGHT'? {StatusEnum.PURCHASED.value == 'BOUGHT'}")
    print(f"get_enum_value(StatusEnum.PURCHASED) == 'BOUGHT'? {get_enum_value(StatusEnum.PURCHASED) == 'BOUGHT'}")
    
    # Simular expressões Jinja
    print("\nSimulando expressões Jinja:")
    status = StatusEnum.PURCHASED
    status_value = get_enum_value(status)
    print(f"StatusEnum.PURCHASED via enum_value: {status_value}")
    print(f"status_value == 'BOUGHT'? {status_value == 'BOUGHT'}")
    print(f"status_value == 'PENDING'? {status_value == 'PENDING'}")

if __name__ == "__main__":
    check_enum_values() 
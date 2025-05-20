from typing import List, Optional
from sqlalchemy.orm import Session, selectinload

from app.crud.base import CRUDBase
from app.models.shopping import ShoppingList, ShoppingItem
from app.schemas.shopping import ShoppingListCreate, ShoppingListUpdate, ShoppingItemCreate, ShoppingItemUpdate

class CRUDShoppingList(CRUDBase[ShoppingList, ShoppingListCreate, ShoppingListUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[ShoppingList]:
        return db.query(ShoppingList).filter(ShoppingList.name == name).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(ShoppingList)
            .options(selectinload(ShoppingList.items))
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDShoppingItem(CRUDBase[ShoppingItem, ShoppingItemCreate, ShoppingItemUpdate]):
    def get_by_list(self, db: Session, *, shopping_list_id: int, skip: int = 0, limit: int = 100) -> List[ShoppingItem]:
        return db.query(ShoppingItem).filter(ShoppingItem.shopping_list_id == shopping_list_id).offset(skip).limit(limit).all()
    
    def get_by_name(self, db: Session, *, shopping_list_id: int, name: str) -> Optional[ShoppingItem]:
        return db.query(ShoppingItem).filter(
            ShoppingItem.shopping_list_id == shopping_list_id,
            ShoppingItem.name == name
        ).first()

shopping_list = CRUDShoppingList(ShoppingList)
shopping_item = CRUDShoppingItem(ShoppingItem) 
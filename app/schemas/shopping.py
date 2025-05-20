from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.shopping import PriorityEnum, StatusEnum, CategoryEnum

class ShoppingItemBase(BaseModel):
    name: str
    quantity: int = 1
    category: CategoryEnum = CategoryEnum.OTHER
    priority: PriorityEnum = PriorityEnum.MEDIUM
    status: StatusEnum = StatusEnum.PENDING
    notes: Optional[str] = None

class ShoppingItemCreate(ShoppingItemBase):
    pass

class ShoppingItemUpdate(ShoppingItemBase):
    name: Optional[str] = None
    quantity: Optional[int] = None
    category: Optional[CategoryEnum] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None

class ShoppingItemInDB(ShoppingItemBase):
    id: int
    shopping_list_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ShoppingListBase(BaseModel):
    name: str
    description: Optional[str] = None

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingListUpdate(ShoppingListBase):
    name: Optional[str] = None

class ShoppingListInDB(ShoppingListBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[ShoppingItemInDB] = []

    class Config:
        from_attributes = True 
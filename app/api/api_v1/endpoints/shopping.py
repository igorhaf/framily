from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.shopping import (
    ShoppingListInDB,
    ShoppingListCreate,
    ShoppingListUpdate,
    ShoppingItemInDB,
    ShoppingItemCreate,
    ShoppingItemUpdate
)

router = APIRouter()

@router.get("/lists/", response_model=List[ShoppingListInDB])
def get_shopping_lists(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve shopping lists.
    """
    shopping_lists = crud.shopping_list.get_multi(db, skip=skip, limit=limit)
    return shopping_lists

@router.post("/lists/", response_model=ShoppingListInDB)
def create_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    shopping_list_in: ShoppingListCreate,
) -> Any:
    """
    Create new shopping list.
    """
    shopping_list = crud.shopping_list.get_by_name(db, name=shopping_list_in.name)
    if shopping_list:
        raise HTTPException(
            status_code=400,
            detail="A shopping list with this name already exists.",
        )
    shopping_list = crud.shopping_list.create(db, obj_in=shopping_list_in)
    return shopping_list

@router.get("/lists/{list_id}", response_model=ShoppingListInDB)
def get_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
) -> Any:
    """
    Get shopping list by ID.
    """
    shopping_list = crud.shopping_list.get(db, id=list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return shopping_list

@router.put("/lists/{list_id}", response_model=ShoppingListInDB)
def update_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
    shopping_list_in: ShoppingListUpdate,
) -> Any:
    """
    Update shopping list.
    """
    shopping_list = crud.shopping_list.get(db, id=list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    shopping_list = crud.shopping_list.update(db, db_obj=shopping_list, obj_in=shopping_list_in)
    return shopping_list

@router.delete("/lists/{list_id}", response_model=ShoppingListInDB)
def delete_shopping_list(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
) -> Any:
    """
    Delete shopping list.
    """
    shopping_list = crud.shopping_list.get(db, id=list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    shopping_list = crud.shopping_list.remove(db, id=list_id)
    return shopping_list

@router.get("/lists/{list_id}/items/", response_model=List[ShoppingItemInDB])
def get_shopping_items(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get items from a shopping list.
    """
    items = crud.shopping_item.get_by_list(db, shopping_list_id=list_id, skip=skip, limit=limit)
    return items

@router.post("/lists/{list_id}/items/", response_model=ShoppingItemInDB)
def create_shopping_item(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
    item_in: ShoppingItemCreate,
) -> Any:
    """
    Create new shopping item.
    """
    shopping_list = crud.shopping_list.get(db, id=list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    item = crud.shopping_item.get_by_name(db, shopping_list_id=list_id, name=item_in.name)
    if item:
        raise HTTPException(
            status_code=400,
            detail="An item with this name already exists in this list.",
        )
    item_in.shopping_list_id = list_id
    item = crud.shopping_item.create(db, obj_in=item_in)
    return item

@router.put("/lists/{list_id}/items/{item_id}", response_model=ShoppingItemInDB)
def update_shopping_item(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
    item_id: int,
    item_in: ShoppingItemUpdate,
) -> Any:
    """
    Update shopping item.
    """
    item = crud.shopping_item.get(db, id=item_id)
    if not item or item.shopping_list_id != list_id:
        raise HTTPException(status_code=404, detail="Shopping item not found")
    item = crud.shopping_item.update(db, db_obj=item, obj_in=item_in)
    return item

@router.delete("/lists/{list_id}/items/{item_id}", response_model=ShoppingItemInDB)
def delete_shopping_item(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
    item_id: int,
) -> Any:
    """
    Delete shopping item.
    """
    item = crud.shopping_item.get(db, id=item_id)
    if not item or item.shopping_list_id != list_id:
        raise HTTPException(status_code=404, detail="Shopping item not found")
    item = crud.shopping_item.remove(db, id=item_id)
    return item 
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.api import deps
from app.crud import shopping_list
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi import Depends
import enum

templates = Jinja2Templates(directory="templates")

# Filtros personalizados para Jinja2
def get_enum_value(enum_obj):
    """Retorna o valor de um objeto Enum"""
    if isinstance(enum_obj, enum.Enum):
        return enum_obj.value
    return enum_obj

templates.env.filters["enum_value"] = get_enum_value

pages_router = APIRouter()

@pages_router.get("/calendar")
async def calendar_page(request: Request):
    return templates.TemplateResponse(
        "calendar.html",
        {"request": request, "title": "Calendar"}
    )

@pages_router.get("/tasks")
async def tasks_page(request: Request):
    return templates.TemplateResponse(
        "tasks.html",
        {"request": request, "title": "Tasks"}
    )

@pages_router.get("/finances")
async def finances_page(request: Request):
    return templates.TemplateResponse(
        "finances.html",
        {"request": request, "title": "Finances"}
    )

@pages_router.get("/health")
async def health_page(request: Request):
    return templates.TemplateResponse(
        "health.html",
        {"request": request, "title": "Health"}
    )

@pages_router.get("/shopping")
async def shopping_page(request: Request):
    db = next(deps.get_db())
    shopping_lists = shopping_list.get_multi(db)
    # Debug para entender o que está chegando ao template
    print(f"Total de listas: {len(shopping_lists)}")
    for lst in shopping_lists:
        print(f"Lista {lst.id}: {lst.name}")
        print(f"  Tipo de lst.items: {type(lst.items)}")
        print(f"  Total de itens: {len(lst.items) if hasattr(lst, 'items') else 0}")
        if hasattr(lst, 'items') and lst.items:
            for item in lst.items:
                print(f"  - Item: {item.name}, Status: {item.status}, Status.name: {item.status.name}")
    
    return templates.TemplateResponse(
        "shopping.html",
        {"request": request, "title": "Shopping", "shopping_lists": shopping_lists}
    )

@pages_router.get("/shopping_debug", response_class=HTMLResponse)
async def shopping_debug(request: Request, db: Session = Depends(deps.get_db)):
    """Página de debug para visualização das listas de compras."""
    lists = shopping_list.get_multi(db=db)
    return templates.TemplateResponse(
        "shopping_debug.html",
        {"request": request, "shopping_lists": lists}
    )

@pages_router.get("/shopping_test", response_class=HTMLResponse)
async def shopping_test(request: Request, db: Session = Depends(deps.get_db)):
    """Página simplificada para testar o acesso aos itens das listas de compras."""
    lists = shopping_list.get_multi(db=db)
    return templates.TemplateResponse(
        "shopping_test.html",
        {"request": request, "shopping_lists": lists}
    ) 
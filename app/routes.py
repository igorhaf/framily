from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from app.api import deps
from app.crud import shopping_list
from app.crud.crud_education import education_institution, education_event, education_expense
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi import Depends
import enum
from app.schemas.shopping import ShoppingListInDB
from app.schemas.education import EducationEventInDB, EducationExpenseInDB

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
    try:
        db = next(deps.get_db())
        shopping_lists_db = shopping_list.get_multi(db)
        shopping_lists = [ShoppingListInDB.model_validate(lst) for lst in shopping_lists_db]

        # Contadores para os cards
        total_items = 0
        pending_items = 0
        bought_items = 0

        for lst in shopping_lists:
            for item in lst.items:
                total_items += 1
                if item.status.value == "PENDING":
                    pending_items += 1
                elif item.status.value == "BOUGHT":
                    bought_items += 1

        return templates.TemplateResponse(
            "shopping.html",
            {
                "request": request,
                "title": "Shopping",
                "shopping_lists": shopping_lists,
                "total_items": total_items,
                "pending_items": pending_items,
                "bought_items": bought_items,
            }
        )
    except Exception as e:
        print(f"Erro na página de shopping: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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

@pages_router.get("/education")
async def education_page(request: Request):
    db = next(deps.get_db())
    institutions = education_institution.get_multi(db)
    events = sorted(education_event.get_multi(db), key=lambda e: e.data_hora)
    # Converter eventos para schema Pydantic
    events_schema = [EducationEventInDB.model_validate(event) for event in events]
    expenses = sorted(education_expense.get_multi(db), key=lambda e: e.data, reverse=True)
    # Converter despesas para schema Pydantic
    expenses_schema = [EducationExpenseInDB.model_validate(expense) for expense in expenses]
    return templates.TemplateResponse(
        "education.html",
        {
            "request": request,
            "title": "Educação",
            "institutions": institutions,
            "events": events_schema,
            "expenses": expenses_schema,
        }
    )

# Update the login_page route to include the request parameter
@pages_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request}) 
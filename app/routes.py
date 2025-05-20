from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.api import deps
from app.crud import shopping_list

templates = Jinja2Templates(directory="templates")
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
    return templates.TemplateResponse(
        "shopping.html",
        {"request": request, "title": "Shopping", "shopping_lists": shopping_lists}
    ) 
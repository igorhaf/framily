from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.routes import pages_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Inicializa o banco de dados
init_db()

# Monta os arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura os templates
templates = Jinja2Templates(directory="templates")

# Inclui as rotas da API
app.include_router(api_router, prefix=settings.API_V1_STR)

# Inclui as rotas das páginas
app.include_router(pages_router)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Dashboard"}
    )

# ... resto do código ... 
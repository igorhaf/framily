from fastapi import APIRouter
from app.api.api_v1.endpoints.tasks import router as tasks_router
from app.api.api_v1.endpoints.finance import router as finance_router
from app.api.api_v1.endpoints.health import router as health_router
from app.api.api_v1.endpoints.calendar import router as calendar_router
from app.api.api_v1.endpoints.whatsapp import router as whatsapp_router
from app.api.api_v1.endpoints.shopping import router as shopping_router

api_router = APIRouter()

# Task management
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

# Financial management
api_router.include_router(finance_router, prefix="/finance", tags=["finance"])

# Health tracking
api_router.include_router(health_router, prefix="/health", tags=["health"])

# Calendar management
api_router.include_router(calendar_router, prefix="/calendar", tags=["calendar"])

# WhatsApp management
api_router.include_router(whatsapp_router, prefix="/whatsapp", tags=["whatsapp"])

# Shopping management
api_router.include_router(shopping_router, prefix="/shopping", tags=["shopping"]) 
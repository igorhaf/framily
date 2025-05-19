from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    tasks,
    finance,
    health,
    calendar
)

api_router = APIRouter()

# Import routers from endpoints
from app.api.api_v1.endpoints.tasks import router as tasks_router
from app.api.api_v1.endpoints.finance import router as finance_router
from app.api.api_v1.endpoints.health import router as health_router
from app.api.api_v1.endpoints.calendar import router as calendar_router

# Task management
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

# Financial management
api_router.include_router(finance_router, prefix="/finance", tags=["finance"])

# Health tracking
api_router.include_router(health_router, prefix="/health", tags=["health"])

# Calendar management
api_router.include_router(calendar_router, prefix="/calendar", tags=["calendar"]) 
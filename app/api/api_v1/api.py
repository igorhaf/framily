from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    tasks,
    finance,
    health,
    health_dashboard
)

api_router = APIRouter()

# Import routers from endpoints
from app.api.api_v1.endpoints.tasks import router as tasks_router
from app.api.api_v1.endpoints.finance import router as finance_router
from app.api.api_v1.endpoints.health import router as health_router
from app.api.api_v1.endpoints.health_dashboard import router as health_dashboard_router

# Task management
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

# Financial management
api_router.include_router(finance_router, prefix="/finance", tags=["finance"])

# Health tracking
api_router.include_router(health_router, prefix="/health", tags=["health"])

# Health dashboard
api_router.include_router(health_dashboard_router, prefix="/health-dashboard", tags=["health-dashboard"]) 
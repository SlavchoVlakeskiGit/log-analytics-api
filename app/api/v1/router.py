from fastapi import APIRouter

from app.api.v1.endpoints import analytics, health, logs

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(logs.router)
api_router.include_router(analytics.router)
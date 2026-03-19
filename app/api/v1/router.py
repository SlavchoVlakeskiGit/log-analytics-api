from fastapi import APIRouter

from app.api.v1.endpoints import analytics, auth, health, logs

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(logs.router)
api_router.include_router(analytics.router)
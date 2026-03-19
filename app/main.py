from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API for ingesting, querying, and analyzing application logs."
)

app.include_router(api_router, prefix=settings.api_v1_str)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}
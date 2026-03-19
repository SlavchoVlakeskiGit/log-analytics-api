from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API for ingesting, querying, and analyzing application logs."
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}
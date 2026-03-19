from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "REST API for ingesting, querying, and analyzing operational log data "
        "from multiple services."
    ),
    contact={
        "name": "Portfolio Project",
    },
    openapi_tags=[
        {"name": "Health", "description": "Service health and availability checks."},
        {"name": "Auth", "description": "Authentication and JWT access token generation."},
        {"name": "Logs", "description": "Log ingestion, retrieval, filtering, pagination, and sorting."},
        {"name": "Analytics", "description": "Aggregated insights for log monitoring and investigation."},
    ],
)

app.include_router(api_router, prefix=settings.api_v1_str)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}
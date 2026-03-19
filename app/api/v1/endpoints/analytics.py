from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.log_repository import LogRepository
from app.schemas.analytics import (
    AnalyticsOverview,
    SeverityDistributionItem,
    SourceDistributionItem,
)
from app.services.log_service import LogService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/overview",
    response_model=AnalyticsOverview,
    summary="Get log analytics overview",
)
def get_overview(db: Session = Depends(get_db)) -> AnalyticsOverview:
    repository = LogRepository(db)
    service = LogService(repository)
    return service.get_overview()


@router.get(
    "/severity-distribution",
    response_model=list[SeverityDistributionItem],
    summary="Get log counts grouped by severity",
)
def get_severity_distribution(
    db: Session = Depends(get_db),
) -> list[SeverityDistributionItem]:
    repository = LogRepository(db)
    service = LogService(repository)
    return service.get_severity_distribution()


@router.get(
    "/source-distribution",
    response_model=list[SourceDistributionItem],
    summary="Get log counts grouped by source",
)
def get_source_distribution(
    db: Session = Depends(get_db),
) -> list[SourceDistributionItem]:
    repository = LogRepository(db)
    service = LogService(repository)
    return service.get_source_distribution()
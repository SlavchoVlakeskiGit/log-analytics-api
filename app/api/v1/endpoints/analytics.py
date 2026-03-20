from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.repositories.log_repository import LogRepository
from app.schemas.analytics import (
    AlertItem,
    AnalyticsOverview,
    ErrorRateResponse,
    ErrorTrendItem,
    SeverityDistributionItem,
    SourceDistributionItem,
    SuspiciousActivityItem,
    TopFailingServiceItem,
)
from app.services.log_service import LogService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/overview",
    response_model=AnalyticsOverview,
    summary="Get analytics overview",
)
def get_overview(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> AnalyticsOverview:
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
    user: dict = Depends(get_current_user),
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
    user: dict = Depends(get_current_user),
) -> list[SourceDistributionItem]:
    repository = LogRepository(db)
    service = LogService(repository)
    return service.get_source_distribution()


@router.get(
    "/error-trends",
    response_model=list[ErrorTrendItem],
    summary="Get daily count of error and critical logs",
)
def get_error_trends(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> list[ErrorTrendItem]:
    repository = LogRepository(db)
    service = LogService(repository)
    return service.get_error_trends()


@router.get(
    "/top-failing-services",
    response_model=list[TopFailingServiceItem],
    summary="Get services with the highest number of errors",
)
def get_top_failing_services(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> list[TopFailingServiceItem]:
    repository = LogRepository(db)
    service = LogService(repository)
    return service.get_top_failing_services()


@router.get(
    "/error-rate",
    response_model=ErrorRateResponse,
    summary="Get percentage of logs classified as errors",
)
def get_error_rate(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> ErrorRateResponse:
    repository = LogRepository(db)
    service = LogService(repository)
    return service.get_error_rate()


@router.get(
    "/suspicious-activity",
    response_model=list[SuspiciousActivityItem],
    summary="Get suspicious activity based on repeated failed logins",
)
def get_suspicious_activity(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> list[SuspiciousActivityItem]:
    repository = LogRepository(db)
    service = LogService(repository)
    return service.get_suspicious_activity()


@router.get(
    "/alerts",
    response_model=list[AlertItem],
    summary="Get alert conditions based on recent log activity",
)
def get_alerts(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> list[AlertItem]:
    repository = LogRepository(db)
    service = LogService(repository)
    return service.get_alerts()
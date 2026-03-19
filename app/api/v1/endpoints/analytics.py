from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.repositories.log_repository import LogRepository
from app.schemas.analytics import (
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
    from sqlalchemy import func
    from app.models.log_entry import LogEntry

    results = (
        db.query(
            func.date(LogEntry.timestamp).label("date"),
            func.count().label("count"),
        )
        .filter(LogEntry.severity.in_(["ERROR", "CRITICAL"]))
        .group_by(func.date(LogEntry.timestamp))
        .order_by(func.date(LogEntry.timestamp))
        .all()
    )

    return [
        ErrorTrendItem(date=str(row.date), count=row.count)
        for row in results
    ]


@router.get(
    "/top-failing-services",
    response_model=list[TopFailingServiceItem],
    summary="Get services with the highest number of errors",
)
def get_top_failing_services(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> list[TopFailingServiceItem]:
    from sqlalchemy import func
    from app.models.log_entry import LogEntry

    results = (
        db.query(
            LogEntry.source,
            func.count().label("error_count"),
        )
        .filter(LogEntry.severity.in_(["ERROR", "CRITICAL"]))
        .group_by(LogEntry.source)
        .order_by(func.count().desc())
        .limit(5)
        .all()
    )

    return [
        TopFailingServiceItem(source=row.source, error_count=row.error_count)
        for row in results
    ]


@router.get(
    "/error-rate",
    response_model=ErrorRateResponse,
    summary="Get percentage of logs classified as errors",
)
def get_error_rate(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> ErrorRateResponse:
    from sqlalchemy import func
    from app.models.log_entry import LogEntry

    total = db.query(func.count(LogEntry.id)).scalar() or 0
    errors = (
        db.query(func.count(LogEntry.id))
        .filter(LogEntry.severity.in_(["ERROR", "CRITICAL"]))
        .scalar()
        or 0
    )

    error_rate = (errors / total * 100) if total else 0.0

    return ErrorRateResponse(
        total_logs=total,
        error_logs=errors,
        error_rate_percent=round(error_rate, 2),
    )


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
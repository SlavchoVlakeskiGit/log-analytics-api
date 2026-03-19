from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.log_repository import LogRepository
from app.schemas.log_entry import LogEntryCreate, LogEntryResponse
from app.services.log_service import LogService
from app.schemas.log_entry import LogEntryQuery

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.post(
    "",
    response_model=LogEntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new log entry",
)
def create_log(
    payload: LogEntryCreate,
    db: Session = Depends(get_db),
) -> LogEntryResponse:
    repository = LogRepository(db)
    service = LogService(repository)
    created_log = service.create_log(payload)
    return created_log


@router.get(
    "/{log_id}",
    response_model=LogEntryResponse,
    summary="Get a log entry by ID",
)
def get_log_by_id(
    log_id: int,
    db: Session = Depends(get_db),
) -> LogEntryResponse:
    repository = LogRepository(db)
    service = LogService(repository)
    log_entry = service.get_log_by_id(log_id)

    if log_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log entry not found",
        )

    return log_entry

@router.get(
    "",
    response_model=list[LogEntryResponse],
    summary="List logs with filtering and pagination",
)
def list_logs(
    severity: str | None = None,
    source: str | None = None,
    environment: str | None = None,
    event_type: str | None = None,
    keyword: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    skip: int = 0,
    limit: int = 50,
    sort_by: str = "timestamp",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
):
    query_params = LogEntryQuery(
        severity=severity,
        source=source,
        environment=environment,
        event_type=event_type,
        keyword=keyword,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    repository = LogRepository(db)
    service = LogService(repository)

    return service.list_logs(query_params)
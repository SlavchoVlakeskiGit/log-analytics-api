from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.log_repository import LogRepository
from app.schemas.log_entry import LogEntryCreate, LogEntryResponse
from app.services.log_service import LogService

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
from sqlalchemy.orm import Session

from app.models.log_entry import LogEntry
from app.schemas.log_entry import LogEntryCreate


class LogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, log_data: LogEntryCreate) -> LogEntry:
        log_entry = LogEntry(
            timestamp=log_data.timestamp,
            source=log_data.source,
            host=log_data.host,
            severity=log_data.severity.value,
            message=log_data.message,
            environment=log_data.environment.value,
            event_type=log_data.event_type,
            status_code=log_data.status_code,
            ip_address=log_data.ip_address,
            user_id=log_data.user_id,
            request_id=log_data.request_id,
        )
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)
        return log_entry

    def get_by_id(self, log_id: int) -> LogEntry | None:
        return self.db.query(LogEntry).filter(LogEntry.id == log_id).first()
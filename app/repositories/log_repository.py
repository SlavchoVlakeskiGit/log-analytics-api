from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.log_entry import LogEntry
from app.schemas.log_entry import LogEntryCreate, LogEntryQuery


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

    def list_logs(self, query_params: LogEntryQuery) -> list[LogEntry]:
        query = self.db.query(LogEntry)

        if query_params.severity:
            query = query.filter(LogEntry.severity == query_params.severity.value)

        if query_params.source:
            query = query.filter(LogEntry.source == query_params.source)

        if query_params.environment:
            query = query.filter(LogEntry.environment == query_params.environment.value)

        if query_params.event_type:
            query = query.filter(LogEntry.event_type == query_params.event_type)

        if query_params.keyword:
            query = query.filter(LogEntry.message.ilike(f"%{query_params.keyword}%"))

        if query_params.start_date:
            query = query.filter(LogEntry.timestamp >= query_params.start_date)

        if query_params.end_date:
            query = query.filter(LogEntry.timestamp <= query_params.end_date)

        sort_column = getattr(LogEntry, query_params.sort_by, LogEntry.timestamp)

        if query_params.sort_order == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        return query.offset(query_params.skip).limit(query_params.limit).all()
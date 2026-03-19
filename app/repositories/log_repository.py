from sqlalchemy import asc, desc, func
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

    def get_overview(self) -> dict:
        total_logs = self.db.query(func.count(LogEntry.id)).scalar() or 0
        total_errors = (
            self.db.query(func.count(LogEntry.id))
            .filter(LogEntry.severity == "ERROR")
            .scalar()
            or 0
        )
        total_warnings = (
            self.db.query(func.count(LogEntry.id))
            .filter(LogEntry.severity == "WARNING")
            .scalar()
            or 0
        )

        top_source_row = (
            self.db.query(LogEntry.source, func.count(LogEntry.id).label("count"))
            .group_by(LogEntry.source)
            .order_by(desc("count"))
            .first()
        )

        most_recent_timestamp = self.db.query(func.max(LogEntry.timestamp)).scalar()

        return {
            "total_logs": total_logs,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "top_source": top_source_row[0] if top_source_row else None,
            "most_recent_log_timestamp": most_recent_timestamp,
        }

    def get_severity_distribution(self) -> list[dict]:
        rows = (
            self.db.query(LogEntry.severity, func.count(LogEntry.id).label("count"))
            .group_by(LogEntry.severity)
            .order_by(desc("count"))
            .all()
        )

        return [{"severity": row[0], "count": row[1]} for row in rows]

    def get_source_distribution(self) -> list[dict]:
        rows = (
            self.db.query(LogEntry.source, func.count(LogEntry.id).label("count"))
            .group_by(LogEntry.source)
            .order_by(desc("count"))
            .all()
        )

        return [{"source": row[0], "count": row[1]} for row in rows]

    def get_error_trends(self) -> list[dict]:
        rows = (
            self.db.query(
                func.date(LogEntry.timestamp).label("date"),
                func.count(LogEntry.id).label("count"),
            )
            .filter(LogEntry.severity == "ERROR")
            .group_by(func.date(LogEntry.timestamp))
            .order_by(desc("date"))
            .all()
        )

        return [{"date": row[0], "count": row[1]} for row in rows]

    def get_suspicious_activity(self) -> list[dict]:
        rows = (
            self.db.query(LogEntry.ip_address, func.count(LogEntry.id).label("count"))
            .filter(
                LogEntry.severity == "ERROR",
                LogEntry.event_type == "login_failed",
                LogEntry.ip_address.isnot(None),
            )
            .group_by(LogEntry.ip_address)
            .having(func.count(LogEntry.id) >= 3)
            .order_by(desc("count"))
            .all()
        )

        return [
            {
                "description": f"Repeated failed logins from IP {row[0]}",
                "count": row[1],
            }
            for row in rows
        ]
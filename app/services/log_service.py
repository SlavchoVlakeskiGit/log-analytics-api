from app.repositories.log_repository import LogRepository
from app.schemas.log_entry import LogEntryCreate, LogEntryQuery


class LogService:
    def __init__(self, repository: LogRepository) -> None:
        self.repository = repository

    def create_log(self, log_data: LogEntryCreate):
        return self.repository.create(log_data)

    def get_log_by_id(self, log_id: int):
        return self.repository.get_by_id(log_id)

    def list_logs(self, query_params: LogEntryQuery):
        return self.repository.list_logs(query_params)

    def get_overview(self):
        return self.repository.get_overview()

    def get_severity_distribution(self):
        return self.repository.get_severity_distribution()

    def get_source_distribution(self):
        return self.repository.get_source_distribution()

    def get_error_trends(self):
        return self.repository.get_error_trends()

    def get_suspicious_activity(self):
        return self.repository.get_suspicious_activity()
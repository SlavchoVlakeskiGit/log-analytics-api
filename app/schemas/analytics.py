from datetime import date, datetime

from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_logs: int
    total_errors: int
    total_warnings: int
    top_source: str | None
    most_recent_log_timestamp: datetime | None


class SeverityDistributionItem(BaseModel):
    severity: str
    count: int


class SourceDistributionItem(BaseModel):
    source: str
    count: int


class ErrorTrendItem(BaseModel):
    date: date
    count: int


class SuspiciousActivityItem(BaseModel):
    description: str
    count: int
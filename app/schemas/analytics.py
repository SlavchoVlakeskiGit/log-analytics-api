from datetime import datetime

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
    date: str
    count: int


class SuspiciousActivityItem(BaseModel):
    description: str
    count: int


class TopFailingServiceItem(BaseModel):
    source: str
    error_count: int


class ErrorRateResponse(BaseModel):
    total_logs: int
    error_logs: int
    error_rate_percent: float


class AlertItem(BaseModel):
    type: str
    severity: str
    count: int
    window_minutes: int
    message: str
    source: str | None = None
    ip_address: str | None = None
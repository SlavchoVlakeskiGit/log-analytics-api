from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.log_entry import EnvironmentType, SeverityLevel


class LogEntryBase(BaseModel):
    timestamp: datetime
    source: str = Field(..., min_length=2, max_length=100)
    host: str = Field(..., min_length=2, max_length=100)
    severity: SeverityLevel
    message: str = Field(..., min_length=3)
    environment: EnvironmentType
    event_type: str = Field(..., min_length=2, max_length=50)
    status_code: int | None = None
    ip_address: str | None = None
    user_id: str | None = None
    request_id: str | None = None


class LogEntryCreate(LogEntryBase):
    pass


class LogEntryResponse(LogEntryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LogEntryQuery(BaseModel):
    severity: SeverityLevel | None = None
    source: str | None = None
    environment: EnvironmentType | None = None
    event_type: str | None = None
    keyword: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    skip: int = 0
    limit: int = 50
    sort_by: str = "timestamp"
    sort_order: str = "desc"
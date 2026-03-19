import os
import random
import sys
from datetime import UTC, datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.log_entry import LogEntry

SEVERITIES = ["INFO", "WARNING", "ERROR", "CRITICAL"]
ENVIRONMENTS = ["prod", "staging"]
IPS = [
    "192.168.1.15",
    "192.168.1.20",
    "10.0.0.21",
    "10.0.0.35",
    "172.16.0.8",
]
USERS = ["admin", "user-101", "user-202", "customer-42", None]


def build_log(index: int) -> LogEntry:
    event_type = random.choice(
        [
            "login_success",
            "login_failed",
            "payment_processed",
            "api_error",
            "db_timeout",
            "service_restart",
        ]
    )

    if event_type == "login_failed":
        severity = "ERROR"
        message = "Failed login attempt for user admin"
        status_code = 401
        ip_address = random.choice(
            ["192.168.1.15", "192.168.1.15", "192.168.1.15", "10.0.0.21"]
        )
        user_id = "admin"
        source = "auth-service"
        host = "srv-auth-01"
    elif event_type == "api_error":
        severity = random.choice(["ERROR", "CRITICAL"])
        message = "API request returned server error"
        status_code = random.choice([500, 502, 503, 504])
        ip_address = random.choice(IPS)
        user_id = random.choice(USERS)
        source = "api-gateway"
        host = "srv-api-01"
    elif event_type == "db_timeout":
        severity = "ERROR"
        message = "Database query timeout detected"
        status_code = 504
        ip_address = None
        user_id = None
        source = "db-service"
        host = "srv-db-01"
    elif event_type == "service_restart":
        severity = "WARNING"
        message = "Service restarted after health check failure"
        status_code = None
        ip_address = None
        user_id = None
        source = "worker-service"
        host = "srv-worker-01"
    elif event_type == "payment_processed":
        severity = "INFO"
        message = "Payment processed successfully"
        status_code = 200
        ip_address = random.choice(IPS)
        user_id = random.choice(["customer-42", "user-202"])
        source = "billing-service"
        host = "srv-bill-01"
    else:
        severity = "INFO"
        message = "User login successful"
        status_code = 200
        ip_address = random.choice(IPS)
        user_id = random.choice(["user-101", "user-202", "admin"])
        source = "auth-service"
        host = "srv-auth-01"

    timestamp = datetime.now(UTC) - timedelta(
        hours=random.randint(0, 120),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )

    return LogEntry(
        timestamp=timestamp,
        source=source,
        host=host,
        severity=severity,
        message=message,
        environment=random.choice(ENVIRONMENTS),
        event_type=event_type,
        status_code=status_code,
        ip_address=ip_address,
        user_id=user_id,
        request_id=f"req-{1000 + index}",
        created_at=datetime.now(UTC),
    )


def seed_logs(count: int = 250) -> None:
    db = SessionLocal()
    try:
        logs = [build_log(i) for i in range(count)]
        db.add_all(logs)
        db.commit()
        print(f"Inserted {count} log entries.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_logs()
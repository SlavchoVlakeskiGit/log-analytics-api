from datetime import UTC, datetime


def test_create_log_entry(client) -> None:
    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "source": "auth-service",
        "host": "srv-auth-01",
        "severity": "ERROR",
        "message": "Failed login attempt for user admin",
        "environment": "prod",
        "event_type": "login_failed",
        "status_code": 401,
        "ip_address": "192.168.1.10",
        "user_id": "admin",
        "request_id": "req-1001",
    }

    response = client.post("/api/v1/logs", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["source"] == "auth-service"
    assert body["severity"] == "ERROR"
    assert body["event_type"] == "login_failed"
    assert "id" in body


def test_get_log_entry_not_found(client) -> None:
    response = client.get("/api/v1/logs/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Log entry not found"
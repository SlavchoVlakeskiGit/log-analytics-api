from datetime import UTC, datetime


def get_token(client) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_create_log_entry(client) -> None:
    token = get_token(client)

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

    response = client.post(
        "/api/v1/logs",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["source"] == "auth-service"
    assert body["severity"] == "ERROR"
    assert body["event_type"] == "login_failed"
    assert "id" in body


def test_get_log_entry_not_found(client) -> None:
    token = get_token(client)

    response = client.get(
        "/api/v1/logs/999999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Log entry not found"
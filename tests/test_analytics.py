from datetime import UTC, datetime


def get_token(client) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def create_log(client, token: str, payload: dict) -> None:
    response = client.post(
        "/api/v1/logs",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_analytics_overview(client) -> None:
    token = get_token(client)
    response = client.get(
        "/api/v1/analytics/overview",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "total_logs" in body
    assert "total_errors" in body
    assert "total_warnings" in body
    assert "top_source" in body
    assert "most_recent_log_timestamp" in body


def test_severity_distribution(client) -> None:
    token = get_token(client)
    response = client.get(
        "/api/v1/analytics/severity-distribution",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_source_distribution(client) -> None:
    token = get_token(client)
    response = client.get(
        "/api/v1/analytics/source-distribution",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_error_trends(client) -> None:
    token = get_token(client)
    response = client.get(
        "/api/v1/analytics/error-trends",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_top_failing_services(client) -> None:
    token = get_token(client)
    response = client.get(
        "/api/v1/analytics/top-failing-services",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_error_rate(client) -> None:
    token = get_token(client)
    response = client.get(
        "/api/v1/analytics/error-rate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "total_logs" in body
    assert "error_logs" in body
    assert "error_rate_percent" in body


def test_suspicious_activity(client) -> None:
    token = get_token(client)
    response = client.get(
        "/api/v1/analytics/suspicious-activity",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_alerts_endpoint_returns_error_spike(client) -> None:
    token = get_token(client)
    source_name = "alert-test-auth-service"

    for index in range(5):
        create_log(
            client,
            token,
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "source": source_name,
                "host": "srv-auth-01",
                "severity": "ERROR",
                "message": f"Authentication error {index}",
                "environment": "prod",
                "event_type": "auth_error",
                "status_code": 500,
                "ip_address": f"10.10.0.{index}",
                "user_id": None,
                "request_id": f"err-req-{index}",
            },
        )

    response = client.get(
        "/api/v1/analytics/alerts",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()

    assert any(
        alert["type"] == "error_spike" and alert["source"] == source_name
        for alert in body
    )


def test_alerts_endpoint_returns_failed_login_alert(client) -> None:
    token = get_token(client)
    test_ip = "203.0.113.25"

    for index in range(3):
        create_log(
            client,
            token,
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "source": "auth-service",
                "host": "srv-auth-02",
                "severity": "ERROR",
                "message": f"Failed login attempt {index}",
                "environment": "prod",
                "event_type": "login_failed",
                "status_code": 401,
                "ip_address": test_ip,
                "user_id": "demo-user",
                "request_id": f"login-req-{index}",
            },
        )

    response = client.get(
        "/api/v1/analytics/alerts",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()

    assert any(
        alert["type"] == "repeated_failed_logins"
        and alert["ip_address"] == test_ip
        for alert in body
    )
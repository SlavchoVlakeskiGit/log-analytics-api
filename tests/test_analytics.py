def get_token(client) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


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
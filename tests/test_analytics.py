def test_analytics_overview(client) -> None:
    response = client.get("/api/v1/analytics/overview")
    assert response.status_code == 200

    body = response.json()
    assert "total_logs" in body
    assert "total_errors" in body
    assert "total_warnings" in body
    assert "top_source" in body
    assert "most_recent_log_timestamp" in body


def test_severity_distribution(client) -> None:
    response = client.get("/api/v1/analytics/severity-distribution")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_source_distribution(client) -> None:
    response = client.get("/api/v1/analytics/source-distribution")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
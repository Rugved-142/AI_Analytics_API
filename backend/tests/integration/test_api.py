from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics_endpoint() -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "request_duration_seconds" in response.text


def test_timeseries_endpoint() -> None:
    response = client.get("/api/v1/analytics/timeseries", params={"granularity": "1h"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["granularity"] == "1h"
    assert "pagination" in payload

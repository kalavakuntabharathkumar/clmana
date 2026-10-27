from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_is_available():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["mode"] == "synthetic-demo"

def test_score_returns_bounded_demo_score():
    response = client.post("/score", json={
        "amount": 2500.0,
        "provider_claim_count_30d": 40,
        "days_since_service": 10
    })
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["anomaly_score"] <= 1
    assert "warning" in body

def test_summary_requires_secret_when_not_configured(monkeypatch):
    monkeypatch.delenv("DEMO_JWT_SECRET", raising=False)
    response = client.post("/summarize", json={
        "claim_id": "DEMO-1001", "anomaly_score": 0.8, "signals": ["amount outlier"]
    })
    assert response.status_code == 503

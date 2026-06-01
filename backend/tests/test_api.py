import importlib
from fastapi.testclient import TestClient


def build_client():
    import app.core.config as config
    importlib.reload(config)
    import app.main as main
    importlib.reload(main)
    return TestClient(main.app)


def test_health_endpoint():
    client = build_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

import os
import importlib
from fastapi.testclient import TestClient


def build_client():
    os.environ.setdefault("SECRET_KEY", "test")
    os.environ.setdefault("POSTGRES_HOST", "localhost")
    os.environ.setdefault("POSTGRES_PORT", "5432")
    os.environ.setdefault("POSTGRES_DB", "rl_hedging")
    os.environ.setdefault("POSTGRES_USER", "rl_user")
    os.environ.setdefault("POSTGRES_PASSWORD", "rl_password")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
    os.environ.setdefault("CELERY_BROKER_URL", "redis://localhost:6379/1")
    os.environ.setdefault("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")
    os.environ.setdefault("MLFLOW_TRACKING_URI", "http://localhost:5000")
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

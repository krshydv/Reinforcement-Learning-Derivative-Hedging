#!/usr/bin/env python
import os
import socket
import sys
import time
from urllib.parse import urlparse

REQUIRED = [
    "SECRET_KEY",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "REDIS_URL",
    "CELERY_BROKER_URL",
    "CELERY_RESULT_BACKEND",
    "MLFLOW_TRACKING_URI",
    "WAND_B_PROJECT"
]


def require_env() -> None:
    missing = [name for name in REQUIRED if not os.getenv(name)]
    if missing:
        sys.stderr.write("Missing required environment variables: " + ", ".join(missing) + "\n")
        sys.exit(1)


def wait_for(host: str, port: int, name: str) -> None:
    deadline = time.time() + 90
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=3):
                return
        except OSError:
            time.sleep(2)
    sys.stderr.write(f"Dependency {name} at {host}:{port} is unavailable\n")
    sys.exit(1)


def parse_url(url: str) -> tuple[str, int]:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port
    if not host or not port:
        sys.stderr.write(f"Invalid URL for dependency: {url}\n")
        sys.exit(1)
    return host, port


def main() -> None:
    require_env()
    postgres_host = os.getenv("POSTGRES_HOST", "")
    postgres_port = int(os.getenv("POSTGRES_PORT", "0"))
    if not postgres_host or not postgres_port:
        sys.stderr.write("Postgres host or port is invalid\n")
        sys.exit(1)
    wait_for(postgres_host, postgres_port, "postgres")
    redis_host, redis_port = parse_url(os.getenv("REDIS_URL", ""))
    wait_for(redis_host, redis_port, "redis")
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "")
    if mlflow_uri.startswith("http"):
        mlflow_host, mlflow_port = parse_url(mlflow_uri)
        wait_for(mlflow_host, mlflow_port, "mlflow")


if __name__ == "__main__":
    main()

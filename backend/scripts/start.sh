#!/usr/bin/env bash
set -e
python /app/scripts/preflight.py
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

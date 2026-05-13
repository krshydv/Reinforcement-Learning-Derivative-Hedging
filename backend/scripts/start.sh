#!/usr/bin/env bash
set -e
python /app/scripts/preflight.py
if ls /app/alembic/versions/*.py >/dev/null 2>&1; then
  alembic upgrade head
fi
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

#!/usr/bin/env bash
set -e
python /app/scripts/preflight.py
exec celery -A app.worker.celery_app worker --loglevel=info

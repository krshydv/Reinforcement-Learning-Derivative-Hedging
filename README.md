# Reinforcement Learning Derivative Hedging Platform

## Overview
Institutional-grade quantitative research and RL hedging platform with FastAPI, Next.js, PostgreSQL, Redis, Celery, MLflow, Prometheus, Grafana, and a production dashboard.

## Quick Start

```bash
cp .env.example .env
make up
```

Services
- API: http://localhost:8000
- Web: http://localhost:3000
- MLflow: http://localhost:5000
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090

## Development

```bash
make backend-dev
make frontend-dev
```

## Migrations

```bash
make migrate
```

## Tests

```bash
make test-backend
make test-frontend
```

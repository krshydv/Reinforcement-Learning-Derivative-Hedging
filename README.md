# Reinforcement Learning Derivative Hedging Platform

An enterprise-grade quantitative finance platform for **derivative pricing, risk analytics, portfolio management, and reinforcement learning–based hedging strategies**.

The platform combines modern quantitative research infrastructure with scalable backend systems, real-time analytics, ML training pipelines, and production-ready deployment architecture.

---

# Overview

This project is designed to simulate and optimize derivative hedging strategies using **Reinforcement Learning (RL)** and advanced quantitative finance models.

The system integrates:

- Reinforcement Learning training environments
- Option pricing engines
- Portfolio risk analytics
- Backtesting infrastructure
- Real-time websocket streaming
- Production-grade backend APIs
- Interactive frontend dashboards
- Containerized deployment infrastructure

The objective is to create a scalable research and deployment platform for algorithmic hedging and quantitative trading workflows.

---

# Core Features

## Quantitative Finance Engine

- Black-Scholes pricing
- Monte Carlo simulation
- Heston stochastic volatility model
- Jump diffusion models
- Greeks computation
- Portfolio risk metrics
- PnL analytics
- Drawdown analysis

---

## Reinforcement Learning Infrastructure

- RL training environments
- Stable-Baselines3 integration
- Continuous-action hedging agents
- Market simulation engine
- Reward optimization pipelines
- Strategy experimentation workflows

---

## Portfolio & Risk Management

- Portfolio exposure tracking
- Risk analytics dashboard
- Strategy monitoring
- Performance metrics
- Scenario analysis
- Backtesting engine

---

## Frontend Dashboard

- Interactive analytics dashboard
- Real-time websocket updates
- Multi-page Next.js frontend
- Strategy visualization panels
- Research monitoring interface
- Training metrics visualization

---

## Backend Infrastructure

- FastAPI backend services
- REST API architecture
- Websocket communication layer
- Authentication system
- Redis integration
- PostgreSQL integration
- MLflow experiment tracking

---

## Infrastructure & Deployment

- Docker Compose orchestration
- Kubernetes deployment manifests
- NGINX reverse proxy
- Prometheus monitoring
- Grafana dashboards
- Healthcheck systems
- Runtime validation pipelines

---

# Tech Stack

## Backend

- Python 3.11+ (Docker image); local tests support Python 3.9+ with `eval_type_backport`
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Celery

---

## Machine Learning & Quant

- PyTorch
- Stable-Baselines3
- NumPy
- Pandas
- SciPy

---

## Frontend

- Next.js
- React
- TypeScript
- Zustand
- React Query

---

## DevOps & Infrastructure

- Docker
- Kubernetes
- NGINX
- Prometheus
- Grafana
- MLflow

---

# Architecture

```text
Frontend (Next.js)
        │
        ▼
NGINX Reverse Proxy
        │
        ▼
FastAPI Backend Services
        │
 ┌──────┼─────────┐
 ▼      ▼         ▼
Redis  PostgreSQL MLflow
 │
 ▼
Celery Workers
 │
 ▼
RL Training + Quant Engine
```

---

# Project Structure

```text
Reinforcement-Learning-Derivative-Hedging/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── quant/
│   │   ├── services/
│   │   ├── websocket/
│   │   ├── middleware/
│   │   └── db/
│   │
│   ├── scripts/
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── store/
│   │   └── lib/
│   │
│   └── public/
│
├── infra/
│   ├── kubernetes/
│   ├── nginx/
│   ├── prometheus/
│   └── grafana/
│
├── docker-compose.yml
├── README.md
└── .env.example
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/Reinforcement-Learning-Derivative-Hedging.git
```

## Move Into Project Directory

```bash
cd Reinforcement-Learning-Derivative-Hedging
```

## Start Full Stack

```bash
docker compose up --build
```

---

# Services

| Service | Port (host) |
|---|---|
| NGINX (unified entry) | 8080 |
| Frontend | 3000 |
| Backend API | 8000 |
| MLflow | 5001 |
| Grafana | 3001 |
| Prometheus | 9090 |
| PostgreSQL | 55432 |
| Redis | 6380 |

---

# API Endpoints

## Training

- `POST /api/v1/training/start` — launch a training run with `TrainingRequest` config.
- `GET /api/v1/training/` — list training runs for the authenticated user.
- `GET /api/v1/training/{run_id}` — fetch a single training run.
- `POST /api/v1/training/stop/{run_id}` — stop a training run.

## Benchmarks

- `POST /api/v1/benchmarks/run` — run pricing, risk, and backtest benchmarks.

### Websocket
- `WS /ws/{client_id}?token=<JWT>` — live stream with heartbeat (`ping`/`pong`).
- `WS /ws/telemetry?token=<JWT>&channels=training,risk,portfolio&replay=50` — telemetry stream with replay.


---

# Phase 3 Telemetry & Observability

## Telemetry architecture

- **Gateway**: `TelemetryGateway` publishes typed events to Redis pub/sub and persists short replay buffers.
- **Channels**: training, training.metrics, portfolio, risk, and api.latency are streamed over websocket fanout.
- **Recovery**: websocket clients support heartbeat ping/pong, reconnect backoff, replay windows, and bounded queues.
- **Middleware**: request latency is captured by `TelemetryMiddleware` and emitted automatically as telemetry events.

## Data flow

1. Backend services emit typed telemetry events.
2. Redis pub/sub fans events out to websocket subscribers.
3. The frontend telemetry bootstrap subscribes to live channels on app load.
4. The dashboard pages render the live event stream, latency stats, and RL observability panels.

## Operational workflows

- **Training monitoring**: start a run through `POST /api/v1/training/start`, then watch `training` and `training.metrics` channels.
- **Portfolio/risk monitoring**: open the dashboard or call `GET /api/v1/metrics/latest` and `GET /api/v1/portfolios/overview`.
- **Replay recovery**: connect to `WS /ws/telemetry?...&replay=50` to recover missed events after a disconnect.
- **Compression**: pass `compress=1` on the websocket URL if you want compressed event payloads.

## Debugging

- **API health**: `GET /health`.
- **Prometheus**: `GET /metrics` exposes application and websocket counters.
- **Container logs**: `docker-compose logs -f api` and `docker-compose logs -f worker`.
- **Websocket verification**: confirm the client receives `ping`/`pong` and replay events before live updates.
- **Redis checks**: verify the `telemetry:*` keys to inspect buffered event history.

## Deployment notes

- Use `docker-compose build --pull=false api` when offline or on constrained networks.
- The backend image avoids system-package installs to keep builds lightweight and memory-safe.
- The training pipeline lazily imports MLflow/W&B so the API can start cleanly even when experiment tooling is unavailable.

---

# Project Status

## Completed

- Quant pricing engine
- Reinforcement learning training environment
- FastAPI backend architecture
- Multi-page frontend dashboard
- Real-time websocket infrastructure
- Portfolio analytics system
- Backtesting engine
- Dockerized deployment stack
- Kubernetes deployment manifests
- Prometheus monitoring integration
- Grafana dashboard provisioning
- MLflow experiment tracking
- Runtime validation pipelines
- NGINX reverse proxy integration
- Redis and PostgreSQL integration
- Healthcheck and readiness systems
- Runtime stabilization improvements
- Security hardening foundation
- Deployment orchestration system

---

# Production Capabilities

- Enterprise-ready backend architecture
- Real-time analytics infrastructure
- Reinforcement learning research workflows
- Quantitative risk management pipelines
- Distributed service orchestration
- Monitoring and observability stack
- Containerized deployment support
- Kubernetes-native infrastructure
- Scalable websocket communication
- Experiment tracking and analytics

---

# Monitoring & Observability

- Prometheus metrics
- Grafana dashboards
- Runtime healthchecks
- Service readiness probes
- API monitoring
- Training telemetry
- Infrastructure observability

---

# Future Expansion Goals

- Multi-agent RL hedging
- Live market data integration
- Institutional-grade risk systems
- High-frequency simulation support
- Distributed RL training
- Cloud-native scaling
- Advanced strategy optimization
- Automated model evaluation

---

# License

This project is licensed under the MIT License.

---

# Author

## KRISH YADAV

Developed as a full-stack quantitative finance and reinforcement learning research platform focused on scalable derivative hedging infrastructure and production-grade quantitative systems.

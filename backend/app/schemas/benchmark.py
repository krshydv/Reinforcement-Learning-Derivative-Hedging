from __future__ import annotations

from pydantic import BaseModel


class BenchmarkRequest(BaseModel):
    spot: float = 100.0
    strike: float = 100.0
    rate: float = 0.02
    vol: float = 0.2
    tau: float = 1.0
    paths: int = 50_000
    steps: int = 252
    seed: int = 7
    include_backtests: bool = True
    include_risk: bool = True


class BenchmarkResult(BaseModel):
    pricing: dict
    risk: dict | None
    backtests: dict | None
    timings: dict

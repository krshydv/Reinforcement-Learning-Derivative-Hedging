from app.schemas.benchmark import BenchmarkRequest, BenchmarkResult
from app.quant.benchmarks import run_benchmarks


class BenchmarkService:
    async def run(self, payload: BenchmarkRequest) -> BenchmarkResult:
        result = run_benchmarks(payload.model_dump())
        return BenchmarkResult(**result)

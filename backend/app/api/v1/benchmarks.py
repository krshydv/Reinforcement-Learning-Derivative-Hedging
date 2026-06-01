from fastapi import APIRouter, Depends
from app.schemas.benchmark import BenchmarkRequest, BenchmarkResult
from app.services.benchmark_service import BenchmarkService
from app.services.auth_service import require_permission

router = APIRouter()


@router.post("/run", response_model=BenchmarkResult)
async def run_benchmarks(payload: BenchmarkRequest, user=Depends(require_permission("access"))) -> BenchmarkResult:
    _ = user
    return await BenchmarkService().run(payload)

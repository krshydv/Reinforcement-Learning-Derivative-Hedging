from app.quant.benchmarks import run_benchmarks

class StrategyService:
    async def benchmark(self, user_id: str) -> dict:
        _ = user_id
        return run_benchmarks({})

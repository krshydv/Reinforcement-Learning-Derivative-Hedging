from app.quant.benchmarks import run_benchmarks


def test_benchmark_suite_outputs():
    result = run_benchmarks(
        {
            "seed": 42,
            "paths": 8000,
            "steps": 80,
            "include_backtests": True,
            "include_risk": True,
        }
    )
    assert "pricing" in result
    assert "timings" in result
    pricing = result["pricing"]
    assert pricing["black_scholes"] > 0
    assert 0.0 <= pricing["relative_error_mc"] < 0.3
    assert result["backtests"] is not None
    assert "delta" in result["backtests"]
    assert result["risk"] is not None

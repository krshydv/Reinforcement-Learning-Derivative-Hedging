from app.quant.risk import risk_metrics


def test_risk_metrics_consistency():
    returns = [0.01, -0.02, 0.015, -0.005, 0.02]
    metrics = risk_metrics(returns)
    assert "sharpe" in metrics
    assert metrics["var"] <= metrics["cvar"] + 1e-6
    assert metrics["max_drawdown"] <= 0

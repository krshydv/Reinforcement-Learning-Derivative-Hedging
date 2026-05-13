import numpy as np
from app.schemas.market import MarketConfig
from app.quant.market_models import simulate_market


def test_market_simulation_shapes():
    np.random.seed(7)
    config = MarketConfig(model="heston", steps=50, dt=0.01, spot=100, rate=0.02, vol=0.2, assets=["a", "b"], correlation=[[1.0, 0.3], [0.3, 1.0]])
    series = simulate_market(config)
    assert len(series) == 50
    assert series[0].prices is not None and len(series[0].prices) == 2


def test_market_bid_ask_spread():
    np.random.seed(11)
    config = MarketConfig(model="gbm", steps=10, dt=0.01, spot=100, rate=0.02, vol=0.2, bid_ask_spread=0.02, slippage=0.001)
    series = simulate_market(config)
    assert series[0].bid is not None and series[0].ask is not None
    assert series[0].ask > series[0].bid

import os
import numpy as np
from app.quant.options import OptionPricer


def test_black_scholes_call():
    pricer = OptionPricer()
    price = pricer.black_scholes(spot=100, strike=100, rate=0.05, vol=0.2, tau=1.0, call=True)
    assert abs(price - 10.4506) < 0.05


def test_black_scholes_put():
    pricer = OptionPricer()
    price = pricer.black_scholes(spot=100, strike=100, rate=0.05, vol=0.2, tau=1.0, call=False)
    assert abs(price - 5.5735) < 0.05


def test_greeks_delta_gamma():
    pricer = OptionPricer()
    greeks = pricer.greeks(spot=100, strike=100, rate=0.05, vol=0.2, tau=1.0, call=True)
    assert 0.63 < greeks["delta"] < 0.64
    assert 0.018 < greeks["gamma"] < 0.02


def test_monte_carlo_consistency():
    np.random.seed(42)
    pricer = OptionPricer()
    bs = pricer.black_scholes(spot=100, strike=100, rate=0.02, vol=0.25, tau=1.0, call=True)
    mc = pricer.monte_carlo(spot=100, strike=100, rate=0.02, vol=0.25, tau=1.0, call=True, paths=50000)
    assert abs(bs - mc) / bs < 0.05

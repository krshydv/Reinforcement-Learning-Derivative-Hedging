import numpy as np

def simulate_gbm(spot: float, rate: float, vol: float, steps: int, dt: float) -> tuple[np.ndarray, np.ndarray]:
    prices = np.zeros(steps)
    vols = np.full(steps, vol)
    prices[0] = spot
    for t in range(1, steps):
        z = np.random.normal()
        prices[t] = prices[t-1] * np.exp((rate - 0.5 * vol ** 2) * dt + vol * np.sqrt(dt) * z)
    return prices, vols

def simulate_heston(spot: float, rate: float, vol: float, steps: int, dt: float) -> tuple[np.ndarray, np.ndarray]:
    kappa = 2.0
    theta = vol ** 2
    xi = 0.5
    prices = np.zeros(steps)
    variances = np.zeros(steps)
    prices[0] = spot
    variances[0] = vol ** 2
    for t in range(1, steps):
        z1 = np.random.normal()
        z2 = np.random.normal()
        variances[t] = np.abs(variances[t-1] + kappa * (theta - variances[t-1]) * dt + xi * np.sqrt(variances[t-1] * dt) * z2)
        prices[t] = prices[t-1] * np.exp((rate - 0.5 * variances[t]) * dt + np.sqrt(variances[t] * dt) * z1)
    return prices, np.sqrt(variances)

def simulate_jump(spot: float, rate: float, vol: float, steps: int, dt: float) -> tuple[np.ndarray, np.ndarray]:
    lam = 0.2
    mu_j = -0.1
    sigma_j = 0.3
    prices = np.zeros(steps)
    vols = np.full(steps, vol)
    prices[0] = spot
    for t in range(1, steps):
        z = np.random.normal()
        jump = np.random.poisson(lam * dt)
        jump_size = np.random.normal(mu_j, sigma_j) * jump
        prices[t] = prices[t-1] * np.exp((rate - 0.5 * vol ** 2) * dt + vol * np.sqrt(dt) * z + jump_size)
    return prices, vols

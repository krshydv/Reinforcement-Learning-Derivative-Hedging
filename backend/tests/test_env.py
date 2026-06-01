import numpy as np
from app.quant.env import HedgingEnv


def test_env_step():
    np.random.seed(1)
    env = HedgingEnv(steps=5)
    obs, _ = env.reset()
    assert obs.shape[0] == 12
    obs, reward, terminated, truncated, _ = env.step(np.array([0.1, -0.2, 0.05], dtype=np.float32))
    assert isinstance(reward, float)
    assert terminated is False
    assert truncated is False

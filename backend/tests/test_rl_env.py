import numpy as np
from app.quant.env import HedgingEnv


def test_env_reset_and_step_shapes():
    env = HedgingEnv(steps=10, seed=42)
    obs, info = env.reset()
    assert obs.shape == (12,)
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    assert obs.shape == (12,)
    assert isinstance(reward, float)
    assert terminated in [True, False]
    assert truncated is False


def test_env_seed_reproducibility():
    env1 = HedgingEnv(steps=5, seed=123)
    env2 = HedgingEnv(steps=5, seed=123)
    obs1, _ = env1.reset()
    obs2, _ = env2.reset()
    np.testing.assert_allclose(obs1, obs2, rtol=1e-6, atol=1e-6)

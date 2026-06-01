from __future__ import annotations

import uuid
from typing import Callable
from app.quant.rl_config import TrainConfig
from app.quant.train import train_agent


class TrainingManager:
    def run(self, config: TrainConfig, run_id: str | None = None, on_event: Callable[[str, str], None] | None = None) -> dict:
        run_id = run_id or str(uuid.uuid4())
        if on_event:
            on_event(run_id, "started")
        train_agent(config, run_id=run_id)
        if on_event:
            on_event(run_id, "completed")
        return {"run_id": run_id, "status": "completed"}

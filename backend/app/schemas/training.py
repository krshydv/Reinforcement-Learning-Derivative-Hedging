from pydantic import BaseModel

class TrainingRequest(BaseModel):
    experiment_name: str
    algorithm: str
    timesteps: int

class TrainingRun(BaseModel):
    run_id: str
    status: str

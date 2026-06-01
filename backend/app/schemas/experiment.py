from pydantic import BaseModel

class ExperimentCreate(BaseModel):
    name: str
    algorithm: str

class ExperimentRead(BaseModel):
    id: str
    name: str
    algorithm: str
    status: str

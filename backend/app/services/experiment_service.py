import uuid
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Experiment
from app.schemas.experiment import ExperimentCreate, ExperimentRead

class ExperimentService:
    async def create_experiment(self, user_id: str, payload: ExperimentCreate) -> ExperimentRead:
        async with AsyncSessionLocal() as session:
            experiment = Experiment(id=str(uuid.uuid4()), user_id=user_id, name=payload.name, algorithm=payload.algorithm, status="created")
            session.add(experiment)
            await session.commit()
            return ExperimentRead(id=experiment.id, name=experiment.name, algorithm=experiment.algorithm, status=experiment.status)

    async def list_experiments(self, user_id: str) -> list[ExperimentRead]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Experiment).where(Experiment.user_id == user_id))
            experiments = result.scalars().all()
            return [ExperimentRead(id=e.id, name=e.name, algorithm=e.algorithm, status=e.status) for e in experiments]

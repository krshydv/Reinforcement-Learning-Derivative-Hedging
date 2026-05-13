from fastapi import APIRouter
from app.api.v1 import auth, portfolios, training, market, metrics, experiments, strategies, users, backtests

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(users.router, tags=["users"], prefix="/users")
api_router.include_router(portfolios.router, tags=["portfolios"], prefix="/portfolios")
api_router.include_router(training.router, tags=["training"], prefix="/training")
api_router.include_router(market.router, tags=["market"], prefix="/market")
api_router.include_router(metrics.router, tags=["metrics"], prefix="/metrics")
api_router.include_router(experiments.router, tags=["experiments"], prefix="/experiments")
api_router.include_router(strategies.router, tags=["strategies"], prefix="/strategies")
api_router.include_router(backtests.router, tags=["backtests"], prefix="/backtests")

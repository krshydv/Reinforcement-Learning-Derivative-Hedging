from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "rl-derivative-hedging"
    env: str = "development"
    api_v1_str: str = "/api/v1"
    secret_key: str
    access_token_expire_minutes: int = 60
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str
    mlflow_tracking_uri: str
    wand_b_project: str
    wand_b_entity: str | None = None
    wand_b_api_key: str | None = None
    prometheus_port: int = 8001
    jwt_algorithm: str = "HS256"
    rate_limit: str = "100/minute"
    cors_origins: str = ""
    training_log_dir: str = "/app/logs"
    checkpoint_dir: str = "/app/checkpoints"
    num_envs: int = 4

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()

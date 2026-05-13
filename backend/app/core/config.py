from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ai-analytics-api"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:3000"]

    database_url: str = "postgresql+psycopg://analytics:analytics@localhost:5432/analytics"
    database_pool_size: int = 5
    database_max_overflow: int = 5
    database_pool_pre_ping: bool = True

    redis_url: str = "redis://localhost:6379/0"
    redis_cache_ttl_seconds: int = 60
    rate_limit_per_minute: int = 1000

    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_events_topic: str = "analytics.events"
    kafka_dlq_topic: str = "analytics.events.dlq"
    kafka_consumer_group: str = "analytics-consumer"

    jwt_secret_key: str = "replace-with-strong-secret"
    jwt_refresh_secret_key: str = "replace-with-strong-refresh-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 43200
    bcrypt_rounds: int = 12

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_cors(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()

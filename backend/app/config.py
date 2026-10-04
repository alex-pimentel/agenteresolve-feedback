"""Service configuration (env driven)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    tool_slug: str = "feedback"
    tool_name: str = "FeedbackClassifier"
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str = "openai/gpt-4o-mini"
    llm_timeout: float = 60.0
    inference_url: str | None = None
    inference_key: str | None = None
    cors_origins: str = "*"
    results_dir: str = "results"
    max_bytes: int = 200000


@lru_cache
def get_settings() -> Settings:
    return Settings()

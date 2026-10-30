"""talkaty configuration — pydantic settings with TALKATY_* env overrides."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="TALKATY_", extra="ignore")

    default_backend: str = Field(default="edge-tts")
    default_voice: str = Field(default="smooth female")
    default_accent: str = Field(default="US")
    default_pitch: float = Field(default=0.0)
    default_speed: float = Field(default=1.0)
    output_dir: str = Field(default=".")


@lru_cache
def get_settings() -> Settings:
    return Settings()

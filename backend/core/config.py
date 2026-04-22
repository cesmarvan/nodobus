from dataclasses import Field
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nodobus API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"

    DB_USER:str = Field("nodobus", env="DB_USER")
    DB_PASSWORD:str = Field("nodobus123", env="DB_PASSWORD")
    DB_HOST:str = Field("localhost", env="DB_HOST")
    DB_PORT:str = Field("5432", env="DB_PORT")
    DB_NAME:str = Field("nodobus", env="DB_NAME")

    @property
    def database_url(self) -> str:
        """Construct the database URL from individual components.

        Returns:
            str: The full database connection URL.
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: The application settings, cached after first call.
    """
    return Settings()
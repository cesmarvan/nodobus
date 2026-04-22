from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nodobus API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"

    DB_USER: str = Field(default="nodobus", validation_alias="DB_USER")
    DB_PASSWORD: str = Field(default="nodobus123", validation_alias="DB_PASSWORD")
    DB_HOST: str = Field(default="localhost", validation_alias="DB_HOST")
    DB_PORT: str = Field(default="5432", validation_alias="DB_PORT")
    DB_NAME: str = Field(default="nodobus", validation_alias="DB_NAME")

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
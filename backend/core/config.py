from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nodobus API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"

    DB_USER: str = Field(default="nodobus", validation_alias="DB_USER")
    DB_PASSWORD: str = Field(default="nodobus123", validation_alias="DB_PASSWORD")
    DB_HOST: str = Field(default="localhost", validation_alias="DB_HOST")
    DB_PORT: str = Field(default="5432", validation_alias="DB_PORT")
    DB_NAME: str = Field(default="nodobus", validation_alias="DB_NAME")

    # External API URLs for fetcher service
    TUSSAM_ARCGIS_LINEAS_URL: str = Field(
        default="https://services1.arcgis.com/hcmP7kr0Cx3AcTJk/arcgis/rest/services/TUSSAM_Lineas/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json",
        validation_alias="TUSSAM_ARCGIS_LINEAS_URL",
    )
    TUSSAM_ARCGIS_PARADAS_URL: str = Field(
        default="https://services1.arcgis.com/hcmP7kr0Cx3AcTJk/arcgis/rest/services/TUSSAM_Paradas/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json",
        validation_alias="TUSSAM_ARCGIS_PARADAS_URL",
    )
    TUSSAM_INFOTUS_BASE_URL: str = Field(
        default="https://reddelineas.tussam.es/API/infotus-ui/buses",
        validation_alias="TUSSAM_INFOTUS_BASE_URL",
    )

    # Internal API service URLs
    LINEAS_SERVICE_BASE_URL: str = Field(
        default="http://localhost:8000",
        validation_alias="LINEAS_SERVICE_BASE_URL",
    )

    # Celery configuration
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/0",
        validation_alias="CELERY_BROKER_URL",
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/0",
        validation_alias="CELERY_RESULT_BACKEND",
    )

    @property
    def database_url(self) -> str:
        """Construct the database URL from individual components.

        Returns:
            str: The full database connection URL.
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def tussam_arcgis_lineas_url(self) -> str:
        """Get TUSSAM ArcGIS líneas URL."""
        return self.TUSSAM_ARCGIS_LINEAS_URL

    @property
    def tussam_arcgis_paradas_url(self) -> str:
        """Get TUSSAM ArcGIS paradas URL."""
        return self.TUSSAM_ARCGIS_PARADAS_URL

    @property
    def tussam_infotus_base_url(self) -> str:
        """Get TUSSAM infotus base URL."""
        return self.TUSSAM_INFOTUS_BASE_URL

    @property
    def lineas_service_base_url(self) -> str:
        """Get lineas service base URL."""
        return self.LINEAS_SERVICE_BASE_URL

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
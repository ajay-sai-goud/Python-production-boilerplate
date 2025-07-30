from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from typing import Optional

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Settings(BaseSettings):
    """
    Holds all application settings, loaded from environment variables.
    """
    APP_NAME: str = "AWSLambdaBoilerplate"
    
    # Logging configuration
    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOGURU_JSON_LOGS: bool = False

    # OpenTelemetry configuration
    OTEL_SERVICE_NAME: str = "lambda-boilerplate"
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[str] = None
    OTEL_DEBUG_LOG_SPANS: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False,
    )

settings = Settings()

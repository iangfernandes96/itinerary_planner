"""Configuration management for the application."""

from typing import Any, Dict

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Database settings
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""
    database_url: str = ""

    # LLM settings
    gemini_api_key: str = ""  # Default empty string to avoid None

    # Logging settings
    log_level: str = "INFO"
    sql_echo: bool = False

    # Prompt templates
    prompts: Dict[str, str] = {
        "itinerary": (
            "Create a detailed itinerary based on the following request.\n"
            "Format the response in a clear, day-by-day structure with "
            "specific times.\n"
            "Request: {query}"
        )
    }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",  # Allow extra fields in the configuration
        env_prefix="",  # Ensure no prefix is added to env var names
    )

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        required_fields = [
            self.postgres_user,
            self.postgres_password,
            self.postgres_db,
            self.database_url,
        ]
        if not all(required_fields):
            raise ValueError(
                "Missing required database configuration. "
                "Please check your environment variables."
            )


settings = Settings()

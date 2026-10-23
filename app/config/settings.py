import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
DEFAULT_TEMPERATURE = 0.2


class ConfigurationError(ValueError):
    """Raised when required application configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = field(repr=False)
    gemini_model: str = DEFAULT_GEMINI_MODEL
    temperature: float = DEFAULT_TEMPERATURE


def get_settings() -> Settings:
    """Load and validate Gemini settings from environment variables."""
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ConfigurationError(
            "Gemini API key is missing. Create a .env file and set GEMINI_API_KEY."
        )

    model = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip()
    if not model:
        raise ConfigurationError("GEMINI_MODEL must not be empty.")

    raw_temperature = os.getenv("TEMPERATURE", str(DEFAULT_TEMPERATURE))
    try:
        temperature = float(raw_temperature)
    except ValueError as error:
        raise ConfigurationError(
            "TEMPERATURE must be a number between 0 and 2."
        ) from error

    if not 0 <= temperature <= 2:
        raise ConfigurationError("TEMPERATURE must be a number between 0 and 2.")

    return Settings(
        gemini_api_key=api_key,
        gemini_model=model,
        temperature=temperature,
    )

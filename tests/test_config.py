import pytest

from app.config import settings as config


def test_settings_load_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "load_dotenv", lambda: False)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "test-model")
    monkeypatch.setenv("TEMPERATURE", "0.4")

    settings = config.get_settings()

    assert settings.gemini_api_key == "test-key"
    assert settings.gemini_model == "test-model"
    assert settings.temperature == 0.4
    assert "test-key" not in repr(settings)


def test_settings_load_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "load_dotenv", lambda: False)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.delenv("TEMPERATURE", raising=False)

    settings = config.get_settings()

    assert settings.gemini_model == config.DEFAULT_GEMINI_MODEL
    assert settings.temperature == config.DEFAULT_TEMPERATURE


def test_missing_api_key_has_clear_configuration_message(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(config, "load_dotenv", lambda: False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(
        config.ConfigurationError, match=r"Gemini API key.*Create a \.env file"
    ):
        config.get_settings()


@pytest.mark.parametrize("value", ["not-a-number", "-0.1", "2.1"])
def test_invalid_temperature_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
) -> None:
    monkeypatch.setattr(config, "load_dotenv", lambda: False)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("TEMPERATURE", value)

    with pytest.raises(config.ConfigurationError, match="TEMPERATURE"):
        config.get_settings()

from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock

import pytest

from app.config.settings import Settings
from app.services import gemini_service


def test_service_initializes_gemini_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, str] = {}

    class FakeClient:
        def __init__(self, *, api_key: str) -> None:
            captured["api_key"] = api_key
            self.models = SimpleNamespace()

    monkeypatch.setattr(gemini_service.genai, "Client", FakeClient)

    service = gemini_service.GeminiService(Settings("test-key"))

    assert isinstance(service, gemini_service.GeminiService)
    assert captured == {"api_key": "test-key"}


def test_generate_answer_passes_history_and_returns_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}
    client_options: dict[str, str] = {}

    class FakeModels:
        def generate_content(self, **kwargs: Any) -> SimpleNamespace:
            captured.update(kwargs)
            return SimpleNamespace(text="  A useful answer.  ")

    class FakeClient:
        def __init__(self, *, api_key: str) -> None:
            client_options["api_key"] = api_key
            self.models = FakeModels()

    monkeypatch.setattr(gemini_service.genai, "Client", FakeClient)
    service = gemini_service.GeminiService(
        Settings("test-key", "test-model", 0.4)
    )

    answer = service.generate_answer(
        [
            {"role": "system", "content": "Be helpful."},
            {"role": "user", "content": "First question?"},
            {"role": "assistant", "content": "Prior answer."},
            {"role": "user", "content": "Follow-up?"},
        ]
    )

    assert answer == "A useful answer."
    assert client_options == {"api_key": "test-key"}
    assert captured["model"] == "test-model"
    assert captured["config"].system_instruction == "Be helpful."
    assert captured["config"].temperature == 0.4
    assert [item.role for item in captured["contents"]] == [
        "user",
        "model",
        "user",
    ]
    assert [item.parts[0].text for item in captured["contents"]] == [
        "First question?",
        "Prior answer.",
        "Follow-up?",
    ]


def test_api_error_does_not_expose_internal_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client_options: dict[str, str] = {}

    class FakeModels:
        generate_content = Mock(
            side_effect=gemini_service.errors.APIError(
                code=401,
                response_json={"error": {"message": "sensitive credential detail"}},
            )
        )

    class FakeClient:
        def __init__(self, *, api_key: str) -> None:
            client_options["api_key"] = api_key
            self.models = FakeModels()

    monkeypatch.setattr(gemini_service.genai, "Client", FakeClient)
    service = gemini_service.GeminiService(Settings("test-key"))

    with pytest.raises(gemini_service.GeminiServiceError) as error:
        service.generate_answer([{"role": "user", "content": "Question?"}])

    assert client_options == {"api_key": "test-key"}
    assert "sensitive credential detail" not in str(error.value)
    assert error.value.__cause__ is None


@pytest.mark.parametrize("text", [None, "  "])
def test_empty_response_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    text: str | None,
) -> None:
    client_options: dict[str, str] = {}

    class FakeModels:
        generate_content = Mock(return_value=SimpleNamespace(text=text))

    class FakeClient:
        def __init__(self, *, api_key: str) -> None:
            client_options["api_key"] = api_key
            self.models = FakeModels()

    monkeypatch.setattr(gemini_service.genai, "Client", FakeClient)
    service = gemini_service.GeminiService(Settings("test-key"))

    with pytest.raises(gemini_service.GeminiServiceError, match="empty response"):
        service.generate_answer([{"role": "user", "content": "Question?"}])

    assert client_options == {"api_key": "test-key"}

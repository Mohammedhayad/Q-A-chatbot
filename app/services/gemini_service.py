from collections.abc import Sequence
from typing import Literal, TypedDict

from google import genai
from google.genai import errors, types

from app.config.settings import Settings


class ConversationMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class GeminiServiceError(RuntimeError):
    """Raised when Gemini cannot provide a usable answer."""


class GeminiService:
    def __init__(self, settings: Settings) -> None:
        """Initialize a Gemini client with validated application settings."""
        self._settings = settings
        self._client = genai.Client(api_key=settings.gemini_api_key)

    def generate_answer(self, messages: Sequence[ConversationMessage]) -> str:
        """Generate answer text from the system prompt and conversation history."""
        instructions = "\n".join(
            message["content"] for message in messages if message["role"] == "system"
        )
        conversation = [
            types.Content(
                role="model" if message["role"] == "assistant" else "user",
                parts=[types.Part.from_text(text=message["content"])],
            )
            for message in messages
            if message["role"] != "system"
        ]

        try:
            response = self._client.models.generate_content(
                model=self._settings.gemini_model,
                contents=conversation,
                config=types.GenerateContentConfig(
                    system_instruction=instructions or None,
                    temperature=self._settings.temperature,
                ),
            )
        except errors.APIError:
            raise GeminiServiceError(
                "Gemini could not generate an answer. Check your API key and "
                "model configuration, then try again."
            ) from None

        answer = response.text
        if answer is None or not answer.strip():
            raise GeminiServiceError(
                "Gemini returned an empty response. Please try again."
            )

        return answer.strip()

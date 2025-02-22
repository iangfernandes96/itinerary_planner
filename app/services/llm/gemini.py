import asyncio
from typing import Any, Optional

import google.generativeai as genai

from .base import LLMProvider


class GeminiError(Exception):
    """Base exception for Gemini provider errors."""

    pass


class GeminiProvider(LLMProvider):
    """Gemini implementation of LLM provider."""

    def __init__(self) -> None:
        self._model: Optional[genai.GenerativeModel] = None
        self._model_name: str = "gemini-pro"
        self._initialized: bool = False

    async def initialize(self, api_key: str, **kwargs: Any) -> None:
        """Initialize Gemini with API key."""
        try:
            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel(self._model_name)
            self._initialized = True
        except Exception as e:
            raise GeminiError(f"Failed to initialize Gemini: {str(e)}") from e

    async def generate_text(self, prompt: str) -> str:
        """Generate text using Gemini."""
        if not self._initialized or not self._model:
            raise GeminiError("Gemini provider not initialized")

        try:
            # Run the blocking API call in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self._model.generate_content(prompt)  # type: ignore
            )
            return str(response.text)  # Ensure we return a string
        except Exception as e:
            raise GeminiError(f"Gemini text generation failed: {str(e)}") from e

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def is_initialized(self) -> bool:
        return self._initialized

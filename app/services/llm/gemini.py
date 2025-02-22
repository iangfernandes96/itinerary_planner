import asyncio
import google.generativeai as genai
from .base import LLMProvider


class GeminiProvider(LLMProvider):
    """Gemini implementation of LLM provider"""

    def __init__(self):
        self._model = None
        self._model_name = "gemini-pro"

    async def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize Gemini with API key"""
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(self._model_name)

    async def generate_text(self, prompt: str) -> str:
        """Generate text using Gemini"""
        if not self._model:
            raise RuntimeError("Gemini provider not initialized")

        # Run the blocking API call in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: self._model.generate_content(prompt)  # type: ignore
        )
        return response.text

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self._model_name

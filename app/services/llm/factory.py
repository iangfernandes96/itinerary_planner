from typing import Dict, Type
from .base import LLMProvider
from .gemini import GeminiProvider


class LLMFactory:
    """Factory for creating and managing LLM providers"""

    _providers: Dict[str, Type[LLMProvider]] = {
        "gemini": GeminiProvider
    }

    @classmethod
    def register_provider(
        cls, name: str, provider_class: Type[LLMProvider]
    ) -> None:
        """Register a new LLM provider"""
        cls._providers[name] = provider_class

    @classmethod
    def create_provider(cls, name: str) -> LLMProvider:
        """Create a new instance of an LLM provider"""
        if name not in cls._providers:
            raise ValueError(f"Unknown LLM provider: {name}")
        return cls._providers[name]() 
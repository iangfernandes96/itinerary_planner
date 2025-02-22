from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Base class for LLM providers"""

    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        """Generate text from prompt"""
        pass

    @abstractmethod
    async def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize the LLM provider with credentials"""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get the provider name"""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the model name"""
        pass

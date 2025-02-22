from dotenv import load_dotenv

from ..config import settings
from .llm import LLMFactory

load_dotenv()


class ItineraryServiceError(Exception):
    """Base exception for itinerary service errors."""

    pass


class ItineraryService:
    """Service for generating itineraries using LLM providers."""

    def __init__(self, provider_name: str = "gemini"):
        """Initialize the service with specified LLM provider."""
        try:
            self.provider = LLMFactory.create_provider(provider_name)
        except ValueError as e:
            raise ItineraryServiceError(f"Failed to create provider: {str(e)}")

    async def initialize(self) -> None:
        """Initialize the LLM provider with API key from settings."""
        try:
            api_key = settings.gemini_api_key
            if not api_key:
                raise ItineraryServiceError(
                    f"API key not found for provider {self.provider.provider_name}"
                )
            await self.provider.initialize(api_key)
        except Exception as e:
            raise ItineraryServiceError(
                f"Failed to initialize provider: {str(e)}"
            ) from e

    async def generate_itinerary(self, query: str) -> str:
        """Generate an itinerary using the configured LLM provider."""
        try:
            prompt = self._create_prompt(query)
            return await self.provider.generate_text(prompt)
        except Exception as e:
            raise ItineraryServiceError(
                f"Failed to generate itinerary: {str(e)}"
            ) from e

    def _create_prompt(self, query: str) -> str:
        """Create a standardized prompt for itinerary generation."""
        try:
            return settings.prompts["itinerary"].format(query=query)
        except (KeyError, ValueError) as e:
            raise ItineraryServiceError(f"Failed to create prompt: {str(e)}") from e

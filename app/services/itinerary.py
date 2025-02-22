import os
from dotenv import load_dotenv
from .llm import LLMFactory

load_dotenv()


class ItineraryService:
    """Service for generating itineraries using LLM"""

    def __init__(self, provider_name: str = "gemini"):
        self.provider = LLMFactory.create_provider(provider_name)

    async def initialize(self) -> None:
        """Initialize the LLM provider"""
        api_key = os.getenv(f"{self.provider.provider_name.upper()}_API_KEY")
        if not api_key:
            raise ValueError(
                f"API key not found for provider {self.provider.provider_name}"
            )
        await self.provider.initialize(api_key)

    async def generate_itinerary(self, query: str) -> str:
        """Generate an itinerary using the configured LLM provider"""
        prompt = self._create_prompt(query)
        return await self.provider.generate_text(prompt)

    def _create_prompt(self, query: str) -> str:
        """Create a standardized prompt for itinerary generation"""
        return (
            "Create a detailed itinerary based on the following request.\n"
            "Format the response in a clear, day-by-day structure with "
            "specific times.\n"
            f"Request: {query}"
        )

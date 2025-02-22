import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


async def generate_itinerary(query: str) -> str:
    """Generate itinerary using Gemini API asynchronously"""
    prompt = f"""
    Create a detailed itinerary based on the following request.
    Format the response in a clear, day-by-day structure with specific times.
    Request: {query}
    """

    # Run the blocking API call in a thread pool
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, lambda: model.generate_content(prompt)
    )
    return response.text

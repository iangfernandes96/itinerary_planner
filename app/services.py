import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


async def generate_itinerary(query: str) -> str:
    prompt = f"""
    Create a detailed itinerary based on the following request.
    Format the response in a clear, day-by-day structure with specific times.
    Request: {query}
    """

    response = model.generate_content(prompt)
    return response.text

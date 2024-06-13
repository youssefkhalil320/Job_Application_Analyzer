import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the generative model with API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the generative model with desired configuration
model = genai.GenerativeModel(
    'gemini-1.5-pro',
    generation_config=genai.GenerationConfig(
        max_output_tokens=2000,
        temperature=0.9,
    )
)

# Start a chat session with an empty history
chat = model.start_chat(history=[])


def gemini_chat(message):
    """
    Send a message to the generative model and return the response text.

    Args:
        message (str): The message to send to the generative model.

    Returns:
        str: The response text from the generative model.
    """
    response = chat.send_message(message)
    return response.text

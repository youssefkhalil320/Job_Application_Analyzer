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

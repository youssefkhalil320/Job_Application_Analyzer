import google.generativeai as genai
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.0-pro-latest')
chat = model.start_chat(history=[])
# response = model.generate_content("The opposite of hot is")
# print(response.text)

prompt = """
- I am a recruiter and you are virtual assistant
- I will provide you with candidate resumes and ask you questions about them
- If i ask you about experience summary please show the year's of experience and the companies he worked for
"""

response = chat.send_message(prompt)


def gemini_chat(message):
    if message == "bye":
        return ""

    response = chat.send_message(message)
    return response.text

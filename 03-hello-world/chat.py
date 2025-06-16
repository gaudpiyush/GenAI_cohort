import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Zero-shot Prompting: The model is given a direct question or task

SYSTEM_PROMPT = """
You are an AI expert in Coding. You only know Python and nothing else.
You help users in solving their Python doubts only and nothing else.
If a user asks something else apart from Python, you can just roast them.
"""

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

chat = model.start_chat(history=[
    {"role": "user", "parts": ["Hey, My name is Piyush"]},
    {"role": "model", "parts": ["Hey Piyush! If you have any Python questions or need help with code, feel free to ask!"]},
    {"role": "user", "parts": ["How to make a chai or tea without milk?"]},
    {"role": "model", "parts": ["Hey Piyush, I’m here to help with Python, not making tea! If you want help brewing some Python code instead, just ask!"]},
])

response = chat.send_message("how to add two numbers in python.")


print(response.text)

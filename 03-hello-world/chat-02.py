import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """
You are an AI expert in Coding. You only know Python and nothing else.
You help users in solving their Python doubts only and nothing else.
If a user tries to ask something else apart from Python, you roast them.

Examples:
User: How to make a Tea?
Assistant: Oh my love! It seems like you don't have a girlfriend.

Examples:
User: How to write a function in python
Assistant: def fn_name(x: int) -> int:
                pass  # Logic of the function
"""

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

chat = model.start_chat(history=[
    {"role": "user", "parts": ["Hey, My name is Piyush"]},
    {"role": "model", "parts": ["Hey Piyush! If you have any Python questions or need help with code, feel free to ask!"]}
])

response = chat.send_message("Why 75 attendence is imp for colleges?")

print(response.text)

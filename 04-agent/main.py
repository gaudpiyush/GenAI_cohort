from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai
import json
import requests
import os
import time  

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who is specialized in resolving user queries.
You work in start, plan, action, observe, output mode.

For the given user query and available tools, plan the step-by-step execution. 
Based on the planning, select the relevant tool from the available tools and perform an action to call the tool.

Wait for the observation and based on the observation from the tool call, resolve the user query.

Rules:
- Follow the Output JSON Format.
- Always perform one step at a time and wait for next input.
- Carefully analyze the user query.

Output JSON Format:
{{
    "step": "string",
    "content": "string",
    "function": "The name of function if the step is action",
    "input": "The input parameter for the function"
}}

Available Tools:
- "get_weather": Takes a city name as input and returns the current weather.
- "run_command": Takes a Linux command as a string and executes it.
"""

messages = [ { "role": "user", "parts": [SYSTEM_PROMPT] } ]
chat = model.start_chat(history=messages)


while True:
    query = input("> ")
    response = chat.send_message(query)
    time.sleep(5)  
    raw = response.text.strip()

    while True:
        if raw.startswith("```json"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        if raw == "":
            print("❌ Gemini response is empty!")
            break

        try:
            parsed_response = json.loads(raw)
        except json.JSONDecodeError:
            print("❌ Gemini did not return valid JSON:")
            print(response.text)
            break

        step = parsed_response.get("step")

        if step == "plan":
            print(f"🧠: {parsed_response.get('content')}")
            response = chat.send_message(
                "Continue with next step. REMEMBER: Reply ONLY in valid JSON format as specified."
            )
            time.sleep(5)
            raw = response.text.strip()
            continue

        if step == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")
            print(f"🛠️: Calling Tool: {tool_name} with input {tool_input}")

            if tool_name in available_tools:
                output = available_tools[tool_name](tool_input)
                response = chat.send_message(json.dumps({
                    "step": "observe",
                    "output": output
                }))
                time.sleep(5)
                raw = response.text.strip()
                continue

        if step == "output":
            print(f"🤖: {parsed_response.get('content')}")
            break

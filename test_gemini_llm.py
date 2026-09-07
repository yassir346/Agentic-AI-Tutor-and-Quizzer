import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(os.environ.get("GEMINI_API_KEY"))

with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

response = client.models.generate_content(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(system_instruction=system_prompt),
    contents="I want to start learning about AI agents. Where should I begin?"
)

print(response.text)
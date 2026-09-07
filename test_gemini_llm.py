from google import genai
from google.genai import types

client = genai.Client(api_key="AQ.Ab8RN6I2os8DGt617sd_bajGcJvrdPJkCdfYfBFJzXjig0WWCw")

with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

response = client.models.generate_content(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(system_instruction=system_prompt),
    contents="I want to start learning about AI agents. Where should I begin?"
)

print(response.text)
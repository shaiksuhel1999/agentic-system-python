import os
from dotenv import load_dotenv
load_dotenv("..\\.env")

from openai import OpenAI

# Initialize the client pointing to OpenRouter's endpoint
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# For GLM 5.3 Flash
completion__ = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages=[{"role": "user", "content": "Analyze this data."}]
)

print(completion__.choices[0].message.content)
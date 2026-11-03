from groq import Groq
from dotenv import load_dotenv
load_dotenv(dotenv_path="..\\.env")
client = Groq(
    timeout=600,
    max_retries=2
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Explain quantum computing in one short paragraph.",
        }
    ],
    stream=True
)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
print()
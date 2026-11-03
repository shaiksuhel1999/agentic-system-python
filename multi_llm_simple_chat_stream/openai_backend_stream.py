from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path="..\\.env")

client = OpenAI(
    timeout=600,
    max_retries=2
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain quantum computing in one short paragraph."}
    ],
    stream=True
)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
print()
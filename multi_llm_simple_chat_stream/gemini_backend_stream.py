from google import genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="..\\.env")

client = genai.Client()


response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="poem on coding in python"
)

for chunk in response:
    print(chunk.text, end="", flush=True)
print()
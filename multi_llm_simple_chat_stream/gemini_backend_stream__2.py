from google import genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="..\\.env")

client = genai.Client()
chat = client.chats.create(model="gemini-2.5-flash",)
response = chat.send_message_stream(message=[
    "poem about the writing code in python"
])

for chunk in response:
    print(chunk.text, end="", flush=True)
print()
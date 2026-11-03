from google import genai

from dotenv import load_dotenv
from pyexpat.errors import messages

load_dotenv(dotenv_path="..\\.env")

client = genai.Client()
chat = client.chats.create(model="gemini-2.5-flash")
response1 = chat.send_message("Hey, I'm Suhel and I'm software engineer")
print("Response: ",  response1.candidates[0].content.parts[0].text)


response2=chat.send_message("who am I? and what I do?")
print("response2: ", response2.candidates[0].content.parts[0].text)
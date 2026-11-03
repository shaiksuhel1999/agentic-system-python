from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="..\\.env")
client = Groq(
    timeout=600 ,
    max_retries=2
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "what is the Importance of fast language models",
        },
        {
            "role": "system",
            "content": """
            Respond only with 300 tokens or less than that and output shouldn't be exceed the 300 tokens: strictlyt follows
            """
        }
    ],
    model="openai/gpt-oss-120b",
)

print(chat_completion.choices[0].message.content)


from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path="..\\.env")

client = OpenAI(timeout=600 ,
                max_retries=2)

chat_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "What is importance of Fast Language Models",
        },
        {
            "role": "system",
            "content": """
            Respond only with 300 tokens or less than that and output shouldn't be exceed the 300 tokens: strictlyt follows
            """
        }
    ]
)

print(chat_response.choices[0].message.content)
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True, dotenv_path="..\\.env")

model = init_chat_model(
    model="gpt-4o-mini",
    temperature=0.3,
    max_tokens=1000,
    max_retries=5
)

response = model.invoke("what's the meaning of back  in machine learning?")
print(response.content)

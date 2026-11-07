from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True, dotenv_path="..\\.env")

system_prompt = SystemMessage("you're an Intelligent Investor")
user_message = HumanMessage("what's the current price of apple stock?")

messages = [user_message, system_prompt]


model = init_chat_model(
    model="gpt-4o-mini",
    temperature=0.3,
    max_retries=5,
    max_tokens=100
)

response = model.invoke(messages)
ai_message = AIMessage(response.content)
messages.append(ai_message)
print(messages)

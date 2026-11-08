from typing import TypedDict, List

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv(dotenv_path="../.env")


# 1. Define runtime context
class UserContext(TypedDict):
    user_name: str
    user_memories: List[str]


# 2. Define tools
@tool
def weather_tool(city: str) -> str:
    """
    This function gives information about the weather in a specific city.
    """
    return city + " is always sunny"


# 3. Define dynamic prompt
@dynamic_prompt
def dynamic(request: ModelRequest) -> str:
    context = request.runtime.context
    user_name = context["user_name"]
    user_memories = context["user_memories"]
    return f"""
You are a personalized AI assistant.

User name: {user_name}

User memories:
{user_memories}

Instructions:
- Personalize responses using the user's context.
- Address the user by their user_name when appropriate.
- Use relevant user_memories to improve your answers.
- Never invent user information.
"""


# 4. Create model
model = ChatOpenAI(model="gpt-4o-mini")


# 5. Create agent
agent = create_agent(
    model=model,
    tools=[weather_tool],
    middleware=[dynamic]
)


# 6. Invoke agent with dynamic context
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What's the weather in Bengaluru?"
            }
        ]
    },
    context=UserContext(
        user_name="Suhel",
        user_memories=[
            "Iam developer",
            "I'm traveller"
        ]
    )
)

print(response["messages"][-1].content)
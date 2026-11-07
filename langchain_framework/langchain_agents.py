from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


@tool
def weather_tool(city: str) -> str:
    """
    This function gives information about the weather in specific city.
    :param city:
    :return: String
    """
    return city + " is always sunny"

load_dotenv(dotenv_path="..\\.env")

model = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(
    model=model,
    tools=[weather_tool]
)

response = agent.invoke({"messages": [{"role": "user", "content": "What's the weather in Bengaluru?"}]})

print(response)
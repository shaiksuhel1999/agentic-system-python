from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path="..\\.env")

@tool
def weather_tool(city: str) -> str:
    """
    This function gives information about the weather in specific city.
    :param city:
    :return: String
    """
    return city + " is always sunny"

client = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    max_retries=5,
    max_tokens=1000
)

# 1. Bind the tools to the model
tools = [weather_tool]
tools_map = {tool.name: tool for tool in tools}
client_with_tools = client.bind_tools(tools)

# 2. Invoke the model with bound tools
response = client_with_tools.invoke("what is the weather in bengaluru?")

for tool_call in response.tool_calls:
    print(tools_map[tool_call["name"]].invoke(tool_call["args"]))

## Manually we have to capture the tool result and send back the response to LLM for summarization
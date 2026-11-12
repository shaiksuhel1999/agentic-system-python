import asyncio
from google.adk import Runner
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from tavily import TavilyClient

client = TavilyClient()


def weather_search(city: str) -> dict:
    """Gets the real-time weather of a specific city.

    Args:
        city: The name of the city to check the weather for.

    Returns:
        A dictionary containing search results for the city's weather.
    """
    response = client.search(
        query=f"What's the weather in {city}",
        max_results=1,
        search_depth="basic",
    )
    return response


root_agent = Agent(
    model=LiteLlm(model="gpt-4o-mini"),
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge.",
    tools=[weather_search],
)

session_service_gpt = InMemorySessionService()
APP_NAME_GPT = "weather_tutorial_app_gpt"
USER_ID_GPT = "user_1_gpt"
SESSION_ID_GPT = "session_001_gpt"


async def main():
    await session_service_gpt.create_session(
        app_name=APP_NAME_GPT,
        user_id=USER_ID_GPT,
        session_id=SESSION_ID_GPT,
    )

    runner = Runner(
        session_service=session_service_gpt,
        app_name=APP_NAME_GPT,
        agent=root_agent,
    )

    events = runner.run(
        user_id=USER_ID_GPT,
        session_id=SESSION_ID_GPT,
        new_message=Content(
            role="user", parts=[Part(text="What's the weather in Hyderabad?")]
        ),
    )

    for event in events:
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
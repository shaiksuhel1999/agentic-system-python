
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")


# 1. Define tools

@tool
def search_tool(query: str) -> str:
    """Search for information using the given query."""
    return query + " is done"


@tool
def send_email_tool(recipient: str, message: str) -> str:
    """Send an email to the specified recipient."""
    return f"Email sent to {recipient}"


@tool
def delete_database_tool(database_name: str) -> str:
    """Delete the specified database."""
    return f"Database {database_name} deleted"


# 2. Create agent with HITL middleware

agent = create_agent(
    model="gpt-5.5",
    tools=[
        search_tool,
        send_email_tool,
        delete_database_tool
    ],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                # Require human approval
                "send_email_tool": True,
                "delete_database_tool": True,

                # Automatically execute
                "search_tool": False,
            }
        )
    ],
    checkpointer=InMemorySaver()
)


# 3. Configure thread

config = {
    "configurable": {
        "thread_id": "some_id"
    }
}


# 4. Invoke agent

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Send an email to textures@gmail.com "
                    "with the message: Hello team!"
                )
            }
        ]
    },
    config=config
)


# 5. Check for human approval interrupt

if "__interrupt__" in result:

    print("\nWaiting for human approval...")

    for interrupt in result["__interrupt__"]:
        print(interrupt.value)

    # 6. Resume after approval

    result = agent.invoke(
        Command(
            resume={
                "decisions": [
                    {
                        "type": "approve"
                    }
                ]
            }
        ),
        config=config
    )

else:
    print("\nNo human approval required.")


# 7. Display final response

print("\nFinal Response:")

for message in result["messages"]:
    if message.type == "ai" and message.content:
        print(message.content)

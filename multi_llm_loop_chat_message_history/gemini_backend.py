from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal, List


class StepContent(BaseModel):
    # Gemini API uses "model" instead of "assistant"
    role: Literal["user", "model"]
    content: str


class MultiStepContent(BaseModel):
    steps: List[StepContent]


load_dotenv(dotenv_path="..\\.env")
chat_client = genai.Client()

# System instructions should be set in config, not passed as a user message
system_prompt = "You're an intelligent system"
config = types.GenerateContentConfig(
    system_instruction=system_prompt
)

message_history = MultiStepContent(steps=[])


def chat():
    # Convert Pydantic models into a format the Gemini SDK understands
    formatted_contents = [
        types.Content(
            role=step.role,
            parts=[types.Part.from_text(text=step.content)]
        )
        for step in message_history.steps
    ]

    chat_response = chat_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=formatted_contents,
        config=config  # Pass the system prompt here
    )
    return chat_response.text  # Simpler shortcut to get the text directly


def invoke():
    try:
        while True:
            user_query = input("👤> ")
            if user_query.lower() in ["exit", "quit", "bye"]:
                print("🤖> bye🙂")
                break

            message_history.steps.append(StepContent(
                role="user",
                content=user_query
            ))

            chat_response = chat()

            message_history.steps.append(StepContent(
                role="model",
                content=chat_response
            ))
            print("🤖> ", chat_response)
    except Exception as e:
        print("Exiting the session due to the error: ", e)


if __name__ == "__main__":
    invoke()

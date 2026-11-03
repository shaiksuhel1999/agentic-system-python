from google import genai
from dotenv import load_dotenv
from google.genai import types
from mem0 import MemoryClient
from typing import List
from pydantic import BaseModel, Field

## Initializing

load_dotenv(verbose=True, dotenv_path="..\\.env")
gemini_client = genai.Client()
mem0_client = MemoryClient()

# System instructions should be set in config, not passed as a user message
system_prompt = (
    "you're an intelligent advisor. "
    "you always respond based on user memories. "
    "user_memories: {memories}")

## Base models
class RequestModel(BaseModel):
    role: str = Field(..., description="The role of the message author, e.g., 'user' or 'assistant'")
    content: str = Field(..., description="The text content of the message")

## memory implementation

def add_to_memory(messages, user_id):
    try:
        mem0_client.add(messages=messages, user_id=user_id)
    except Exception as e:
        print(f"Mem0 Adding Warning: {e}")


def get_specific_memory(query, user_id) -> List[str]:
    try:
        results_list = mem0_client.search(
            query=query,
            filters={"user_id": user_id},
        )
        return [item["memory"] for item in results_list["results"] if "memory" in item]
    except Exception as e:
        print(f"Mem0 Get Warning: {e}")
        return []

def get_memory(user_id)-> List[str]:
    try:
        results_lists = mem0_client.get(
            filters={"user_id": user_id}
        )
        return [item["memory"] for item in results_lists["results"] if "memory" in item]
    except Exception as e:
        print(f"Mem0 Get Warning: {e}")
        return []

## LLM Chat
def chat(request: RequestModel, config: types.GenerateContentConfig)-> str:
    try:
        formatted_content = types.Content(
            role=request.role,
            parts=[types.Part.from_text(text=request.content)]
        )

        chat_response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            config=config,
            contents=formatted_content,

        )
        return chat_response.text
    except Exception as e:
        print(f"LLM chat Error: {e}")
        return str("no result")

## User Invocation
def invoke():
    user_id = input("👤 Enter user ID: ").strip()
    if not user_id:
        user_id = "default_user"

    print("🤖> Memory chat initialized. Type 'exit' or press Ctrl+C to quit.\n")

    try:
        while True:
            user_query = input("👤 User Question / Followup > ").strip()

            if not user_query:
                continue

            if user_query.lower() in ["exit", "bye", "quit"]:
                print("🤖> bye🙂")
                break

            # 1. Fetch short-term/long-term context from Mem0
            memory_result = get_specific_memory(user_query, user_id)
            if len(memory_result) == 0:
                memory_result = get_memory(user_id)
            request = RequestModel(role="user", content=user_query)
            config = types.GenerateContentConfig(
                system_instruction=system_prompt.format(memories=memory_result),
            )
            chat_response = chat(request, config)
            print("🤖> ", chat_response)

            # 3. Stream the interaction back into Mem0 to update the profile
            add_to_memory([
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": chat_response}
            ], user_id)

    except KeyboardInterrupt:
        print("\n🤖> Chat interrupted by user. Goodbye! 🙂")


if __name__ == "__main__":
    invoke()




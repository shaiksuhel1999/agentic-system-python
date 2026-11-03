import os
from typing import List
from openai import OpenAI
from mem0 import MemoryClient
from dotenv import load_dotenv

# Load environmental variables
load_dotenv(dotenv_path="..\\.env")

# Initialize API clients
open_client = OpenAI(
    timeout=600,
    max_retries=5
)
mem0_client = MemoryClient()

system_content = (
    "you're an intelligent advisor. "
    "you always respond based on user memories. "
    "user_memories: {memories}")


def get_user_specific_memories(query: str, user_id: str) -> List[str]:
    try:
        results_list = mem0_client.search(
            query=query,
            filters={"user_id": user_id}
        )
        return [item["memory"] for item in results_list["results"] if "memory" in item]
    except Exception as e:
        print(f"\n[Mem0 Search Warning: {e}]")
        return []

def get_user_all_memories(user_id: str) -> List[str]:
    try:
        results_list = mem0_client.get_all(filters={"user_id": user_id})
        return [item["memory"] for item in results_list["results"] if "memory" in item]
    except Exception as e:
        print(f"\n[Mem0 Search Warning: {e}]")
        return  []


def add_to_memory(messages: List[dict], user_id: str):
    try:
        # Explicitly pass the array to the 'messages' parameter
        mem0_client.add(messages=messages, user_id=user_id)
    except Exception as e:
        print(f"\n[Mem0 Save Warning: {e}]")


def chat(user_query: str, user_memory: List[str]) -> str:
    # Convert list of memories to a clean, comma-separated string string
    memories_str = ", ".join(user_memory) if user_memory else "None"

    char_response = open_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_content.format(memories=memories_str)
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )
    return char_response.choices[0].message.content


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
            memory_result = get_user_specific_memories(user_query, user_id)
            if len(memory_result) == 0:
                memory_result = get_user_all_memories(user_id)
            chat_response = chat(user_query, memory_result)
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

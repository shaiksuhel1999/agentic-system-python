from mem0 import MemoryClient
from groq import Groq
from dotenv import load_dotenv
from typing import List

load_dotenv(dotenv_path="..\\.env")
mem0_client=MemoryClient()
groq_client=Groq(
    timeout=600,
    max_retries=5
)

system_content = (
    "you're an intelligent advisor. "
    "you always respond based on user memories. "
    "user_memories: {memories}")

def get_user_specific_memories(query, user_id) -> List[str]:
    try:
        results_list = mem0_client.search(
            query=query,
            filters={"user_id": user_id},
        )
        return [item["memory"] for item in results_list["results"] if "memory" in item]
    except Exception as e:
        print(f"Mem0 Searching Warning: {e}")
        return []

def get_user_all_memories(user_id)-> List[str]:
    try:
        results_list = mem0_client.get_all(
            filters={"user_id": user_id},
        )
        return [iter["memory"] for item in results_list["results"] if "memory" in item]
    except Exception as e:
        print(f"Mem0 Searching Warning: {e}")
        return []

def add_to_memory(messages: List[dict], user_id: str):
    try:
        # Explicitly pass the array to the 'messages' parameter
        mem0_client.add(messages=messages, user_id=user_id)
    except Exception as e:
        print(f"\n[Mem0 Save Warning: {e}]")


def chat(user_query, user_memories)-> str:
    chat_response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages = [
            {
                "role": "system",
                "content": system_content.format(memories=user_memories)
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )
    return chat_response.choices[0].message.content

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
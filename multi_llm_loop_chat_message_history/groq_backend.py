from groq import Groq
from dotenv import load_dotenv


load_dotenv(dotenv_path="..\\.env")

client = Groq(
    timeout=600,
    max_retries=2
)
system_prompt="you're an intelligent system"
message_history=[{
    "role": "system",
    "content": system_prompt
}]



def chat()-> str:
    chat_response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=message_history
    )
    return chat_response.choices[0].message.content

def invoke():
    try:
        while True:
            user_query = input("👤> ")
            if user_query == "exit" or user_query == "quit" or user_query == "bye":
                print("🤖 > bye🙂")
                break
            message_history.append({
                "role": "user",
                "content": user_query
            })
            chat_response = chat()
            if chat_response:
                message_history.append({
                    "role": "assistant",
                    "content": chat_response
                })
                print("🤖 > ", chat_response)
    except Exception as e:
        print("Exiting the session due to the error: ", e)

if __name__ == "__main__":
    invoke()


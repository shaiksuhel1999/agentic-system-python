import asyncio
from google import genai
from typing import List, AsyncGenerator

from google.genai import types
from google.genai.types import GenerateContentConfig
from mem0 import MemoryClient
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header
from fastapi.responses import StreamingResponse

## System prompts
system_prompt = (
    "you're an intelligent advisor. "
    "you always respond based on user memories. "
    "user_memories: {memories}"
)

load_dotenv(verbose=True, override=True, dotenv_path="..\\.env")
app = FastAPI()
gemini_client = genai.Client()
mem0_client = MemoryClient()


async def add_to_memory(messages: List[dict], user_id: str):
    try:
        mem0_client.add(messages=messages, user_id=user_id)
    except Exception as e:
        print(f"Mem0 Adding Warning: {e}")

async def get_from_memory(query, user_id: str) -> List[str]:
    try:
        results_list = mem0_client.search(
            query=query,
            filters={
                "user_id": user_id,
            }
        )
        return [item["memory"] for item in results_list["results"] if "memory" in item]
    except Exception as e:
        print(f"Mem0 Getting Warning: {e}")
        return []

async def get_all_from_memory(user_id) -> List[str]:
    try:
        results_list = mem0_client.get_all(
            filters={
                "user_id": user_id,
            }
        )
        return [item["memory"] for item in results_list["results"] if "memory" in item]
    except Exception as e:
        print(f"Mem0 Getting Warning: {e}")
        return []

async def chat(user_query: str, user_id: str, user_memories: List[str]) -> AsyncGenerator[str, None]:
    config = GenerateContentConfig(
        system_instruction=system_prompt.format(memories=",".join(user_memories)),
    )
    formatted_contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_query)]
        )
    ]
    chat_response = await asyncio.to_thread(
        gemini_client.models.generate_content_stream,
        model="gemini-2.5-flash",
        config =config,
        contents=formatted_contents,
    )
    assistant_response = ""
    for chunk in chat_response:
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            assistant_response += content
            yield f"{content} "

    # Stitched payload conversation sync
    if assistant_response.strip():
        mem0_message = [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": assistant_response}
        ]
        await asyncio.to_thread(add_to_memory, mem0_message, user_id)


@app.middleware('http')
async def middleware(request: Request, call_next):
    response = await call_next(request)
    return response


@app.get("/stream/{prompt}")
async def stream_prompt(prompt: str, user_id: str = Header(..., alias="user_id")):
    user_memories = await asyncio.to_thread(get_from_memory, prompt, user_id)
    return StreamingResponse(
        chat(user_query=prompt, user_id=user_id, user_memories=user_memories),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        },
    )
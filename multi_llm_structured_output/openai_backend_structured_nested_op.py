from typing import List

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(verbose=True, override=True, dotenv_path="..\\.env")

class Steps(BaseModel):
    explanation: str = Field(..., title="explanation")
    output: str = Field(..., title="output")

class MathematicalReasoning(BaseModel):
    steps: List[Steps] = Field(..., title="steps")
    final_answer: str = Field(..., title="final answer")

client = OpenAI(
    timeout=600,
    max_retries=2
)

response = client.responses.parse(
    model="gpt-4o-mini",
    input=[
        {
            "role": "system",
            "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
        },
        {"role": "user", "content": "how can I solve 8x + 7 = -23"},
    ],
    text_format=MathematicalReasoning
)
print(response.output_text)


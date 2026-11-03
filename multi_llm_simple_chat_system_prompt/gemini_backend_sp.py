import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Literal

# Load environmental variables
load_dotenv(dotenv_path="..\\.env")

# 1. Define the Structured Output Schema using Pydantic
class StepContent(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ExecutionStep(BaseModel):
    step: Literal["start", "plan", "research", "observe", "summarize", "output"]
    content: StepContent

class MultiStepResponse(BaseModel):
    steps: List[ExecutionStep]

# Initialize the Gemini GenAI client
client = genai.Client()

user_template = "explain about the {subject} in {words} words"

# Clean system instructions emphasizing the step-by-step thinking breakdown
system_instruction = """
You are an intelligent student who knows all subjects. 
Break down your entire thinking, planning, and execution process into granular steps 
before providing the final answer in the 'output' step.
"""

# Configure the request to force a JSON structure matching our Pydantic model
config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    response_mime_type="application/json",
    response_schema=MultiStepResponse,
    temperature=0.2, # Lower temperature helps follow complex structures strictly
)

# Format the user prompt
formatted_user_prompt = user_template.format(subject="maths", words=100)

# Make the streaming call using the correct SDK syntax
response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=formatted_user_prompt,
    config=config
)

# Print chunks as they stream in
print("--- STREAMING STRUCTURED JSON ---")
for chunk in response:
    if chunk.text:
        print(chunk.text, end="", flush=True)
print()
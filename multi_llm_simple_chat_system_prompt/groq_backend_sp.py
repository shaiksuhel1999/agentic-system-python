from groq import Groq
from dotenv import load_dotenv
from pydantic.v1 import BaseModel

load_dotenv(dotenv_path="..\\.env")

client = Groq(
    timeout=600,
    max_retries=2,
)

user_content="""
explain about the {subject} in {words} words
"""

system_content="""
you're an Intelligent student and you know all the subjects
you should perform in below format

{steps: start | plan | research | observe | summarize| output, content: {role: user| assistant, content: text}}
elaborate to more steps

example:
{ step: start, content: {role: user, content: what is calculus?}
{ step; plan, content: {role: assistant, content: searching for it}
{ step; plan, content: {role: assistant, content: found it}
{ step; output, content: {role: assistant, content: result}
"""

chat_response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": user_content.format(subject="maths", words=100)
        }
    ],
    stream=True
)

for chunk in chat_response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
print()
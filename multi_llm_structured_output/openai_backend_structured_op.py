from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(verbose=True, override=True, dotenv_path="..\\.env")
class Family(BaseModel):
    family_name: str = Field(..., alias="family_name", description="This field defines the family name.")
class Persona(BaseModel):
    name: str = Field(..., alias="name", description="This field specifies the person's name.")
    age: int = Field(..., alias="age", description="This field specifies the person's age.")
    place: int = Field(..., alias="place", description="This field specifies the person's place.")
    family_name: Family = Field(..., alias="family_name", description="This field defines the family name.")

client = OpenAI(
    timeout=600,
    max_retries=2
)

response = client.responses.parse(
    model="gpt-4o-mini",
    input=[
        {
            "role": "system",
            "content": "you're an intelligent family info capturer"
        },
        {
            "role": "user",
            "content": "hey there!, I'm Jhon , 27 years old , stay at Bengaluru, by the way my last name is Doe"
        }
    ],
    text_format=Persona
)
print(response.output_parsed)


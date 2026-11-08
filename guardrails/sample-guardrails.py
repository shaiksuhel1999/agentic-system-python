from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True, dotenv_path="..\\.env")

model = ChatOpenAI(
    model="gpt-4o-mini",
    max_retries=5,
    streaming=True
)

agent = create_agent(
    model=model,
    middleware=[
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
            apply_to_output=True,
            apply_to_tool_results=True
        ),
        PIIMiddleware(
            "email",
            strategy="hash",
            apply_to_input=True,
            apply_to_tool_results=True,
            apply_to_output=True
        ),
        # Custom PII middleware for account numbers using a regular expression
        PIIMiddleware(
            "account_number",
            strategy="mask",
            detector=r"\b\d{9,18}\b",  # Matches any standalone 9 to 18-digit number
            apply_to_input=True,
            apply_to_tool_results=True,
            apply_to_output=True
        )
    ]
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": (
            "My credit card number is 5105-1051-0510-5100 and my email is shaiksuhelbasha@gmail.com"
            " and my bank account number is 123456789012."
            "Can you explain how I can protect these details"
            "when making online transactions?"
            "Do not repeat my actual financial information."
        )
    }]
})

print(result)

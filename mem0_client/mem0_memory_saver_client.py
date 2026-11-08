from mem0 import  MemoryClient
from dotenv import load_dotenv
load_dotenv(dotenv_path="..\\.env")
memory_client = MemoryClient()
# messages = []
# memory_client.add(messages, user_id="<user-id>")
# query = "<query-here>"
result = memory_client.search("hello", filters={"user_id": "shaiksuhelbasha16.509@gmail.com"})
print(result)

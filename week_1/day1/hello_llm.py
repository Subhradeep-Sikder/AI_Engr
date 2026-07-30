import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
role="user"
prompt="Do you know Padho with Pratyush"
# message me role and content
message={
    "role": role,
    "content": prompt
}

messages=[message]

response=client.chat.completions.create(model=model, messages=messages)
print(response)

print("#######################################")

answer=response.choices[0].message.content
print(answer)



# $ uv init day1
# $ uv venv --python 3.14.3
# .\.venv\Scripts\activate.ps1
# python --version
# code hello_llm.py
# uv add groq python-dotenv
# python ./hello_llm.py
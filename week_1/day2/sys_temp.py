import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your .env file.")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
role="user"
prompt="suggest a name for my clothing company"

#system
message_system = {
    "role": "system",
    "content": "you are a professional branding expert and you are helping a user come up with a name for their clothing company"
}

#message me role and content
message={
    "role": role,
    "content": prompt
}

messages=[message_system,message]

#temperature by default is 0 meaning safe, range is [0,2]
response=client.chat.completions.create(model=model, messages=messages, temperature=2)


print("#######################################")

answer=response.choices[0].message.content
print(answer)
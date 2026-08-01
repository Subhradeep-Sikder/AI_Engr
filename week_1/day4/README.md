

---

# AI Engineer Course — Day 05: Pydantic + JSON & Structured Output

---

## 1. Prerequisites & Lecture Context

* **Sequential Learning:** The instructor emphasizes starting from Day 1 / Intro episode rather than jumping directly into Day 5 to avoid confusion regarding prerequisites (such as whether Python is required).
* **Objective:** Move beyond basic trial-and-error text generation into building production-ready, deterministic backend applications that can consume LLM outputs seamlessly.

---

## 2. Why Structured Output? (Unstructured vs. Structured Output)

### The Problem with Plain Text Output

Up to Day 4, LLM interactions primarily returned unstructured text (plain strings or markdown). While easy for human reading, unstructured text causes severe limitations in software engineering:

* **Parsing Fragility:** Hard to programmatically extract specific key values using regex or substring indexing.
* **Lack of Validation:** Non-deterministic output structures can cause backend errors when fed directly into databases or secondary API pipelines.

### The Solution: Structured Output (JSON + Pydantic)

Enforcing structured output guarantees that the LLM returns data strictly conforming to a defined schema (JSON), making it instantly readable by both humans and automated downstream software modules.

---

## 3. Core Concepts Covered

### A. Pydantic (`BaseModel` & `Field`)

* **Pydantic** is Python's standard library for data validation using Python type annotations.
* **`BaseModel`**: The base class for defining data schemas.
* **`Field`**: Used to supply metadata, field constraints, and detailed description prompts to guide the LLM on what each attribute represents.

### B. Structural Schema Definition

By passing a Pydantic model into the LLM API call (`response_format`), the model is constrained at the decoding level to generate syntactically valid JSON matching the specified class.

---

## 4. Step-by-Step Code Implementation

### Example: Extracting Support Ticket Data

The demonstration extracts structured entity fields (Customer Name, Email, and Issue) from unstructured customer support message text.

```python
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

#strcture it 
from pydantic import BaseModel
class Ticket(BaseModel):
    name: str
    email: str
    issue: str

schema=Ticket.model_json_schema()

response_format={
    "type": "json_object",
}

system_prompt=f"""
Extract the personal information from the ticket strictly based on this schema and give a json output.
{schema}
"""

message_system={
    "role": "system",
    "content": system_prompt
}

text="Hello My name is Pratyush. Yesterday I broke up with my girlfriend sheetal I have an iphone which is not working at all. My address is delhi. My email is abc@gmail.com. My contact number is 82134"


prompt=f"""
This is a customer ticket. Please extract the personal information from this.
{text}
"""

# message me role and content
message={
    "role": role,
    "content": prompt
}

messages=[message_system,message]

response=client.chat.completions.create(model=model, messages=messages, response_format=response_format)


answer=response.choices[0].message.content
print(answer)


print("#######################################")


# isko padhte kaise hai
import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)


# inko pass kr sakte hai aage!
print(ticket.name)
print(ticket.email)
print(ticket.issue)


# $ uv init day1
# $ uv venv --python 3.14.3
# .\.venv\Scripts\activate.ps1
# python --version
# code json_pydantic.py
# uv add groq python-dotenv pydantic
# python ./json_pydantic.py

```

### Execution Output Flow

```text
Extracted Name : Pratyush
Extracted Email: pratyush@example.com
Extracted Issue: iPhone not working

```

---


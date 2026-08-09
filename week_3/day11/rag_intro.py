import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"


# step 1 : create knowledge base
knowledge_base = {
    "age": "subhra age is 20",
    "name": "subhra name is subhra",
    "net worth": "subhra net worth is 1000000"
}

# step 2 : retrieval
def retrieve_info(question):
    question = question.lower()
    if "age" in question:
        return knowledge_base["age"]
    elif "name" in question:
        return knowledge_base["name"]
    elif "net worth" in question:
        return knowledge_base["net worth"]
    else:
        return "I don't know"


def ask_llm(question):

    context = retrieve_info(question)
    sys_prompt = f"""answer in one line only. Answer only based on this context. do not hallucinate. Context: {context}"""

    system_message={
        "role": "system",
        "content": sys_prompt
    }

    message={
        "role": "user",
        "content": question
    }

    messages=[system_message, message]
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    answer = response.choices[0].message.content
    return answer


question = "What is subhra car name ?"
print(ask_llm(question))
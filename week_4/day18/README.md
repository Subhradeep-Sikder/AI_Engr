# Day 18: Our First AI Agent | AI Engineer Course

> **Lecturer:** Pratyush  
> **Source:** [YouTube Video](https://youtu.be/RNj0AY4VueA)  
> **Course:** Free AI Engineer Course (8 Weeks)

---

## 1. Introduction and Concept of AI Agents

### 1.1 What is an AI Agent?

* An **AI Agent** is a combination of a core Large Language Model (LLM) and external capabilities such as functions, tools, or API access.
* **Formula:**
  $$\text{AI Agent} = \text{Core LLM} + \text{Functions / APIs / Tools Access}$$
* Standard LLMs operate purely on natural language and token probability predictions; they cannot reliably perform arithmetic computations or fetch real-time external data on their own.
* When an LLM is granted access to an external execution tool (e.g., a Python interpreter or calculator), it transforms into an AI Agent.

> **Example from video:**  
> ChatGPT cannot multiply very large numbers directly through next-token prediction. To solve this, ChatGPT uses a Python interpreter/calculator. A base LLM connected to a Python calculator tool forms an AI Agent capable of accurate math calculations.

---

### 1.2 Purpose of this Introduction

* Demonstrates how to build an AI Agent from scratch using pure Python and LLM API calls without relying on high-level frameworks.
* Serves as a foundational prerequisite for upcoming lectures on **LangGraph**.
* Understanding manual agent architecture is essential before using LangGraph to manage and orchestrate multi-agent systems.

---

## 2. Real-World Agent Examples & Tool Terminology

### 2.1 Real-World Application Use Cases

* **Flight Booking Agent:** Core LLM + Paytm Flight Booking API
  * The LLM takes user requests (e.g., *"Book a flight from Bangalore to Delhi"*), queries the Paytm API for available flights and prices, and completes the booking on the user's behalf using stored user details and payment credentials.

* **Movie Ticket Booking Agent:** Core LLM + BookMyShow API
  * A base LLM cannot check movie showtimes or buy tickets independently. Giving the LLM access to the BookMyShow API enables it to query showtimes for a movie (e.g., *Toxic*) and purchase tickets.

* **Advanced Multi-Action Agent:** Core LLM + Telegram API + Email API + Calling API
  * An agent with multiple API integrations can autonomously send messages on Telegram, dispatch emails, or make phone calls depending on user requests.

### 2.2 Terminology: Functions vs. Tools

| Engineering Domain | Terminology | Description |
| :--- | :--- | :--- |
| **Standard Software Engineering** | **Functions / APIs** | Standard executable routines or endpoints. |
| **AI Agent Architecture** | **Tools** | Functions and API endpoints made available to an LLM. |

* In standard software engineering, executable routines are called **Functions** or **APIs**.
* In AI Agent terminology, functions and API endpoints made available to an LLM are called **Tools**.

---

## 3. Designing a Dual-Tool AI Agent (Web Search & Math Calculator)

### 3.1 Goal of the AI Agent

Build an AI Agent capable of performing two distinct tasks:
1. **Mathematical Calculations:** Add, subtract, multiply, and divide arithmetic expressions.
2. **Web Searching:** Retrieve live, up-to-date facts and news from the internet.

---

### 3.2 Defining the Two Tools

1. **Math Tool (`calculate`):**
   * A Python function that accepts a string math expression (e.g., `"2 + 2"` or `"10 * 21"`) and evaluates it to return the numerical answer.

2. **Web Search Tool (`web_search`):**
   * A Python function that integrates with the **Tavily API** (a search engine API optimized for AI models).
   * Accepts a search query string (e.g., `"Who is Pratyush Narayan?"`), queries Tavily, and returns real-time web search results without opening a browser manually.

> **Example from video:**  
> If a user asks `"Give me answer of 10 * 21"` vs. `"Who is Pratyush Narayan?"`, the LLM must route the first query to the `calculate` tool and the second query to the `web_search` tool.

---

## 4. Tool Schemas and LLM Tool Selection Mechanism

### 4.1 How the LLM Knows Which Tool to Use

* The LLM itself does not run Python functions directly; it decides *which* function to call and *what arguments* to pass based on structured JSON tool descriptions provided by the developer.

### 4.2 Anatomy of a Tool Schema (JSON Structure)

For every tool provided, the developer defines a schema containing:

* **`type`:** Specifies the tool type (e.g., `"function"`).
* **`name`:** Exact name of the Python function (e.g., `"web_search"`, `"calculate"`).
* **`description`:** Explains **when** and **why** the LLM should use this tool.
  * *Crucial Role:* Because LLMs have training cutoff dates, the description informs the LLM to use `web_search` for current events, prices, or facts that change over time.
* **`parameters`:** JSON Schema defining input arguments, data types (e.g., `string`), and required fields.

> **Schema Descriptions from Video:**  
> * **`web_search` Description:** `"Search the web for up-to-date information, recent events, or facts that may have changed."`  
> * **`calculate` Description:** `"Perform mathematical calculations such as addition, subtraction, multiplication, and division."`

---

## 5. Agent Execution Loop, System Prompts, and Iteration Limits

### 5.1 API Configuration & Parameters

* **System Prompt:** Sets the agent's identity and instructions (e.g., `"You are an AI Agent. Use web_search for changing or current information and calculate for mathematical calculations."`).
* **`tools` Parameter:** Passes the list of JSON tool schemas into `groq.chat.completions.create(..., tools=tools)`.
* **`tool_choice="auto"`:** Instructs the LLM to automatically decide whether to call a tool or respond directly based on the user prompt.

---

### 5.2 Multi-Step Execution & Iteration Limits

* **Layered/Multi-Step Tasks:** Tasks like *"Find who Pratyush Narayan is, find his YouTube channel name, and check how many subscribers it has"* cannot be solved in a single web search call; they require sequential tool iterations.
* **Why Iteration Limits are Mandatory:**
  * If a user gives an impossible task (e.g., *"Build GTA 6"*), an unconstrained LLM might loop infinitely making tool calls.
  * Setting a maximum iteration limit (e.g., `max_iterations = 3`) halts execution after 3 attempts, preventing token burning and exhausting free API credits (e.g., Tavily's 1000 free search credits).

---

## 6. Live Prompt-Driven Coding Walkthrough with Claude

### 6.1 Prompting the AI to Generate the Agent Code

* Rather than manually writing every line of boilerplate code, the lecturer writes a detailed English prompt instructing Claude to generate the entire single-file Python AI Agent.
* **Key prompt constraints provided to Claude:**
  * Use Groq LLM with a supported model (e.g., `openai/gpt-oss-120b`).
  * Load `GROQ_API_KEY` and `TAVILY_API_KEY` from `.env` using `python-dotenv`.
  * Define two Python functions: `web_search` (using Tavily API) and `calculate` (evaluating string math expressions).
  * Construct standard JSON tool schemas (`type`, `name`, `description`, `parameters`).
  * Set `tool_choice="auto"` and implement an interactive CLI loop with an iteration limit.

---

### 6.2 Execution Verification in Terminal

* **Query 1:** `"Who is Pratyush Narayan?"`
  * The LLM analyzes the prompt, identifies it as a query needing current web facts, triggers `web_search` with argument `query="Pratyush Narayan"`, queries Tavily, and returns the biography.
* **Query 2:** `"What is 3 * 90?"`
  * The LLM identifies the math expression, triggers `calculate` with argument `expression="3 * 90"`, evaluates it via Python, and returns `270`.

---

### Code Implementation

```python
import os
import ast
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

# Load Environment Variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize Clients
groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# 1. Define Tool Functions
def web_search(query: str) -> str:
    """Performs web search using Tavily API."""
    response = tavily_client.search(query=query)
    return str(response)

def calculate(expression: str) -> str:
    """Evaluates basic mathematical expressions safely."""
    try:
        # Evaluates string mathematical expressions
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

# Map Function Names to Callable Objects
available_functions = {
    "web_search": web_search,
    "calculate": calculate
}

# 2. Define Structured Tool Schemas for LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for up-to-date information, current events, recent prices, or facts that may have changed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A concise web search query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations such as addition, subtraction, multiplication, and division.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression string, e.g., '3 * 90' or '2 + 2'."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 3. Agent Runner Function with Iteration Limits
def run_agent(user_query: str, max_iterations: int = 3):
    messages = [
        {
            "role": "system",
            "content": "You are an AI Agent. Use web_search for changing or current information, and calculate for mathematical calculations."
        },
        {"role": "user", "content": user_query}
    ]
    
    for iteration in range(max_iterations):
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # Check if the LLM requested a tool call
        if response_message.tool_calls:
            messages.append(response_message)
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = ast.literal_eval(tool_call.function.arguments)
                
                # Execute the corresponding Python function
                function_to_call = available_functions[function_name]
                tool_output = function_to_call(**function_args)
                
                # Feed tool output back to the LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_output)
                })
        else:
            # Final text response from LLM
            return response_message.content
            
    return "Reached maximum iterations without completing task."

# Interactive Loop
if __name__ == "__main__":
    query = input("Ask something: ")
    answer = run_agent(query)
    print("Answer:", answer)
```

---

## 7. Limitations of Manual Agent Building & Need for LangGraph

### 7.1 Scalability Bottlenecks of Pure Python Agents

* Writing manual tool schemas, dispatcher mapping dictionaries, and multi-turn message loops for 2 tools requires substantial boilerplate code.
* As agents scale to enterprise complexity (e.g., dozens of agents, each possessing 20+ specialized tools for email, phone calls, databases, and messaging), managing state and execution manually in a single Python file becomes unmaintainable.

### 7.2 Role of LangGraph

* **LangGraph** serves as a management and orchestration system for AI Agents.
* Handles multi-agent coordination, state persistence, error recovery, and tool routing without writing repetitive low-level message dispatcher loops.

---

## Quick Revision Summary

1. An AI Agent is defined as a base LLM combined with tools, APIs, or executable functions (`AI Agent = Core LLM + Tools`).
2. LLMs operate on language probabilities and cannot perform exact arithmetic or fetch live web facts without external tools.
3. Real-world agents integrate APIs like Paytm (Flight Booking) or BookMyShow (Movie Tickets).
4. In agent architecture, functions and APIs made available to an LLM are called **Tools**.
5. Web search tools for LLMs often use specialized search APIs like **Tavily**.
6. LLMs select tools using structured JSON Tool Schemas containing `type`, `name`, `description`, and `parameters`.
7. The `description` property in a tool schema tells the LLM *when* and *why* to use a specific tool.
8. Tool integration in Groq/OpenAI APIs uses `tools=tools` and `tool_choice="auto"`.
9. Multi-step queries require iterative tool execution loops (ReAct loop).
10. Setting an `iteration limit` (e.g., max 3 iterations) prevents infinite execution loops, token burning, and API credit exhaustion on impossible tasks.
11. Writing manual agent code becomes tedious as tool counts scale.
12. **LangGraph** acts as an orchestration framework to manage complex multi-agent systems and tool routing cleanly.

---

## Definitions (from Video Only)

* **AI Agent:** A system comprising a core Large Language Model (LLM) integrated with external tools, APIs, or executable functions.
* **Tool:** A Python function, API endpoint, or external service made accessible to an LLM within an agent framework.
* **Tavily:** A search engine API optimized for AI models and LLMs to fetch real-time web search results.
* **Tool Schema:** A structured JSON object describing a tool's type, name, purpose description, and parameter types to an LLM.
* **`tool_choice="auto"`:** An API parameter instructing the LLM to automatically decide whether to call a tool or output natural text.
* **Iteration Limit:** A safety threshold restricting the maximum number of consecutive tool calls an agent can execute for a single request.
* **LangGraph:** A management and orchestration framework used to structure, coordinate, and control complex multi-agent systems.

---

## Examples Used in Video

* **ChatGPT Calculator:** ChatGPT accessing a Python interpreter to execute large number multiplications.
* **Paytm Flight Booking Agent:** An LLM calling the Paytm API to check flight availability and prices between Bangalore and Delhi and complete bookings.
* **BookMyShow Movie Ticket Agent:** An LLM calling BookMyShow API to query showtimes for the movie *Toxic* and purchase tickets.
* **Tavily Search vs. Calculator Routing:**
  * Query `"Who is Pratyush Narayan?"` $\rightarrow$ LLM selects `web_search` tool.
  * Query `"Give me answer of 10 * 21"` or `"What is 3 * 90?"` $\rightarrow$ LLM selects `calculate` tool.
* **Layered Task Execution:** Searching `"Who is Pratyush Narayan?"`, discovering his YouTube channel name (*Padho with Pratyush*), and checking subscriber counts over 3 sequential tool iterations.
* **Impossible Task Boundary:** Asking an agent to `"Build GTA 6"` or `"Write a research paper to guarantee a job at Google"`, triggering the iteration cap to prevent endless looping.

---

## Code Written in Video (Summary)

* **Python AI Agent Script using Groq & Tavily:**
  * Demonstrates loading `.env` keys (`GROQ_API_KEY`, `TAVILY_API_KEY`) via `python-dotenv`.
  * Implements `web_search(query)` via `TavilyClient` and `calculate(expression)` via Python math evaluation.
  * Defines `tools` JSON schema array with `type="function"`, `name`, `description`, and `parameters`.
  * Implements `run_agent(user_query, max_iterations=3)` calling `groq_client.chat.completions.create(tools=tools, tool_choice="auto")`.
  * Dispatches `tool_calls` requests back to local Python functions and appends tool outputs to `messages` for final LLM response generation.
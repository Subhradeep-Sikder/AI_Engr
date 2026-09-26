# Build Multi-Agent AI System From Scratch | AI Engineer Series

> **Lecturer:** Pratyush  
> **Source:** [YouTube Lecture](http://www.youtube.com/watch?v=Uf71it2BKgQ)

---

## 1. Recapping Multi-Agent Systems & Addressing Doubts

### 1.1 Clarifying the "Multiple LLMs" Concept

* A common misconception is that a Multi-Agent System requires using completely different LLM providers (e.g., mixing Groq, OpenAI, and Anthropic).
* In practice, "Multiple LLMs" refers to creating **distinct LLM functional instances/clients**, each assigned a specific role, system prompt, and restricted tool set.
* You can run a Multi-Agent System using the **same underlying model/client** (e.g., Groq Llama/GPT-OSS) across all agents, or choose different models depending on the task requirements.

---

## 2. Intuitive Conceptual Model: The YouTube Channel Analogy

To clarify the difference between single-agent and multi-agent systems, consider managing a YouTube channel:

### 2.1 Single-Agent Channel Setup

* **Scenario:** A single solo creator handles every task independently — teaching/recording lectures, editing raw footage, designing thumbnails, and uploading the video.
* **Mechanism:** One person holds all internal context in their head, makes every execution decision sequentially, and resolves errors internally without communicating with anyone else.

### 2.2 Multi-Agent Channel Setup

* **Scenario:** A **Manager** supervises three specialized role entities:
  1. **Teacher (Creator Agent):** Focuses solely on recording the educational video.
  2. **Editor Agent:** Focuses solely on stitching clips and producing the final cut.
  3. **Uploader Agent:** Focuses solely on uploading the finished file with a thumbnail to YouTube.

* **Execution Flow Managed by Manager:**
  1. Manager receives task: *"Upload a Multi-Agent lecture today."*
  2. Manager calls **Teacher** $\rightarrow$ Teacher records raw video and returns it.
  3. Manager passes raw video to **Editor** $\rightarrow$ Editor edits and returns final cut.
  4. If Editor detects mistakes, Manager routes re-record requests back to Teacher.
  5. Manager passes final video to **Uploader** $\rightarrow$ Video goes live.

* **Crucial Rule:** The Manager possesses **NO execution skills** (cannot teach, edit, or upload); its sole responsibility is task routing and coordination.

---

## 3. Architecture Comparison: Single-Agent vs. Multi-Agent Systems

| Feature / Aspect | Single-Agent System | Multi-Agent System (No LangGraph) |
| :--- | :--- | :--- |
| **LLM Functions** | One `ask_llm` function. | Multiple functions (`ask_manager_llm`, `ask_search_llm`, `ask_math_llm`). |
| **Tool Distribution** | Single LLM has access to **ALL** tools (Web Search + Calculator). | Each agent has access to **RESTRICTED** tool sets. |
| **Supervisor Role** | No manager; single LLM self-routes tasks internally. | Dedicated `Manager LLM` holding **NO tools**, tracking state in a Notes file. |
| **Context Window Usage** | Shared single context window (risk of context overflow). | Isolated context windows per agent. |
| **Communication Overhead** | Zero inter-agent communication overhead. | High communication overhead (hand-over reports between sub-agents and Manager). |
| **Token Usage & Cost** | Lower token usage and fewer API calls. | **20%+ higher token usage** and ~2x LLM API calls. |

---

## 4. Multi-Agent Execution Flow (The Gold Price & Math Query)

### 4.1 Sample Problem

* **User Query:** *"What is today's 100g gold price, and if I have ₹1 Crore, how many grams of gold can I buy?"*

### 4.2 Step-by-Step Multi-Agent Routing

1. **User Request to Manager:**
   * User sends query to `ask_manager_llm`.

2. **Manager Identifies Step 1 (Search):**
   * Manager sees it needs live gold prices.
   * Calls `ask_search_llm` with prompt: *"Search today's 100g gold price."*

3. **Search Agent Execution:**
   * `ask_search_llm` uses Tavily Web Search $\rightarrow$ returns price (e.g., ₹2 Lakh per 100g).
   * *Note:* Search Agent cannot do division math because it has no calculator tool.

4. **Manager Notes Entry:**
   * Manager writes `₹2 Lakh per 100g` into its internal Notes Diary.

5. **Manager Identifies Step 2 (Math):**
   * Manager needs division math: ₹1 Crore / ₹2 Lakh.
   * Calls `ask_math_llm` with prompt: *"Calculate ₹10,000,000 / ₹200,000."*

6. **Math Agent Execution:**
   * `ask_math_llm` uses Python Calculator $\rightarrow$ returns result (`50` units of 100g = 5,000 grams).
   * *Note:* Math Agent cannot search the web because it has no search tool.

7. **Final Synthesis:**
   * Manager receives math result and outputs final answer to user.

---

## 5. Model Selection Strategy: Heterogeneous Models

You do not need to use the exact same LLM model for every agent. Models can be selected based on task complexity:

* **Manager Agent:** Requires high reasoning and decision-making capabilities $\rightarrow$ Use top-tier reasoning models (e.g., Opus / high-tier models).
* **Research/Search Agent:** Requires strong search understanding $\rightarrow$ Use mid-to-high tier models.
* **Simple Formatting / Email Agent:** Requires minimal reasoning $\rightarrow$ Use lightweight/cheaper models (e.g., Sonnet or free-tier models).

---

## 6. The Golden Rule of Multi-Agent Engineering & Cost Disadvantage

### 6.1 The Engineering Golden Rule

> *"If something is working, don't touch it!"*

* Always build and benchmark a **Single-Agent System first**.
* If the Single-Agent System achieves **~85%+ accuracy**, **DO NOT** convert it into a Multi-Agent System.
* **When to upgrade to Multi-Agent:**
  1. Single-agent context window overflows due to lengthy conversation histories.
  2. Single agent confuses tools across heavily distinct, complex domains.
  3. Sub-tasks require vastly different model tiers for cost/speed optimization.

### 6.2 The Cost Penalty of Multi-Agent Systems

* **Increased Token Usage:** Because agents cannot read each other's memory, detailed hand-over reports must be written to and from the Manager LLM.
* Empirical test results show Multi-Agent Systems consume **~20% more tokens** and make **almost double the LLM API calls** compared to single agents for the exact same task.

---

## 7. Python Implementation (Building Multi-Agent from Scratch)

```python
import os
import ast
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# ---------------------------------------------------------
# 1. DEFINE TOOL FUNCTIONS
# ---------------------------------------------------------
def web_search(query: str) -> str:
    """Performs web search using Tavily API."""
    response = tavily_client.search(query=query)
    return str(response)

def calculate(expression: str) -> str:
    """Evaluates mathematical expressions."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Math Error: {str(e)}"

# Tool Schemas
search_tool_schema = [{
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for up-to-date facts.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
}]

math_tool_schema = [{
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluate basic mathematical expressions.",
        "parameters": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"]
        }
    }
}]

# ---------------------------------------------------------
# 2. SPECIALIZED SUB-AGENTS
# ---------------------------------------------------------
def ask_search_llm(query: str) -> str:
    """Search Agent - Has ACCESS ONLY to Web Search."""
    messages = [
        {"role": "system", "content": "You are a Search Specialist. You ONLY have access to the web_search tool. Search facts once and return the result."},
        {"role": "user", "content": query}
    ]
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=search_tool_schema,
        tool_choice="auto"
    )
    msg = response.choices[0].message
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        args = ast.literal_eval(tool_call.function.arguments)
        result = web_search(**args)
        return result
    return msg.content

def ask_math_llm(query: str) -> str:
    """Math Agent - Has ACCESS ONLY to Calculator."""
    messages = [
        {"role": "system", "content": "You are a Math Specialist. You ONLY have access to the calculate tool. ALWAYS use the calculator; never compute in your head."},
        {"role": "user", "content": query}
    ]
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=math_tool_schema,
        tool_choice="auto"
    )
    msg = response.choices[0].message
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        args = ast.literal_eval(tool_call.function.arguments)
        result = calculate(**args)
        return result
    return msg.content

# ---------------------------------------------------------
# 3. MANAGER / ORCHESTRATOR AGENT (NO TOOLS)
# ---------------------------------------------------------
def ask_manager_llm(user_query: str, max_rounds: int = 5) -> str:
    """Manager Agent - Holds NO execution tools; orchestrates sub-agents."""
    notes = []
    
    manager_system_prompt = (
        "You are a Manager Agent supervising two sub-agents: 'search_agent' and 'math_agent'. "
        "You have NO execution tools yourself. "
        "Analyze the user query and notes diary, then choose which sub-agent to call next, "
        "or output 'FINAL_ANSWER: <your answer>' when finished."
    )
    
    history = [
        {"role": "system", "content": manager_system_prompt},
        {"role": "user", "content": f"User Query: {user_query}"}
    ]
    
    for round_num in range(max_rounds):
        # Pass current notes into conversation history
        history_with_notes = history + [{"role": "system", "content": f"Current Notes Diary: {notes}"}]
        
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=history_with_notes
        )
        
        content = response.choices[0].message.content
        
        if "FINAL_ANSWER:" in content:
            return content.split("FINAL_ANSWER:")[1].strip()
        elif "CALL: search_agent" in content:
            sub_prompt = content.replace("CALL: search_agent", "").strip()
            search_result = ask_search_llm(sub_prompt)
            notes.append({"step": f"round_{round_num}_search", "result": search_result})
            history.append({"role": "assistant", "content": content})
            history.append({"role": "user", "content": f"Search Agent Output: {search_result}"})
        elif "CALL: math_agent" in content:
            sub_prompt = content.replace("CALL: math_agent", "").strip()
            math_result = ask_math_llm(sub_prompt)
            notes.append({"step": f"round_{round_num}_math", "result": math_result})
            history.append({"role": "assistant", "content": content})
            history.append({"role": "user", "content": f"Math Agent Output: {math_result}"})
        else:
            return content

    return "Reached maximum manager rounds."

# ---------------------------------------------------------
# 4. TEST BENCHMARK QUERY
# ---------------------------------------------------------
if __name__ == "__main__":
    test_query = (
        "Search the height in meters of the Eiffel Tower and the Burj Khalifa. "
        "Then calculate what percentage of the Burj Khalifa's height the Eiffel Tower is, "
        "and how many Eiffel Towers stacked on top of each other would reach the Burj Khalifa's height."
    )
    
    print("--- Running Multi-Agent System ---")
    output = ask_manager_llm(test_query)
    print("Final Output:\n", output)
```

---

## ⚡ QUICK REVISION SUMMARY

1. A Multi-Agent System partitions responsibilities and tool access across distinct LLM instances supervised by a Manager LLM.
2. Multi-agent architecture does not mandate different external API providers; it can be built using the same LLM client/model with restricted tool access per function.
3. In the YouTube channel analogy, the Manager handles task coordination while specialized agents handle Teaching, Editing, and Uploading.
4. The Manager/Director LLM possesses **NO execution tools**; its sole responsibility is sub-agent selection and notes tracking.
5. Sub-agents (Search Agent, Math Agent) hold **restricted tool access** and cannot perform tasks outside their domain.
6. Heterogeneous models can be used: high-reasoning models for the Manager and cheaper/faster models for simple formatting tasks.
7. Golden Rule: Always build a Single-Agent System first.
8. Software engineering principle: *"If something is working (~85%+ accuracy), don't touch it!"*
9. Multi-Agent Systems consume **~20% more tokens** and require almost double the LLM API calls due to inter-agent communication overhead.
10. `max_attempts` or `max_rounds` limits are mandatory to prevent infinite agent execution loops.

---

## ❓ QUESTIONS RAISED BY LECTURER

* **Q:** Does building a Multi-Agent System require opening separate API accounts or using different LLM models for every agent?  
  **A:** No. You can use the exact same LLM client and model for all agents; the difference lies in assigning unique system prompts and restricted tool schemas to each agent instance.

* **Q:** Why shouldn't developers always build Multi-Agent Systems by default?  
  **A:** Because Multi-Agent Systems increase token consumption by 20%+ and double API calls due to inter-agent communication overhead, making them significantly more expensive and slower.

---

## ⚠️ IMPORTANT POINTS LECTURER EMPHASIZED

* **Manager Tool Restriction:** The Manager LLM must explicitly have no execution tools assigned to force it to delegate work.
* **Notes Tracker:** The Manager maintains a Notes file/diary to record sub-agent outputs and prevent loss of context across rounds.
* **Infinite Loop Guard:** Setting `max_attempts` (e.g., 5 rounds) is essential to stop agents if they repeatedly fail or encounter loop conditions.
* **AI-Human Engagement Warning:** Relying blindly on automated code generators without reading the generated code obscures underlying bugs and weakens developer skills.

---

## 🔗 CONNECTIONS LECTURER MADE

* Connected single-agent vs. multi-agent execution to a solo YouTube creator vs. a YouTube team with a Manager, Teacher, Editor, and Uploader.
* Connected inter-agent communication overhead to software development teams writing pull request documentation and hand-over files.
* Connected model selection to job specialization (hiring expensive senior engineers for management/reasoning and junior/cheaper workers for simple formatting).

---

## 📖 DEFINITIONS (from video only)

* **Multi-Agent System (MAS):** An architecture where multiple specialized LLMs, each possessing restricted tool access, collaborate under a tool-less Manager LLM to execute complex workflows.
* **Manager / Orchestrator LLM:** A supervisor LLM that holds no direct execution tools and functions purely to select sub-agents and synthesize results.
* **Notes Diary / Tracker:** An internal state array maintained by the Manager LLM to log sub-agent outputs across execution rounds.
* **Inter-Agent Communication Overhead:** The additional prompt tokens generated when agents write hand-over reports to pass context between one another.

---

## 💡 EXAMPLES USED IN VIDEO

* **YouTube Channel Management:** Solo creator doing teaching, editing, and uploading (Single-Agent) vs. Manager supervising Teacher, Editor, and Uploader (Multi-Agent).
* **Gold Price Purchasing Calculation:** Searching 100g gold price via Search Agent $\rightarrow$ calculating budget division via Math Agent $\rightarrow$ outputting result via Manager.
* **Eiffel Tower vs. Burj Khalifa Benchmark Query:** Searching Eiffel Tower (330m) and Burj Khalifa (828m) heights $\rightarrow$ calculating percentage ratio and stacking count via Math Agent.

---

## 💻 CODE WRITTEN IN VIDEO

* Demonstrates Python implementation of `ask_search_llm()` (restricted to `web_search`), `ask_math_llm()` (restricted to `calculate`), and `ask_manager_llm()` (no tools, notes array tracker, `max_rounds=5` cap) using Groq and Tavily APIs.
---

# ReAct (Reasoning + Action) AI Agents

## 1. Introduction to ReAct and AI Agents

* **The Shift:** We are moving from simple LLMs (where you ask a question and get a text answer based on training data) to full-fledged **AI Agents**. An AI Agent is a service that can take actions (like booking a ticket or checking a status).
* **What is ReAct?** ReAct stands for **Reasoning + Action**. It is the crucial step and logic loop that bridges the gap between a standard LLM and an active AI Agent.
* **The Core Problem with Standard LLMs:**
* LLMs are trained on historical data up to a specific cutoff date.
* They cannot natively answer *present-day* questions (e.g., "What is the temperature today?" or "What are hotel prices in Dubai right now?").
* The solution is to provide the LLM with **Tools** (usually APIs, like a weather API or a MakeMyTrip API).



## 2. The Complexity of Using Tools

Simply giving an LLM access to 100 tools isn't enough. The LLM must know *how* and *when* to use them.

* **The Permutation Problem:** If you build an Amazon AI agent with 7 tools (check order, refund, track delivery, search product, update address, etc.), you cannot write simple `if/else` code to decide which tool to use.
* If a user says, *"Where is my order?"* the agent needs `Order Status` and `Track Delivery`.
* If a user says, *"Refund my order,"* the agent needs `Order Status`, `Track Delivery`, and `Refund`.
* Because users speak in unstructured, natural language, there are infinite permutations.


* **Chaining Tools:** Often, the output of one tool must become the input of the next (e.g., using a tool to find an Order ID, then passing that Order ID into a "Track Delivery" tool).

## 3. The ReAct Loop (How It Works)

The ReAct loop solves the complexity of tool selection by forcing the LLM to think step-by-step. It follows a continuous loop of **Reasoning -> Action -> Observation** until it finds the final answer.

### The Loop Execution (Step-by-Step):

1. **Reasoning (Thought):** The LLM reads the prompt, breaks down the problem, and decides what immediate step to take next.
2. **Action:** The LLM decides which specific tool to call (and what input/arguments to pass to it) to solve that immediate step. *Crucially, the LLM stops here and waits.*
3. **Observation:** The external tool runs (e.g., executing a Python function or an API call) and returns a result to the LLM.
4. **Repeat or Finalize:** The LLM takes that Observation, adds it to its memory, and starts Reasoning again. It asks: *"Do I have enough info to give the final answer, or do I need another tool?"*

### Example Scenario:

**User Prompt:** *"I want to buy an iPhone 17. I have ₹5000. How much money will I have left?"*

* **Step 1:**
* **Thought:** I need to find the current price of an iPhone 17 first.
* **Action:** Call `Get_Product_Price("iPhone 17")`
* **Observation:** The tool returns `₹1000`.


* **Step 2:**
* **Thought:** Now I know the price is ₹1000. The user has ₹5000. I need to calculate the difference.
* **Action:** Call `Calculator(5000 - 1000)`
* **Observation:** The tool returns `4000`.


* **Step 3:**
* **Thought:** I have all the information needed to answer the prompt.
* **Action:** Provide the Final Answer.
* **Final Answer:** "The iPhone 17 costs ₹1000, and you will have ₹4000 left."



## 4. Implementing ReAct in Code

To build a ReAct agent, you don't need a special library; you just need to structure your Python code and your System Prompt correctly.

### I. Define the Tools

Create basic Python functions that represent your tools (e.g., `def get_product_price(product_name):` or `def calculator(expression):`).

### II. Write a Strict System Prompt

You must instruct the LLM exactly how to behave. Since base models can be "dumb," the prompt must be highly detailed:

* Tell it who it is (e.g., *"You are a shopping assistant"*).
* List the specific tools available to it.
* Provide strict examples of how to call those tools syntactically (e.g., *"Write Action: get_product_price('iPhone 17')"*).
* Provide the "Rules of Engagement" (The ReAct Loop):
1. Decide what to do next.
2. Call *only one tool at a time*.
3. Stop and wait for an Observation.
4. Do *not* guess or invent tool results.
5. Once the task is complete, provide the Final Answer.



### III. The Agent Code Logic

The Python code handles the loop execution (usually set to a maximum number of steps, like 5 or 20, depending on complexity):

1. Send the System Prompt and User Prompt to the LLM.
2. Extract the `Action` (the tool name and inputs) from the LLM's response using Regular Expressions (Regex).
3. Execute the corresponding Python function (the tool) locally.
4. Take the result (the Observation) and append it to the `messages` array as an "Assistant" role, giving the LLM memory of what just happened.
5. Send the updated conversation history back to the LLM to trigger the next loop.
6. *Crucial Check:* Implement a `time.sleep(5)` between calls to prevent rate-limiting the LLM API.
7. Break the loop when the LLM outputs the "Final Answer."
# 🛠️ Build Your Own MCP Server & Connect It to Claude

> **Series:** AI Engineer Series  
> **Topic:** Build Your Own MCP Server and Connect it To Claude  
> **Lecturer:** Pratyush  
> **Source:** [Watch on YouTube](http://www.youtube.com/watch?v=anvXVT46Oog)

---

## 📑 Table of Contents

- [1. High-Level Concept: The Kitchen Analogy](#1-high-level-concept-the-kitchen-analogy)
- [2. Step-by-Step Implementation: Building a Custom MCP Server](#2-step-by-step-implementation-building-a-custom-mcp-server)
  - [2.1 Project Setup & Environment Initialisation](#21-project-setup--environment-initialisation)
  - [2.2 Writing the Server Code (`mcp_server.py`)](#22-writing-the-server-code-mcp_serverpy)
- [3. Testing the MCP Server Locally (MCP Dev Inspector)](#3-testing-the-mcp-server-locally-mcp-dev-inspector)
- [4. Connecting the MCP Server to Claude Desktop](#4-connecting-the-mcp-server-to-claude-desktop)
  - [4.1 Locating `claude_desktop_config.json`](#41-locating-claude_desktop_configjson)
  - [4.2 Editing Configuration JSON](#42-editing-configuration-json)
- [5. Verification & Live Execution](#5-verification--live-execution)
- [6. ⚡ Quick Revision Summary](#6--quick-revision-summary)
- [7. ❓ Questions Raised by Lecturer](#7--questions-raised-by-lecturer)
- [8. 📖 Definitions (From Video Only)](#8--definitions-from-video-only)
- [9. 💡 Examples Used in Video](#9--examples-used-in-video)

---

## 1. High-Level Concept: The Kitchen Analogy

To understand how an MCP (Model Context Protocol) Server interacts with an LLM client, consider a restaurant kitchen setup [[00:53](https://www.youtube.com/watch?v=anvXVT46Oog&t=53)]:

* **MCP Server = Kitchen:** The hosting environment where tools reside [[00:58](https://www.youtube.com/watch?v=anvXVT46Oog&t=58)].
* **Tools = Menu Dishes:** Specific operational capabilities/functions packaged inside the server [[01:02](https://www.youtube.com/watch?v=anvXVT46Oog&t=62)].
* **LLM Client (Claude Desktop / ChatGPT / Gemini) = Customer:** The client that requests specific tools ("dishes") from the server without needing to know how the kitchen cooks them [[01:07](https://www.youtube.com/watch?v=anvXVT46Oog&t=67)].

---

## 2. Step-by-Step Implementation: Building a Custom MCP Server

### 2.1 Project Setup & Environment Initialisation

1. Create a project directory (e.g., `my_mcp_server`) [[01:36](https://www.youtube.com/watch?v=anvXVT46Oog&t=96)].
2. Activate a Python virtual environment (Python 3.11+) [[01:48](https://www.youtube.com/watch?v=anvXVT46Oog&t=108)].
3. Install the MCP CLI SDK using the UV package manager [[02:29](https://www.youtube.com/watch?v=anvXVT46Oog&t=149)]:

```bash
uv add mcp-cli
```

### 2.2 Writing the Server Code (`mcp_server.py`)

To prove that Claude is executing the custom MCP server tool rather than its own internal math capabilities, an intentional "+100" bug logic is introduced into the addition tool [[03:37](https://www.youtube.com/watch?v=anvXVT46Oog&t=217)].

```python
# mcp_server.py
from mcp.server import FastMCP

# 1. Initialize the MCP Server (Kitchen Name)
mcp = FastMCP("pratyush_mcp_kitchen")

# 2. Register a Tool Decorator
@mcp.tool()
def pratyush_add(a: int, b: int) -> int:
    """Adds two numbers together (includes intentional +100 offset for verification)."""
    return a + b + 100

# 3. Run the Server
if __name__ == "__main__":
    mcp.run()
```

---

## 3. Testing the MCP Server Locally (MCP Dev Inspector)

Before connecting the server to Claude Desktop, test it locally using the built-in developer UI [[04:46](https://www.youtube.com/watch?v=anvXVT46Oog&t=286)]:

```bash
uv run mcp dev mcp_server.py
```

* This command opens a local web interface in Chrome [[05:03](https://www.youtube.com/watch?v=anvXVT46Oog&t=303)].
* Connect to the server, select the registered `pratyush_add` tool, and pass test parameters (e.g., `a=10`, `b=30`) [[05:20](https://www.youtube.com/watch?v=anvXVT46Oog&t=320)].
* Expected verification result: `140` (since `10 + 30 + 100 = 140`) [[05:30](https://www.youtube.com/watch?v=anvXVT46Oog&t=330)].

---

## 4. Connecting the MCP Server to Claude Desktop

### 4.1 Locating `claude_desktop_config.json`

Locate the Claude Desktop configuration file on your system [[05:45](https://www.youtube.com/watch?v=anvXVT46Oog&t=345)]:

* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json` [[07:01](https://www.youtube.com/watch?v=anvXVT46Oog&t=421)]
* **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

### 4.2 Editing Configuration JSON

Add your custom MCP server entry under the `mcpServers` JSON block [[06:16](https://www.youtube.com/watch?v=anvXVT46Oog&t=376)].

> [!IMPORTANT]
> **Crucial JSON Rule:** On Windows, always use double backslashes (`\\`) in path strings to prevent JSON parsing errors [[08:12](https://www.youtube.com/watch?v=anvXVT46Oog&t=492)].

```json
{
  "mcpServers": {
    "pratyush_mcp_kitchen": {
      "command": "C:\\Users\\<YourUsername>\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "C:\\Users\\<YourUsername>\\path\\to\\my_mcp_server",
        "run",
        "mcp_server.py"
      ]
    }
  }
}
```

#### Finding Executable & Directory Paths:

1. **Find UV executable path:** Run `where.exe uv` in Terminal [[06:56](https://www.youtube.com/watch?v=anvXVT46Oog&t=416)].
2. **Find project directory path:** Run `pwd` inside your project directory [[07:36](https://www.youtube.com/watch?v=anvXVT46Oog&t=456)].

---

## 5. Verification & Live Execution

1. **Restart Claude Desktop:** Close Claude completely, including terminating its processes via Task Manager / Activity Monitor, and reopen it [[09:06](https://www.youtube.com/watch?v=anvXVT46Oog&t=546)].
2. **Check Connectors Indicator:** Click the plug/connectors icon in Claude Desktop. `pratyush_mcp_kitchen` will now appear as an active connected tool source [[09:50](https://www.youtube.com/watch?v=anvXVT46Oog&t=590)].
3. **Run Query Prompt:**
   > *"Use the pratyush tool and add 40 and 30."* [[10:04](https://www.youtube.com/watch?v=anvXVT46Oog&t=604)]
4. **Result:** Claude executes the connected tool dynamically and outputs **170** (`40 + 30 + 100`), confirming that Claude successfully invoked your local custom MCP server [[10:24](https://www.youtube.com/watch?v=anvXVT46Oog&t=624)].

---

## 6. ⚡ Quick Revision Summary

1. **MCP Server Architecture:** Uses a Kitchen (Server), Dishes (Tools), and Customer (LLM Client) model [[00:53](https://www.youtube.com/watch?v=anvXVT46Oog&t=53)].
2. **FastMCP Decorator:** Use `@mcp.tool()` to automatically register functions without manually declaring complex JSON schemas [[04:22](https://www.youtube.com/watch?v=anvXVT46Oog&t=262)].
3. **Testing Tool:** Run `uv run mcp dev <file>.py` to test tool functions in Chrome before deploying [[04:54](https://www.youtube.com/watch?v=anvXVT46Oog&t=294)].
4. **Claude Config Path:** Connected servers are declared inside `claude_desktop_config.json` under `mcpServers` [[05:45](https://www.youtube.com/watch?v=anvXVT46Oog&t=345)].
5. **Path Formatting:** Always escape backslashes (`\\`) in Windows configuration paths [[08:12](https://www.youtube.com/watch?v=anvXVT46Oog&t=492)].
6. **Live Integration:** Fully restart Claude via Task Manager to refresh registered MCP connectors [[09:12](https://www.youtube.com/watch?v=anvXVT46Oog&t=552)].

---

## 7. ❓ Questions Raised by Lecturer

### Q1: Why was an intentional bug (`+ 100`) added to the addition function during testing?
> **Answer:** To verify conclusively that Claude invoked the external MCP server tool rather than evaluating the math internally [[03:37](https://www.youtube.com/watch?v=anvXVT46Oog&t=217)].

### Q2: Do you need to write detailed JSON parameter descriptions or function schemas when creating tools with FastMCP?
> **Answer:** No. FastMCP dynamically infers the parameters, types, and schema directly from the Python function definition [[04:22](https://www.youtube.com/watch?v=anvXVT46Oog&t=262)].

---

## 8. 📖 Definitions (From Video Only)

| Term | Definition |
| :--- | :--- |
| **FastMCP** | A high-level Python framework for declaring Model Context Protocol servers and tool functions efficiently [[02:54](https://www.youtube.com/watch?v=anvXVT46Oog&t=174)]. |
| **MCP Dev Inspector** | A local developer UI launched via `uv run mcp dev` to test server tools interactively in the browser [[04:54](https://www.youtube.com/watch?v=anvXVT46Oog&t=294)]. |
| **`claude_desktop_config.json`** | The system configuration file used by Claude Desktop to register external local and remote MCP servers [[05:45](https://www.youtube.com/watch?v=anvXVT46Oog&t=345)]. |

---

## 9. 💡 Examples Used in Video

* **Kitchen Analogy:** Kitchen (Server), Dishes (Tools), Customer (LLM Client) [[00:53](https://www.youtube.com/watch?v=anvXVT46Oog&t=53)].
* **Add Function Benchmark:** Adding 10 + 30 returning 140, and 40 + 30 returning 170 due to the intentional `+100` offset [[05:25](https://www.youtube.com/watch?v=anvXVT46Oog&t=325)].

---

For additional hands-on context on building MCP servers, check out Pratyush's tutorial video on [Building an MCP Server with Python](https://www.youtube.com/watch?v=anvXVT46Oog), which covers step-by-step local development and Claude Desktop integration.
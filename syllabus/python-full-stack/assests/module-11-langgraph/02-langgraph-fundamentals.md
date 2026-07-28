# LangGraph Fundamentals

**Module 11 -- LangGraph | Topic 2**

---

## What is LangGraph?

LangGraph is a Python library by LangChain for building **stateful, multi-step AI workflows**. Think of it as a way to draw a flowchart that your AI follows.

**Why not just use LangChain chains?** LangChain chains go in one direction: A -> B -> C -> done. But agents need **loops** (go back and try again), **conditions** (if X then do Y, else do Z), and **state** (remember what happened in previous steps). LangGraph provides all of this.

### Installation

```bash
pip install langgraph langchain langchain-openai python-dotenv
```

---

## Core Concepts

LangGraph has three building blocks: **State**, **Nodes**, and **Edges**.

| Concept | What It Is | Analogy |
|---------|-----------|---------|
| **State** | Data that flows through the graph | A shared notebook everyone can read/write |
| **Node** | A function that processes the state | A worker at a station on an assembly line |
| **Edge** | A connection between nodes | A conveyor belt between stations |

---

## State -- The Shared Data

State is a Python dictionary that holds all the data your graph needs. Every node can read from it and write to it.

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]   # Chat history
    current_step: str                          # Which step we are on
    tool_results: dict                         # Results from tools
```

### The add_messages Annotation

The `Annotated[list, add_messages]` is special. It tells LangGraph to **append** new messages instead of replacing the entire list.

```python
# Without add_messages:
state["messages"] = [new_message]    # Replaces everything!

# With add_messages:
state["messages"] = [new_message]    # Appends to the existing list
```

This is important because you want to keep the full conversation history.

---

## Nodes -- The Workers

Nodes are Python functions that take the state, do some work, and return updates to the state.

### The Chatbot Node (LLM)

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def chatbot_node(state: AgentState):
    """The LLM thinks and decides what to do."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}
```

### The Tool Node (Action)

```python
def tool_node(state: AgentState):
    """Execute the tool the LLM asked for."""
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]
    
    # Run the tool
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    result = available_tools[tool_name].invoke(tool_args)
    
    # Return the result as a tool message
    from langchain_core.messages import ToolMessage
    tool_message = ToolMessage(content=str(result), tool_call_id=tool_call["id"])
    return {"messages": [tool_message]}
```

---

## Edges -- The Connections

Edges connect nodes together. There are two types:

### Normal Edges

Always go from A to B, no conditions.

```python
graph.add_edge("tools", "chatbot")
# After the tools node, ALWAYS go to the chatbot node
```

### Conditional Edges

Choose the next node based on the state.

```python
def should_use_tool(state: AgentState) -> str:
    """Decide: use a tool or finish?"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"     # LLM wants to use a tool
    return "end"           # LLM gave a final answer

graph.add_conditional_edges(
    "chatbot",                     # From this node
    should_use_tool,               # Use this function to decide
    {"tools": "tools", "end": END} # Map return values to nodes
)
```

---

## Building a Complete Graph

### Step 1: Define State

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

### Step 2: Create Nodes

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def search_courses(query: str) -> str:
    """Search for TechPath courses."""
    if "python" in query.lower():
        return "Python Full Stack: Rs 45,000, 6 months"
    return "No courses found"

tools = [search_courses]
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

def agent_node(state):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

### Step 3: Build the Graph

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

graph = StateGraph(State)

# Add nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))

# Add edges
graph.add_edge("tools", "agent")           # After tools, go back to agent
graph.add_conditional_edges("agent", tools_condition)  # Agent decides: tools or END

# Set entry point
graph.set_entry_point("agent")

# Compile the graph
app = graph.compile()
```

### Step 4: Run It

```python
result = app.invoke({
    "messages": [("user", "What Python courses does TechPath offer?")]
})

print(result["messages"][-1].content)
```

---

## The Agent Loop Visualized

```
                +----------+
                | START    |
                +----+-----+
                     |
                +----v-----+
         +----->| Agent    |------+
         |      | (LLM)   |      |
         |      +----------+      |
         |           |            |
         |     Has tool calls?    |
         |      /          \      |
         |    YES           NO    |
         |    /               \   |
    +----v-----+          +---v--+
    | Tools    |          | END  |
    | (execute)|          +------+
    +----------+
```

The loop continues until the LLM decides it has enough information and gives a final answer (no more tool calls).

---

## Checkpoints -- Saving State

Checkpoints let you save the graph's state at any point. This enables:
- Resuming conversations later
- Human-in-the-loop (pause, wait for approval, continue)
- Debugging by replaying from a saved state

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Every conversation gets a unique thread_id
config = {"configurable": {"thread_id": "student-rahul-001"}}

# First message
result = app.invoke(
    {"messages": [("user", "Show me Python courses")]},
    config
)

# Later, continue the same conversation
result = app.invoke(
    {"messages": [("user", "What is the fee?")]},
    config   # Same thread_id, so it remembers the previous messages
)
```

### Checkpoint Storage Options

| Storage | Type | Best For |
|---------|------|----------|
| `MemorySaver` | In-memory | Development, testing |
| `SqliteSaver` | SQLite file | Small applications |
| `PostgresSaver` | PostgreSQL | Production |

---

## The tools_condition Helper

LangGraph provides a built-in function that checks if the LLM made a tool call:

```python
from langgraph.prebuilt import tools_condition

# Instead of writing your own should_use_tool function:
graph.add_conditional_edges("agent", tools_condition)

# tools_condition returns:
# - "tools" if the last message has tool_calls
# - END if there are no tool_calls
```

---

## The ToolNode Helper

LangGraph also provides a built-in node that executes tools:

```python
from langgraph.prebuilt import ToolNode

tools = [search_courses, calculate_emi]
tool_node = ToolNode(tools)

graph.add_node("tools", tool_node)
# No need to write your own tool execution code
```

---

## Minimal Agent Template

Here is the shortest possible LangGraph agent:

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# 1. State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Tools
@tool
def greet(name: str) -> str:
    """Greet a student by name."""
    return f"Namaste {name}! Welcome to TechPath Institute."

tools = [greet]
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

# 3. Graph
graph = StateGraph(State)
graph.add_node("agent", lambda s: {"messages": [llm.invoke(s["messages"])]})
graph.add_node("tools", ToolNode(tools))
graph.add_edge("tools", "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.set_entry_point("agent")

app = graph.compile()

# 4. Run
result = app.invoke({"messages": [("user", "Say hello to Priya")]})
print(result["messages"][-1].content)
```

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| LangGraph | Library for building stateful, multi-step AI workflows |
| State | Shared data dictionary that flows through the graph |
| Node | A function that processes state (LLM, tools, etc.) |
| Edge | Connection between nodes (normal or conditional) |
| Conditional edge | Chooses next node based on state |
| `add_messages` | Annotation that appends messages instead of replacing |
| Checkpoint | Saved snapshot of state for resume/debug |
| `tools_condition` | Built-in function: has tool calls -> "tools", else -> END |
| `ToolNode` | Built-in node that executes tool calls |
| `set_entry_point()` | Defines which node runs first |

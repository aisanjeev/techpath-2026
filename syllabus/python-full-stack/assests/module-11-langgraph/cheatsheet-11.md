# Cheat Sheet: LangGraph -- AI Agents & Agentic Workflows

**Module 11 -- Quick Reference**

---

## Installation

```bash
pip install langgraph langchain langchain-openai langsmith python-dotenv
```

---

## Essential Imports

```python
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
```

---

## Minimal Agent Template

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

graph = StateGraph(State)
graph.add_node("agent", lambda s: {"messages": [llm.invoke(s["messages"])]})
graph.add_node("tools", ToolNode(tools))
graph.add_edge("tools", "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.set_entry_point("agent")

app = graph.compile()
result = app.invoke({"messages": [("user", "Hello!")]})
```

---

## ReAct Pattern

```
THINK  --> "I need to search for courses"
ACT    --> search_courses("Python")
OBSERVE --> "Found: Python Full Stack, Rs 45,000"
THINK  --> "I have the answer"
RESPOND --> "The Python course costs Rs 45,000"
```

---

## Creating Tools

```python
@tool
def search_courses(query: str) -> str:
    """Search for TechPath courses by topic."""
    return "Python Full Stack: Rs 45,000, 6 months"

@tool
def calculate_emi(fee: float, months: int) -> str:
    """Calculate monthly EMI for a course fee."""
    return f"Rs {fee/months:,.0f}/month"
```

| Rule | Why |
|------|-----|
| Clear name | LLM picks tool by name |
| Detailed docstring | LLM reads this to decide when to use |
| Type hints | LLM knows what args to pass |
| Return strings | LLM can read the result |
| Handle errors | Return message, don't raise |

---

## Graph Components

| Component | What It Is |
|-----------|-----------|
| **State** | Shared data dictionary |
| **Node** | Function that processes state |
| **Edge** | Connection between nodes |
| **Conditional Edge** | Chooses next node based on state |

```python
graph.add_node("name", function)
graph.add_edge("from", "to")
graph.add_conditional_edges("from", routing_fn, {"a": "node_a", "b": END})
graph.set_entry_point("first_node")
```

---

## Checkpoints (Saving State)

```python
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "user-001"}}
result = app.invoke({"messages": [("user", "Hi")]}, config)
```

---

## Human-in-the-Loop

```python
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute_action"]   # Pause before this node
)

# Run until pause
result = app.invoke(input, config)

# Resume after approval
result = app.invoke(None, config)
```

---

## Memory Types

| Type | Scope | Duration |
|------|-------|----------|
| Short-term | Current chat | Session |
| Long-term | Across sessions | Persistent (vector store) |
| Episodic | Past interactions | Persistent |

---

## Multi-Agent (Supervisor)

```
Supervisor --> Research Agent
           --> Writer Agent
           --> Coder Agent
           --> FINISH
```

```python
graph.add_conditional_edges("supervisor", route_fn, {
    "research": "research",
    "writer": "writer",
    END: END,
})
```

---

## Agentic RAG Flow

```
Search --> Grade Docs --> Rewrite Query (if bad) --> Search again
                      --> Generate (if good) --> Check Quality --> Done
```

---

## LangSmith Setup

```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"
os.environ["LANGCHAIN_PROJECT"] = "project-name"
```

---

## Key Terms

| Term | Meaning |
|------|---------|
| Agent | LLM + tools + reasoning loop |
| ReAct | Reasoning + Acting pattern |
| State | Data flowing through the graph |
| Node | A function/step in the workflow |
| Conditional Edge | Routing based on state |
| Checkpoint | Saved snapshot for resume |
| HITL | Human-in-the-loop -- pause for approval |
| Supervisor | Agent that manages other agents |
| Agentic RAG | RAG with search-grade-rewrite-verify loop |

# Custom Tools for Agents

**Module 11 -- LangGraph | Topic 3**

---

## What Are Tools?

Tools are Python functions that an AI agent can call. The LLM reads the function's name, description, and parameters to decide **when** and **how** to use each tool.

**Analogy:** An agent's tools are like apps on your phone. You have a calculator app, a maps app, a contacts app. When someone asks you to add numbers, you open the calculator -- not the maps app. The AI agent works the same way: it reads the tool descriptions and picks the right one.

---

## Creating Tools with the @tool Decorator

The simplest way to create a tool is with the `@tool` decorator:

```python
from langchain_core.tools import tool

@tool
def search_courses(query: str, city: str = "Bhopal") -> str:
    """Search for TechPath Institute courses by topic and city.
    
    Args:
        query: What the student wants to learn (e.g., "Python", "web development")
        city: City to search in (default: Bhopal)
    """
    courses = {
        "python": {"name": "Python Full Stack", "fee": 45000, "duration": "6 months"},
        "web": {"name": "Web Development", "fee": 30000, "duration": "4 months"},
        "data": {"name": "Data Science", "fee": 55000, "duration": "8 months"},
    }
    for key, course in courses.items():
        if key in query.lower():
            return f"Found: {course['name']} in {city} -- Rs {course['fee']:,}, {course['duration']}"
    return f"No courses found for '{query}' in {city}"
```

### What the LLM Sees

When you bind tools to an LLM, it sees:
- **Name**: `search_courses`
- **Description**: "Search for TechPath Institute courses by topic and city"
- **Parameters**: `query` (required string), `city` (optional string, default "Bhopal")

The LLM uses this information to decide when to call the tool and what arguments to pass.

---

## Common Tool Types

### Calculator Tool

LLMs are notoriously bad at math. A calculator tool ensures accurate calculations.

```python
@tool
def calculate_emi(total_fee: float, months: int) -> str:
    """Calculate monthly EMI (Equal Monthly Installment) for a course fee.
    
    Args:
        total_fee: Total course fee in Rupees
        months: Number of monthly installments (3, 6, or 12)
    """
    if months <= 0:
        return "Error: months must be positive"
    emi = total_fee / months
    return f"EMI for Rs {total_fee:,.0f} over {months} months = Rs {emi:,.0f}/month"
```

### Database Query Tool

Search a database for information:

```python
@tool
def get_student_info(student_id: str) -> str:
    """Look up a student's enrollment details by their ID.
    
    Args:
        student_id: The student's unique ID (e.g., "TP-2026-001")
    """
    # In a real app, this would query a database
    students = {
        "TP-2026-001": {"name": "Rahul Sharma", "course": "Python Full Stack", "city": "Bhopal"},
        "TP-2026-002": {"name": "Priya Patel", "course": "Data Science", "city": "Indore"},
    }
    student = students.get(student_id)
    if student:
        return f"Student: {student['name']}, Course: {student['course']}, City: {student['city']}"
    return f"No student found with ID {student_id}"
```

### Web Search Tool

Search the internet for information:

```python
@tool
def web_search(query: str) -> str:
    """Search the web for current information.
    
    Args:
        query: The search query
    """
    # Using Tavily (a search API designed for LLMs)
    from langchain_community.tools import TavilySearchResults
    search = TavilySearchResults(max_results=3)
    results = search.invoke(query)
    return str(results)
```

### API Tool

Call an external API:

```python
import requests

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city in India.
    
    Args:
        city: City name (e.g., "Bhopal", "Delhi", "Pune")
    """
    # Using a free weather API
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=5)
        return response.text.strip()
    except Exception as e:
        return f"Could not get weather for {city}: {str(e)}"
```

### Date/Time Tool

```python
from datetime import datetime

@tool
def get_current_datetime() -> str:
    """Get the current date and time in India (IST)."""
    now = datetime.now()
    return f"Current date and time: {now.strftime('%B %d, %Y at %I:%M %p IST')}"
```

---

## Tool Design Best Practices

| Practice | Why It Matters | Example |
|----------|---------------|---------|
| Clear function name | LLM uses name to decide when to call it | `search_courses` not `func1` |
| Detailed docstring | LLM reads description to understand the tool | Include what it does and when to use it |
| Type hints on args | LLM knows what data type to pass | `fee: float`, `months: int` |
| Return strings | LLM can easily read and reason about text | Return `"Rs 7,500/month"` not `7500` |
| Handle errors gracefully | Return error message, do not raise exceptions | Return `"Error: invalid input"` |
| One tool, one job | Keep tools focused and simple | Separate `search` and `calculate` |

### Good vs Bad Tool Descriptions

```python
# BAD -- vague, LLM won't know when to use this
@tool
def do_stuff(x: str) -> str:
    """Does stuff."""
    pass

# GOOD -- clear, specific, LLM knows exactly when to call this
@tool
def calculate_course_emi(fee: float, months: int) -> str:
    """Calculate monthly EMI (Equal Monthly Installment) for a TechPath course.
    Use this when a student asks about payment plans or installment options.
    
    Args:
        fee: Total course fee in Indian Rupees
        months: Number of installments (typically 3, 6, or 12)
    """
    pass
```

---

## Binding Tools to the LLM

After creating tools, you bind them to the LLM so it knows they are available:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [search_courses, calculate_emi, get_student_info]

# Bind tools to the LLM
llm_with_tools = llm.bind_tools(tools)

# Now the LLM can decide to call these tools
response = llm_with_tools.invoke("What is the EMI for Rs 45,000 over 6 months?")

if response.tool_calls:
    print("LLM wants to call:", response.tool_calls[0]["name"])
    print("With args:", response.tool_calls[0]["args"])
```

---

## Using Tools in a LangGraph Agent

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Create all tools
tools = [search_courses, calculate_emi, get_student_info, get_weather]
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

# Build the graph
graph = StateGraph(State)
graph.add_node("agent", lambda s: {"messages": [llm.invoke(s["messages"])]})
graph.add_node("tools", ToolNode(tools))
graph.add_edge("tools", "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.set_entry_point("agent")

app = graph.compile()

# The agent can now use any of the tools as needed
result = app.invoke({
    "messages": [("user", "Find Python courses and calculate EMI for 6 months")]
})
print(result["messages"][-1].content)
```

---

## Error Handling in Tools

Tools should never crash the agent. Always handle errors gracefully:

```python
@tool
def divide_numbers(a: float, b: float) -> str:
    """Divide two numbers.
    
    Args:
        a: The numerator
        b: The denominator
    """
    try:
        if b == 0:
            return "Error: Cannot divide by zero"
        result = a / b
        return f"{a} / {b} = {result:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"
```

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Tool | A Python function an agent can call |
| `@tool` decorator | Marks a function as available for agent use |
| Docstring | The LLM reads this to decide when to use the tool |
| Type hints | Tell the LLM what type of arguments to pass |
| `bind_tools()` | Attaches tools to the LLM so it can call them |
| `ToolNode` | LangGraph built-in that executes tool calls |
| Error handling | Return error strings, never raise exceptions in tools |
| One tool, one job | Keep each tool focused on a single task |

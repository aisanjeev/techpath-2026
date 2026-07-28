# AI Agents and the ReAct Pattern

**Module 11 -- LangGraph | Topic 1**

---

## What is an AI Agent?

An AI agent is an LLM (like GPT-4 or Claude) that can **decide what to do**, **use tools**, and **loop until the task is done**. Unlike a simple chatbot that just answers questions, an agent can take actions.

**Analogy:** Think of a regular chatbot like a receptionist who only answers phone calls. An AI agent is like a full-time assistant at TechPath Institute who can:
- Answer questions (like a chatbot)
- Look up course details in the database
- Calculate EMI for a student
- Check available batches
- Send an email with course information

The assistant **decides** which steps to take based on what the student needs.

### Chatbot vs Agent

| Feature | Chatbot | Agent |
|---------|---------|-------|
| Answers questions | Yes | Yes |
| Uses tools | No | Yes |
| Makes decisions | No | Yes (decides what to do next) |
| Multiple steps | No (one question, one answer) | Yes (loops until done) |
| Handles complex tasks | No | Yes |

---

## The ReAct Pattern

ReAct stands for **Reasoning + Acting**. It is the most common pattern for building AI agents.

The agent follows a loop:
1. **Think** -- Reason about what to do next
2. **Act** -- Use a tool to gather information or take action
3. **Observe** -- Look at the result
4. **Repeat** -- If not done, think again and take another action

### Example: Student Inquiry Agent

```
Student: "I want to learn Python. What courses do you have and can I pay in EMIs?"

Agent's internal loop:
  THINK:  "The student wants Python courses and EMI info. Let me search courses first."
  ACT:    search_courses("Python")
  OBSERVE: "Found: Python Full Stack -- Rs 45,000, 6 months"

  THINK:  "Good, found the course. Now let me calculate EMI."
  ACT:    calculate_emi(45000, 6)
  OBSERVE: "EMI: Rs 7,500/month for 6 months"

  THINK:  "I have both pieces of information. Let me respond."
  RESPOND: "We offer the Python Full Stack course for Rs 45,000. 
           You can pay in 6 monthly EMIs of Rs 7,500 each."
```

### The ReAct Loop Diagram

```
         +---------+
         | START   |
         +----+----+
              |
         +----v----+
    +--->| THINK   |  "What should I do next?"
    |    +----+----+
    |         |
    |    +----v----+
    |    | ACT     |  Use a tool (search, calculate, etc.)
    |    +----+----+
    |         |
    |    +----v----+
    |    | OBSERVE |  Look at the tool's result
    |    +----+----+
    |         |
    |    Done?|
    |    /    \
    |  NO     YES
    |  /        \
    +--+    +----v----+
              | RESPOND |  Give the final answer
              +---------+
```

---

## Key Components of an Agent

Every agent has five parts:

| Component | What It Does | Example |
|-----------|-------------|---------|
| **LLM (Brain)** | Decides what to do next | GPT-4, Claude |
| **Tools** | Actions the agent can perform | Search database, calculate, call APIs |
| **Memory** | Remembers the conversation | Chat history, past interactions |
| **Reasoning** | Plans steps and reflects on results | "I should check the fee before recommending" |
| **Orchestrator** | Controls the loop (Think-Act-Observe) | LangGraph, LangChain AgentExecutor |

### Why the LLM is the "Brain"

The LLM does not just answer questions -- it also:
- Reads the list of available tools
- Decides which tool to use
- Generates the correct arguments for the tool
- Interprets the tool's output
- Decides if more steps are needed

```python
# The LLM sees something like this:
"""
You have access to these tools:
1. search_courses(query) -- Search for TechPath courses
2. calculate_emi(amount, months) -- Calculate monthly EMI

Student asks: "How much is the Python course in EMIs?"

Think step by step. Use tools as needed.
"""
```

---

## Tool Use -- How Agents Call Functions

When an agent needs to take an action, it generates a **tool call** -- a structured request to run a specific function.

### How Tool Calls Work

```
LLM receives: "Calculate EMI for Rs 45,000 over 6 months"
LLM outputs:  {
    "tool": "calculate_emi",
    "arguments": {"amount": 45000, "months": 6}
}
System runs:  calculate_emi(45000, 6)
System returns: "Rs 7,500/month"
LLM receives:  "Tool result: Rs 7,500/month"
LLM responds:  "The EMI would be Rs 7,500 per month for 6 months."
```

### Creating a Simple Tool

```python
from langchain_core.tools import tool

@tool
def search_courses(query: str) -> str:
    """Search for TechPath Institute courses by topic.
    
    Args:
        query: What the student wants to learn (e.g., "Python", "web development")
    """
    courses = {
        "python": "Python Full Stack -- Rs 45,000, 6 months",
        "web": "Web Development -- Rs 30,000, 4 months",
        "data": "Data Science -- Rs 55,000, 8 months",
    }
    for key, info in courses.items():
        if key in query.lower():
            return f"Found: {info}"
    return f"No courses found for '{query}'"
```

The `@tool` decorator tells LangChain:
- **Function name** = the tool's name (search_courses)
- **Docstring** = the tool's description (LLM reads this to decide when to use it)
- **Type hints** = what arguments the tool expects

---

## The Reasoning Loop in Detail

### Step 1: LLM Reads the Situation

The LLM receives:
- The user's question
- The conversation history
- The list of available tools
- Any previous tool results

### Step 2: LLM Decides

The LLM responds in one of two ways:
1. **Tool call**: "I need more information. Let me use a tool."
2. **Final answer**: "I have enough information. Here is my answer."

### Step 3: System Executes

If the LLM requested a tool call:
- The system runs the function
- Sends the result back to the LLM
- The loop continues

If the LLM gave a final answer:
- The loop ends
- The answer is returned to the user

```
User: "What Python courses are available in Bhopal?"
  |
  v
LLM: "I should search for Python courses" --> tool_call: search_courses("Python")
  |
  v
System: runs search_courses("Python") --> "Python Full Stack, Rs 45,000, 6 months"
  |
  v
LLM: "I should check batch availability" --> tool_call: check_batches("Python Full Stack")
  |
  v
System: runs check_batches(...) --> "Aug 5, Sep 1 batches available"
  |
  v
LLM: "I have all the info" --> Final answer: "We offer Python Full Stack..."
```

---

## Simple Agent with LangChain

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# Define tools
@tool
def search_courses(query: str) -> str:
    """Search for courses at TechPath Institute."""
    if "python" in query.lower():
        return "Python Full Stack: Rs 45,000, 6 months, Mon-Fri 10 AM"
    return "No courses found"

@tool
def calculate_emi(fee: float, months: int) -> str:
    """Calculate monthly EMI for a course fee."""
    emi = fee / months
    return f"EMI: Rs {emi:,.0f}/month for {months} months"

# Create agent LLM with tools
llm = ChatOpenAI(model="gpt-4o-mini")
tools = [search_courses, calculate_emi]
llm_with_tools = llm.bind_tools(tools)

# The LLM can now decide to call these tools
response = llm_with_tools.invoke("What is the Python course fee and EMI for 6 months?")
print(response.tool_calls)
# [{'name': 'search_courses', 'args': {'query': 'Python'}, 'id': '...'}]
```

---

## Limitations of Simple Agents

| Limitation | Description |
|-----------|-------------|
| No state management | Cannot track complex multi-step workflows |
| No conditional routing | Cannot choose different paths based on results |
| No human-in-the-loop | Cannot pause for human approval |
| No checkpoints | Cannot save and resume |
| Limited error handling | Hard to recover from tool failures |

These limitations are why **LangGraph** was created -- it provides state machines, conditional routing, checkpoints, and human-in-the-loop support.

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| AI Agent | LLM + tools + reasoning loop -- decides and acts |
| ReAct | Reasoning + Acting -- think, act, observe, repeat |
| Tool | A Python function the agent can call |
| Tool call | Structured request from LLM to run a function |
| Brain (LLM) | Decides which tool to use and when to stop |
| Orchestrator | Controls the think-act-observe loop |
| Key difference | Chatbot answers; agent acts and solves |

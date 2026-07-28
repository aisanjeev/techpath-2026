# Memory Systems for AI Agents

**Module 11 -- LangGraph | Topic 4**

---

## Why Do Agents Need Memory?

Without memory, every conversation starts from scratch. The agent cannot remember that Rahul asked about Python courses yesterday, or that Priya prefers weekend batches.

**Analogy:** Imagine calling TechPath Institute and getting a different receptionist every time, and each one has never heard of you. You would have to explain everything from the beginning. Memory lets the agent be like a receptionist who remembers you.

### Three Types of Memory

| Type | What It Remembers | Duration | Example |
|------|------------------|----------|---------|
| **Short-term** | Current conversation messages | Until session ends | "You asked about Python 2 minutes ago" |
| **Long-term** | Facts and preferences across sessions | Persistent | "Rahul prefers morning batches" |
| **Episodic** | Complete past interactions | Persistent | "Last Tuesday, Amit asked about a refund" |

---

## Short-Term Memory (Message History)

This is the simplest and most common form. The conversation messages are stored in the graph's state.

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]   # This IS short-term memory
```

Every message (user, assistant, tool results) gets appended to this list. The LLM sees the full conversation history and can refer to earlier messages.

### Example: Remembering Context

```
User:    "What Python courses are available?"
Agent:   "We offer Python Full Stack for Rs 45,000."

User:    "How long is it?"        <-- "it" = the Python course
Agent:   "The course is 6 months."  <-- Agent knows "it" refers to Python Full Stack
                                       because it can see the previous messages
```

### The Problem: Token Limits

LLMs have a maximum context window (e.g., 128K tokens for GPT-4o). For very long conversations, you cannot send all messages. You need to trim old ones.

```python
from langchain_core.messages import trim_messages

trimmer = trim_messages(
    max_tokens=4000,
    strategy="last",           # Keep the most recent messages
    token_counter=llm,
    include_system=True,       # Always keep the system prompt
)

# Use in your agent node
def agent_node(state):
    trimmed = trimmer.invoke(state["messages"])
    response = llm.invoke(trimmed)
    return {"messages": [response]}
```

### Trimming Strategies

| Strategy | What It Keeps | Best For |
|----------|-------------|----------|
| `"last"` | Most recent N tokens | Most conversations |
| `"first"` | First N tokens | When opening context matters |

---

## Long-Term Memory (Vector Store)

Long-term memory stores facts across sessions. When the agent needs to recall something about a user, it searches the memory store.

### Storing User Facts

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# Store facts about students
facts = [
    "Rahul Sharma is interested in Python and web development",
    "Rahul prefers morning batch timings (10 AM to 1 PM)",
    "Priya Patel wants weekend batches only",
    "Priya is from Indore and needs online classes",
    "Amit Kumar has completed the HTML/CSS module",
    "Amit wants to learn React next",
    "Sneha Gupta is a working professional, needs evening batches",
    "Ananya from Delhi asked about the Data Science course",
]

memory_store = FAISS.from_texts(facts, embeddings)
memory_store.save_local("student_memories")
```

### Retrieving Relevant Memories

```python
# When Rahul messages again, search for his info
results = memory_store.similarity_search("Tell me about Rahul", k=2)
for doc in results:
    print(f"- {doc.page_content}")
# - Rahul Sharma is interested in Python and web development
# - Rahul prefers morning batch timings (10 AM to 1 PM)
```

### Using Memory in an Agent

```python
@tool
def recall_student_info(student_name: str) -> str:
    """Recall what we know about a student from previous interactions.
    
    Args:
        student_name: The student's name
    """
    results = memory_store.similarity_search(f"about {student_name}", k=3)
    if results:
        return "Known facts:\n" + "\n".join(f"- {r.page_content}" for r in results)
    return f"No previous information about {student_name}"
```

### Saving New Memories

```python
@tool
def remember_fact(fact: str) -> str:
    """Save a new fact about a student for future reference.
    
    Args:
        fact: The fact to remember (e.g., "Rahul wants to learn Django")
    """
    memory_store.add_texts([fact])
    memory_store.save_local("student_memories")
    return f"Remembered: {fact}"
```

---

## Episodic Memory

Episodic memory stores **complete past interactions** as episodes. This lets the agent answer questions like "What happened last time Vikram contacted us?"

### Storing Episodes

```python
episodes = [
    {
        "student": "Vikram",
        "date": "2026-07-20",
        "summary": "Asked about refund for Django course. Offered reschedule to September batch.",
        "outcome": "Accepted September batch with Rs 2,000 discount",
    },
    {
        "student": "Ananya",
        "date": "2026-07-18",
        "summary": "Inquired about Python Full Stack course fees and EMI options.",
        "outcome": "Enrolled in August batch, chose 6-month EMI of Rs 7,500/month",
    },
    {
        "student": "Rahul",
        "date": "2026-07-15",
        "summary": "Asked about placement stats and average packages after course.",
        "outcome": "Shared placement report. Rahul is considering enrollment.",
    },
]

# Convert to text for vector storage
episode_texts = [
    f"[{ep['date']}] {ep['student']}: {ep['summary']} Outcome: {ep['outcome']}"
    for ep in episodes
]

episode_store = FAISS.from_texts(episode_texts, embeddings)
```

### Recalling Episodes

```python
results = episode_store.similarity_search("Vikram refund", k=1)
print(results[0].page_content)
# "[2026-07-20] Vikram: Asked about refund for Django course..."
```

---

## Memory in LangGraph with Checkpoints

LangGraph checkpoints automatically save and restore conversation state:

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Conversation 1 with Rahul
config_rahul = {"configurable": {"thread_id": "rahul-session-1"}}

app.invoke(
    {"messages": [("user", "Hi, I am Rahul from Bhopal")]},
    config_rahul
)
app.invoke(
    {"messages": [("user", "Tell me about Python courses")]},
    config_rahul   # Same thread_id = agent remembers previous messages
)

# Separate conversation with Priya
config_priya = {"configurable": {"thread_id": "priya-session-1"}}

app.invoke(
    {"messages": [("user", "Hi, I am Priya from Indore")]},
    config_priya   # Different thread_id = fresh conversation
)
```

---

## Combining All Three Memory Types

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]   # Short-term memory
    # Long-term and episodic memory accessed via tools

tools = [
    search_courses,
    calculate_emi,
    recall_student_info,    # Long-term memory (reads)
    remember_fact,          # Long-term memory (writes)
]
```

### Flow with Memory

```
User: "Hi, this is Rahul. What was that Python course you told me about?"
  |
  v
Agent: recall_student_info("Rahul")
  --> "Rahul is interested in Python and web development, prefers morning batches"
  |
  v
Agent: search_courses("Python")
  --> "Python Full Stack: Rs 45,000, 6 months"
  |
  v
Agent: "Hi Rahul! The Python Full Stack course I mentioned is Rs 45,000 
        for 6 months. Since you prefer morning batches, the 10 AM slot 
        would be perfect for you."
```

---

## Summary

| Memory Type | Scope | Storage | Access Method |
|------------|-------|---------|---------------|
| Short-term | Current conversation | State (messages list) | Automatic via `add_messages` |
| Long-term | Across all sessions | Vector store (FAISS) | Via recall/remember tools |
| Episodic | Past interactions | Vector store | Via episode search tool |
| Checkpoints | Per-thread state | MemorySaver / DB | Automatic via thread_id |

| Best Practice | Why |
|--------------|-----|
| Trim old messages | Prevents exceeding token limits |
| Use thread_id for each user | Keeps conversations separate |
| Save important facts explicitly | Long-term memory does not happen automatically |
| Handle "I don't remember" | Not every query will have matching memories |

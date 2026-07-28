# Module 11: LangGraph -- AI Agents and Agentic Workflows

## 1. What is an AI Agent?

### The Big Idea

Think of an AI agent like a smart assistant at the TechPath Institute front desk. When a student asks "Which Python course should I take?", a regular chatbot gives a fixed answer. But an **agent** can:

1. **Think** about what the student needs
2. **Use tools** -- check the course database, look at available batches, check fees
3. **Reason** about the results -- "This student knows basics, so the advanced course fits better"
4. **Act** -- give a personalized recommendation

An AI agent is an LLM (like GPT-4 or Claude) that can **decide what to do next**, **use tools**, and **loop until the task is done**.

### The ReAct Pattern

ReAct stands for **Reasoning + Acting**. It is the most common pattern for building agents.

```
Loop:
  1. THINK  -- "I need to find courses in Bhopal"
  2. ACT    -- Call the search_courses tool
  3. OBSERVE -- "Found 3 courses: Python Basics, Django, Full Stack"
  4. THINK  -- "The student asked about web development, so Django fits"
  5. ACT    -- Call the get_course_details tool for Django
  6. OBSERVE -- "Django course: 12 weeks, Rs. 15,000, starts August"
  7. RESPOND -- "I recommend our Django course..."
```

The agent keeps looping through Think-Act-Observe until it has enough information to give a final answer.

### Key Components of an Agent

| Component | What It Does | Example |
|-----------|-------------|---------|
| **LLM (Brain)** | Decides what to do next | GPT-4, Claude, Gemini |
| **Tools** | Actions the agent can take | Search database, calculate, call APIs |
| **Memory** | Remembers past interactions | Chat history, student preferences |
| **Reasoning** | Plans and reflects | "I should check the fee before recommending" |
| **Orchestrator** | Controls the loop | LangGraph state machine |

---

## 2. LangGraph Fundamentals

### What is LangGraph?

LangGraph is a Python library by LangChain for building **stateful, multi-step AI workflows**. Think of it like a flowchart that your AI follows.

**Why not just use LangChain?** LangChain is great for simple chains (do A, then B, then C). But agents need **loops**, **conditions**, and **state** -- that is where LangGraph comes in.

### Installation

```bash
pip install langgraph langchain langchain-openai python-dotenv
```

### Core Concepts

#### State

State is the data that flows through your graph. It is like a shared notebook that every step can read and write to.

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]   # Chat history
    current_step: str                          # Where we are
    tool_results: dict                         # Results from tools
```

The `Annotated[list, add_messages]` is special -- it tells LangGraph to **append** new messages instead of replacing the list.

#### Nodes

Nodes are the **actions** in your flowchart. Each node is a Python function that takes the state and returns updated state.

```python
def chatbot_node(state: AgentState):
    """The LLM thinks and decides what to do."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def tool_node(state: AgentState):
    """Execute the tool the LLM asked for."""
    last_message = state["messages"][-1]
    tool_name = last_message.tool_calls[0]["name"]
    # Run the tool and return result
    result = run_tool(tool_name, last_message.tool_calls[0]["args"])
    return {"messages": [result]}
```

#### Edges

Edges connect nodes together. There are two types:

1. **Normal edges** -- always go from A to B
2. **Conditional edges** -- choose the next node based on the state

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState)

# Add nodes
graph.add_node("chatbot", chatbot_node)
graph.add_node("tools", tool_node)

# Normal edge: after tools, always go back to chatbot
graph.add_edge("tools", "chatbot")

# Conditional edge: chatbot decides whether to use tools or finish
graph.add_conditional_edges(
    "chatbot",
    should_use_tool,          # Function that returns "tools" or "end"
    {"tools": "tools", "end": END}
)

# Set entry point
graph.set_entry_point("chatbot")
```

#### The Routing Function

```python
def should_use_tool(state: AgentState) -> str:
    """Decide: does the LLM want to call a tool, or is it done?"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"        # LLM wants to use a tool
    return "end"              # LLM gave a final answer
```

### Putting It Together -- The Agent Loop

```
                    +----------+
                    | START    |
                    +----+-----+
                         |
                    +----v-----+
             +----->| Chatbot  |------+
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

The graph loops: Chatbot -> Tools -> Chatbot -> Tools -> ... -> END

### Checkpoints (Saving State)

Checkpoints let you save the agent's state at any point, so you can:
- Resume a conversation later
- Implement human-in-the-loop (pause, wait for approval, continue)
- Debug by replaying from a saved state

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Every conversation gets a thread_id
config = {"configurable": {"thread_id": "student-rahul-001"}}
result = app.invoke({"messages": [("user", "Show me Python courses")]}, config)
```

---

## 3. Building Custom Tools for Agents

### What Are Tools?

Tools are Python functions that the agent can call. The LLM reads the function name, description, and parameters to decide when and how to use each tool.

### Creating Tools with LangChain

```python
from langchain_core.tools import tool

@tool
def search_courses(query: str, city: str = "Bhopal") -> str:
    """Search for TechPath Institute courses by topic and city.
    
    Args:
        query: What the student wants to learn (e.g., "Python", "web development")
        city: City to search in (default: Bhopal)
    """
    # In a real app, this would query a database
    courses = {
        "python": {"name": "Python Full Stack", "fee": 25000, "duration": "16 weeks"},
        "web": {"name": "Web Development", "fee": 20000, "duration": "12 weeks"},
        "data": {"name": "Data Science", "fee": 30000, "duration": "20 weeks"},
    }
    for key, course in courses.items():
        if key in query.lower():
            return f"Found: {course['name']} in {city} -- Rs. {course['fee']}, {course['duration']}"
    return f"No courses found for '{query}' in {city}"


@tool
def calculate_emi(total_fee: float, months: int) -> str:
    """Calculate monthly EMI for a course fee.
    
    Args:
        total_fee: Total course fee in Rupees
        months: Number of monthly installments
    """
    emi = total_fee / months
    return f"EMI for Rs. {total_fee:,.0f} over {months} months = Rs. {emi:,.0f}/month"


@tool
def check_batch_availability(course_name: str) -> str:
    """Check available batches and start dates for a course.
    
    Args:
        course_name: Name of the course to check
    """
    batches = [
        {"date": "August 5, 2026", "time": "10:00 AM", "seats": 8},
        {"date": "September 1, 2026", "time": "2:00 PM", "seats": 15},
    ]
    result = f"Available batches for {course_name}:\n"
    for b in batches:
        result += f"  - {b['date']} ({b['time']}) -- {b['seats']} seats left\n"
    return result
```

### Tool Design Best Practices

| Practice | Why It Matters |
|----------|---------------|
| Clear function name | LLM uses the name to decide when to call it |
| Detailed docstring | LLM reads the description to understand what the tool does |
| Type hints on args | LLM knows what type of data to pass |
| Return strings | LLM can easily read and reason about the result |
| Handle errors | Return error messages, do not raise exceptions |

### Common Tool Types

- **Search tools** -- look up data in a database or API
- **Calculator tools** -- do math the LLM might get wrong
- **API tools** -- call external services (weather, maps, payment)
- **Database tools** -- query, insert, update records
- **File tools** -- read/write files, generate reports

---

## 4. Memory Systems

### Why Agents Need Memory

Without memory, every conversation starts fresh. The agent cannot remember that Priya asked about Python courses yesterday, or that Amit prefers weekend batches.

### Short-Term Memory (Message History)

This is the simplest form -- just keep the conversation messages in the state.

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # This IS short-term memory
```

LangGraph's `add_messages` annotation automatically manages the message list. Each new message gets appended.

**Limitation:** The context window has a token limit. For long conversations, you need to trim old messages.

```python
from langchain_core.messages import trim_messages

trimmer = trim_messages(
    max_tokens=4000,
    strategy="last",          # Keep the most recent messages
    token_counter=llm,
    include_system=True,      # Always keep the system message
)
```

### Long-Term Memory (Vector Store)

For remembering facts across sessions -- like student preferences or past interactions.

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Store facts about students
embeddings = OpenAIEmbeddings()
memory_store = FAISS.from_texts(
    [
        "Rahul is interested in Python and web development",
        "Priya prefers weekend batches",
        "Amit has completed the HTML/CSS module",
        "Neha is from Indore and wants online classes",
    ],
    embeddings
)

# Later, retrieve relevant memories
results = memory_store.similarity_search("Tell me about Rahul", k=2)
```

### Episodic Memory

Episodic memory stores **complete past interactions** -- like remembering "Last Tuesday, Vikram asked about refund policy and we helped him reschedule."

```python
# Store a full episode
episode = {
    "student": "Vikram",
    "date": "2026-07-20",
    "summary": "Asked about refund for Django course, offered reschedule to September batch",
    "outcome": "Accepted September batch, applied Rs. 2000 discount",
}
```

### Memory Comparison

| Type | Scope | Duration | Use Case |
|------|-------|----------|----------|
| **Short-term** | Current conversation | Until session ends | Chat context |
| **Long-term** | Across sessions | Persistent | Student profiles, preferences |
| **Episodic** | Past interactions | Persistent | "What happened last time?" |

---

## 5. Multi-Agent Systems

### Why Multiple Agents?

One agent trying to do everything is like one employee handling reception, teaching, billing, and marketing. It works for simple tasks but gets overwhelmed with complex ones.

Multi-agent systems split the work among **specialized agents**, each expert in one area.

### The Supervisor Pattern

A **supervisor agent** receives the task, decides which specialist to assign it to, and coordinates the work.

```
                    +------------+
                    | Supervisor |
                    +-----+------+
                          |
            +-------------+-------------+
            |             |             |
       +----v----+   +----v----+   +----v----+
       |Research |   | Writer  |   |  Coder  |
       | Agent   |   | Agent   |   |  Agent  |
       +---------+   +---------+   +---------+
```

```python
from langgraph.graph import StateGraph, END

def supervisor_node(state):
    """Decide which agent should handle the current task."""
    messages = state["messages"]
    # LLM decides: "research", "writer", "coder", or "FINISH"
    response = supervisor_llm.invoke(messages)
    return {"next_agent": response.content}

def research_node(state):
    """Research agent: finds information."""
    # Uses search tools to gather data
    result = research_llm.invoke(state["messages"])
    return {"messages": [result]}

def writer_node(state):
    """Writer agent: creates content."""
    result = writer_llm.invoke(state["messages"])
    return {"messages": [result]}

def coder_node(state):
    """Coder agent: writes and explains code."""
    result = coder_llm.invoke(state["messages"])
    return {"messages": [result]}
```

### Agent Handoffs

When one agent finishes its part, it hands off to the next agent. The supervisor decides the routing.

```python
def route_to_agent(state) -> str:
    """Route to the correct agent based on supervisor decision."""
    next_agent = state.get("next_agent", "FINISH")
    if next_agent == "FINISH":
        return END
    return next_agent

graph.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "research": "research",
        "writer": "writer",
        "coder": "coder",
        END: END,
    }
)
```

### Hierarchical Agent Teams

For very complex tasks, you can create **teams of agents** with their own supervisors.

```
                    +-------------------+
                    | Top Supervisor    |
                    +--------+----------+
                             |
               +-------------+-------------+
               |                           |
        +------v-------+           +-------v------+
        | Content Team |           | Tech Team    |
        | Supervisor   |           | Supervisor   |
        +------+-------+           +-------+------+
               |                           |
          +----+----+                 +----+----+
          |         |                 |         |
       Writer   Researcher        Coder    Tester
```

---

## 6. Human-in-the-Loop

### Why Involve Humans?

Some agent decisions are too important for full automation:
- Approving a refund of Rs. 15,000
- Sending an email to all students
- Making changes to a student's enrollment

### Interrupt and Resume

LangGraph lets you **pause** the agent at specific nodes and wait for human input.

```python
# Compile with interrupt_before -- pause BEFORE the action node
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["send_email"]    # Pause before sending
)

# Run until it hits the interrupt point
result = app.invoke(
    {"messages": [("user", "Send discount email to all Bhopal students")]},
    config
)

# Show the human what the agent wants to do
print("Agent wants to send this email:")
print(result["draft_email"])

# Human approves? Resume the graph
approval = input("Approve? (yes/no): ")
if approval == "yes":
    app.invoke(None, config)    # Continue from where it paused
```

### Approval Flows

```
User Request -> Agent Plans -> PAUSE -> Human Reviews -> APPROVE/REJECT -> Agent Executes
```

```python
def approval_node(state):
    """Check if human approved the action."""
    if state.get("human_approval") == "approved":
        return {"next": "execute"}
    return {"next": "cancel"}
```

### Human Feedback Integration

The agent can ask the human for clarification mid-task:

```python
def ask_human_node(state):
    """Pause and ask the human a question."""
    question = state["agent_question"]
    # In a real app, this would show a UI prompt
    return {"waiting_for": "human_response"}
```

---

## 7. LangSmith: Observability and Debugging

### What is LangSmith?

LangSmith is a platform by LangChain for **monitoring, debugging, and testing** your AI agents. Think of it like Chrome DevTools but for AI workflows.

### Setting Up LangSmith

```bash
pip install langsmith
```

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"
os.environ["LANGCHAIN_PROJECT"] = "techpath-course-agent"
```

Once set, every LLM call, tool call, and graph step is automatically logged.

### What You Can See in Traces

| Feature | What It Shows |
|---------|--------------|
| **Call tree** | Every step the agent took, in order |
| **Inputs/Outputs** | What went into and came out of each step |
| **Token usage** | How many tokens each step consumed |
| **Latency** | How long each step took |
| **Errors** | Where and why things broke |
| **Tool calls** | Which tools were called with what arguments |

### Debugging Common Issues

**Agent stuck in a loop:**
- Check the trace -- is the LLM calling the same tool repeatedly?
- Fix: Add a max iterations limit or better tool descriptions

**Wrong tool selected:**
- Check the tool descriptions -- are they clear enough?
- Fix: Make tool names and descriptions more specific

**Slow responses:**
- Check latency per step -- which step is the bottleneck?
- Fix: Use caching, simpler models for easy decisions, or parallel tool calls

### Evaluations

LangSmith lets you run automated tests on your agent:

```python
from langsmith import Client

client = Client()

# Create a dataset of test cases
dataset = client.create_dataset("course-agent-tests")
client.create_examples(
    inputs=[
        {"question": "What Python courses are available in Bhopal?"},
        {"question": "Calculate EMI for Rs. 25000 over 6 months"},
        {"question": "Are there weekend batches for Django?"},
    ],
    outputs=[
        {"expected": "Should mention Python Full Stack course"},
        {"expected": "Should return Rs. 4,167/month"},
        {"expected": "Should check batch availability"},
    ],
    dataset_id=dataset.id
)
```

---

## 8. Agentic RAG

### What is Agentic RAG?

Regular RAG (Retrieval-Augmented Generation) searches a document store and generates an answer. **Agentic RAG** adds intelligence -- the agent can:

1. **Decide** whether it needs to search at all
2. **Rewrite** the query if results are poor
3. **Search multiple times** with different queries
4. **Reflect** on whether the answer is good enough
5. **Retry** if the answer is incomplete

### The Agentic RAG Flow

```
User Question
     |
     v
  +--+---+        +----------+
  | Route |------->| Direct   |  (If the agent already knows the answer)
  +--+---+        | Answer   |
     |             +----------+
     v
  +--+--------+
  | Rewrite   |  (Improve the search query)
  | Query     |
  +--+--------+
     |
     v
  +--+--------+
  | Search    |  (Query the vector store)
  | Documents |
  +--+--------+
     |
     v
  +--+--------+      +----------+
  | Grade     |---NO->| Rewrite  |  (Documents not relevant? Try again)
  | Documents |       | & Retry  |
  +--+--------+       +----------+
     |
     YES
     v
  +--+--------+
  | Generate  |  (Create the answer from documents)
  | Answer    |
  +--+--------+
     |
     v
  +--+-----------+      +----------+
  | Check Answer |--NO-->| Retry    |  (Answer not good? Search again)
  | Quality      |       | Search   |
  +--+-----------+       +----------+
     |
     YES
     v
  Final Answer
```

### Building Agentic RAG with LangGraph

```python
class RAGState(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    documents: list
    generation: str
    retry_count: int

def retrieve_node(state):
    """Search the document store."""
    question = state["question"]
    docs = vector_store.similarity_search(question, k=4)
    return {"documents": docs}

def grade_documents_node(state):
    """Check if retrieved documents are relevant."""
    docs = state["documents"]
    question = state["question"]
    
    graded = []
    for doc in docs:
        # Use LLM to grade relevance
        score = grader_llm.invoke(
            f"Is this document relevant to '{question}'?\n\n{doc.page_content}"
        )
        if "yes" in score.content.lower():
            graded.append(doc)
    
    return {"documents": graded}

def rewrite_query_node(state):
    """Rewrite the query for better search results."""
    question = state["question"]
    rewritten = rewriter_llm.invoke(
        f"Rewrite this search query to get better results: {question}"
    )
    return {"question": rewritten.content, "retry_count": state["retry_count"] + 1}

def generate_node(state):
    """Generate answer from relevant documents."""
    docs = state["documents"]
    question = state["question"]
    context = "\n\n".join([doc.page_content for doc in docs])
    
    answer = generator_llm.invoke(
        f"Answer based on this context:\n{context}\n\nQuestion: {question}"
    )
    return {"generation": answer.content}

def should_retry(state) -> str:
    """Decide whether to retry or finish."""
    if not state["documents"]:
        if state["retry_count"] < 3:
            return "rewrite"
        return "end"
    return "generate"
```

### Key Differences: Regular RAG vs Agentic RAG

| Feature | Regular RAG | Agentic RAG |
|---------|------------|-------------|
| Query | Single fixed query | Rewrites query if needed |
| Search | One-shot | Multiple attempts |
| Quality check | None | Grades document relevance |
| Answer check | None | Verifies answer quality |
| Fallback | Returns whatever it gets | Retries or says "I don't know" |
| Complexity | Simple, fast | More steps, smarter results |

---

## Quick Reference: LangGraph Cheat Sheet

### Essential Imports
```python
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
```

### Minimal Agent Template
```python
from typing import TypedDict, Annotated

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [my_tool_1, my_tool_2]
llm_with_tools = llm.bind_tools(tools)

graph = StateGraph(State)
graph.add_node("agent", lambda s: {"messages": [llm_with_tools.invoke(s["messages"])]})
graph.add_node("tools", ToolNode(tools))
graph.add_edge("tools", "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.set_entry_point("agent")

app = graph.compile()
result = app.invoke({"messages": [("user", "Hello!")]})
```

### Key Terms Glossary

| Term | Meaning |
|------|---------|
| **Agent** | LLM + tools + reasoning loop |
| **State** | Data flowing through the graph |
| **Node** | A function that processes state |
| **Edge** | Connection between nodes |
| **Conditional edge** | Edge that chooses path based on state |
| **Checkpoint** | Saved snapshot of state |
| **Tool** | Function the agent can call |
| **ReAct** | Reasoning + Acting pattern |
| **RAG** | Retrieval-Augmented Generation |
| **Supervisor** | Agent that manages other agents |

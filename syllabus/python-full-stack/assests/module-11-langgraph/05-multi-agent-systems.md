# Multi-Agent Systems

**Module 11 -- LangGraph | Topic 5**

---

## Why Multiple Agents?

One agent handling everything is like one employee at TechPath doing reception, teaching, billing, and marketing all at once. It works for simple tasks but gets overwhelmed with complex ones.

Multi-agent systems split the work among **specialized agents**, each expert in one area.

| Single Agent | Multi-Agent |
|-------------|-------------|
| One LLM does everything | Specialized agents for each task |
| Gets confused on complex tasks | Each agent is focused and accurate |
| One long prompt with many tools | Short, focused prompts per agent |
| Hard to debug | Easy to debug (check each agent separately) |

---

## The Supervisor Pattern

The most common multi-agent architecture. A **supervisor agent** receives the task, decides which specialist should handle it, and coordinates the work.

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

### How the Supervisor Works

```
User: "Write a Python tutorial about lists with code examples"

Supervisor thinks: "This needs research and coding. Let me route to the right agents."

Step 1: Supervisor --> Research Agent
        "Find key concepts about Python lists that beginners need to know"
        Research Agent returns: "lists, indexing, slicing, append, remove, loops..."

Step 2: Supervisor --> Writer Agent
        "Write a beginner tutorial covering these concepts"
        Writer Agent returns: "Python lists are like containers..."

Step 3: Supervisor --> Coder Agent
        "Write code examples for each concept in the tutorial"
        Coder Agent returns: "fruits = ['apple', 'banana']..."

Step 4: Supervisor --> Final Answer
        Combines everything into a complete tutorial
```

### Building a Supervisor Agent

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

supervisor_llm = ChatOpenAI(model="gpt-4o-mini")
research_llm = ChatOpenAI(model="gpt-4o-mini")
writer_llm = ChatOpenAI(model="gpt-4o-mini")
coder_llm = ChatOpenAI(model="gpt-4o-mini")

def supervisor_node(state):
    """Decide which agent should handle the task next."""
    messages = state["messages"]
    response = supervisor_llm.invoke([
        ("system", """You are a team supervisor. Based on the conversation,
        decide who should work next:
        - "research" for finding information
        - "writer" for creating content
        - "coder" for writing code
        - "FINISH" if the task is complete"""),
        *messages
    ])
    return {"next_agent": response.content.strip().lower()}

def research_node(state):
    """Research agent: gathers information."""
    response = research_llm.invoke([
        ("system", "You are a research expert. Find and summarize information."),
        *state["messages"]
    ])
    return {"messages": [("assistant", f"[Research]: {response.content}")]}

def writer_node(state):
    """Writer agent: creates content."""
    response = writer_llm.invoke([
        ("system", "You are a content writer. Write clear, beginner-friendly content."),
        *state["messages"]
    ])
    return {"messages": [("assistant", f"[Writer]: {response.content}")]}

def coder_node(state):
    """Coder agent: writes and explains code."""
    response = coder_llm.invoke([
        ("system", "You are a Python expert. Write clean, commented code."),
        *state["messages"]
    ])
    return {"messages": [("assistant", f"[Coder]: {response.content}")]}
```

---

## Agent Handoffs

When one agent finishes its part, the supervisor decides who goes next. This is done with **conditional routing**.

```python
def route_to_agent(state) -> str:
    """Route to the correct agent based on supervisor's decision."""
    next_agent = state.get("next_agent", "FINISH")
    if next_agent == "finish":
        return END
    return next_agent

# Build the graph
graph = StateGraph(AgentState)

# Add all nodes
graph.add_node("supervisor", supervisor_node)
graph.add_node("research", research_node)
graph.add_node("writer", writer_node)
graph.add_node("coder", coder_node)

# After each agent, go back to supervisor
graph.add_edge("research", "supervisor")
graph.add_edge("writer", "supervisor")
graph.add_edge("coder", "supervisor")

# Supervisor decides the next step
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

graph.set_entry_point("supervisor")
app = graph.compile()
```

### The Flow

```
User Question
      |
      v
 [Supervisor] --> "research"
      |
      v
 [Research Agent] --> results
      |
      v
 [Supervisor] --> "writer"
      |
      v
 [Writer Agent] --> content
      |
      v
 [Supervisor] --> "FINISH"
      |
      v
   [END]
```

---

## Hierarchical Agent Teams

For very complex tasks, you can create **teams of agents**, each with their own supervisor.

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

### Example: TechPath Course Creation Team

```python
# Content Team handles research and writing
content_team = StateGraph(AgentState)
content_team.add_node("content_supervisor", content_supervisor_node)
content_team.add_node("researcher", research_node)
content_team.add_node("writer", writer_node)
# ... edges ...
content_app = content_team.compile()

# Tech Team handles code and testing
tech_team = StateGraph(AgentState)
tech_team.add_node("tech_supervisor", tech_supervisor_node)
tech_team.add_node("coder", coder_node)
tech_team.add_node("tester", tester_node)
# ... edges ...
tech_app = tech_team.compile()

# Top-level graph coordinates both teams
top_graph = StateGraph(AgentState)
top_graph.add_node("top_supervisor", top_supervisor_node)
top_graph.add_node("content_team", content_app)
top_graph.add_node("tech_team", tech_app)
```

---

## Practical Example: TechPath Support System

A multi-agent system for handling student inquiries:

```python
# Agent 1: Course Advisor
def course_advisor_node(state):
    """Recommends courses based on student interests."""
    response = llm.invoke([
        ("system", """You are a TechPath Institute course advisor.
        Recommend courses based on the student's interests and goals.
        Courses: Python Full Stack (Rs 45,000), Data Science (Rs 55,000),
        Web Development (Rs 30,000), AI/ML (Rs 60,000)."""),
        *state["messages"]
    ])
    return {"messages": [response]}

# Agent 2: Fee Calculator
def fee_calculator_node(state):
    """Handles fee calculations, EMIs, and discounts."""
    response = llm.invoke([
        ("system", """You are a TechPath fee calculator.
        Calculate fees, EMIs, and apply discounts.
        EMI options: 3, 6, or 12 months.
        Early bird discount: 10% off if enrolled before month end."""),
        *state["messages"]
    ])
    return {"messages": [response]}

# Agent 3: Schedule Planner
def schedule_planner_node(state):
    """Handles batch timings and scheduling."""
    response = llm.invoke([
        ("system", """You are a TechPath schedule planner.
        Available batches: Morning (10 AM-1 PM), Afternoon (2-5 PM),
        Weekend (Sat-Sun 10 AM-4 PM). Online batches also available."""),
        *state["messages"]
    ])
    return {"messages": [response]}
```

---

## Agent Communication Patterns

| Pattern | How Agents Communicate | Best For |
|---------|----------------------|----------|
| **Supervisor** | All agents report to one coordinator | Most use cases |
| **Sequential** | Agent A passes to Agent B passes to Agent C | Pipeline tasks |
| **Parallel** | Multiple agents work simultaneously | Independent subtasks |
| **Debate** | Two agents discuss and reach consensus | Quality-critical decisions |

---

## Preventing Infinite Loops

Multi-agent systems can get stuck in loops if agents keep routing to each other. Set a maximum number of iterations:

```python
# Method 1: Add iteration counter to state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str
    iteration: int

def supervisor_node(state):
    if state.get("iteration", 0) >= 5:
        return {"next_agent": "FINISH", "iteration": state.get("iteration", 0) + 1}
    # ... normal routing logic ...
    return {"next_agent": decision, "iteration": state.get("iteration", 0) + 1}

# Method 2: Use recursion_limit when compiling
app = graph.compile()
result = app.invoke(input, config={"recursion_limit": 20})
```

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Multi-agent | Split complex tasks among specialized agents |
| Supervisor | Central agent that routes tasks to specialists |
| Handoff | One agent finishes, supervisor routes to the next |
| Hierarchical | Teams of agents with their own supervisors |
| Sequential | Agents work one after another in a pipeline |
| Parallel | Multiple agents work at the same time |
| Recursion limit | Prevents infinite loops between agents |
| Key benefit | Each agent has focused expertise and a simple prompt |

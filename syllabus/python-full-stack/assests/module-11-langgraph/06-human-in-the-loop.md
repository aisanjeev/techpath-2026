# Human-in-the-Loop

**Module 11 -- LangGraph | Topic 6**

---

## Why Involve Humans?

AI agents are powerful, but some decisions are too important for full automation. You would not want an agent to:
- Process a refund of Rs 15,000 without someone checking
- Send a bulk email to all students without review
- Change a student's enrollment without confirmation

Human-in-the-loop (HITL) lets the agent **pause** at critical points and wait for a human to approve, reject, or modify the action before continuing.

**Analogy:** Think of it like a bank where a teller can process small withdrawals, but withdrawals above Rs 50,000 need a manager's signature. The agent handles routine tasks automatically but pauses for high-stakes decisions.

---

## Interrupt and Resume

LangGraph lets you define **interrupt points** -- nodes where the graph pauses and waits for human input.

### Setting Up Interrupts

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Build your graph with nodes
graph = StateGraph(AgentState)
graph.add_node("plan_action", plan_action_node)
graph.add_node("execute_action", execute_action_node)
graph.add_edge("plan_action", "execute_action")
graph.add_edge("execute_action", END)
graph.set_entry_point("plan_action")

# Compile with interrupt BEFORE the execute node
checkpointer = MemorySaver()
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute_action"]    # Pause BEFORE executing
)
```

### Running with Interrupts

```python
config = {"configurable": {"thread_id": "review-001"}}

# Step 1: Run until the interrupt point
result = app.invoke(
    {"messages": [("user", "Send discount email to all Bhopal students")]},
    config
)

# The graph pauses here -- the agent has planned the action but not executed it
print("Agent wants to do:")
print(result["planned_action"])
# "Send email: 'Special 20% discount on Python Full Stack' to 150 students in Bhopal"

# Step 2: Human reviews and decides
human_decision = input("Approve? (yes/no): ")

if human_decision == "yes":
    # Resume the graph -- it continues from where it paused
    result = app.invoke(None, config)
    print("Action executed!")
else:
    print("Action cancelled by human.")
```

---

## Interrupt Before vs Interrupt After

| Setting | When It Pauses | Use Case |
|---------|---------------|----------|
| `interrupt_before=["node"]` | Before the node runs | Review what the agent WANTS to do |
| `interrupt_after=["node"]` | After the node runs | Review what the agent DID |

```python
# Pause BEFORE executing (for approval)
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["send_email"]
)

# Pause AFTER executing (for review)
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_after=["generate_report"]
)
```

---

## Approval Flows

A common pattern: the agent plans an action, a human approves or rejects it, and the agent proceeds accordingly.

```
User Request
      |
      v
[Agent Plans Action]
      |
      v
[PAUSE -- Show plan to human]
      |
      v
Human: Approve? ----NO----> [Cancel / Modify]
      |
     YES
      |
      v
[Agent Executes Action]
      |
      v
[Return Result]
```

### Building an Approval Flow

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class ApprovalState(TypedDict):
    messages: Annotated[list, add_messages]
    planned_action: str
    approved: bool

def plan_node(state):
    """Agent plans what it wants to do."""
    messages = state["messages"]
    response = llm.invoke([
        ("system", "Plan the action but do NOT execute it. Describe what you would do."),
        *messages
    ])
    return {
        "messages": [response],
        "planned_action": response.content,
    }

def execute_node(state):
    """Execute the planned action (only runs if approved)."""
    if not state.get("approved", False):
        return {"messages": [("assistant", "Action was not approved. Cancelled.")]}
    
    # Execute the action
    action = state["planned_action"]
    result = perform_action(action)
    return {"messages": [("assistant", f"Done: {result}")]}

# Graph with interrupt
graph = StateGraph(ApprovalState)
graph.add_node("plan", plan_node)
graph.add_node("execute", execute_node)
graph.add_edge("plan", "execute")
graph.add_edge("execute", END)
graph.set_entry_point("plan")

app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["execute"]
)
```

### Using the Approval Flow

```python
config = {"configurable": {"thread_id": "approval-001"}}

# Agent plans the action
result = app.invoke(
    {"messages": [("user", "Refund Rs 5,000 to student Amit Kumar")]},
    config
)
print(f"Planned: {result['planned_action']}")

# Human approves
app.update_state(config, {"approved": True})
result = app.invoke(None, config)
print(result["messages"][-1])
```

---

## Human Feedback During Execution

Sometimes the agent needs to ask the human a question mid-task:

```python
def ask_clarification_node(state):
    """Ask the human for more information."""
    return {
        "messages": [("assistant", "Which batch timing do you prefer? Morning (10 AM) or Afternoon (2 PM)?")],
        "waiting_for": "human_response",
    }

# Interrupt after asking the question
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_after=["ask_clarification"]
)

# Run until it asks the question
result = app.invoke(
    {"messages": [("user", "Enroll me in Python course")]},
    config
)
# "Which batch timing do you prefer?"

# Human responds
result = app.invoke(
    {"messages": [("user", "Morning please")]},
    config
)
# Agent continues with the morning batch selection
```

---

## Practical Example: Course Enrollment Agent

```python
class EnrollmentState(TypedDict):
    messages: Annotated[list, add_messages]
    student_name: str
    course: str
    fee: float
    batch: str
    confirmed: bool

def collect_info_node(state):
    """Collect student information."""
    # LLM extracts info from conversation
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def show_summary_node(state):
    """Show enrollment summary for confirmation."""
    summary = f"""
    Enrollment Summary:
    Student: {state['student_name']}
    Course: {state['course']}
    Fee: Rs {state['fee']:,.0f}
    Batch: {state['batch']}
    
    Please confirm to proceed with enrollment.
    """
    return {"messages": [("assistant", summary)]}

def process_enrollment_node(state):
    """Process the enrollment (runs only after human confirmation)."""
    # Save to database, send confirmation email, etc.
    return {"messages": [("assistant", f"Enrollment confirmed for {state['student_name']}!")]}

# Graph with interrupt before processing
graph = StateGraph(EnrollmentState)
graph.add_node("collect", collect_info_node)
graph.add_node("summary", show_summary_node)
graph.add_node("process", process_enrollment_node)

graph.add_edge("collect", "summary")
graph.add_edge("summary", "process")
graph.add_edge("process", END)
graph.set_entry_point("collect")

app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["process"]    # Pause before processing enrollment
)
```

---

## When to Use Human-in-the-Loop

| Scenario | Should You Use HITL? | Why |
|----------|---------------------|-----|
| Answering FAQs | No | Low risk, routine task |
| Processing a refund | Yes | Financial action, needs approval |
| Sending bulk email | Yes | Affects many people, hard to undo |
| Course recommendation | No | Informational, no permanent action |
| Changing student records | Yes | Data modification, needs verification |
| Generating a report | Maybe | Low risk but review is good practice |

### The Rule

**If the action is irreversible or affects money/people, use human-in-the-loop.**

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Human-in-the-loop | Pause agent for human approval at critical points |
| `interrupt_before` | Pause before a node runs (approve what agent wants to do) |
| `interrupt_after` | Pause after a node runs (review what agent did) |
| Checkpointer | Required for interrupts -- saves state so graph can resume |
| `update_state()` | Modify the graph's state while paused (e.g., set approved=True) |
| Resume | Pass `None` to `invoke()` with same config to continue |
| Key rule | Use HITL for irreversible actions or anything involving money/people |

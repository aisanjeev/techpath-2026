"""
TechPath Institute -- Multi-Agent System: Supervisor Pattern
==============================================================
Demonstrates a supervisor agent that coordinates three specialized agents:
  1. Research Agent  -- finds information and answers factual questions
  2. Writer Agent    -- creates content, emails, summaries
  3. Coder Agent     -- writes and explains Python code

The supervisor reads the student's request, decides which specialist
to assign it to, and routes the conversation accordingly.

Install dependencies:
  pip install langgraph langchain langchain-openai python-dotenv

Setup:
  Create a .env file with your OpenAI API key:
    OPENAI_API_KEY=sk-your-key-here

Run:
  python code-multi-agent-system.py
"""

# ──────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────

import os
import json
from typing import TypedDict, Annotated, Literal
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()


# ──────────────────────────────────────────────
# 1. DEFINE THE STATE
# ──────────────────────────────────────────────
# The state carries messages AND tracks which agent should act next.

class MultiAgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str          # Which agent should handle this? Set by supervisor.
    task_history: list       # Track which agents have worked on this task


# ──────────────────────────────────────────────
# 2. CREATE SPECIALIZED LLMs
# ──────────────────────────────────────────────
# Each agent gets its own LLM instance with a specific system prompt.
# In production, you might use different models for different agents
# (e.g., a cheaper model for simple tasks, a powerful one for coding).

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- Supervisor System Prompt ---
SUPERVISOR_PROMPT = """You are the TechPath Institute Task Supervisor.
Your job is to read the student's request and decide which specialist agent
should handle it.

Available agents:
  - "research"  -- For factual questions, course info, comparisons, career advice
  - "writer"    -- For creating content: emails, study plans, summaries, notes
  - "coder"     -- For writing Python code, debugging, explaining code concepts

Rules:
1. Read the student's message carefully
2. Pick EXACTLY ONE agent that best fits the request
3. If the task is done (all agents have responded), say "FINISH"
4. Respond with ONLY a JSON object: {"next": "research"} or {"next": "writer"} or {"next": "coder"} or {"next": "FINISH"}

Do NOT include any other text -- only the JSON object.
"""

# --- Research Agent System Prompt ---
RESEARCH_PROMPT = """You are the Research Specialist at TechPath Institute, Bhopal.
You help students with:
- Finding course information and comparing options
- Career guidance for IT students in India
- Answering technical questions about programming topics
- Explaining concepts in simple language

TechPath courses and fees:
  - Python Full Stack: Rs. 25,000 (16 weeks)
  - Data Science: Rs. 30,000 (20 weeks)
  - Web Development: Rs. 20,000 (12 weeks)
  - AI Agents & LangGraph: Rs. 35,000 (10 weeks)
  - DevOps Engineering: Rs. 28,000 (14 weeks)

Location: Bhopal, Madhya Pradesh
EMI available: 2-12 months, no interest

Always be encouraging and use simple English. Use Indian Rupee (Rs.) for fees.
Keep responses concise but helpful.
"""

# --- Writer Agent System Prompt ---
WRITER_PROMPT = """You are the Content Writer at TechPath Institute, Bhopal.
You help students by creating:
- Study plans and learning roadmaps
- Email drafts (to instructors, for leave, for queries)
- Summaries and notes from topics
- LinkedIn/resume content for freshers
- Motivational messages and tips

Guidelines:
- Use simple English suitable for fresher students
- Include Indian context (Indian names, cities, Rupee amounts)
- Keep content practical and actionable
- Format nicely with headings, bullet points, and clear structure
"""

# --- Coder Agent System Prompt ---
CODER_PROMPT = """You are the Code Mentor at TechPath Institute, Bhopal.
You help students with:
- Writing Python code with clear comments
- Debugging and fixing errors
- Explaining code line by line
- Suggesting best practices
- Creating small project examples

Guidelines:
- Write clean, well-commented Python code
- Use Indian-context examples (student names like Rahul, Priya; Rs. for currency)
- Explain every important line in simple English
- Include how to run the code
- Show expected output
"""


# ──────────────────────────────────────────────
# 3. DEFINE THE NODES
# ──────────────────────────────────────────────

def supervisor_node(state: MultiAgentState):
    """
    The Supervisor reads the conversation and decides which
    specialist agent should handle the next step.

    It returns a JSON with {"next": "agent_name"} or {"next": "FINISH"}.
    """
    messages = [SystemMessage(content=SUPERVISOR_PROMPT)] + state["messages"]

    # Check if any agent has already responded in this round
    task_history = state.get("task_history", [])
    if task_history:
        # Add context about what has already been done
        history_note = f"\n\nAgents that have already responded: {', '.join(task_history)}. If the task is complete, respond with {{\"next\": \"FINISH\"}}."
        messages.append(HumanMessage(content=history_note))

    response = llm.invoke(messages)

    # Parse the supervisor's JSON response
    try:
        decision = json.loads(response.content.strip())
        next_agent = decision.get("next", "FINISH")
    except (json.JSONDecodeError, AttributeError):
        # If parsing fails, try to extract the agent name from text
        content = response.content.lower()
        if "research" in content:
            next_agent = "research"
        elif "writer" in content:
            next_agent = "writer"
        elif "coder" in content:
            next_agent = "coder"
        else:
            next_agent = "FINISH"

    print(f"  [Supervisor] Routing to: {next_agent}")
    return {"next_agent": next_agent}


def research_node(state: MultiAgentState):
    """Research Agent: handles factual questions and course information."""
    print("  [Research Agent] Working...")
    messages = [SystemMessage(content=RESEARCH_PROMPT)] + state["messages"]
    response = llm.invoke(messages)

    # Tag the response so we know which agent produced it
    tagged_response = AIMessage(
        content=f"[Research Agent]\n{response.content}"
    )

    task_history = state.get("task_history", [])
    task_history.append("research")

    return {"messages": [tagged_response], "task_history": task_history}


def writer_node(state: MultiAgentState):
    """Writer Agent: creates content, emails, study plans."""
    print("  [Writer Agent] Working...")
    messages = [SystemMessage(content=WRITER_PROMPT)] + state["messages"]
    response = llm.invoke(messages)

    tagged_response = AIMessage(
        content=f"[Writer Agent]\n{response.content}"
    )

    task_history = state.get("task_history", [])
    task_history.append("writer")

    return {"messages": [tagged_response], "task_history": task_history}


def coder_node(state: MultiAgentState):
    """Coder Agent: writes and explains Python code."""
    print("  [Coder Agent] Working...")
    messages = [SystemMessage(content=CODER_PROMPT)] + state["messages"]
    response = llm.invoke(messages)

    tagged_response = AIMessage(
        content=f"[Coder Agent]\n{response.content}"
    )

    task_history = state.get("task_history", [])
    task_history.append("coder")

    return {"messages": [tagged_response], "task_history": task_history}


# ──────────────────────────────────────────────
# 4. ROUTING FUNCTION
# ──────────────────────────────────────────────

def route_to_agent(state: MultiAgentState) -> str:
    """
    Conditional edge function: routes to the correct agent
    based on the supervisor's decision.
    """
    next_agent = state.get("next_agent", "FINISH")
    if next_agent == "FINISH":
        return END
    if next_agent in ("research", "writer", "coder"):
        return next_agent
    return END  # Safety fallback


# ──────────────────────────────────────────────
# 5. BUILD THE GRAPH
# ──────────────────────────────────────────────

def build_multi_agent_graph():
    """
    Build the multi-agent graph with supervisor pattern.

    Flow:
      START -> Supervisor -> (Research | Writer | Coder) -> Supervisor -> ... -> END

    The supervisor keeps routing to specialists until the task is done.
    """
    graph = StateGraph(MultiAgentState)

    # --- Add all nodes ---
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research", research_node)
    graph.add_node("writer", writer_node)
    graph.add_node("coder", coder_node)

    # --- Edges from specialists back to supervisor ---
    # After any specialist finishes, go back to supervisor
    # so it can decide: is the task done, or does another agent need to help?
    graph.add_edge("research", "supervisor")
    graph.add_edge("writer", "supervisor")
    graph.add_edge("coder", "supervisor")

    # --- Conditional edge from supervisor ---
    # Supervisor decides which specialist to call (or END)
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

    # --- Entry point ---
    graph.set_entry_point("supervisor")

    # --- Compile with checkpointing ---
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


# ──────────────────────────────────────────────
# 6. HELPER FUNCTIONS
# ──────────────────────────────────────────────

def run_task(app, task: str, thread_id: str = "task-001"):
    """Run a task through the multi-agent system and print results."""
    print(f"\n{'=' * 60}")
    print(f"Student Request: {task}")
    print(f"{'=' * 60}")

    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke(
        {
            "messages": [HumanMessage(content=task)],
            "next_agent": "",
            "task_history": [],
        },
        config
    )

    # Print the final agent response (last AI message)
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage):
            print(f"\n{msg.content}")
            break

    return result


def run_interactive(app):
    """Run the multi-agent system in interactive mode."""
    print("\n" + "=" * 60)
    print("  TechPath Institute -- Multi-Agent Assistant")
    print("  Specialists: Research | Writer | Coder")
    print("  Type your request below. Type 'quit' to exit.")
    print("=" * 60)

    task_counter = 0
    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print("\nThank you for using TechPath Multi-Agent Assistant! Happy learning!")
            break

        task_counter += 1
        run_task(app, user_input, thread_id=f"interactive-{task_counter}")


# ──────────────────────────────────────────────
# 7. MAIN -- DEMO SCENARIOS
# ──────────────────────────────────────────────

def main():
    """Run demo scenarios showing the supervisor routing to different agents."""

    app = build_multi_agent_graph()

    print("\n" + "#" * 60)
    print("#  TechPath Institute -- Multi-Agent System Demo")
    print("#")
    print("#  Supervisor Pattern:")
    print("#    Student Request -> Supervisor -> Specialist -> Response")
    print("#")
    print("#  Specialists:")
    print("#    Research Agent  -- facts, courses, career advice")
    print("#    Writer Agent    -- emails, study plans, summaries")
    print("#    Coder Agent     -- Python code, debugging, examples")
    print("#" * 60)

    # --- Scenario 1: Research question (routes to Research Agent) ---
    run_task(
        app,
        "I am Amit from Indore. I want to compare the Python Full Stack and "
        "Data Science courses at TechPath. Which one has better job prospects?",
        thread_id="scenario-1"
    )

    # --- Scenario 2: Writing task (routes to Writer Agent) ---
    run_task(
        app,
        "I am Sneha. I just completed the Web Development course at TechPath Institute. "
        "Can you help me write a LinkedIn post announcing my achievement?",
        thread_id="scenario-2"
    )

    # --- Scenario 3: Coding task (routes to Coder Agent) ---
    run_task(
        app,
        "I am Vikram, a Python beginner. Can you write a simple program that "
        "takes student marks in 5 subjects, calculates the percentage, "
        "and prints the grade? Use Indian grading system.",
        thread_id="scenario-3"
    )

    # --- Scenario 4: Mixed task (might involve multiple agents) ---
    run_task(
        app,
        "I am Neha from Mumbai. I want to learn AI but I have zero programming experience. "
        "What learning path should I follow? Also give me a simple first Python program to try.",
        thread_id="scenario-4"
    )

    # --- Interactive mode ---
    print("\n\n" + "-" * 60)
    print("Demo complete! Starting interactive mode...")
    print("-" * 60)

    run_interactive(app)


if __name__ == "__main__":
    main()

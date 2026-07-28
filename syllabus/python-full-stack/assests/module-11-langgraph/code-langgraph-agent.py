"""
TechPath Institute -- LangGraph ReAct Agent: Course Advisor
=============================================================
A fully runnable agent that helps students find TechPath courses,
calculate fees, and check batch availability using LangGraph.

This agent demonstrates:
  - LangGraph state graph with nodes and conditional edges
  - Custom tools (calculator, search simulator, course lookup)
  - The ReAct reasoning loop in action
  - Checkpointing for conversation memory

Install dependencies:
  pip install langgraph langchain langchain-openai python-dotenv

Setup:
  Create a .env file with your OpenAI API key:
    OPENAI_API_KEY=sk-your-key-here

Run:
  python code-langgraph-agent.py
"""

# ──────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────

import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables from .env file
load_dotenv()


# ──────────────────────────────────────────────
# 1. DEFINE THE STATE
# ──────────────────────────────────────────────
# State is like a shared notebook that every node in the graph
# can read and write to. The `add_messages` annotation tells
# LangGraph to APPEND new messages instead of replacing the list.

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ──────────────────────────────────────────────
# 2. BUILD CUSTOM TOOLS
# ──────────────────────────────────────────────
# Tools are Python functions the agent can call.
# The @tool decorator + docstring tells the LLM what each tool does.

# --- Course Database (simulated) ---
COURSE_DATABASE = {
    "python-fullstack": {
        "name": "Python Full Stack Development",
        "fee": 25000,
        "duration": "16 weeks",
        "city": "Bhopal",
        "topics": ["Python", "Django", "REST APIs", "React", "PostgreSQL"],
        "level": "Beginner to Advanced",
    },
    "data-science": {
        "name": "Data Science with Python",
        "fee": 30000,
        "duration": "20 weeks",
        "city": "Bhopal",
        "topics": ["Python", "Pandas", "NumPy", "ML", "Deep Learning"],
        "level": "Intermediate",
    },
    "web-dev": {
        "name": "Web Development Bootcamp",
        "fee": 20000,
        "duration": "12 weeks",
        "city": "Bhopal",
        "topics": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
        "level": "Beginner",
    },
    "ai-agents": {
        "name": "AI Agents & LangGraph",
        "fee": 35000,
        "duration": "10 weeks",
        "city": "Bhopal",
        "topics": ["LangChain", "LangGraph", "RAG", "Multi-Agent Systems"],
        "level": "Advanced",
    },
    "devops": {
        "name": "DevOps Engineering",
        "fee": 28000,
        "duration": "14 weeks",
        "city": "Pune",
        "topics": ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform"],
        "level": "Intermediate",
    },
}

BATCH_SCHEDULE = [
    {"course": "python-fullstack", "date": "August 5, 2026", "time": "10:00 AM", "seats": 8, "mode": "Offline"},
    {"course": "python-fullstack", "date": "September 1, 2026", "time": "7:00 PM", "seats": 15, "mode": "Online"},
    {"course": "data-science", "date": "August 12, 2026", "time": "2:00 PM", "seats": 5, "mode": "Offline"},
    {"course": "web-dev", "date": "August 8, 2026", "time": "10:00 AM", "seats": 12, "mode": "Online"},
    {"course": "ai-agents", "date": "September 15, 2026", "time": "6:00 PM", "seats": 10, "mode": "Online"},
    {"course": "devops", "date": "August 20, 2026", "time": "11:00 AM", "seats": 6, "mode": "Offline"},
]


@tool
def search_courses(query: str) -> str:
    """Search for TechPath Institute courses by topic, skill, or keyword.

    Args:
        query: What the student wants to learn (e.g., "Python", "web development", "AI")
    """
    query_lower = query.lower()
    results = []

    for key, course in COURSE_DATABASE.items():
        # Check if query matches course name, topics, or level
        searchable = f"{course['name']} {' '.join(course['topics'])} {course['level']}".lower()
        if query_lower in searchable or any(q in searchable for q in query_lower.split()):
            results.append(
                f"- {course['name']}\n"
                f"  Fee: Rs. {course['fee']:,} | Duration: {course['duration']} | "
                f"City: {course['city']} | Level: {course['level']}\n"
                f"  Topics: {', '.join(course['topics'])}"
            )

    if results:
        return f"Found {len(results)} course(s) at TechPath Institute:\n\n" + "\n\n".join(results)
    return f"No courses found matching '{query}'. Try searching for: Python, Web, Data Science, AI, or DevOps."


@tool
def calculate_emi(total_fee: float, months: int) -> str:
    """Calculate monthly EMI (installment) for a course fee. No interest charged.

    Args:
        total_fee: Total course fee in Rupees
        months: Number of monthly installments (2 to 12)
    """
    if months < 2 or months > 12:
        return "EMI is available for 2 to 12 months only."
    if total_fee <= 0:
        return "Fee must be a positive amount."

    emi = total_fee / months
    # TechPath offers a 5% discount for full upfront payment
    upfront_discount = total_fee * 0.05

    return (
        f"EMI Calculation for Rs. {total_fee:,.0f}:\n"
        f"  - Monthly EMI ({months} months): Rs. {emi:,.0f}/month\n"
        f"  - Total paid: Rs. {total_fee:,.0f}\n"
        f"  - Upfront payment discount (5%): Save Rs. {upfront_discount:,.0f}\n"
        f"  - Upfront price: Rs. {total_fee - upfront_discount:,.0f}"
    )


@tool
def check_batch_availability(course_name: str) -> str:
    """Check available batches, start dates, and seat availability for a course.

    Args:
        course_name: Name or keyword of the course (e.g., "Python", "Data Science")
    """
    course_lower = course_name.lower()
    matching_batches = []

    for batch in BATCH_SCHEDULE:
        course = COURSE_DATABASE.get(batch["course"], {})
        course_full_name = course.get("name", "").lower()
        if course_lower in course_full_name or course_lower in batch["course"]:
            matching_batches.append(
                f"  - {batch['date']} at {batch['time']} ({batch['mode']})\n"
                f"    Seats remaining: {batch['seats']}"
            )

    if matching_batches:
        return f"Available batches for '{course_name}':\n\n" + "\n".join(matching_batches)
    return f"No upcoming batches found for '{course_name}'. Contact TechPath Bhopal for custom scheduling."


@tool
def get_course_details(course_keyword: str) -> str:
    """Get detailed information about a specific course including syllabus topics.

    Args:
        course_keyword: Keyword to identify the course (e.g., "python", "ai-agents")
    """
    keyword_lower = course_keyword.lower()

    for key, course in COURSE_DATABASE.items():
        if keyword_lower in key or keyword_lower in course["name"].lower():
            topics_list = "\n".join(f"    {i+1}. {t}" for i, t in enumerate(course["topics"]))
            return (
                f"Course: {course['name']}\n"
                f"  Fee: Rs. {course['fee']:,}\n"
                f"  Duration: {course['duration']}\n"
                f"  City: {course['city']}\n"
                f"  Level: {course['level']}\n"
                f"  Syllabus Topics:\n{topics_list}\n\n"
                f"  Includes: Certificate, placement assistance, project portfolio"
            )

    return f"Course '{course_keyword}' not found. Available: Python Full Stack, Data Science, Web Dev, AI Agents, DevOps."


@tool
def simple_calculator(expression: str) -> str:
    """Evaluate a simple math expression. Use for fee calculations, discounts, etc.

    Args:
        expression: A math expression like '25000 * 0.18' or '30000 - 5000'
    """
    # Only allow safe characters for math
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: Only numbers and basic operators (+, -, *, /) are allowed."

    try:
        result = eval(expression)  # Safe because we validated characters above
        return f"{expression} = {result:,.2f}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


# ──────────────────────────────────────────────
# 3. SET UP THE LLM WITH TOOLS
# ──────────────────────────────────────────────

# Gather all tools into a list
tools = [search_courses, calculate_emi, check_batch_availability, get_course_details, simple_calculator]

# Create the LLM and bind the tools to it
# The LLM will know about these tools and can decide when to call them
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)


# ──────────────────────────────────────────────
# 4. DEFINE GRAPH NODES
# ──────────────────────────────────────────────
# Nodes are the "steps" in our agent's flowchart.

# System message that tells the agent who it is and how to behave
SYSTEM_MESSAGE = SystemMessage(content="""You are the TechPath Institute Course Advisor, a helpful AI assistant
for TechPath Institute in Bhopal, India. You help students find the right courses,
understand fees, check batch availability, and answer questions about the institute.

Guidelines:
- Always be friendly and encouraging to students
- Use Indian Rupee (Rs.) for all fees
- Recommend courses based on the student's interests and skill level
- If a student seems unsure, ask clarifying questions
- Mention EMI options when discussing fees
- Always check batch availability when recommending a course
- Use the tools available to you -- do not make up course details
""")


def chatbot_node(state: AgentState):
    """
    The 'brain' of our agent. This node:
    1. Takes the current messages (conversation so far)
    2. Sends them to the LLM
    3. The LLM either gives a final answer OR asks to call a tool
    """
    # Prepend the system message so the LLM knows its role
    messages = [SYSTEM_MESSAGE] + state["messages"]

    # The LLM responds -- it might include tool_calls in its response
    response = llm_with_tools.invoke(messages)

    # Return the response as a new message to add to state
    return {"messages": [response]}


# ToolNode automatically handles executing whatever tool the LLM requested
# It reads the tool_calls from the last message, runs the matching function,
# and returns the result as a ToolMessage
tool_node = ToolNode(tools)


# ──────────────────────────────────────────────
# 5. BUILD THE STATE GRAPH
# ──────────────────────────────────────────────
# This is where we wire everything together into a flowchart.

def build_agent_graph():
    """Build and compile the LangGraph agent."""

    # Create a new graph with our state type
    graph = StateGraph(AgentState)

    # --- Add nodes ---
    graph.add_node("chatbot", chatbot_node)     # The LLM thinking step
    graph.add_node("tools", tool_node)           # The tool execution step

    # --- Add edges ---

    # After executing a tool, ALWAYS go back to the chatbot
    # so it can see the tool result and decide what to do next
    graph.add_edge("tools", "chatbot")

    # After the chatbot responds, check: did it request a tool call?
    # tools_condition is a built-in function that returns:
    #   "tools" if the LLM's response contains tool_calls
    #   END     if the LLM gave a final text response
    graph.add_conditional_edges("chatbot", tools_condition)

    # The conversation starts at the chatbot node
    graph.set_entry_point("chatbot")

    # --- Compile with checkpointing ---
    # MemorySaver stores state in memory (use SqliteSaver for persistence)
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


# ──────────────────────────────────────────────
# 6. RUN THE AGENT
# ──────────────────────────────────────────────

def run_single_query(app, query: str, thread_id: str = "demo-001"):
    """Run a single query through the agent and print the conversation."""
    print(f"\n{'=' * 60}")
    print(f"Student: {query}")
    print(f"{'=' * 60}")

    # Config with thread_id allows the agent to remember previous messages
    # in the same thread (conversation)
    config = {"configurable": {"thread_id": thread_id}}

    # Invoke the agent -- it will loop through chatbot -> tools -> chatbot
    # until the LLM gives a final answer (no more tool calls)
    result = app.invoke(
        {"messages": [HumanMessage(content=query)]},
        config
    )

    # The last message in the result is the agent's final response
    final_message = result["messages"][-1]
    print(f"\nAdvisor: {final_message.content}")

    return result


def run_interactive(app):
    """Run the agent in interactive chat mode."""
    print("\n" + "=" * 60)
    print("  TechPath Institute -- AI Course Advisor")
    print("  Type your questions below. Type 'quit' to exit.")
    print("=" * 60)

    thread_id = "interactive-session"
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print("\nAdvisor: Thank you for visiting TechPath Institute! Good luck with your learning journey!")
            break

        # Run the agent
        result = app.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config
        )

        # Print the final response
        final_message = result["messages"][-1]
        print(f"\nAdvisor: {final_message.content}")


# ──────────────────────────────────────────────
# 7. MAIN -- DEMO + INTERACTIVE MODE
# ──────────────────────────────────────────────

def main():
    """Run demo queries and then start interactive mode."""

    # Build the agent graph
    app = build_agent_graph()

    print("\n" + "#" * 60)
    print("#  TechPath Institute -- LangGraph ReAct Agent Demo")
    print("#  This agent uses the ReAct pattern:")
    print("#    THINK -> ACT (use tool) -> OBSERVE -> repeat")
    print("#" * 60)

    # --- Demo 1: Simple course search ---
    run_single_query(
        app,
        "Hi! I am Rahul from Bhopal. I want to learn Python. What courses do you have?",
        thread_id="demo-rahul"
    )

    # --- Demo 2: Multi-step (search + EMI + batch) ---
    # Same thread_id so the agent remembers Demo 1 context
    run_single_query(
        app,
        "That sounds great! Can you tell me the EMI options for the Python Full Stack course? "
        "Also, when does the next batch start?",
        thread_id="demo-rahul"
    )

    # --- Demo 3: New student, different query ---
    run_single_query(
        app,
        "I am Priya and I already know HTML and CSS. I want to learn AI and build chatbots. "
        "What do you recommend?",
        thread_id="demo-priya"
    )

    # --- Interactive mode ---
    print("\n\n" + "-" * 60)
    print("Demo complete! Starting interactive mode...")
    print("-" * 60)

    run_interactive(app)


if __name__ == "__main__":
    main()

"""
Function Calling (Tool Use) — Module 09 Code Snap

Install: pip install openai
Set env: set OPENAI_API_KEY=sk-...
Run:     python code-function-calling.py

This file demonstrates how to make LLMs call external functions.
The LLM decides WHEN to call a function and WHAT arguments to pass.
You execute the function and return the result to the LLM.

Example scenario: A chatbot for TechPath Institute that can look up
student marks, course fees, and batch schedules from a "database".
"""

import os
import json
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o-mini"


# ============================================================
# PART 1: Define Your Functions (the "tools")
# ============================================================

# Simulated database (in a real app, these would query your Django/FastAPI API)
STUDENTS_DB = {
    "Rahul Sharma": {"marks": 85, "course": "Python Full Stack", "city": "Bhopal", "email": "rahul@email.com"},
    "Priya Patel": {"marks": 92, "course": "Data Science", "city": "Indore", "email": "priya@email.com"},
    "Ananya Singh": {"marks": 78, "course": "Web Development", "city": "Delhi", "email": "ananya@email.com"},
    "Vikram Joshi": {"marks": 45, "course": "Python Full Stack", "city": "Pune", "email": "vikram@email.com"},
    "Neha Gupta": {"marks": 88, "course": "Data Science", "city": "Bhopal", "email": "neha@email.com"},
}

COURSES_DB = {
    "Python Full Stack": {"fee": 45000, "duration": "8 months", "trainer": "Mr. Sanjeev Kumar", "seats": 30},
    "Data Science": {"fee": 35000, "duration": "6 months", "trainer": "Ms. Ritu Sharma", "seats": 25},
    "Web Development": {"fee": 25000, "duration": "4 months", "trainer": "Mr. Amit Verma", "seats": 30},
}


def get_student_info(student_name: str) -> dict:
    """Look up a student's details from the database"""
    # Case-insensitive search
    for name, info in STUDENTS_DB.items():
        if student_name.lower() in name.lower():
            return {"name": name, **info}
    return {"error": f"Student '{student_name}' not found in TechPath database"}


def get_course_info(course_name: str) -> dict:
    """Get details about a course at TechPath Institute"""
    for name, info in COURSES_DB.items():
        if course_name.lower() in name.lower():
            return {"name": name, **info, "fee_display": f"Rs.{info['fee']:,}"}
    return {"error": f"Course '{course_name}' not found"}


def get_all_students(course: str = None, city: str = None) -> dict:
    """List all students, optionally filtered by course or city"""
    results = []
    for name, info in STUDENTS_DB.items():
        if course and course.lower() not in info["course"].lower():
            continue
        if city and city.lower() not in info["city"].lower():
            continue
        results.append({"name": name, **info})

    return {
        "total": len(results),
        "students": results,
    }


def calculate_grade(marks: int) -> dict:
    """Calculate grade and status from marks"""
    if marks >= 80:
        grade, status = "A", "Distinction"
    elif marks >= 60:
        grade, status = "B", "First Class"
    elif marks >= 40:
        grade, status = "C", "Pass"
    else:
        grade, status = "F", "Fail"

    return {
        "marks": marks,
        "grade": grade,
        "status": status,
        "passed": marks >= 40,
    }


# ============================================================
# PART 2: Define Tool Schemas (tell the LLM about your functions)
# ============================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_student_info",
            "description": "Look up a student's marks, course, city, and email from the TechPath Institute database",
            "parameters": {
                "type": "object",
                "properties": {
                    "student_name": {
                        "type": "string",
                        "description": "Full or partial name of the student (e.g., 'Rahul Sharma' or 'Rahul')"
                    }
                },
                "required": ["student_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_course_info",
            "description": "Get fee, duration, trainer name, and available seats for a course at TechPath Institute",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_name": {
                        "type": "string",
                        "description": "Name of the course (e.g., 'Python Full Stack', 'Data Science')"
                    }
                },
                "required": ["course_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_students",
            "description": "List all students at TechPath Institute, optionally filtered by course or city",
            "parameters": {
                "type": "object",
                "properties": {
                    "course": {
                        "type": "string",
                        "description": "Filter by course name (optional)"
                    },
                    "city": {
                        "type": "string",
                        "description": "Filter by city name (optional)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_grade",
            "description": "Calculate the grade (A/B/C/F) and pass/fail status from marks",
            "parameters": {
                "type": "object",
                "properties": {
                    "marks": {
                        "type": "integer",
                        "description": "Marks scored (0-100)"
                    }
                },
                "required": ["marks"]
            }
        }
    }
]

# Map function names to actual functions
FUNCTION_MAP = {
    "get_student_info": get_student_info,
    "get_course_info": get_course_info,
    "get_all_students": get_all_students,
    "calculate_grade": calculate_grade,
}


# ============================================================
# PART 3: The Function Calling Loop
# ============================================================

def chat_with_tools(user_message: str, verbose: bool = True) -> str:
    """
    Send a message to the LLM with tool definitions.
    If the LLM wants to call a function, execute it and send the result back.
    Repeat until the LLM gives a final text response.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant for TechPath Institute, Bhopal. "
                "You can look up student information, course details, and calculate grades. "
                "Always be helpful and provide clear answers. "
                "When reporting fees, use the Indian Rupee format (e.g., Rs.45,000)."
            )
        },
        {"role": "user", "content": user_message}
    ]

    if verbose:
        print(f"\nUser: {user_message}")
        print("-" * 50)

    # Loop: the LLM might call multiple tools before giving a final answer
    max_iterations = 5
    for i in range(max_iterations):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",   # Let the model decide
        )

        message = response.choices[0].message

        # If no tool calls, we have the final answer
        if not message.tool_calls:
            if verbose:
                print(f"\nAssistant: {message.content}")
            return message.content

        # Process each tool call
        messages.append(message)  # Add assistant's tool call to history

        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            if verbose:
                print(f"  [Tool Call] {func_name}({func_args})")

            # Execute the function
            func = FUNCTION_MAP.get(func_name)
            if func:
                result = func(**func_args)
            else:
                result = {"error": f"Unknown function: {func_name}"}

            if verbose:
                print(f"  [Result]    {json.dumps(result, ensure_ascii=False)}")

            # Add the function result to the conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False),
            })

    return "Error: Too many tool calls"


# ============================================================
# PART 4: Example Queries
# ============================================================

def run_examples():
    """Run example queries that trigger different function calls"""

    print("=" * 60)
    print("  FUNCTION CALLING DEMO — TechPath Institute Chatbot")
    print("=" * 60)

    # Example 1: Simple lookup
    chat_with_tools("What are Rahul Sharma's marks?")

    print("\n" + "=" * 60)

    # Example 2: Course info
    chat_with_tools("How much does the Python Full Stack course cost? And who is the trainer?")

    print("\n" + "=" * 60)

    # Example 3: Multiple tool calls (student + grade)
    chat_with_tools("Look up Priya Patel's marks and tell me what grade she got.")

    print("\n" + "=" * 60)

    # Example 4: Filtering
    chat_with_tools("List all students from Bhopal")

    print("\n" + "=" * 60)

    # Example 5: Question that does NOT need a tool call
    chat_with_tools("What is Python programming language?")

    print("\n" + "=" * 60)

    # Example 6: Complex query (multiple tools)
    chat_with_tools(
        "Compare the Python Full Stack and Data Science courses. "
        "Which is cheaper and which has more students from Bhopal?"
    )


# ============================================================
# PART 5: Interactive Chat Mode
# ============================================================

def interactive_chat():
    """Run an interactive chat loop — ask anything about TechPath"""
    print("\n" + "=" * 60)
    print("  INTERACTIVE CHAT — Ask about students, courses, grades")
    print("  Type 'quit' to exit")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        if not user_input:
            continue

        chat_with_tools(user_input)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set!")
        print("Set it with: set OPENAI_API_KEY=sk-your-key-here")
        print()
        print("Here is what the functions return when called directly:")
        print()
        print("get_student_info('Rahul'):")
        print(json.dumps(get_student_info("Rahul"), indent=2))
        print()
        print("get_course_info('Python'):")
        print(json.dumps(get_course_info("Python"), indent=2))
        print()
        print("get_all_students(city='Bhopal'):")
        print(json.dumps(get_all_students(city="Bhopal"), indent=2))
        print()
        print("calculate_grade(85):")
        print(json.dumps(calculate_grade(85), indent=2))
    else:
        run_examples()

        # Uncomment to try interactive mode:
        # interactive_chat()

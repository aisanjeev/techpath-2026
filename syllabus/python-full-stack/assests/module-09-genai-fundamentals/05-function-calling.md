# Function Calling / Tool Use

**Module 09 — Generative AI Fundamentals & Prompt Engineering | Topic 5**

*TechPath Institute — Python Full Stack Development Program*

---

## What Is Function Calling?

Imagine you ask a very smart friend, "What is the weather in Bhopal right now?" Your friend is brilliant — he knows history, science, poetry — but he does not have a phone or internet. He cannot check the weather. He can only *guess*.

Now imagine you give your friend a phone and say, "Whenever you need weather data, call this number." Now he can give you a real answer.

**Function calling** (also called **tool use**) works the same way. An LLM like GPT or Claude is very smart, but it cannot access live data, run calculations, or interact with databases on its own. Function calling lets you give the LLM a list of tools it can "call" when it needs to do something beyond generating text.

| Without Function Calling | With Function Calling |
|---|---|
| LLM can only generate text | LLM can trigger real actions |
| Cannot access live data | Can fetch weather, stock prices, etc. |
| Cannot do math reliably | Can call a calculator function |
| Cannot query your database | Can look up student records |
| "I think the weather might be..." | "The temperature in Bhopal is 34C" |

---

## Why Does Function Calling Matter?

Before function calling, LLMs could only **talk**. Now they can **do things**.

Think of it like this: a customer care executive who can only talk on the phone vs. one who can also open your account, check your order, and process a refund. The second one is far more useful.

Real-world uses:
- **Rahul** builds a chatbot for his college. Students ask "What are my marks?" and the bot *actually checks the database* and replies.
- **Priya** creates a travel assistant that *books tickets* when you ask it to.
- **Amit** builds a helpdesk bot that can *raise support tickets* in the company system.

---

## How Does Function Calling Work?

The process has four steps:

```
Step 1: You DEFINE the tools (tell the LLM what functions exist)
Step 2: The LLM CHOOSES which tool to call (based on the user's question)
Step 3: YOU EXECUTE the function (run your Python code)
Step 4: You SEND the result back to the LLM (it generates a human-friendly reply)
```

**Important:** The LLM never runs your code. It only *decides* which function to call and what arguments to pass. You run the actual code on your server.

Think of the LLM as a manager who says, "Sneha, please check the attendance for Roll No. 42." Sneha (your code) does the actual work and reports back. The manager then tells the student the result in a nice way.

---

## Defining Functions / Tools

You describe your functions using a **JSON schema** format. This tells the LLM:
- What the function is called
- What it does (description)
- What inputs it needs (parameters)

Here is an example — a function to check student attendance:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "check_attendance",
            "description": "Check the attendance percentage of a student by their roll number",
            "parameters": {
                "type": "object",
                "properties": {
                    "roll_number": {
                        "type": "integer",
                        "description": "The student's roll number"
                    }
                },
                "required": ["roll_number"]
            }
        }
    }
]
```

| Field | Purpose | Example |
|---|---|---|
| `name` | Function name (no spaces) | `"check_attendance"` |
| `description` | What the function does (helps LLM decide when to use it) | `"Check attendance by roll number"` |
| `parameters` | What inputs are needed | `roll_number` (integer) |
| `required` | Which inputs are mandatory | `["roll_number"]` |

---

## Implementing with OpenAI API

Here is how function calling works with OpenAI's API:

```python
import openai
import json

client = openai.OpenAI(api_key="your-api-key")

# Step 1: Define your actual Python functions
def check_attendance(roll_number):
    """Simulate checking attendance from a database."""
    records = {
        101: {"name": "Rahul Sharma", "attendance": 87},
        102: {"name": "Priya Patel", "attendance": 92},
        103: {"name": "Amit Verma", "attendance": 65},
    }
    if roll_number in records:
        return records[roll_number]
    return {"error": "Student not found"}

# Step 2: Define tools for the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "check_attendance",
            "description": "Check attendance percentage of a student by roll number",
            "parameters": {
                "type": "object",
                "properties": {
                    "roll_number": {
                        "type": "integer",
                        "description": "The student's roll number"
                    }
                },
                "required": ["roll_number"]
            }
        }
    }
]

# Step 3: Send the user's message
messages = [{"role": "user", "content": "What is the attendance for roll number 102?"}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

# Step 4: Check if the LLM wants to call a function
message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # Step 5: Execute the function
    if function_name == "check_attendance":
        result = check_attendance(**arguments)

    # Step 6: Send the result back to the LLM
    messages.append(message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(result)
    })

    # Step 7: Get the final human-friendly response
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )
    print(final_response.choices[0].message.content)
```

**Output:**
```
Priya Patel (Roll No. 102) has an attendance of 92%.
```

---

## Implementing with Anthropic API

Anthropic's Claude uses a similar concept, but the format is slightly different:

```python
import anthropic
import json

client = anthropic.Anthropic(api_key="your-api-key")

# Define tools for Claude
tools = [
    {
        "name": "check_attendance",
        "description": "Check attendance percentage of a student by roll number",
        "input_schema": {
            "type": "object",
            "properties": {
                "roll_number": {
                    "type": "integer",
                    "description": "The student's roll number"
                }
            },
            "required": ["roll_number"]
        }
    }
]

# Send message with tools
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Check attendance for roll 101"}]
)

# Check if Claude wants to use a tool
for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        tool_use_id = block.id

        # Execute the function
        result = check_attendance(**tool_input)

        # Send the result back
        final_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=[
                {"role": "user", "content": "Check attendance for roll 101"},
                {"role": "assistant", "content": response.content},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(result)
                        }
                    ]
                }
            ]
        )
        print(final_response.content[0].text)
```

### Key Differences Between OpenAI and Anthropic

| Feature | OpenAI | Anthropic (Claude) |
|---|---|---|
| Tool definition key | `"parameters"` | `"input_schema"` |
| Result role | `"tool"` | `"user"` with `tool_result` type |
| Tool call ID | `tool_call.id` | `block.id` |
| Response location | `message.tool_calls` | `response.content` blocks |

---

## Real-World Examples

| Use Case | Function Name | What It Does |
|---|---|---|
| Weather app | `get_weather(city)` | Fetches live weather for a city |
| Student portal | `get_marks(roll_number)` | Looks up exam marks from database |
| Calculator | `calculate(expression)` | Evaluates math expressions accurately |
| Booking system | `book_appointment(date, time)` | Books a slot in the calendar |
| E-commerce | `check_order_status(order_id)` | Tracks a delivery |
| Banking chatbot | `get_balance(account_id)` | Checks account balance |

---

## Complete Example: Student Helpdesk Bot

Let us build a helpdesk bot for a college that can do three things:
1. Check attendance
2. Get exam marks
3. Book an appointment with a professor

```python
import json

# ---- Simulated database ----
student_db = {
    101: {"name": "Rahul Sharma", "attendance": 87,
          "marks": {"Python": 78, "DBMS": 85, "Web Dev": 92}},
    102: {"name": "Priya Patel", "attendance": 92,
          "marks": {"Python": 95, "DBMS": 88, "Web Dev": 90}},
    103: {"name": "Amit Verma", "attendance": 65,
          "marks": {"Python": 55, "DBMS": 60, "Web Dev": 70}},
}

appointments = []

# ---- Functions the bot can call ----
def check_attendance(roll_number: int) -> dict:
    student = student_db.get(roll_number)
    if student:
        return {"name": student["name"], "attendance": student["attendance"]}
    return {"error": f"No student found with roll number {roll_number}"}

def get_marks(roll_number: int, subject: str = None) -> dict:
    student = student_db.get(roll_number)
    if not student:
        return {"error": f"No student found with roll number {roll_number}"}
    if subject:
        mark = student["marks"].get(subject)
        if mark is not None:
            return {"name": student["name"], "subject": subject, "marks": mark}
        return {"error": f"Subject '{subject}' not found"}
    return {"name": student["name"], "marks": student["marks"]}

def book_appointment(roll_number: int, professor: str, date: str) -> dict:
    student = student_db.get(roll_number)
    if not student:
        return {"error": f"No student found with roll number {roll_number}"}
    appointment = {
        "student": student["name"],
        "professor": professor,
        "date": date,
        "status": "confirmed"
    }
    appointments.append(appointment)
    return appointment

# ---- Tool definitions for the LLM ----
tools = [
    {
        "type": "function",
        "function": {
            "name": "check_attendance",
            "description": "Check attendance percentage of a student",
            "parameters": {
                "type": "object",
                "properties": {
                    "roll_number": {
                        "type": "integer",
                        "description": "Student roll number"
                    }
                },
                "required": ["roll_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_marks",
            "description": "Get exam marks for a student, optionally for a specific subject",
            "parameters": {
                "type": "object",
                "properties": {
                    "roll_number": {
                        "type": "integer",
                        "description": "Student roll number"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject name (optional). Example: Python, DBMS, Web Dev"
                    }
                },
                "required": ["roll_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment with a professor for a student",
            "parameters": {
                "type": "object",
                "properties": {
                    "roll_number": {
                        "type": "integer",
                        "description": "Student roll number"
                    },
                    "professor": {
                        "type": "string",
                        "description": "Professor's name"
                    },
                    "date": {
                        "type": "string",
                        "description": "Appointment date in YYYY-MM-DD format"
                    }
                },
                "required": ["roll_number", "professor", "date"]
            }
        }
    }
]

# ---- Map function names to actual functions ----
available_functions = {
    "check_attendance": check_attendance,
    "get_marks": get_marks,
    "book_appointment": book_appointment,
}
```

**Sample conversations this bot can handle:**
- "What is the attendance of roll number 103?" -- Calls `check_attendance(103)`
- "Show me Priya's Python marks (roll 102)" -- Calls `get_marks(102, "Python")`
- "Book a meeting with Prof. Ananya on 2026-08-15 for roll 101" -- Calls `book_appointment(101, "Prof. Ananya", "2026-08-15")`

---

## Common Mistakes to Avoid

| Mistake | Why It Is Wrong | Correct Approach |
|---|---|---|
| Not validating function inputs | User could send bad data | Always validate before executing |
| Trusting LLM arguments blindly | LLM might hallucinate values | Check that roll numbers exist, dates are valid |
| Too many tools at once | LLM gets confused with 50+ tools | Keep it under 10-15 tools |
| Vague descriptions | LLM cannot decide when to use the tool | Write clear, specific descriptions |
| No error handling | Function crashes silently | Always return error messages in a dict |

---

## Key Takeaways

1. **Function calling lets LLMs DO things**, not just talk about things.
2. **The LLM never runs your code** — it only decides which function to call and with what arguments.
3. **You define tools** using a JSON schema that describes the function name, description, and parameters.
4. **The flow is**: Define tools, LLM picks one, you execute, send result back, LLM responds in natural language.
5. **Always validate** the arguments the LLM sends before executing your functions.

---

*Next Topic: Streaming Responses and Multi-Turn Conversations*

---
*TechPath Institute | Python Full Stack Development Program | Module 09*

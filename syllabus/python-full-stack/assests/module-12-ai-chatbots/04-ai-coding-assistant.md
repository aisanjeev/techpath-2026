# AI Coding Assistant

**Module 12 -- AI Chatbots | Topic 4**

---

## What is an AI Coding Assistant?

An AI coding assistant helps developers write, understand, debug, and improve code. It is like having a patient senior developer sitting next to you who can explain any code, find bugs, and suggest improvements.

### What It Can Do

| Feature | What It Does | Example |
|---------|-------------|---------|
| Code explanation | Explains what code does in simple language | "What does this for loop do?" |
| Debugging | Finds and fixes bugs | "Why am I getting IndexError?" |
| Code generation | Writes code from a description | "Write a function to sort students by marks" |
| Code review | Suggests improvements | "How can I make this code faster?" |
| Refactoring | Restructures code without changing behavior | "Convert this to use list comprehension" |

---

## Building a Code Explanation Feature

The most useful feature for students -- paste code and get a simple explanation.

```python
import anthropic

client = anthropic.Anthropic()

def explain_code(code: str, language: str = "python") -> str:
    """Explain code in simple English for a beginner student."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="""You are a patient coding tutor at TechPath Institute, Bhopal.
        Explain code in simple language that a fresher student can understand.
        - Break it down line by line
        - Use analogies from everyday life
        - Mention what the output would be
        - If there are common mistakes beginners make, mention them""",
        messages=[{
            "role": "user",
            "content": f"Explain this {language} code:\n\n```{language}\n{code}\n```"
        }],
    )
    return response.content[0].text

# Example usage
code = """
students = {"Rahul": 85, "Priya": 92, "Amit": 78}
topper = max(students, key=students.get)
print(f"Topper: {topper} with {students[topper]} marks")
"""
print(explain_code(code))
```

---

## Building a Debugging Helper

Students often get error messages they do not understand. The debugging helper explains the error and shows the fix.

```python
def debug_code(code: str, error_message: str) -> str:
    """Find and fix bugs in student code."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="""You are a debugging expert at TechPath Institute.
        When a student shows you their code and error:
        1. Explain WHAT went wrong (in simple language)
        2. Explain WHY it happened
        3. Show the FIXED code with comments
        4. Give a tip to avoid this mistake in the future""",
        messages=[{
            "role": "user",
            "content": f"My code:\n```python\n{code}\n```\n\nError:\n```\n{error_message}\n```\n\nHelp me fix it."
        }],
    )
    return response.content[0].text

# Example
buggy_code = """
marks = [85, 92, 78, 95, 88]
average = sum(marks) / len(mark)
print(f"Average: {average}")
"""
error = "NameError: name 'mark' is not defined"
print(debug_code(buggy_code, error))
```

---

## Building a Code Generator

Generate code from a plain English description:

```python
def generate_code(description: str, language: str = "python") -> str:
    """Generate code from a description."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=f"""You are a {language} expert at TechPath Institute.
        Generate clean, well-commented code.
        - Include docstrings for functions
        - Add example usage at the bottom
        - Use simple variable names
        - Follow PEP 8 style guidelines""",
        messages=[{
            "role": "user",
            "content": f"Write {language} code for: {description}"
        }],
    )
    return response.content[0].text

# Example
print(generate_code("a function that takes a list of student names and marks, and returns the top 3 students"))
```

---

## Building a Code Review Feature

```python
def review_code(code: str) -> str:
    """Review code and suggest improvements."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="""You are a senior Python developer reviewing code.
        Provide feedback on:
        1. Bugs or errors (if any)
        2. Code style and readability
        3. Performance improvements
        4. Security concerns (if applicable)
        5. One specific suggestion to make it better
        
        Be encouraging -- this is a student's code.""",
        messages=[{
            "role": "user",
            "content": f"Review this code:\n\n```python\n{code}\n```"
        }],
    )
    return response.content[0].text
```

---

## Combining Into a Coding Assistant API

```python
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class ActionType(str, Enum):
    explain = "explain"
    debug = "debug"
    generate = "generate"
    review = "review"

class CodingRequest(BaseModel):
    action: ActionType
    code: str = ""
    error: str = ""
    description: str = ""
    language: str = "python"

@app.post("/coding-assistant")
async def coding_assistant(request: CodingRequest):
    if request.action == "explain":
        result = explain_code(request.code, request.language)
    elif request.action == "debug":
        result = debug_code(request.code, request.error)
    elif request.action == "generate":
        result = generate_code(request.description, request.language)
    elif request.action == "review":
        result = review_code(request.code)
    
    return {"result": result, "action": request.action}
```

---

## System Prompt Design

The system prompt is the most important part. It defines the assistant's personality and behavior.

### Good System Prompt Principles

| Principle | Why | Example |
|-----------|-----|---------|
| Set the role | AI knows its job | "You are a Python tutor" |
| Define the audience | Adjusts complexity | "for fresher students" |
| Give structure | Consistent output format | "1. What, 2. Why, 3. Fix" |
| Set boundaries | Prevents off-topic answers | "Only answer coding questions" |
| Be encouraging | Student-friendly | "This is a common mistake, here's how to fix it" |

```python
SYSTEM_PROMPT = """You are a friendly Python coding tutor at TechPath Institute, Bhopal.

RULES:
- Explain everything in simple language a fresher student can understand
- Use Indian examples (Rahul, Priya, Rs, Bhopal)
- Always show the correct code with comments
- Be encouraging -- mistakes are part of learning
- If the question is not about coding, say "I can only help with coding questions"

FORMAT your responses:
1. Brief answer (2-3 sentences)
2. Code example (with comments)
3. Key takeaway (one line)
"""
```

---

## Structured Output for Code

Use structured output to get consistent results:

```python
from pydantic import BaseModel

class CodeAnalysis(BaseModel):
    has_bugs: bool
    bug_description: str
    fixed_code: str
    explanation: str
    difficulty_level: str    # "beginner", "intermediate", "advanced"

# Parse the LLM's response into this structure
```

---

## Summary

| Feature | System Prompt Focus | Input | Output |
|---------|-------------------|-------|--------|
| Explain | "Break down line by line" | Code snippet | Plain English explanation |
| Debug | "What, why, fix, tip" | Code + error message | Bug analysis + fixed code |
| Generate | "Clean, commented code" | Description | Working code |
| Review | "Bugs, style, performance" | Code snippet | Improvement suggestions |

| Best Practice | Why |
|--------------|-----|
| Detailed system prompt | Consistent, student-friendly responses |
| Structured output | Easy to parse and display in UI |
| Language parameter | Support Python, JavaScript, SQL, etc. |
| Be encouraging | Students learn better with positive feedback |

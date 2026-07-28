# AI SDK Introduction — Anthropic & OpenAI

**Module 03 — Python Libraries: Data, Automation & APIs | Topic 7**

---

## Why Learn AI SDKs?

AI is transforming how software is built. As a Python developer, you can use AI APIs to add powerful features to your applications:
- Generate text, summaries, and translations
- Build chatbots and virtual assistants
- Analyze documents and extract information
- Generate code and solve problems

**You don't need to build AI models** — you just call an API. Think of it like using Google Maps API instead of building your own satellite system.

---

## How AI APIs Work

```
Your Python Code → API Request → AI Provider (Anthropic/OpenAI) → Response
                   (text prompt)                                  (AI output)
```

1. You send a **prompt** (text instruction) to the API
2. The AI model processes it
3. You get back a **response** (generated text)

This is called a **completion** or **message**.

---

## Anthropic SDK (Claude)

Claude is made by Anthropic. It excels at long-context understanding, analysis, and coding.

```bash
pip install anthropic
```

### Your First API Call

```python
import anthropic

client = anthropic.Anthropic(
    api_key="your-api-key-here"    # Or set ANTHROPIC_API_KEY env var
)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain Python list comprehensions in 3 sentences for a beginner."}
    ],
)

print(message.content[0].text)
```

### System Prompts — Setting the AI's Role

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a Python tutor at TechPath Institute, Bhopal. "
           "Explain concepts simply with Indian examples. "
           "Use ₹ for prices and Indian names in examples.",
    messages=[
        {"role": "user", "content": "What are decorators in Python?"}
    ],
)

print(message.content[0].text)
```

### Multi-Turn Conversation

```python
messages = [
    {"role": "user", "content": "What is a Python dictionary?"},
]

# First turn
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages,
)

# Add AI response to history
messages.append({"role": "assistant", "content": response.content[0].text})

# Second turn
messages.append({"role": "user", "content": "Show me an example with student data"})

response2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages,
)

print(response2.content[0].text)
```

### Streaming — Real-Time Output

```python
# Stream the response word by word (like ChatGPT typing effect)
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a short poem about learning Python"}
    ],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()    # Newline at the end
```

---

## OpenAI SDK (GPT)

GPT is made by OpenAI. It is widely used for text generation and chat applications.

```bash
pip install openai
```

### Basic Usage

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key-here")    # Or set OPENAI_API_KEY env var

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful Python tutor."},
        {"role": "user", "content": "What is the difference between a list and a tuple?"},
    ],
    max_tokens=500,
    temperature=0.7,    # 0 = deterministic, 1 = creative
)

answer = response.choices[0].message.content
print(answer)
```

### Streaming with OpenAI

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain async/await in Python"}
    ],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## API Parameters Explained

| Parameter | What It Does | Typical Value |
|-----------|-------------|---------------|
| `model` | Which AI model to use | `claude-sonnet-4-20250514`, `gpt-4o-mini` |
| `messages` | Conversation history | List of role/content dicts |
| `max_tokens` | Maximum response length | 500 - 4096 |
| `temperature` | Creativity (0=focused, 1=creative) | 0.3 - 0.7 |
| `system` | AI's role/personality | "You are a Python tutor" |

### Message Roles

| Role | Purpose | Example |
|------|---------|---------|
| `system` | Set AI behavior (Anthropic: separate param) | "You are a helpful tutor" |
| `user` | Your question/instruction | "Explain decorators" |
| `assistant` | AI's previous response | Used for conversation history |

---

## Practical: Code Reviewer

```python
import anthropic

client = anthropic.Anthropic()

def review_code(code: str) -> str:
    """Send code to Claude for review."""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=(
            "You are an expert Python code reviewer. "
            "Review the code for bugs, style issues, and improvements. "
            "Be constructive and specific."
        ),
        messages=[
            {"role": "user", "content": f"Review this Python code:\n\n```python\n{code}\n```"}
        ],
    )
    return message.content[0].text

# Usage
code = '''
def calculate_avg(marks):
    total = 0
    for m in marks:
        total = total + m
    avg = total / len(marks)
    return avg

students = [85, 92, 78, 0, 88]
print(calculate_avg(students))
'''

review = review_code(code)
print(review)
```

---

## Practical: AI Study Assistant

```python
import anthropic

client = anthropic.Anthropic()

def explain_topic(topic: str, level: str = "beginner") -> str:
    """Get an explanation of a Python topic."""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=(
            f"You are a Python tutor at TechPath Institute, Bhopal. "
            f"Explain concepts at a {level} level. "
            f"Use Indian names and ₹ prices in examples. "
            f"Include a code example and a practice exercise."
        ),
        messages=[
            {"role": "user", "content": f"Explain: {topic}"}
        ],
    )
    return message.content[0].text

# Usage
explanation = explain_topic("decorators", level="beginner")
print(explanation)
```

---

## Error Handling for AI APIs

```python
import anthropic

client = anthropic.Anthropic()

def safe_ai_call(prompt: str) -> str:
    """Make an AI API call with proper error handling."""
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
    except anthropic.AuthenticationError:
        return "Error: Invalid API key. Check your ANTHROPIC_API_KEY."
    except anthropic.RateLimitError:
        return "Error: Too many requests. Please wait and try again."
    except anthropic.APIConnectionError:
        return "Error: Could not connect to the API. Check your internet."
    except anthropic.APIError as e:
        return f"API Error: {e}"

result = safe_ai_call("What is Python?")
print(result)
```

---

## Cost-Saving Tips

| Tip | Why |
|-----|-----|
| Use smaller models for simple tasks | `claude-haiku` / `gpt-4o-mini` are cheaper |
| Set `max_tokens` appropriately | Don't request 4096 tokens for a yes/no answer |
| Cache responses | Don't call the API for the same question twice |
| Use system prompts to keep answers concise | "Answer in 2-3 sentences" |
| Batch multiple questions | Combine related questions into one call |

### Model Comparison

| Model | Best For | Relative Cost |
|-------|----------|---------------|
| Claude Haiku | Simple tasks, fast responses | Low |
| Claude Sonnet | Most tasks, good balance | Medium |
| Claude Opus | Complex analysis, long context | High |
| GPT-4o Mini | Simple tasks | Low |
| GPT-4o | Complex tasks | High |

---

## Environment Setup (Best Practice)

```python
# .env file
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here

# Python code
import os
from dotenv import load_dotenv

load_dotenv()

# The SDKs automatically read from environment variables
# No need to pass api_key if env vars are set!
import anthropic
client = anthropic.Anthropic()    # Reads ANTHROPIC_API_KEY automatically
```

---

## Summary

| Concept | Anthropic (Claude) | OpenAI (GPT) |
|---------|-------------------|--------------|
| Install | `pip install anthropic` | `pip install openai` |
| Client | `anthropic.Anthropic()` | `OpenAI()` |
| Create message | `client.messages.create()` | `client.chat.completions.create()` |
| Access response | `message.content[0].text` | `response.choices[0].message.content` |
| Streaming | `client.messages.stream()` | `stream=True` |
| System prompt | `system=` parameter | `{"role": "system", ...}` |
| Env var | `ANTHROPIC_API_KEY` | `OPENAI_API_KEY` |

---

## Practice Tasks

1. Set up the Anthropic SDK and make your first API call
2. Create a multi-turn chatbot that remembers conversation history
3. Build a code reviewer that sends Python code to Claude for feedback
4. Create a study assistant that explains Python topics at different levels
5. Add streaming to your chatbot so responses appear word by word

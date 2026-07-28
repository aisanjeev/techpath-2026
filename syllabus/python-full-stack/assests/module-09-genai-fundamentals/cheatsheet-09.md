# Cheat Sheet: Generative AI & Prompt Engineering

**Module 09 — Quick Reference**
**TechPath Institute | Python Full Stack Course**

---

## 1. LLM Providers Comparison

| Provider | Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) | Context Window |
|----------|-------|----------------------------|------------------------------|----------------|
| OpenAI | GPT-4o | $2.50 | $10.00 | 128K tokens |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 | 128K tokens |
| Anthropic | Claude Sonnet 4 | $3.00 | $15.00 | 200K tokens |
| Anthropic | Claude Haiku 3.5 | $0.80 | $4.00 | 200K tokens |
| Google | Gemini 1.5 Pro | $1.25 | $5.00 | 2M tokens |
| Google | Gemini 1.5 Flash | $0.075 | $0.30 | 1M tokens |
| Mistral | Mistral Large | $2.00 | $6.00 | 128K tokens |
| Meta | Llama 3.1 405B | Free (self-host) | Free (self-host) | 128K tokens |

> **Tip:** For learning and prototyping, use GPT-4o-mini or Gemini Flash — they are cheapest.

---

## 2. Token Estimation Rules of Thumb

| Rule | Example |
|------|---------|
| 1 token ~ 4 characters (English) | "hello" = ~1.25 tokens |
| 1 token ~ 0.75 words | 100 words ~ 133 tokens |
| 1 page of text ~ 400-500 tokens | A4 page, normal font |
| 1K tokens ~ 750 words | About 3-4 paragraphs |
| Indian names use more tokens | "Rahul" = 1 token, "Chandrasekhar" = 3 tokens |
| Code uses more tokens than prose | `for i in range(10):` = ~7 tokens |

**Quick formula:** `tokens ~ character_count / 4`

```python
# Accurate counting with tiktoken
import tiktoken
encoder = tiktoken.encoding_for_model("gpt-4o")
token_count = len(encoder.encode("Your text here"))
```

---

## 3. Prompt Engineering Techniques

| Technique | When to Use | Example Pattern |
|-----------|-------------|-----------------|
| **Zero-Shot** | Simple tasks the model already knows | `"Translate this to Hindi: {text}"` |
| **Few-Shot** | When you want a specific format or style | `"Example 1: X → Y\nExample 2: A → B\nNow do: C → ?"` |
| **Chain-of-Thought** | Math, logic, multi-step reasoning | `"Think step by step. Step 1: ..."` |
| **Role-Based** | Specialized behaviour (tutor, reviewer) | `"You are a senior Python developer..."` |
| **Structured Output** | When you need JSON/CSV/table back | `"Return a JSON object with fields: name, age, city"` |
| **Self-Consistency** | High-stakes decisions | Ask 3 times with temp=0.7, pick majority answer |
| **ReAct** | Tasks needing external data/tools | `"Think → Act → Observe → Think → Answer"` |
| **Delimiter-Based** | Separating instructions from data | `"Summarize the text between triple backticks: \`\`\`{text}\`\`\`"` |

---

## 4. System Prompt Template

```python
system_prompt = """You are [ROLE] at [ORGANIZATION].

Your task is to [PRIMARY TASK].

Rules:
- [Rule 1: output format]
- [Rule 2: tone/style]
- [Rule 3: constraints]
- [Rule 4: what NOT to do]

Context:
- [Relevant background information]
- [User level: beginner/intermediate/advanced]
"""
```

**Example:**
```python
system_prompt = """You are a Python tutor at TechPath Institute, Bhopal.

Your task is to help students learn Python programming.

Rules:
- Explain in simple English suitable for beginners
- Use Indian names and examples (Rahul, Priya, Rs. for currency)
- Keep answers under 200 words unless asked for more
- If you do not know something, say so honestly

Context:
- Students are absolute beginners with no coding background
- Course: Python Full Stack Developer
"""
```

---

## 5. Model Parameters

| Parameter | Range | Effect | Best For |
|-----------|-------|--------|----------|
| `temperature` | 0.0 - 2.0 | Higher = more random/creative | 0 for code, 0.7 for chat, 1.2 for creative |
| `top_p` | 0.0 - 1.0 | Nucleus sampling (limits word pool) | Usually keep at 1.0, lower for focused output |
| `max_tokens` | 1 - model max | Maximum response length | Set based on expected output size |
| `stop` | list of strings | Stops generation at these sequences | `["\n\n", "END"]` to prevent over-generation |
| `frequency_penalty` | -2.0 - 2.0 | Penalises repeated words | 0.5 to reduce repetition |
| `presence_penalty` | -2.0 - 2.0 | Encourages talking about new topics | 0.5 for variety |

> **Rule:** Adjust either `temperature` or `top_p`, not both at the same time.

---

## 6. OpenAI API Quick Start

```bash
pip install openai
```

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")  # or set OPENAI_API_KEY env variable

# Basic call
response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=500,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain Python lists in 3 lines"}
    ]
)

answer = response.choices[0].message.content
print(answer)

# Check token usage
print(f"Input tokens:  {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
```

---

## 7. Anthropic API Quick Start

```bash
pip install anthropic
```

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")  # or set ANTHROPIC_API_KEY env variable

# Basic call
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful assistant.",    # system prompt is a separate parameter
    messages=[
        {"role": "user", "content": "Explain Python lists in 3 lines"}
    ]
)

answer = message.content[0].text
print(answer)

# Check token usage
print(f"Input tokens:  {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
```

> **Key difference from OpenAI:** In Claude, `system` is a top-level parameter, not a message.

---

## 8. Function Calling Schema Template

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "function_name",
            "description": "What this function does (be specific!)",
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "What this parameter is"
                    },
                    "param2": {
                        "type": "integer",
                        "description": "What this parameter is"
                    }
                },
                "required": ["param1"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# Check if model wants to call a function
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)
    # Execute and send result back
```

---

## 9. Streaming Pattern

### OpenAI Streaming

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Tell me about Python"}],
    stream=True,
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
```

### Anthropic Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me about Python"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

## 10. Multi-Turn Conversation Structure

```python
# Maintain a list of messages — send ALL of them each time
conversation = [
    {"role": "system", "content": "You are a Python tutor."},
]

def chat(user_message):
    # Add user message
    conversation.append({"role": "user", "content": user_message})

    # Send full history
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
    )

    # Add assistant reply to history
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    return reply

# Usage — model remembers previous turns
chat("What is a dictionary?")
chat("Give an example with student data")
chat("How do I loop through it?")
```

> **Remember:** LLMs have no memory. You must send the full conversation every time. Trim older messages if you hit the context window limit.

---

## 11. Safety Checklist

| Check | Why | How |
|-------|-----|-----|
| Never hardcode API keys | Keys in code get leaked via Git | Use `.env` file + `python-dotenv` |
| Set `max_tokens` | Prevents runaway costs | Always set a reasonable limit |
| Validate LLM output | Model can return invalid JSON or nonsense | Use try/except, validate with Pydantic |
| Rate limiting | Avoid hitting API limits and getting blocked | Use `time.sleep()` or `tenacity` for retries |
| Content filtering | Model might generate harmful content | Check output before showing to users |
| Cost monitoring | Bills can grow fast with GPT-4 | Log token usage, set budget alerts in dashboard |
| PII handling | Do not send passwords, Aadhaar numbers to LLMs | Strip sensitive data before sending |
| Prompt injection | Users can trick your system prompt | Validate user input, use delimiters |

---

## 12. Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthenticationError` | Invalid or expired API key | Check key in `.env`, regenerate if needed |
| `RateLimitError` | Too many requests per minute | Add retry with exponential backoff |
| `InvalidRequestError: max context length` | Prompt + response exceeds context window | Trim conversation history or use a model with a larger context |
| `JSONDecodeError` on LLM output | Model returned text instead of JSON | Add `"Return valid JSON only"` to prompt, use `response_format={"type": "json_object"}` |
| `timeout` | Model taking too long | Set `timeout=30` in client constructor |
| `content_filter` | Input/output flagged as unsafe | Rephrase prompt, avoid sensitive topics |
| Empty response | `max_tokens` too low | Increase `max_tokens` |
| `ModuleNotFoundError: openai` | SDK not installed | `pip install openai` |
| Inconsistent outputs | Temperature too high | Lower `temperature` to 0 for deterministic results |
| High API bill | Using GPT-4o for simple tasks | Switch to GPT-4o-mini or cache responses |

---

*TechPath Institute — Bhopal | Python Full Stack Course*

# System Prompts and Model Parameters

**Module 09 — Generative AI Fundamentals & Prompt Engineering | Topic 4**

---

## System Prompt vs User Prompt

When you use the LLM API, you send messages with different **roles**. The two most important are the **system prompt** and the **user prompt**.

**Analogy:** Think of it like hiring someone for a job at TechPath Institute.

- **System prompt = the job description.** It tells the model who it is, how it should behave, and what rules to follow. It is set once and stays the same throughout the conversation.
- **User prompt = the daily task.** It is the specific question or instruction given in each message.

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # SYSTEM PROMPT — sets the behavior for the entire conversation
        {
            "role": "system",
            "content": "You are a helpful Python tutor at TechPath Institute. "
                       "Explain concepts simply for absolute beginners. "
                       "Use Indian names and examples. "
                       "Always include code examples."
        },
        # USER PROMPT — the actual question
        {
            "role": "user",
            "content": "What is a dictionary in Python?"
        }
    ]
)
```

Without the system prompt, the model gives a generic answer. With it, the model responds as a beginner-friendly tutor using Indian examples — every single time, for every question in the conversation.

---

## Crafting Effective System Prompts

A good system prompt has four parts:

| Part | What It Does | Example |
|------|-------------|---------|
| **Role** | Who the model is | "You are a senior Python developer" |
| **Behavior** | How it should respond | "Explain concepts step by step" |
| **Constraints** | What it should NOT do | "Do not use jargon without defining it" |
| **Format** | How to structure output | "Always include a code example" |

### Example: Customer Support Bot

```python
system_prompt = """You are a customer support assistant for TechPath Institute,
an IT training institute in Bhopal, India.

BEHAVIOR:
- Be polite, professional, and helpful
- Answer questions about courses, fees, schedules, and placements
- If you do not know something, say "Let me connect you with our team"

CONSTRAINTS:
- Never discuss competitor institutes
- Never make up information about fees or placement statistics
- Do not answer questions unrelated to TechPath

FORMAT:
- Keep responses under 150 words
- Use bullet points for lists
- End with a call to action (e.g., "Would you like to schedule a demo class?")

CONTEXT:
- Courses offered: Python Full Stack, Data Science, Cloud Computing
- Course duration: 4-6 months
- Fee range: Rs 30,000 to Rs 60,000
- Location: Bhopal, with online options available"""
```

### Example: Code Review Assistant

```python
system_prompt = """You are a code reviewer for a Python FastAPI project.

Review code for:
1. Bug risks and logic errors
2. Security issues (SQL injection, exposed secrets)
3. Performance problems
4. PEP 8 style violations
5. Missing error handling

Format your review as:
- CRITICAL: Must fix before merging
- WARNING: Should fix but not blocking
- SUGGESTION: Nice to have improvements

Be direct and specific. Reference line numbers when possible."""
```

### Example: JSON Data Extractor

```python
system_prompt = """You are a data extraction assistant. Given any text input,
extract structured information and return it as valid JSON.

Rules:
- Return ONLY valid JSON, no other text
- Use snake_case for all keys
- Use null for missing values, never make up data
- Dates should be in YYYY-MM-DD format
- Prices should be numbers (not strings), in INR"""
```

### System Prompt Tips

1. **Be explicit** — do not assume the model will figure out what you mean
2. **Include examples** — show one ideal response inside the system prompt
3. **Set boundaries** — clearly state what the model should NOT do
4. **Keep it focused** — a system prompt for a chatbot should not include instructions for code review
5. **Test it** — try edge cases (rude users, off-topic questions, tricky inputs)

---

## Model Parameters

When you call an LLM API, you can pass several parameters that control how the model generates text. Think of these as "knobs" you can turn to change the output.

---

### Temperature (Most Important Parameter)

**Temperature** controls how random or focused the model's output is.

- **Temperature = 0** — The model always picks the most likely next word. Output is consistent and predictable. Like asking Rahul a math question — there is one right answer.
- **Temperature = 1** — The model considers less likely words too. Output is more creative and varied. Like asking Rahul to write a poem — there are many possible answers.
- **Temperature = 2** — The model becomes very random. Output can be incoherent. Rarely useful.

```python
# Focused, consistent output (for code, facts, data extraction)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    messages=[{"role": "user", "content": "What is 2 + 2?"}]
)
# Always returns: "4"

# Creative, varied output (for stories, brainstorming)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=1.0,
    messages=[{"role": "user", "content": "Write a tagline for a chai brand"}]
)
# Run 1: "Every sip tells a story"
# Run 2: "Warmth in every cup, love in every leaf"
# Run 3: "Brewed with tradition, served with soul"
```

### Same Prompt, Different Temperatures

Prompt: **"Suggest a name for a Python project that tracks daily expenses"**

| Temperature | Output |
|------------|--------|
| 0.0 | ExpenseTracker |
| 0.3 | PyExpenseTracker |
| 0.7 | PaisaWatch |
| 1.0 | RupeeRadar — Your Daily Money Compass |
| 1.5 | KharchaMitra: The Spending Whisperer of Digital Realms |

**Rule of thumb:**

| Use Case | Recommended Temperature |
|----------|------------------------|
| Code generation | 0.0 - 0.2 |
| Data extraction / JSON | 0.0 |
| Factual Q&A | 0.0 - 0.3 |
| General conversation | 0.5 - 0.7 |
| Creative writing | 0.7 - 1.0 |
| Brainstorming | 0.8 - 1.2 |

---

### Top-p (Nucleus Sampling)

**Top-p** is another way to control randomness, working alongside temperature. It limits the model to only consider tokens whose combined probability adds up to `p`.

**Simplified explanation:**

At each step, the model ranks all possible next words by probability:

```
"Python"     → 40%
"JavaScript" → 25%
"Java"       → 15%
"C++"        → 10%
"Go"         → 5%
"Rust"       → 3%
"COBOL"      → 2%
```

- **top_p = 0.65** — Model only considers "Python" and "JavaScript" (40% + 25% = 65%). It ignores the rest.
- **top_p = 0.80** — Model considers "Python," "JavaScript," and "Java" (40% + 25% + 15% = 80%).
- **top_p = 1.0** — Model considers all options (default).

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    top_p=0.5,      # Only consider the most probable tokens
    messages=[{"role": "user", "content": "Name a programming language"}]
)
```

> **Tip from Ananya:** Most developers only adjust temperature and leave top_p at 1.0. Adjusting both at the same time can give unpredictable results. Pick one.

---

### Max Tokens (Output Length)

**max_tokens** sets the maximum number of tokens the model can generate in its response. It does NOT guarantee the response will be that long — it just sets the upper limit.

```python
# Short response
response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=50,    # Maximum ~37 words
    messages=[{"role": "user", "content": "Explain machine learning"}]
)
# Output: "Machine learning is a subset of AI where computers learn
#          patterns from data instead of being explicitly programmed..."
#          (cuts off at 50 tokens)

# Detailed response
response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=2000,  # Maximum ~1,500 words
    messages=[{"role": "user", "content": "Explain machine learning"}]
)
```

**Why set max_tokens?**
1. **Cost control** — you pay per output token, so capping it prevents unexpectedly expensive responses
2. **Response time** — shorter responses generate faster
3. **Application needs** — a chatbot widget might only have space for 200 words

| Use Case | Recommended max_tokens |
|----------|----------------------|
| Chatbot quick reply | 150-300 |
| Code generation | 500-2000 |
| Essay or article | 2000-4000 |
| Data extraction (JSON) | 500-1000 |

---

### Frequency Penalty and Presence Penalty

These two parameters reduce repetition in the model's output.

**Frequency penalty** (0 to 2) — Penalizes words based on how many times they have already appeared. Higher values make the model avoid repeating the same words.

**Presence penalty** (0 to 2) — Penalizes words that have appeared at all, regardless of count. Higher values encourage the model to talk about new topics.

```python
# Without penalties — model might repeat itself
response = client.chat.completions.create(
    model="gpt-4o-mini",
    frequency_penalty=0,
    presence_penalty=0,
    messages=[{"role": "user", "content": "Write 5 benefits of Python"}]
)
# "Python is easy to learn. Python is versatile. Python is popular.
#  Python has many libraries. Python is great for beginners."
#  (repeats "Python is" every sentence)

# With penalties — more varied language
response = client.chat.completions.create(
    model="gpt-4o-mini",
    frequency_penalty=0.5,
    presence_penalty=0.5,
    messages=[{"role": "user", "content": "Write 5 benefits of Python"}]
)
# "Python is easy to learn. The language is remarkably versatile.
#  Its popularity ensures strong community support. Thousands of
#  libraries cover nearly every use case. Beginners find the
#  syntax intuitive and welcoming."
```

| Parameter | Default | Effect When Increased |
|-----------|---------|----------------------|
| frequency_penalty | 0 | Less word repetition |
| presence_penalty | 0 | More topic diversity |

> **When to use:** Turn these up for creative writing, marketing copy, or any output where repetition sounds bad. Keep them at 0 for code generation (where repeating keywords like `def`, `return`, `if` is necessary and normal).

---

### Stop Sequences

**Stop sequences** tell the model to stop generating when it produces a specific string. The model stops immediately — the stop sequence itself is not included in the output.

```python
# Stop when the model tries to generate a second question
response = client.chat.completions.create(
    model="gpt-4o-mini",
    stop=["\nQuestion:", "\n\n"],   # Stop at these strings
    messages=[{"role": "user", "content": "Generate one quiz question about Python"}]
)
```

**Use cases:**
- Preventing the model from generating more content than needed
- Stopping at a specific delimiter in structured output
- Ending generation at a natural boundary (e.g., end of a function)

---

## Parameters Cheat Sheet

Here is the complete reference table you will need when building LLM applications:

| Parameter | Type | Range | Default | What It Controls |
|-----------|------|-------|---------|-----------------|
| temperature | float | 0.0 - 2.0 | 1.0 | Randomness of output (0 = focused, 1 = creative) |
| top_p | float | 0.0 - 1.0 | 1.0 | Limits token pool by cumulative probability |
| max_tokens | int | 1 - model limit | Varies | Maximum length of generated response |
| frequency_penalty | float | 0.0 - 2.0 | 0.0 | Reduces word repetition |
| presence_penalty | float | 0.0 - 2.0 | 0.0 | Encourages topic diversity |
| stop | list[str] | Any strings | None | Strings that halt generation |

### Recommended Presets

| Task | temperature | top_p | max_tokens | freq_penalty | pres_penalty |
|------|------------|-------|-----------|-------------|-------------|
| Code generation | 0.0 | 1.0 | 2000 | 0.0 | 0.0 |
| JSON extraction | 0.0 | 1.0 | 1000 | 0.0 | 0.0 |
| Chatbot | 0.7 | 1.0 | 500 | 0.3 | 0.3 |
| Creative writing | 0.9 | 0.95 | 2000 | 0.5 | 0.5 |
| Summarization | 0.3 | 1.0 | 500 | 0.0 | 0.0 |
| Brainstorming | 1.0 | 1.0 | 1000 | 0.8 | 0.8 |

---

## Putting It All Together

Here is a complete example that combines a system prompt with tuned parameters:

```python
from openai import OpenAI

client = OpenAI()

def ask_tutor(question: str) -> str:
    """Ask the TechPath Python tutor a question."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,          # Mostly focused, slightly varied
        max_tokens=500,           # Keep answers concise
        frequency_penalty=0.2,    # Slight reduction in repetition
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly Python tutor at TechPath Institute, Bhopal. "
                    "Explain concepts for absolute beginners. "
                    "Use simple English and Indian examples. "
                    "Always include a short code example. "
                    "Keep answers under 200 words."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response.choices[0].message.content

# Usage
answer = ask_tutor("What is a for loop?")
print(answer)
```

This function gives you consistent, beginner-friendly answers every time — because the system prompt defines the behavior and the parameters control the style.

---

## Key Takeaways

| Concept | One-Line Summary |
|---------|-----------------|
| System prompt | Defines who the model is and how it behaves (set once per conversation) |
| User prompt | The specific question or instruction (changes every message) |
| Temperature | Controls randomness: 0 for facts, 0.7 for conversation, 1.0 for creativity |
| Top-p | Limits which tokens the model can choose from (usually leave at 1.0) |
| Max tokens | Caps the response length (controls cost and speed) |
| Frequency penalty | Reduces word repetition (use for creative writing) |
| Presence penalty | Encourages new topics (use for brainstorming) |
| Stop sequences | Halts generation at a specific string |

---

*TechPath Institute -- Python Full Stack with Gen AI*

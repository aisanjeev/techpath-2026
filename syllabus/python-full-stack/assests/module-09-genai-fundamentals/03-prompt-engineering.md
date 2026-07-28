# Prompt Engineering Techniques

**Module 09 — Generative AI Fundamentals & Prompt Engineering | Topic 3**

---

## What is a Prompt?

A **prompt** is the text you send to an LLM to get a response. It is your instruction, your question, your request — everything the model reads before generating an answer.

**Analogy:** Think of the LLM as a very talented but literal-minded intern at TechPath Institute. If you tell them "do something with the data," they will give you a random result. If you tell them "create a bar chart showing monthly revenue in rupees for the last 6 months, using blue bars, with axis labels," they will give you exactly what you want.

The quality of the output depends almost entirely on the quality of the prompt. This is why **prompt engineering** — the skill of writing effective prompts — is so important.

---

## Technique 1: Zero-Shot Prompting

**Zero-shot** means you give no examples — you just ask directly. This works well for simple, clear tasks.

### Bad Prompt vs Good Prompt

**Bad prompt:**
```
Tell me about Python
```
**Output:** A very long, unfocused essay about Python's history, features, ecosystem, etc.

**Good prompt:**
```
Explain what Python is in 3 sentences, aimed at a college student
who has never programmed before.
```
**Output:** Python is a programming language that reads almost like English, making it one of the easiest languages to learn. It is used by companies like Google and Instagram to build websites, analyze data, and create AI applications. You can start writing Python code today with just a laptop and a free code editor.

---

**Bad prompt:**
```
Write code for sorting
```
**Output:** Could be any language, any algorithm, any data type.

**Good prompt:**
```
Write a Python function that takes a list of student names (strings)
and returns them sorted alphabetically. Include a docstring and
an example usage.
```
**Output:**
```python
def sort_students(names: list[str]) -> list[str]:
    """Sort a list of student names alphabetically.

    Args:
        names: List of student name strings.

    Returns:
        A new list with names sorted A-Z.
    """
    return sorted(names)

# Example
students = ["Sneha", "Amit", "Priya", "Rahul"]
print(sort_students(students))
# Output: ['Amit', 'Priya', 'Rahul', 'Sneha']
```

**Key rule:** Be specific about the format, audience, language, and length you want.

---

## Technique 2: Few-Shot Prompting

**Few-shot** means you provide a few examples before asking your actual question. The model learns the pattern from your examples and follows it.

**Analogy:** Instead of explaining to Ananya how to format a student report, you show her three already-formatted reports and say "do the next one like these."

### Bad Prompt (Zero-Shot, Unclear Format)

```
Convert these to formal English:
"gonna grab some chai"
```
**Output:** "I am going to get some tea." (works, but you have no control over the format)

### Good Prompt (Few-Shot, Pattern Established)

```
Convert informal text to formal English.

Informal: "gonna grab some chai brb"
Formal: "I will step away briefly to get some tea."

Informal: "this code is super buggy lol"
Formal: "This code contains several significant bugs."

Informal: "ngl the presentation was mid"
Formal: "To be honest, the presentation was mediocre."

Informal: "can't make it tmrw, got stuff to do"
Formal:
```
**Output:** "I will not be able to attend tomorrow as I have other commitments."

The model perfectly follows the pattern you established. Few-shot is excellent when you need a specific output format.

---

### Another Example: Data Extraction

```
Extract the product name and price from the text.

Text: "The new Samsung Galaxy S24 is available for Rs 79,999"
Product: Samsung Galaxy S24
Price: Rs 79,999

Text: "Buy the MacBook Air M3 starting at Rs 1,14,900"
Product: MacBook Air M3
Price: Rs 1,14,900

Text: "OnePlus 12 launched in India at Rs 64,999 for the base variant"
Product:
Price:
```
**Output:**
```
Product: OnePlus 12
Price: Rs 64,999
```

**When to use few-shot:** When you need the model to follow a specific format, pattern, or style that is hard to describe in words.

---

## Technique 3: Chain-of-Thought (CoT)

**Chain-of-thought** prompting asks the model to think step by step before giving the final answer. This dramatically improves accuracy on reasoning, math, and logic problems.

**Analogy:** In an exam, Priya gets better marks when she writes the full solution step by step instead of jumping straight to the answer. The LLM works the same way.

### Bad Prompt (Direct Answer)

```
A shopkeeper in Bhopal buys 50 notebooks at Rs 40 each and sells
them at Rs 55 each. He gives a 10% discount to students who buy
5 or more. If 30 notebooks are sold at full price and 20 are sold
to students in bulk, what is his total profit?
```
**Output:** The model might give a wrong answer because it tries to do all the math at once.

### Good Prompt (Chain-of-Thought)

```
A shopkeeper in Bhopal buys 50 notebooks at Rs 40 each and sells
them at Rs 55 each. He gives a 10% discount to students who buy
5 or more. If 30 notebooks are sold at full price and 20 are sold
to students in bulk, what is his total profit?

Think step by step before giving the final answer.
```
**Output:**
```
Step 1: Calculate total cost
50 notebooks x Rs 40 = Rs 2,000

Step 2: Revenue from full-price sales
30 notebooks x Rs 55 = Rs 1,650

Step 3: Revenue from discounted sales
Discounted price = Rs 55 - 10% = Rs 55 - Rs 5.50 = Rs 49.50
20 notebooks x Rs 49.50 = Rs 990

Step 4: Total revenue
Rs 1,650 + Rs 990 = Rs 2,640

Step 5: Total profit
Rs 2,640 - Rs 2,000 = Rs 640

The shopkeeper's total profit is Rs 640.
```

**The magic phrase:** Just add "Think step by step" or "Let's work through this step by step" to your prompt.

---

### Another CoT Example: Debugging

```
This Python code has a bug. Find it and explain step by step
what goes wrong.

def average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

print(average([]))
```
**Output:**
```
Step 1: The function is called with an empty list [].
Step 2: The for loop does not execute (nothing to iterate over).
Step 3: total remains 0.
Step 4: len(numbers) is 0.
Step 5: The function tries to compute 0 / 0.
Step 6: This raises a ZeroDivisionError.

Fix: Add a check at the start:
    if not numbers:
        return 0
```

---

## Technique 4: Structured Output

Ask the model to return data in a specific structure — JSON, a table, a list, or any format your code can parse.

### Bad Prompt

```
Tell me about 3 Python web frameworks
```
**Output:** A long paragraph mixing all the information together — hard to use in code.

### Good Prompt (JSON Output)

```
List 3 Python web frameworks. Return the result as a JSON array
where each item has: name, type (full-stack or micro), and
best_for. Return ONLY the JSON, no other text.
```
**Output:**
```json
[
  {
    "name": "Django",
    "type": "full-stack",
    "best_for": "Large applications with admin panels"
  },
  {
    "name": "FastAPI",
    "type": "micro",
    "best_for": "High-performance REST APIs"
  },
  {
    "name": "Flask",
    "type": "micro",
    "best_for": "Simple web apps and prototypes"
  }
]
```

### Good Prompt (Table Output)

```
Compare 3 Indian cities for IT jobs. Return as a markdown table
with columns: City, Average Fresher Salary, Top Companies, Cost of Living.
```
**Output:**

| City | Average Fresher Salary | Top Companies | Cost of Living |
|------|----------------------|---------------|---------------|
| Bangalore | Rs 6-10 LPA | Google, Flipkart, Infosys | High |
| Pune | Rs 4-8 LPA | TCS, Persistent, Veritas | Medium |
| Hyderabad | Rs 5-9 LPA | Microsoft, Amazon, TCS | Medium |

**When to use:** Whenever you need to process the model's output in your code. JSON output is especially useful in API backends.

---

## Technique 5: Role-Based Prompting

Give the model a role or persona. This shapes the tone, vocabulary, and depth of the response.

### Bad Prompt

```
Explain what an API is
```
**Output:** A technically accurate but generic explanation.

### Good Prompt (Role Assigned)

```
You are a friendly programming teacher at TechPath Institute in
Bhopal, explaining concepts to absolute beginners who have never
coded before. Use simple Hindi-English (Hinglish) analogies
where helpful.

Explain what an API is.
```
**Output:** An API (Application Programming Interface) is like a waiter in a restaurant. Imagine you are sitting at a table in a Bhopal restaurant. You (the app) want food (data) from the kitchen (the server). You cannot go into the kitchen yourself — you give your order to the waiter (the API), who takes it to the kitchen, gets your food, and brings it back. You never see the kitchen, and the kitchen never sees you. The waiter handles everything in between. In coding, when your app needs data from another service — say weather data or payment processing — it sends a request to that service's API, and the API sends back the response.

### Another Role Example

```
You are a senior Python developer conducting a code review.
Review this code and provide feedback in bullet points:

def calc(x,y,z):
    a=x*y
    b=a-z
    if b>0:
        return b
    else:
        return 0
```
**Output:**
- **Naming:** `calc`, `a`, `b`, `x`, `y`, `z` are not descriptive. Use names like `calculate_profit`, `revenue`, `cost`, `quantity`, `price`, `discount`.
- **Type hints:** Add type annotations: `def calc(x: float, y: float, z: float) -> float:`
- **Docstring:** Missing — add a docstring explaining what this function calculates.
- **Magic return:** Returning 0 when b <= 0 silently hides negative values. Consider raising an error or returning the actual negative value.
- **Formatting:** Add spaces around operators: `a = x * y` not `a=x*y`.

---

## Common Prompt Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Too vague | "Write some code" | Specify language, task, format |
| Too much context | Pasting 10 pages of text and asking "what do you think?" | Ask a specific question about specific parts |
| No format specified | "Give me information about databases" | "Give me a comparison table of SQL vs NoSQL with 5 rows" |
| Assuming knowledge | "Fix the bug" (without showing the code) | Always include the relevant code and error message |
| Multiple questions at once | "Explain Python, write a program, and compare it with Java" | One clear task per prompt |

---

## Prompt Engineering Best Practices

1. **Be specific** — state exactly what you want, in what format, and how long
2. **Provide context** — tell the model who the audience is and what the goal is
3. **Use examples** — show the pattern you want (few-shot)
4. **Ask for step-by-step** — add "think step by step" for reasoning tasks
5. **Specify the format** — ask for JSON, table, bullet points, or numbered list
6. **Iterate** — if the first response is not right, refine your prompt and try again
7. **Set constraints** — "in under 100 words," "using only the standard library," "for Python 3.12"

---

## Key Takeaways

| Technique | When to Use | Key Phrase |
|-----------|------------|------------|
| Zero-shot | Simple, clear tasks | Just ask clearly and specifically |
| Few-shot | Need a specific format or pattern | Show 2-3 examples first |
| Chain-of-thought | Math, logic, debugging | "Think step by step" |
| Structured output | Need machine-readable data | "Return as JSON" or "as a table" |
| Role-based | Need a specific tone or perspective | "You are a..." |

---

*TechPath Institute -- Python Full Stack with Gen AI*

# LCEL -- LangChain Expression Language

**Module 10 -- LangChain | Topic 2**

---

## What is LCEL?

LCEL (LangChain Expression Language) is the modern way to build chains in LangChain. It uses the **pipe operator** (`|`) to connect components together, just like how Unix commands pipe data from one program to another.

**Analogy:** Think of LCEL like a water pipeline. Water (your data) flows through pipes, passing through different filters and processors before reaching the tap (final output). Each `|` is a connection between two pipes.

```
Old way:  chain = LLMChain(llm=llm, prompt=prompt)     # Hard to extend
New way:  chain = prompt | llm | parser                  # Easy to read, extend
```

---

## The Pipe Operator

The pipe operator (`|`) connects components. The output of the left side becomes the input of the right side.

### Basic Example

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Define components
prompt = ChatPromptTemplate.from_template(
    "You are a TechPath Institute trainer. Explain {topic} in 3 bullet points."
)
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Connect with pipes
chain = prompt | llm | parser

# Run
result = chain.invoke({"topic": "REST APIs"})
print(result)
```

### Step-by-Step Flow

```
Input: {"topic": "REST APIs"}
  |
  v
[Prompt Template] -- fills in the variable
  Output: "You are a TechPath Institute trainer. Explain REST APIs in 3 bullet points."
  |
  v
[LLM (ChatOpenAI)] -- sends to OpenAI, gets response
  Output: AIMessage(content="1. REST APIs are...")
  |
  v
[StrOutputParser] -- extracts the text
  Output: "1. REST APIs are..."
```

---

## Runnable Interface

Every component in LCEL follows the **Runnable** interface. This means they all have the same methods:

| Method | What It Does | Example |
|--------|-------------|---------|
| `invoke(input)` | Process one input, get one output | `chain.invoke({"topic": "Python"})` |
| `batch(inputs)` | Process multiple inputs at once | `chain.batch([{"topic": "Python"}, {"topic": "SQL"}])` |
| `stream(input)` | Get output piece by piece (word by word) | `for chunk in chain.stream(...)` |
| `ainvoke(input)` | Async version of invoke | `await chain.ainvoke(...)` |

### Batch Processing

Process multiple inputs in one call -- useful for generating content in bulk.

```python
chain = prompt | llm | parser

# Process 3 topics at once
results = chain.batch([
    {"topic": "Python lists"},
    {"topic": "Python dictionaries"},
    {"topic": "Python functions"},
])

for i, result in enumerate(results):
    print(f"\n--- Topic {i+1} ---")
    print(result)
```

### Streaming

Show output word by word, like ChatGPT does:

```python
chain = prompt | llm | parser

for chunk in chain.stream({"topic": "LangChain"}):
    print(chunk, end="", flush=True)
```

---

## Runnable Sequences

Under the hood, the `|` operator creates a `RunnableSequence`. You can also build one explicitly:

```python
from langchain_core.runnables import RunnableSequence

# These two are identical:
chain_pipe = prompt | llm | parser
chain_explicit = RunnableSequence(prompt, llm, parser)

# Both work the same way
result = chain_explicit.invoke({"topic": "Django"})
```

### Adding Steps to a Chain

You can keep piping more steps:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Generate explanation
explain_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple English."
)

# Step 2: Translate to Hindi
translate_prompt = ChatPromptTemplate.from_template(
    "Translate this text to Hindi:\n\n{text}"
)

# Chain: explain, then translate
explain_chain = explain_prompt | llm | parser
# Note: To pipe into another prompt, you need RunnableLambda or RunnablePassthrough
```

---

## Parallel Chains with RunnableParallel

Sometimes you want to run multiple chains at the same time. `RunnableParallel` does this.

### Example: Beginner and Advanced Explanations

```python
from langchain_core.runnables import RunnableParallel

# Two different prompts for the same topic
beginner_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} for a complete beginner student at TechPath Institute."
)
advanced_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} for someone with Python programming experience."
)

# Run both in parallel
parallel_chain = RunnableParallel(
    beginner=beginner_prompt | llm | parser,
    advanced=advanced_prompt | llm | parser,
)

results = parallel_chain.invoke({"topic": "Python decorators"})
print("Beginner version:", results["beginner"])
print("\nAdvanced version:", results["advanced"])
```

### How Parallel Chains Work

```
Input: {"topic": "decorators"}
        |
        +---- beginner_prompt | llm | parser ----> results["beginner"]
        |
        +---- advanced_prompt | llm | parser ----> results["advanced"]
        |
Output: {"beginner": "...", "advanced": "..."}
```

Both chains run at the same time, so the total time is the time of the **slowest** chain, not the sum of both.

### Practical Use Case: Course Page Generator

```python
parallel_chain = RunnableParallel(
    description=ChatPromptTemplate.from_template(
        "Write a short description for a {course} course at TechPath Institute Bhopal."
    ) | llm | parser,
    syllabus=ChatPromptTemplate.from_template(
        "List 8 topics for a {course} course syllabus."
    ) | llm | parser,
    prerequisites=ChatPromptTemplate.from_template(
        "What should a student know before joining a {course} course?"
    ) | llm | parser,
)

page = parallel_chain.invoke({"course": "Python Full Stack"})
print(page["description"])
print(page["syllabus"])
print(page["prerequisites"])
```

---

## RunnablePassthrough and RunnableLambda

### RunnablePassthrough -- Pass Data Through

`RunnablePassthrough` passes the input through unchanged. Useful when you need the original input alongside processed data.

```python
from langchain_core.runnables import RunnablePassthrough

# Pass the question through while also retrieving documents
chain = RunnableParallel(
    context=retriever | format_docs,       # Process: retrieve and format
    question=RunnablePassthrough(),         # Pass through: keep the original question
)
```

### RunnableLambda -- Custom Functions

`RunnableLambda` wraps any Python function so it can be used in a chain.

```python
from langchain_core.runnables import RunnableLambda

def add_greeting(text):
    return f"Namaste! Here is your answer:\n\n{text}"

# Use it in a chain
chain = prompt | llm | parser | RunnableLambda(add_greeting)
result = chain.invoke({"topic": "Python lists"})
print(result)
# "Namaste! Here is your answer:\n\n1. Python lists are..."
```

### Practical Example: Processing Chain

```python
def count_words(text):
    word_count = len(text.split())
    return {"text": text, "word_count": word_count}

def add_footer(data):
    return f"{data['text']}\n\n---\n(Generated by TechPath AI | {data['word_count']} words)"

chain = (
    prompt
    | llm
    | parser
    | RunnableLambda(count_words)
    | RunnableLambda(add_footer)
)
```

---

## Conditional Routing with RunnableBranch

`RunnableBranch` lets you route inputs to different chains based on conditions.

```python
from langchain_core.runnables import RunnableBranch

# Different prompts for different subjects
python_prompt = ChatPromptTemplate.from_template("Explain this Python concept: {topic}")
web_prompt = ChatPromptTemplate.from_template("Explain this web development concept: {topic}")
general_prompt = ChatPromptTemplate.from_template("Explain: {topic}")

# Route based on topic content
branch = RunnableBranch(
    (lambda x: "python" in x["topic"].lower(), python_prompt | llm | parser),
    (lambda x: "html" in x["topic"].lower() or "css" in x["topic"].lower(), web_prompt | llm | parser),
    general_prompt | llm | parser,  # Default
)

result = branch.invoke({"topic": "Python list comprehension"})
# Uses python_prompt because "python" is in the topic
```

---

## Error Handling with Fallbacks

If a chain fails (API error, timeout), you can set up a fallback chain:

```python
# Primary: use GPT-4o (expensive but powerful)
primary = ChatOpenAI(model="gpt-4o")

# Fallback: use GPT-4o-mini (cheaper, less powerful)
fallback = ChatOpenAI(model="gpt-4o-mini")

# If primary fails, automatically try fallback
llm_with_fallback = primary.with_fallbacks([fallback])

chain = prompt | llm_with_fallback | parser
result = chain.invoke({"topic": "Python"})
```

---

## Combining Everything -- Real Example

Here is a complete example that uses prompts, parallel chains, lambdas, and streaming:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Generate a course summary with key details
course_chain = RunnableParallel(
    overview=ChatPromptTemplate.from_template(
        "Write a 2-line overview of a {course} course for TechPath Institute."
    ) | llm | parser,
    career=ChatPromptTemplate.from_template(
        "List 3 job roles a {course} student can apply for after completing the course."
    ) | llm | parser,
)

def format_output(data):
    return f"COURSE OVERVIEW\n{data['overview']}\n\nCAREER PATHS\n{data['career']}"

full_chain = course_chain | RunnableLambda(format_output)

result = full_chain.invoke({"course": "Python Full Stack"})
print(result)
```

---

## Summary

| Concept | What It Does |
|---------|-------------|
| Pipe operator `\|` | Connects components: output of left goes to right |
| `invoke()` | Process one input |
| `batch()` | Process multiple inputs at once |
| `stream()` | Get output word by word |
| `RunnableSequence` | Chain of steps executed in order |
| `RunnableParallel` | Run multiple chains simultaneously |
| `RunnablePassthrough` | Pass input through unchanged |
| `RunnableLambda` | Wrap any Python function for use in chains |
| `RunnableBranch` | Route to different chains based on conditions |
| `with_fallbacks()` | Try backup chain if primary fails |

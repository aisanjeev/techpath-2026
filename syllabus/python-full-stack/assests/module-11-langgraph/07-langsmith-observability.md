# LangSmith -- Observability and Debugging

**Module 11 -- LangGraph | Topic 7**

---

## What is LangSmith?

LangSmith is a platform by LangChain for **monitoring, debugging, and testing** your AI agents and chains. Think of it like Chrome DevTools but for AI workflows -- you can see every step the agent took, what it sent, what it received, and how long it took.

**Analogy:** Imagine you are a doctor trying to diagnose why a patient is sick. You need blood tests, X-rays, and scans. LangSmith is like those diagnostic tools but for AI applications -- it shows you exactly what is happening inside your agent.

---

## Setting Up LangSmith

### Step 1: Get an API Key

Sign up at [smith.langchain.com](https://smith.langchain.com) and create an API key.

### Step 2: Configure Environment Variables

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"
os.environ["LANGCHAIN_PROJECT"] = "techpath-course-agent"
```

Or in your `.env` file:

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-key-here
LANGCHAIN_PROJECT=techpath-course-agent
```

### Step 3: Install

```bash
pip install langsmith
```

Once configured, every LLM call, tool call, and graph step is **automatically logged** to LangSmith. You do not need to change your code.

---

## What You Can See in Traces

Every time your agent runs, LangSmith creates a **trace** -- a detailed record of everything that happened.

### Trace Information

| Feature | What It Shows | Why It Matters |
|---------|--------------|---------------|
| **Call tree** | Every step the agent took, in order | See the full execution flow |
| **Inputs/Outputs** | What went into and came out of each step | Verify data is correct |
| **Token usage** | How many tokens each step used | Track costs |
| **Latency** | How long each step took (in milliseconds) | Find slow bottlenecks |
| **Errors** | Where and why things broke | Debug failures |
| **Tool calls** | Which tools were called with what arguments | Verify correct tool selection |

### Example Trace

```
[Trace: "What Python courses are available?"]
  |
  +-- Agent Node (1.2s, 150 tokens)
  |     Input: [user: "What Python courses are available?"]
  |     Output: tool_call: search_courses("Python")
  |
  +-- Tool Node (0.05s)
  |     Tool: search_courses
  |     Args: {"query": "Python"}
  |     Result: "Python Full Stack: Rs 45,000, 6 months"
  |
  +-- Agent Node (0.8s, 120 tokens)
        Input: [tool_result: "Python Full Stack..."]
        Output: "We offer the Python Full Stack course for Rs 45,000..."

Total: 2.05s, 270 tokens, Rs 0.05 cost
```

---

## Debugging Common Issues

### Problem 1: Agent Stuck in a Loop

**Symptom:** The agent keeps calling the same tool over and over, never giving a final answer.

**How to find it in LangSmith:**
- Open the trace
- Look at the call tree -- you will see the same tool called 5, 10, or more times
- Check the tool's return value -- is it giving useful information?

**Common causes and fixes:**

| Cause | Fix |
|-------|-----|
| Tool returns unclear results | Improve the tool's return format |
| LLM keeps retrying with same query | Add "if you already have the answer, respond directly" to system prompt |
| No max iteration limit | Add `recursion_limit` to your graph config |

### Problem 2: Wrong Tool Selected

**Symptom:** The agent calls the calculator tool when it should call the search tool.

**How to find it in LangSmith:**
- Look at the tool_call in the trace
- Check the LLM's reasoning (if visible)
- Compare the tool descriptions

**Fix:** Make tool names and descriptions more specific:

```python
# BAD -- too vague
@tool
def get_info(query: str) -> str:
    """Get information."""

# GOOD -- clear and specific
@tool
def search_techpath_courses(query: str) -> str:
    """Search for courses available at TechPath Institute by topic.
    Use this when a student asks about available courses, subjects, or programs."""
```

### Problem 3: Slow Responses

**Symptom:** The agent takes 10+ seconds to respond.

**How to find it in LangSmith:**
- Check latency for each step in the trace
- Identify the slowest step

**Common fixes:**

| Bottleneck | Fix |
|-----------|-----|
| LLM call takes too long | Use a faster model (GPT-4o-mini instead of GPT-4o) |
| Too many tool calls | Combine related tools or improve prompts |
| Tool function is slow | Optimize the tool (cache results, faster queries) |
| Large prompt/context | Reduce context size, trim messages |

### Problem 4: Hallucination (Making Things Up)

**How to find it in LangSmith:**
- Compare the retrieved context with the final answer
- If the answer contains information NOT in the context, it is hallucinating

**Fix:** Strengthen your prompt:
```python
"Answer ONLY based on the provided context. If the information is not available, say 'I don't have that information.'"
```

---

## Evaluations

LangSmith lets you run automated tests on your agent to measure quality.

### Creating a Test Dataset

```python
from langsmith import Client

client = Client()

# Create a dataset of test cases
dataset = client.create_dataset("techpath-agent-tests")
client.create_examples(
    inputs=[
        {"question": "What Python courses are available in Bhopal?"},
        {"question": "Calculate EMI for Rs 45,000 over 6 months"},
        {"question": "Are there weekend batches for Django?"},
        {"question": "What is the placement percentage?"},
    ],
    outputs=[
        {"expected": "Should mention Python Full Stack course"},
        {"expected": "Should calculate Rs 7,500/month"},
        {"expected": "Should check batch availability"},
        {"expected": "Should provide placement statistics or say unknown"},
    ],
    dataset_id=dataset.id
)
```

### Running Evaluations

```python
from langsmith.evaluation import evaluate

def run_agent(inputs):
    """Run the agent and return its answer."""
    result = app.invoke({"messages": [("user", inputs["question"])]})
    return {"answer": result["messages"][-1].content}

def check_relevance(outputs, reference_outputs):
    """Check if the answer is relevant to the expected output."""
    answer = outputs["answer"].lower()
    expected = reference_outputs["expected"].lower()
    # Simple keyword check
    keywords = expected.split()
    matches = sum(1 for kw in keywords if kw in answer)
    return {"score": matches / len(keywords)}

evaluate(
    run_agent,
    data="techpath-agent-tests",
    evaluators=[check_relevance],
)
```

---

## Monitoring in Production

### Key Metrics to Watch

| Metric | What to Monitor | Alert If |
|--------|----------------|----------|
| **Latency** | Average response time | > 5 seconds |
| **Token usage** | Tokens per conversation | > 5000 per conversation |
| **Error rate** | Percentage of failed requests | > 5% |
| **Cost** | Daily/monthly API spend | Exceeds budget |
| **Tool success rate** | How often tools return useful results | < 80% success |

### Cost Tracking

```python
# LangSmith shows token usage per trace
# You can calculate costs:
# GPT-4o-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
# 1000 conversations x 500 tokens avg = 500K tokens
# Cost: ~$0.38/day for 1000 conversations
```

---

## LangSmith vs Print Debugging

| Feature | print() Debugging | LangSmith |
|---------|-------------------|-----------|
| Setup effort | None | 3 lines of config |
| Multi-step visibility | Hard to follow | Clear call tree |
| Token tracking | Manual | Automatic |
| Cost tracking | Not available | Built-in |
| Production use | Not practical | Designed for it |
| Team access | Not possible | Dashboard for everyone |
| Historical data | Lost when terminal closes | Stored permanently |

---

## Best Practices

| Practice | Why |
|----------|-----|
| Always enable tracing in development | Catch issues early |
| Name your projects | Separate traces by feature (e.g., "course-agent", "support-bot") |
| Create test datasets early | Automated testing catches regressions |
| Monitor production costs | Prevent surprise bills |
| Review failed traces regularly | Understand and fix common failure patterns |
| Tag important traces | Makes them easier to find later |

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| LangSmith | Monitoring, debugging, and testing platform for LLM applications |
| Trace | Detailed record of every step in an agent's execution |
| Evaluations | Automated tests to measure agent quality |
| Token tracking | See how many tokens (and money) each conversation costs |
| Latency monitoring | Find and fix slow steps in your agent |
| Test datasets | Collection of questions + expected answers for testing |
| Key setup | Set `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY` |

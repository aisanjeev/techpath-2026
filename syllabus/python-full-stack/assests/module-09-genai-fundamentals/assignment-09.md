# Module 09 — Assignment: Build AI-Powered Applications

**Deadline:** End of module week
**Submission:** Python files + screenshots of outputs + cost analysis

---

## Build: AI Tools for TechPath Institute

Use the OpenAI or Anthropic API to build practical AI tools for TechPath Institute.

### Task 1: Prompt Engineering Lab — 25 marks

Create a Python file `prompt_lab.py` that demonstrates ALL of these prompting techniques:

| Technique | What to Build |
|-----------|--------------|
| Zero-shot | Classify student feedback as positive/negative/neutral |
| Few-shot | Extract student details (name, city, marks) from paragraph text |
| Chain-of-thought | Calculate whether a student passes with multi-subject marks (show reasoning) |
| Structured output | Extract course information from text and return as JSON |

**Requirements:**
- Each technique must be a separate function
- Use at least 3 test inputs per technique
- Print the input, output, and technique name for each test
- Use `temperature=0` for classification/extraction, `0.7` for creative tasks

### Task 2: TechPath AI Chatbot with Function Calling — 30 marks

Create `techpath_chatbot.py` — an AI chatbot that can answer questions about TechPath Institute by calling functions:

**Functions to implement:**

| Function | What It Does |
|----------|-------------|
| `get_student_marks(name)` | Look up a student's marks from a dictionary |
| `get_course_fee(course)` | Return the fee for a course in Rs. |
| `list_students(city=None, course=None)` | List students, optionally filtered |
| `calculate_grade(marks)` | Return grade (A/B/C/F) and pass/fail status |

**Requirements:**
- Define proper tool schemas with descriptions
- Handle the function calling loop (send → tool call → execute → send result → final answer)
- Handle cases where the student/course is not found
- Include at least 8 sample students with Indian names and cities
- Test with at least 5 different queries (simple lookup, filtered list, grade calculation, comparison, non-tool question)

### Task 3: Streaming AI Response with FastAPI — 25 marks

Create `ai_stream.py` — a FastAPI endpoint that streams AI responses:

```
GET /api/chat/stream?prompt=What+is+Python
```

**Requirements:**
- Use Server-Sent Events (SSE) to stream the response
- Stream word by word (not the entire response at once)
- Include a simple HTML page (`chat.html`) that consumes the stream and shows words appearing one by one
- Handle errors (invalid prompt, API down)
- Add a system prompt: "You are a Python tutor at TechPath Institute, Bhopal."

### Task 4: Cost Analysis & Safety — 20 marks

Create `cost_analysis.py` that:

1. **Token counting:** Count tokens for 5 different prompts of varying length using `tiktoken`
2. **Cost estimation:** Calculate the cost (in USD and INR) for:
   - 100 chatbot queries per day using GPT-4o-mini
   - 100 chatbot queries per day using GPT-4o
   - 100 chatbot queries per day using Claude Sonnet
   - Show monthly cost comparison in a table
3. **Safety checks:** Write a function that:
   - Detects if user input contains prompt injection attempts ("ignore previous instructions", "you are now...", etc.)
   - Validates LLM output is valid JSON (for structured output tasks)
   - Logs all prompts and responses to a file for auditing

---

## Project Structure

```
genai-project/
├── prompt_lab.py         (Task 1: Prompting techniques)
├── techpath_chatbot.py   (Task 2: Function calling chatbot)
├── ai_stream.py          (Task 3: Streaming FastAPI endpoint)
├── chat.html             (Task 3: Frontend for streaming)
├── cost_analysis.py      (Task 4: Token counting & costs)
├── requirements.txt      (openai, tiktoken, fastapi, uvicorn)
└── .env                  (API keys — DO NOT submit this file)
```

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Prompting | All 4 techniques with 3+ examples each | 3 techniques work | Only 1-2 techniques |
| Function Calling | Full loop, 4 functions, edge cases | Basic loop works | Functions defined but not called |
| Streaming | SSE works, HTML shows live typing | Streaming works, no HTML | No streaming |
| Cost Analysis | Token counting, 3-model comparison, safety | Basic counting | No analysis |
| Code Quality | Clean, commented, error handling | Mostly clean | Messy, no error handling |
| Indian Context | Indian names, cities, Rs. currency throughout | Mostly Indian context | Generic examples |

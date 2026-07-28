# Module 12 -- Assignment: AI Chatbot Development

**Deadline:** End of Week 12
**Submission:** Upload your project folder (Python files + screenshots) as a ZIP to the student portal. Include a `README.md` with setup instructions and a short video demo (2-3 minutes, screen recording).

**Total Marks:** 100

---

## Task 1: TechPath FAQ Chatbot -- 30 marks

Build a RAG-based FAQ chatbot for TechPath Institute that can answer student queries about courses, fees, batch timings, placement, and admission.

**Requirements:**

1. Create a FastAPI backend with a `/chat` endpoint
2. Store at least 15 FAQ entries in ChromaDB as the knowledge base
3. Use Claude or OpenAI API to generate answers from retrieved context
4. Add a system prompt that makes the bot polite, accurate, and TechPath-branded
5. The bot must say "I don't have that information" when asked something outside the FAQ
6. Add a `/health` endpoint that returns the number of FAQ entries loaded

**Sample FAQs to include:**
- Course fees (Python Full Stack: ₹49,999, ADCA: ₹35,999)
- Batch timings (morning, afternoon, evening, weekend)
- Location (MP Nagar Zone-II, Bhopal)
- Placement statistics
- Admission process

**Test these queries:**
- "What is the fee for Python Full Stack?" (should answer correctly)
- "Do you offer night classes?" (should answer from FAQ or say "don't have info")
- "What is the weather today?" (should politely redirect -- off topic)

**Deliverables:**
- Python file with FastAPI app
- Screenshots of Swagger UI showing successful responses
- Screenshots showing the bot refusing off-topic questions

---

## Task 2: Streaming Chat Interface -- 25 marks

Add streaming support to your chatbot from Task 1 and build a simple frontend.

**Requirements:**

1. Add a `/chat/stream` endpoint that uses Server-Sent Events (SSE)
2. The endpoint should stream the response word-by-word (like ChatGPT)
3. Build a simple HTML page with:
   - A text input for the user's question
   - A "Send" button
   - A response area that shows text appearing gradually
   - A "Clear" button to reset the conversation
4. Add conversation memory so the chatbot remembers the last 5 messages
5. Test: Ask "What courses do you offer?", then ask "How much is the first one?" -- the bot should understand "the first one" refers to a course from the previous answer

**Deliverables:**
- Updated Python backend file
- `index.html` file with the chat interface
- Screenshot showing a multi-turn conversation
- Screenshot showing streaming in action (text appearing word-by-word)

---

## Task 3: Chatbot Evaluation -- 25 marks

Evaluate your chatbot's quality using the RAGAS-style metrics taught in class.

**Requirements:**

1. Create at least 8 test cases with:
   - `question` -- what the user asks
   - `context` -- what the RAG system retrieved
   - `expected_answer` -- the ideal answer
   - `chatbot_answer` -- what your chatbot actually returned
2. Evaluate each test case on three metrics:
   - **Faithfulness** -- does the answer stick to the context?
   - **Relevancy** -- does the answer address the question?
   - **Context Precision** -- was the retrieved context relevant?
3. Use an LLM-as-judge approach (send the test case to Claude/GPT and ask it to score)
4. Generate a report showing:
   - Per-question scores
   - Average scores across all test cases
   - Overall pass/fail (pass if average > 0.7)
   - Recommendations for improvement

**Include at least 2 "bad" test cases** where the chatbot gives a wrong or hallucinated answer, so your evaluation can catch them.

**Deliverables:**
- Python evaluation script
- JSON file with all test cases
- Terminal output showing the evaluation report
- A short write-up (5-10 lines) explaining what the scores mean and how you would improve the chatbot

---

## Task 4: Production Hardening -- 20 marks

Add production-ready features to your chatbot.

**Requirements:**

1. **Rate Limiting** -- Limit each user (by IP) to 15 requests per minute. Return a 429 error with a clear message when exceeded.
2. **Response Caching** -- Cache responses for frequently asked questions. If the same question is asked again within 1 hour, return the cached answer without calling the LLM.
3. **Token Budget** -- Set a daily token limit of 50,000 tokens per user. Track usage and return a 403 error when exceeded.
4. **Error Handling** -- Handle these scenarios gracefully:
   - LLM API key is missing or invalid
   - LLM API returns an error (timeout, rate limit)
   - User sends an empty message
   - User sends a very long message (> 2000 characters)
5. **Logging** -- Log every request with: timestamp, user IP, question, response time, tokens used, whether the response was cached.

**Test scenarios:**
- Send 20 requests rapidly -- verify rate limiting kicks in after 15
- Ask the same question twice -- verify the second response says "cached: true"
- Send an empty message -- verify a clear validation error
- Send a 3000-character message -- verify it is rejected

**Deliverables:**
- Updated Python backend with all features
- Screenshots showing rate limiting, caching, and error handling in action
- Log output showing at least 10 logged requests

---

## Rubric

| Criteria | Excellent (Full Marks) | Good (75%) | Needs Work (50%) |
|----------|----------------------|------------|------------------|
| **FAQ Chatbot (Task 1)** | RAG works correctly, 15+ FAQs, accurate answers, refuses off-topic questions | RAG works with 10+ FAQs, mostly accurate answers | Basic chatbot without RAG or with fewer than 10 FAQs |
| **Streaming (Task 2)** | SSE streaming works, HTML frontend displays text gradually, memory works across turns | Streaming works but UI is basic, memory partially works | No streaming, or streaming breaks after first message |
| **Evaluation (Task 3)** | 8+ test cases, all 3 metrics scored, clear report with recommendations | 5-7 test cases, 2 metrics scored, basic report | Fewer than 5 test cases, scores but no analysis |
| **Production (Task 4)** | Rate limiting, caching, budgets, error handling, and logging all work | 3 out of 5 features implemented correctly | 1-2 features implemented |
| **Code Quality** | Clean code, comments, proper error handling, follows Python best practices | Readable code with some comments | Messy code, no comments, copy-pasted without understanding |
| **Documentation** | README with setup steps, demo video, clear screenshots | README exists but incomplete, some screenshots | No README or screenshots |

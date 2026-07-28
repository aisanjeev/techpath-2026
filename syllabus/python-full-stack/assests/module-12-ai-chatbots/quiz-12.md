# Quiz: AI Chatbots & AI Assistants -- Production Ready

**Module 12 | 15 Questions | Pass Mark: 60%**

---

## Q1. What are the three layers of a production chatbot?
- A) HTML, CSS, JavaScript
- B) Frontend, Backend, Data Layer ✅
- C) Client, Server, CDN
- D) React, Node, MongoDB

> **Explanation:** Frontend (chat UI) + Backend (FastAPI with LLM) + Data Layer (vector DB + SQL for history).

---

## Q2. What does SSE stand for?
- A) Secure Socket Extension
- B) Server-Sent Events ✅
- C) Simple Stream Encoding
- D) Standard System Exchange

> **Explanation:** SSE = Server-Sent Events. The server pushes text chunks to the client for word-by-word streaming.

---

## Q3. What is RAG?
- A) Random Access Generation
- B) Retrieval-Augmented Generation ✅
- C) Real-time Agent Graph
- D) Response Analysis Gateway

> **Explanation:** RAG retrieves relevant documents, then uses them as context for the LLM to generate grounded answers.

---

## Q4. Why use a layered approach for a support bot?
- A) To make the code more complex
- B) To save money by avoiding LLM calls for simple queries ✅
- C) To slow down responses
- D) LLMs cannot answer simple questions

> **Explanation:** Layering saves 50-75% on costs. Simple queries use keyword match and FAQs; only complex ones reach the LLM.

---

## Q5. What is intent detection?
- A) Detecting the user's location
- B) Identifying what the user wants based on keywords ✅
- C) Checking if the user is logged in
- D) Measuring response speed

> **Explanation:** Intent detection uses keywords to classify the user's goal -- "fee" maps to fee_inquiry, "hello" to greeting.

---

## Q6. When should a chatbot escalate to a human?
- A) For every question
- B) Only for greetings
- C) When the user asks for a human, requests refunds, or the bot fails 3 times ✅
- D) Never

> **Explanation:** Escalate for explicit human requests, sensitive issues (refunds, complaints), or repeated failures.

---

## Q7. What does Whisper do?
- A) Generates images from text
- B) Converts speech to text (STT) ✅
- C) Converts text to speech (TTS)
- D) Encrypts messages

> **Explanation:** Whisper is OpenAI's speech-to-text model. It converts audio to text, supporting Hindi and English.

---

## Q8. What is multimodal AI?
- A) AI that only processes text
- B) AI that can process multiple types of input like text, images, and audio ✅
- C) AI with multiple language support
- D) AI with multiple output formats

> **Explanation:** Multimodal AI understands text, images, and audio -- enabling screenshot analysis, OCR, and more.

---

## Q9. What does Faithfulness measure in RAGAS?
- A) How fast the chatbot responds
- B) Whether the answer is supported by the retrieved context (no hallucination) ✅
- C) How many users like the chatbot
- D) The number of tokens used

> **Explanation:** Faithfulness checks if the answer sticks to the source documents. High score = no hallucination.

---

## Q10. What is rate limiting?
- A) Limiting the length of responses
- B) Controlling how many requests a user can make per minute ✅
- C) Limiting the number of documents uploaded
- D) Restricting which models can be used

> **Explanation:** Rate limiting caps requests per time window (e.g., 20/minute) to prevent abuse and control costs.

---

## Q11. What is the purpose of caching AI responses?
- A) To make the chatbot slower
- B) To store frequent answers so the LLM is not called for the same question twice ✅
- C) To encrypt user data
- D) To backup the database

> **Explanation:** Caching stores frequent answers. Same question = instant cached response, no LLM call. Saves 30-50%.

---

## Q12. What is model routing?
- A) Sending all queries to the most expensive model
- B) Using different LLM models based on query complexity ✅
- C) Routing queries to different servers
- D) Switching between databases

> **Explanation:** Cheap models for simple queries, expensive models for complex ones. Saves 40-60% on costs.

---

## Q13. What should a chatbot do when the LLM API is down?
- A) Crash and show an error page
- B) Retry with exponential backoff, then return a fallback response ✅
- C) Ignore the user's message
- D) Keep calling the API indefinitely

> **Explanation:** Retry with increasing waits (1s, 2s, 4s). If all retries fail, return a friendly fallback message.

---

## Q14. Why is logging important for a production chatbot?
- A) To make the code longer
- B) To track conversations, costs, errors, and debug issues ✅
- C) Logging is not important
- D) To slow down the application

> **Explanation:** Logging tracks every interaction for debugging, cost monitoring, and understanding user behavior.

---

## Q15. Recommended target score for RAGAS Faithfulness?
- A) Above 0.3
- B) Above 0.5
- C) Above 0.8 ✅
- D) Exactly 1.0

> **Explanation:** A faithfulness score above 0.8 means the bot answers from its sources with minimal hallucination.

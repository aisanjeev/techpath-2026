# Module 12: AI Chatbots and AI Assistants -- Production Ready

## 1. Chatbot Architecture Overview

### What is a Chatbot?

A chatbot is a software program that can have a conversation with a user. Modern AI chatbots use Large Language Models (LLMs) like Claude, GPT-4, or Gemini to understand questions and generate human-like answers.

Think of it like this: a chatbot is a **waiter at a restaurant**. The user (customer) asks for something, the chatbot (waiter) takes the request to the kitchen (LLM + database), gets the answer, and brings it back.

### Three-Layer Architecture

Every production chatbot has three layers:

```
┌─────────────────────────────────────────────────┐
│  FRONTEND (Browser / Mobile App)                │
│  - Chat UI with message bubbles                 │
│  - Streaming text display                       │
│  - File upload for documents                    │
│  - Voice input/output buttons                   │
├─────────────────────────────────────────────────┤
│  BACKEND (FastAPI Server)                       │
│  - API endpoints (/chat, /upload, /history)     │
│  - Authentication & rate limiting               │
│  - Conversation memory management               │
│  - LLM API calls (Claude / OpenAI)             │
├─────────────────────────────────────────────────┤
│  DATA LAYER                                     │
│  - Vector DB (ChromaDB / Pinecone / Qdrant)     │
│  - Chat history (PostgreSQL / SQLite)           │
│  - Document storage (local / cloud)             │
└─────────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Popular Tools |
|-----------|---------|---------------|
| LLM Provider | Generates responses | Claude API, OpenAI, Gemini |
| Vector Database | Stores document embeddings for search | ChromaDB, Pinecone, Qdrant, Weaviate |
| Embedding Model | Converts text to numbers for search | OpenAI `text-embedding-3-small`, Cohere Embed |
| Backend Framework | Serves API + handles logic | FastAPI, Flask |
| Frontend | Chat interface | React, vanilla JS, Streamlit |
| Streaming | Shows response word-by-word | Server-Sent Events (SSE), WebSockets |

---

## 2. RAG: Retrieval-Augmented Generation

### What is RAG?

RAG stands for **Retrieval-Augmented Generation**. Instead of the LLM answering only from its training data, we first **retrieve** relevant documents, then **augment** the prompt with those documents, so the LLM **generates** a better, more accurate answer.

**Analogy:** Imagine you are a student giving an open-book exam. You do not memorize everything -- you look up the relevant page in your textbook first, then write your answer. That is exactly what RAG does for an AI chatbot.

### RAG Pipeline -- Step by Step

```
Step 1: INGEST (one-time setup)
   PDF/Doc → Split into chunks → Generate embeddings → Store in vector DB

Step 2: QUERY (every user question)
   User question → Generate embedding → Search vector DB → Get top-K chunks
   → Build prompt: "Answer using these chunks: [chunks] Question: [user question]"
   → Send to LLM → Return answer
```

### Chunking Strategies

When you split a large document into pieces, the chunk size matters:

| Strategy | Chunk Size | Overlap | Best For |
|----------|-----------|---------|----------|
| Small chunks | 200-500 tokens | 50 tokens | Precise factual Q&A |
| Medium chunks | 500-1000 tokens | 100 tokens | General document Q&A |
| Large chunks | 1000-2000 tokens | 200 tokens | Summarization tasks |

**Overlap** means that consecutive chunks share some text at the boundaries. This prevents important information from being split across two chunks.

### Code: Basic RAG with ChromaDB

```python
import chromadb
from chromadb.utils import embedding_functions

# 1. Create a ChromaDB client and collection
client = chromadb.Client()
ef = embedding_functions.DefaultEmbeddingFunction()
collection = client.create_collection("techpath_docs", embedding_function=ef)

# 2. Add documents (chunks)
collection.add(
    documents=[
        "TechPath Institute offers Python Full Stack course for ₹49,999.",
        "The course duration is 6 months with weekend batches available.",
        "Students get placement assistance after completing the course.",
        "The campus is located in Bhopal near MP Nagar Zone-II.",
    ],
    ids=["doc1", "doc2", "doc3", "doc4"],
    metadatas=[
        {"source": "brochure", "page": 1},
        {"source": "brochure", "page": 1},
        {"source": "brochure", "page": 2},
        {"source": "website", "page": 1},
    ],
)

# 3. Query -- find relevant chunks
results = collection.query(
    query_texts=["How much does the Python course cost?"],
    n_results=2,
)
print(results["documents"])
# [['TechPath Institute offers Python Full Stack course for ₹49,999.',
#   'The course duration is 6 months with weekend batches available.']]
```

### Code: Loading PDFs

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load a PDF file
loader = PyPDFLoader("techpath_syllabus.pdf")
pages = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "],
)
chunks = splitter.split_documents(pages)
print(f"PDF split into {len(chunks)} chunks")
```

---

## 3. Streaming Responses

### Why Streaming?

Without streaming, the user stares at a blank screen for 5-10 seconds while the LLM generates the full response. With streaming, words appear one by one -- just like ChatGPT does. This feels much faster and more natural.

### Backend: FastAPI Streaming with SSE

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import anthropic

app = FastAPI()
client = anthropic.Anthropic()

@app.post("/chat")
async def chat(question: str):
    async def generate():
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": question}],
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {text}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

### Frontend: JavaScript Streaming

```javascript
async function sendMessage(question) {
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = "";

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
            if (line.startsWith("data: ") && line !== "data: [DONE]") {
                const text = line.slice(6);
                fullText += text;
                document.getElementById("response").innerText = fullText;
            }
        }
    }
}
```

---

## 4. Conversation Memory

### Why Memory Matters

Without memory, every message is independent -- the chatbot forgets what you said 10 seconds ago. With memory, it can refer to earlier messages in the conversation.

### Approaches to Memory

| Approach | How It Works | Pros | Cons |
|----------|-------------|------|------|
| Full history | Send all previous messages | Most accurate | Token cost grows fast |
| Sliding window | Keep last N messages | Controlled cost | Loses old context |
| Summary memory | Summarize old messages | Best of both | Extra LLM call needed |

### Code: Sliding Window Memory

```python
from collections import deque

class ConversationMemory:
    def __init__(self, max_messages: int = 20):
        self.messages = deque(maxlen=max_messages)

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> list:
        return list(self.messages)

    def clear(self):
        self.messages.clear()

# Usage
memory = ConversationMemory(max_messages=10)
memory.add("user", "What courses does TechPath offer?")
memory.add("assistant", "TechPath Institute offers Python Full Stack, ADCA, and Web Development courses.")
memory.add("user", "How much is the Python one?")
# Now the LLM knows "the Python one" refers to "Python Full Stack"
```

---

## 5. AI Customer Support Bot

### Intent Detection

Before sending every question to the LLM (which costs money), first detect what the user wants:

```python
INTENTS = {
    "greeting": ["hello", "hi", "hey", "good morning", "namaste"],
    "fee_inquiry": ["fee", "cost", "price", "kitna", "charge", "payment"],
    "course_info": ["course", "syllabus", "subjects", "duration", "batch"],
    "placement": ["placement", "job", "internship", "career", "salary"],
    "complaint": ["problem", "issue", "not working", "complaint", "bad"],
}

def detect_intent(message: str) -> str:
    message_lower = message.lower()
    for intent, keywords in INTENTS.items():
        if any(keyword in message_lower for keyword in keywords):
            return intent
    return "general"  # fallback to LLM
```

### Escalation Logic

When the bot cannot handle a query, it should hand off to a human:

```python
ESCALATION_TRIGGERS = [
    "speak to human", "talk to person", "manager",
    "refund", "legal", "not satisfied", "complaint",
]

def should_escalate(message: str, failed_attempts: int) -> bool:
    message_lower = message.lower()
    # Escalate if user explicitly asks
    if any(trigger in message_lower for trigger in ESCALATION_TRIGGERS):
        return True
    # Escalate after 3 failed attempts
    if failed_attempts >= 3:
        return True
    return False
```

### FAQ RAG for Support

Instead of hard-coding every answer, store FAQs in a vector database:

```python
faqs = [
    {"q": "What is the fee for Python Full Stack?", "a": "The fee is ₹49,999 for the 6-month program. EMI options available."},
    {"q": "What are the batch timings?", "a": "We have morning (10 AM - 1 PM), afternoon (2 PM - 5 PM), and weekend batches."},
    {"q": "Do you provide placement?", "a": "Yes, TechPath Institute provides 100% placement assistance after course completion."},
    {"q": "Where is TechPath located?", "a": "Our campus is in MP Nagar Zone-II, Bhopal."},
    {"q": "Can I pay in installments?", "a": "Yes, we offer 3-month and 6-month EMI options starting at ₹8,333/month."},
]
# Add these to ChromaDB, then search for the closest FAQ before calling the LLM
```

---

## 6. AI Coding Assistant

### What a Coding Assistant Does

An AI coding assistant helps developers with:
- **Code explanation** -- explain what a piece of code does in simple language
- **Debugging help** -- find and fix errors in code
- **Code generation** -- write code from a description
- **Code review** -- suggest improvements to existing code

### Building a Code Explanation Feature

```python
import anthropic

client = anthropic.Anthropic()

def explain_code(code: str, language: str = "python") -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Explain this {language} code in simple English.
            Break it down line by line. Use analogies a fresher student would understand.

            ```{language}
            {code}
            ```"""
        }],
    )
    return response.content[0].text
```

### Building a Debugging Helper

```python
def debug_code(code: str, error_message: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are a patient coding tutor at TechPath Institute. "
               "Explain bugs in simple language. Show the fix clearly.",
        messages=[{
            "role": "user",
            "content": f"""My code has an error. Help me fix it.

            Code:
            ```python
            {code}
            ```

            Error:
            ```
            {error_message}
            ```

            Tell me: 1) What went wrong, 2) Why it happened, 3) The fixed code."""
        }],
    )
    return response.content[0].text
```

---

## 7. Voice AI

### Text-to-Speech (TTS)

Text-to-speech converts written text into spoken audio. This makes chatbots accessible and natural.

| Service | Quality | Free Tier | Best For |
|---------|---------|-----------|----------|
| ElevenLabs | Excellent | 10,000 chars/month | Realistic voice |
| OpenAI TTS | Good | No free tier | Simple integration |
| Google TTS | Good | Free with limits | Multi-language |
| pyttsx3 | Basic | Fully free, offline | Offline use |

### Code: ElevenLabs TTS

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your-key")

def text_to_speech(text: str, output_file: str = "response.mp3"):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # George voice
        model_id="eleven_multilingual_v2",
    )
    with open(output_file, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return output_file
```

### Speech-to-Text (STT) with Whisper

```python
from openai import OpenAI

client = OpenAI()

def speech_to_text(audio_file_path: str) -> str:
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en",
        )
    return transcript.text

# Usage
text = speech_to_text("student_question.mp3")
print(f"Student said: {text}")
```

---

## 8. Multi-Modal AI

### What is Multi-Modal?

Multi-modal means the AI can understand **more than just text**. It can also understand images, audio, and documents. Claude and GPT-4V can look at images and answer questions about them.

### Sending Images to Claude

```python
import anthropic
import base64

client = anthropic.Anthropic()

def analyze_image(image_path: str, question: str) -> str:
    # Read and encode the image
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {"type": "text", "text": question},
            ],
        }],
    )
    return response.content[0].text

# Usage
result = analyze_image("error_screenshot.png", "What error is shown in this screenshot?")
```

### Use Cases for Multi-Modal in Chatbots

| Use Case | Description | Example |
|----------|-------------|---------|
| OCR | Extract text from images | Student uploads handwritten notes |
| Error diagnosis | Analyze screenshots | "What does this error mean?" |
| Document analysis | Read forms, invoices | "Extract the total from this bill" |
| Code screenshots | Read code from images | "What does this code do?" |
| Diagram understanding | Explain flowcharts | "Explain this ER diagram" |

---

## 9. Chatbot Evaluation with RAGAS

### Why Evaluate?

Building a chatbot is easy. Building a **good** chatbot is hard. You need to measure how well your chatbot answers questions. The RAGAS framework gives you scores for different quality dimensions.

### RAGAS Metrics

| Metric | What It Measures | Score Range | Good Score |
|--------|-----------------|-------------|------------|
| **Faithfulness** | Does the answer stick to the retrieved context? | 0 to 1 | > 0.8 |
| **Answer Relevancy** | Does the answer address the question? | 0 to 1 | > 0.7 |
| **Context Precision** | Are the retrieved chunks relevant? | 0 to 1 | > 0.7 |
| **Context Recall** | Did retrieval find all needed information? | 0 to 1 | > 0.7 |

### Simple Evaluation Without RAGAS Library

You can build basic evaluation using an LLM as a judge:

```python
def evaluate_faithfulness(question: str, context: str, answer: str) -> float:
    """Check if the answer is supported by the context (no hallucination)."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"""Rate from 0.0 to 1.0: Is this answer fully supported by the context?
            Context: {context}
            Question: {question}
            Answer: {answer}
            Reply with just a number between 0.0 and 1.0."""
        }],
    )
    return float(response.content[0].text.strip())
```

---

## 10. Production Concerns

### Rate Limiting

Prevent users from sending too many requests and running up your API bill:

```python
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        now = datetime.now()
        # Remove old requests
        self.requests[user_id] = [
            t for t in self.requests[user_id] if now - t < self.window
        ]
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        self.requests[user_id].append(now)
        return True
```

### Token Budgets

Control costs by setting per-user token limits:

```python
class TokenBudget:
    def __init__(self, daily_limit: int = 50000):
        self.daily_limit = daily_limit
        self.usage = defaultdict(int)  # user_id -> tokens used today

    def can_spend(self, user_id: str, estimated_tokens: int) -> bool:
        return self.usage[user_id] + estimated_tokens <= self.daily_limit

    def record_usage(self, user_id: str, tokens_used: int):
        self.usage[user_id] += tokens_used
```

### Caching AI Responses

If many users ask the same question, cache the answer instead of calling the LLM again:

```python
import hashlib
from functools import lru_cache

def get_cache_key(question: str) -> str:
    return hashlib.md5(question.strip().lower().encode()).hexdigest()

# Simple in-memory cache
response_cache = {}

def get_cached_response(question: str):
    key = get_cache_key(question)
    return response_cache.get(key)

def set_cached_response(question: str, response: str):
    key = get_cache_key(question)
    response_cache[key] = response
```

### Cost Control Comparison

| Strategy | Implementation | Savings |
|----------|---------------|---------|
| Caching | Store frequent answers | 30-50% cost reduction |
| Rate limiting | Cap requests per user | Prevents abuse |
| Token budgets | Limit tokens per user/day | Predictable costs |
| Smaller models | Use Haiku for simple queries | 5-10x cheaper |
| Intent routing | Use keyword match before LLM | Skip LLM for simple queries |

### Production Checklist

Before deploying a chatbot to production, verify:

- [ ] Rate limiting is configured (e.g., 20 requests/minute per user)
- [ ] Token budgets are set (e.g., 50,000 tokens/day per user)
- [ ] Response caching is enabled for common questions
- [ ] Error handling covers LLM API failures (timeouts, rate limits, outages)
- [ ] Logging tracks every question, response, and cost
- [ ] Content filtering prevents harmful or off-topic responses
- [ ] Escalation path exists (chatbot to human handoff)
- [ ] Monitoring alerts on high costs or error rates
- [ ] User feedback collection (thumbs up/down on responses)
- [ ] Fallback responses for when the LLM is unavailable

---

## Quick Reference: API Cost Comparison (as of 2025)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Best For |
|-------|----------------------|------------------------|----------|
| Claude Haiku | ~$0.25 | ~$1.25 | Simple queries, high volume |
| Claude Sonnet | ~$3 | ~$15 | General chatbot use |
| Claude Opus | ~$15 | ~$75 | Complex reasoning |
| GPT-4o mini | ~$0.15 | ~$0.60 | Budget applications |
| GPT-4o | ~$2.50 | ~$10 | General use |

**Tip:** Use a smaller, cheaper model (Haiku or GPT-4o mini) for simple questions like greetings and FAQs. Route complex questions to a more capable model (Sonnet or GPT-4o). This is called **model routing** and can cut costs by 50-70%.

---

## Summary

| Topic | Key Takeaway |
|-------|-------------|
| Architecture | Frontend + Backend (FastAPI) + Data layer (Vector DB + SQL) |
| RAG | Retrieve relevant docs first, then generate answer -- like open-book exam |
| Streaming | Use SSE to show responses word-by-word -- feels 10x faster |
| Memory | Sliding window (last N messages) is the simplest and most practical |
| Support bot | Intent detection + FAQ RAG + LLM fallback + human escalation |
| Coding assistant | System prompts + structured output = great code helper |
| Voice AI | Whisper for speech-to-text, ElevenLabs for text-to-speech |
| Multi-modal | Send images to Claude/GPT-4V for analysis, OCR, debugging |
| Evaluation | RAGAS metrics: faithfulness, relevancy, precision, recall |
| Production | Rate limits + token budgets + caching + monitoring = cost control |

# Chatbot Architecture

**Module 12 -- AI Chatbots | Topic 1**

---

## What is a Chatbot?

A chatbot is a software program that can have a conversation with a user. Modern AI chatbots use Large Language Models (LLMs) like Claude, GPT-4, or Gemini to understand questions and generate human-like answers.

**Analogy:** A chatbot is like a **waiter at a restaurant**. The user (customer) places an order, the chatbot (waiter) takes the request to the kitchen (LLM + database), gets the prepared dish (answer), and brings it back to the customer.

---

## The Three-Layer Architecture

Every production chatbot has three layers:

```
+---------------------------------------------------+
|  FRONTEND (Browser / Mobile App)                  |
|  - Chat UI with message bubbles                   |
|  - Streaming text display (word by word)           |
|  - File upload for documents                       |
|  - Send/receive messages via API calls            |
+---------------------------------------------------+
                      |
                  HTTP / SSE
                      |
+---------------------------------------------------+
|  BACKEND (FastAPI Server)                         |
|  - API endpoints (/chat, /upload, /history)       |
|  - Authentication and rate limiting                |
|  - Conversation memory management                  |
|  - LLM API calls (Claude / OpenAI)               |
+---------------------------------------------------+
                      |
+---------------------------------------------------+
|  DATA LAYER                                        |
|  - Vector DB (ChromaDB / FAISS / Pinecone)        |
|  - Chat history (PostgreSQL / SQLite)             |
|  - Document storage (local files / cloud)          |
+---------------------------------------------------+
```

### Why Three Layers?

| Layer | Responsibility | If Missing |
|-------|---------------|------------|
| Frontend | User sees and types messages | No way to interact |
| Backend | Processes messages, calls LLM | No intelligence |
| Data | Stores documents, history, embeddings | No memory, no RAG |

---

## Backend with FastAPI

FastAPI is the most popular Python framework for chatbot backends because of its speed, async support, and automatic API docs.

### Basic Chat Endpoint

```python
from fastapi import FastAPI
from pydantic import BaseModel
import anthropic

app = FastAPI()
client = anthropic.Anthropic()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"

class ChatResponse(BaseModel):
    reply: str
    conversation_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": request.message}],
    )
    return ChatResponse(
        reply=response.content[0].text,
        conversation_id=request.conversation_id,
    )
```

### Running the Server

```bash
pip install fastapi uvicorn anthropic
uvicorn main:app --reload --port 8000
# API docs at http://localhost:8000/docs
```

---

## Streaming Responses

Without streaming, the user stares at a blank screen for 5-10 seconds. With streaming, words appear one by one -- just like ChatGPT.

### Backend: Server-Sent Events (SSE)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import anthropic

app = FastAPI()
client = anthropic.Anthropic()

@app.post("/chat/stream")
async def chat_stream(message: str):
    async def generate():
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": message}],
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {text}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

### Frontend: JavaScript Streaming

```javascript
async function sendMessage(question) {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class="user-msg">${question}</div>`;
    
    const botMsg = document.createElement("div");
    botMsg.className = "bot-msg";
    chatBox.appendChild(botMsg);

    const response = await fetch("/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: question }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
            if (line.startsWith("data: ") && line !== "data: [DONE]") {
                botMsg.innerText += line.slice(6);
            }
        }
    }
}
```

---

## Choosing an LLM Provider

| Provider | Model | Cost (1M tokens) | Best For |
|----------|-------|------------------|----------|
| Anthropic | Claude Haiku | ~$0.25 in / $1.25 out | High volume, simple queries |
| Anthropic | Claude Sonnet | ~$3 in / $15 out | General chatbot use |
| OpenAI | GPT-4o mini | ~$0.15 in / $0.60 out | Budget applications |
| OpenAI | GPT-4o | ~$2.50 in / $10 out | Complex reasoning |
| Google | Gemini Flash | ~$0.075 in / $0.30 out | Very high volume |

### Cost Example for TechPath

```
100 conversations per day
Average 500 tokens per conversation
= 50,000 tokens/day = 1.5M tokens/month

Using Claude Haiku: 1.5M x $0.25/1M = Rs 30/month (approx)
Using Claude Sonnet: 1.5M x $3/1M = Rs 375/month (approx)
```

---

## Key Components

| Component | Purpose | Tools |
|-----------|---------|-------|
| LLM Provider | Generates responses | Claude API, OpenAI, Gemini |
| Vector Database | Stores document embeddings | ChromaDB, FAISS, Pinecone |
| Embedding Model | Converts text to vectors | OpenAI embeddings, HuggingFace |
| Backend Framework | Serves API and handles logic | FastAPI |
| Frontend | Chat interface | React, vanilla JS, Streamlit |
| Streaming | Word-by-word output | Server-Sent Events (SSE) |
| Authentication | User login and security | Firebase, JWT |
| Rate Limiting | Prevents abuse | Custom middleware |

---

## Project Structure

```
chatbot-project/
  backend/
    main.py              # FastAPI app
    chat.py              # Chat endpoint with streaming
    rag.py               # RAG pipeline (document search)
    memory.py            # Conversation memory
    models.py            # Pydantic schemas
    config.py            # API keys, settings
    requirements.txt
  frontend/
    index.html           # Chat UI
    style.css            # Styling
    script.js            # Streaming logic
  data/
    documents/           # PDFs, text files
    vector_store/        # FAISS/Chroma index
  .env                   # API keys (never commit!)
```

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Three layers | Frontend (UI) + Backend (FastAPI) + Data (Vector DB + SQL) |
| Streaming | Use SSE to show responses word by word |
| FastAPI | Best Python framework for chatbot backends |
| LLM choice | Haiku/GPT-4o-mini for simple queries, Sonnet/GPT-4o for complex |
| SSE | Server-Sent Events -- one-way streaming from server to client |
| Cost control | Choose model based on query complexity |

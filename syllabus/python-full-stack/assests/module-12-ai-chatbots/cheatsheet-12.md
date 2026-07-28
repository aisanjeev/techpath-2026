# Cheat Sheet: AI Chatbots & AI Assistants -- Production Ready

**Module 12 -- Quick Reference**

---

## Architecture

```
Frontend (Chat UI) --> Backend (FastAPI) --> LLM API (Claude/OpenAI)
                                        --> Vector DB (FAISS/Chroma)
                                        --> SQL DB (Chat History)
```

---

## FastAPI Chat Endpoint

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import anthropic

app = FastAPI()
client = anthropic.Anthropic()

@app.post("/chat")
async def chat(message: str):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": message}],
    )
    return {"reply": response.content[0].text}
```

---

## Streaming (SSE)

```python
@app.post("/chat/stream")
async def stream(message: str):
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

---

## RAG Chatbot (Document Q&A)

```
Upload PDF --> Split chunks --> Embed --> Store in FAISS
Question --> Embed --> Search FAISS --> Top-K chunks --> LLM --> Answer
```

```python
vectorstore = FAISS.from_documents(chunks, embeddings)
docs = vectorstore.similarity_search(question, k=3)
context = "\n".join(d.page_content for d in docs)
```

---

## Customer Support Bot Layers

| Layer | Method | Cost |
|-------|--------|------|
| 1. Intent Detection | Keyword match | Free |
| 2. FAQ RAG | Vector search | Cheap |
| 3. LLM Fallback | API call | Moderate |
| 4. Escalation | Human handoff | Free |

---

## Intent Detection

```python
INTENTS = {
    "fee_inquiry": ["fee", "cost", "price", "emi"],
    "course_info": ["course", "syllabus", "duration"],
    "greeting": ["hello", "hi", "namaste"],
}

def detect_intent(msg):
    for intent, kws in INTENTS.items():
        if any(kw in msg.lower() for kw in kws):
            return intent
    return "general"
```

---

## Voice AI

| Component | Tool | Install |
|-----------|------|---------|
| Speech-to-Text | Whisper | `pip install openai` |
| Text-to-Speech | ElevenLabs / OpenAI TTS | `pip install elevenlabs` |
| Offline STT | Local Whisper | `pip install openai-whisper` |
| Offline TTS | pyttsx3 | `pip install pyttsx3` |

```python
# STT
transcript = openai_client.audio.transcriptions.create(model="whisper-1", file=f)

# TTS
audio = openai_client.audio.speech.create(model="tts-1", voice="nova", input=text)
```

---

## Multimodal (Images)

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64_data}},
        {"type": "text", "text": "What error is shown?"},
    ]}],
)
```

---

## RAGAS Evaluation Metrics

| Metric | Checks | Target |
|--------|--------|--------|
| Faithfulness | No hallucination | > 0.8 |
| Answer Relevancy | Addresses the question | > 0.7 |
| Context Precision | Retrieved docs are relevant | > 0.7 |
| Context Recall | Found all needed info | > 0.7 |

---

## Rate Limiting

```python
class RateLimiter:
    def __init__(self, max_req=20, window_sec=60):
        self.max = max_req
        self.window = timedelta(seconds=window_sec)
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id):
        now = datetime.now()
        self.requests[user_id] = [t for t in self.requests[user_id] if now - t < self.window]
        if len(self.requests[user_id]) >= self.max:
            return False
        self.requests[user_id].append(now)
        return True
```

---

## Cost Control

| Strategy | Savings |
|----------|---------|
| Caching frequent answers | 30-50% |
| Model routing (Haiku for simple) | 40-60% |
| Intent routing (skip LLM) | 30% |
| Token budgets per user | Predictable |
| Rate limiting | Prevents abuse |

---

## Model Cost Comparison

| Model | Input/1M tokens | Best For |
|-------|----------------|----------|
| Claude Haiku | ~$0.25 | Simple queries |
| Claude Sonnet | ~$3 | General chatbot |
| GPT-4o mini | ~$0.15 | Budget apps |
| GPT-4o | ~$2.50 | Complex reasoning |

---

## Production Checklist

- [ ] Rate limiting configured
- [ ] Token budgets set
- [ ] Response caching enabled
- [ ] Error handling with retries
- [ ] Fallback responses ready
- [ ] Logging all conversations
- [ ] Content filtering active
- [ ] Model routing by complexity
- [ ] Monitoring and alerts set
- [ ] Escalation path to human

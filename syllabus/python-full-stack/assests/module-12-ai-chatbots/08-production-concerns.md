# Production Concerns

**Module 12 -- AI Chatbots | Topic 8**

---

## Why Production is Different

Building a chatbot that works on your laptop is one thing. Running it for hundreds of real users is completely different. You need to handle:
- Users sending thousands of requests (rate limiting)
- API bills growing out of control (cost control)
- Users wasting tokens on long conversations (token budgets)
- The same questions being asked repeatedly (caching)
- The LLM going down (error handling and fallbacks)

**Analogy:** Building a chatbot is like cooking for yourself. Production is like running a restaurant -- you need to manage ingredients (tokens), handle rush hour (rate limiting), prevent waste (caching), and have a backup plan when the stove breaks (fallbacks).

---

## Rate Limiting

Prevent users from sending too many requests and running up your API bill.

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
        # Remove requests outside the window
        self.requests[user_id] = [
            t for t in self.requests[user_id] if now - t < self.window
        ]
        # Check if under limit
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        self.requests[user_id].append(now)
        return True

# Usage in FastAPI
rate_limiter = RateLimiter(max_requests=20, window_seconds=60)

@app.post("/chat")
async def chat(message: str, user_id: str):
    if not rate_limiter.is_allowed(user_id):
        return {"error": "Too many requests. Please wait a minute.", "retry_after": 60}
    # Process the message...
```

### Recommended Limits

| User Type | Requests/Minute | Daily Token Limit |
|-----------|----------------|-------------------|
| Free tier | 5 | 10,000 |
| Standard | 20 | 50,000 |
| Premium | 100 | 500,000 |

---

## Token Budgets

Control costs by setting per-user token limits:

```python
class TokenBudget:
    def __init__(self, daily_limit: int = 50000):
        self.daily_limit = daily_limit
        self.usage = defaultdict(int)    # user_id -> tokens used today
        self.reset_date = datetime.now().date()
    
    def _check_reset(self):
        """Reset usage at the start of each day."""
        today = datetime.now().date()
        if today > self.reset_date:
            self.usage.clear()
            self.reset_date = today
    
    def can_spend(self, user_id: str, estimated_tokens: int) -> bool:
        self._check_reset()
        return self.usage[user_id] + estimated_tokens <= self.daily_limit
    
    def record_usage(self, user_id: str, tokens_used: int):
        self._check_reset()
        self.usage[user_id] += tokens_used
    
    def remaining(self, user_id: str) -> int:
        self._check_reset()
        return max(0, self.daily_limit - self.usage[user_id])

# Usage
budget = TokenBudget(daily_limit=50000)

@app.post("/chat")
async def chat(message: str, user_id: str):
    if not budget.can_spend(user_id, estimated_tokens=500):
        remaining = budget.remaining(user_id)
        return {"error": f"Daily token limit reached. Remaining: {remaining}"}
    
    response = call_llm(message)
    budget.record_usage(user_id, response.usage.total_tokens)
    return {"reply": response.content[0].text}
```

---

## Caching AI Responses

If many users ask the same question, cache the answer instead of calling the LLM again:

```python
import hashlib

class ResponseCache:
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def _make_key(self, question: str) -> str:
        """Create a cache key from the question."""
        normalized = question.strip().lower()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get(self, question: str) -> str | None:
        key = self._make_key(question)
        entry = self.cache.get(key)
        if entry:
            # Check if cache is still fresh (e.g., 24 hours)
            if datetime.now() - entry["time"] < timedelta(hours=24):
                return entry["response"]
            del self.cache[key]
        return None
    
    def set(self, question: str, response: str):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(self.cache, key=lambda k: self.cache[k]["time"])
            del self.cache[oldest_key]
        key = self._make_key(question)
        self.cache[key] = {"response": response, "time": datetime.now()}

# Usage
cache = ResponseCache()

@app.post("/chat")
async def chat(message: str):
    # Check cache first
    cached = cache.get(message)
    if cached:
        return {"reply": cached, "cached": True}
    
    # Call LLM if not cached
    response = call_llm(message)
    cache.set(message, response)
    return {"reply": response, "cached": False}
```

### Cache Hit Rates

For a TechPath support bot:
- "What is the fee?" -- asked 50 times/day (cache saves 49 API calls)
- "When do classes start?" -- asked 30 times/day
- Unique questions -- about 20% of total

**Expected savings: 30-50% reduction in API costs**

---

## Model Routing

Use cheaper models for simple queries and expensive models for complex ones:

```python
def choose_model(message: str, intent: str) -> str:
    """Pick the right model based on query complexity."""
    
    # Simple queries -- use cheap model
    simple_intents = ["greeting", "goodbye", "timing", "location"]
    if intent in simple_intents:
        return "claude-haiku"    # ~$0.25/1M tokens
    
    # Complex queries -- use better model
    complex_signals = ["compare", "explain", "why", "how does", "difference"]
    if any(signal in message.lower() for signal in complex_signals):
        return "claude-sonnet"   # ~$3/1M tokens
    
    # Default
    return "claude-haiku"

# Usage
model = choose_model(user_message, detected_intent)
response = client.messages.create(model=model, ...)
```

### Cost Savings from Model Routing

| Without Routing | With Routing |
|----------------|-------------|
| All queries use Sonnet | 70% use Haiku, 30% use Sonnet |
| Rs 300/month (100 queries/day) | Rs 100/month (same volume) |
| 100% quality for all queries | High quality where it matters |

---

## Error Handling

LLM APIs can fail. Always have a fallback:

```python
import time

def call_llm_with_retry(message: str, max_retries: int = 3) -> str:
    """Call LLM with retry logic and fallback."""
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": message}],
            )
            return response.content[0].text
        
        except anthropic.RateLimitError:
            # Wait and retry
            wait_time = 2 ** attempt    # 1s, 2s, 4s
            time.sleep(wait_time)
        
        except anthropic.APIStatusError as e:
            if e.status_code >= 500:
                # Server error -- retry
                time.sleep(2)
            else:
                # Client error -- don't retry
                return f"Sorry, I encountered an error: {str(e)}"
        
        except Exception as e:
            return "Sorry, I'm having trouble right now. Please try again later."
    
    # All retries failed
    return "Our AI service is temporarily unavailable. Please try again in a few minutes."
```

### Common API Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `429 Rate Limit` | Too many requests | Wait and retry with backoff |
| `500 Server Error` | Provider is down | Retry or use fallback model |
| `400 Bad Request` | Invalid input | Check message format |
| `401 Unauthorized` | Invalid API key | Check your key |
| Timeout | Response too slow | Set timeout, use faster model |

---

## Logging and Monitoring

Track every conversation for debugging and cost analysis:

```python
import logging
from datetime import datetime

logger = logging.getLogger("chatbot")

def log_conversation(user_id: str, question: str, answer: str, 
                     model: str, tokens: int, latency: float):
    """Log every conversation for monitoring."""
    logger.info({
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "question": question[:100],     # Truncate for logging
        "answer_length": len(answer),
        "model": model,
        "tokens": tokens,
        "latency_ms": round(latency * 1000),
        "estimated_cost_inr": round(tokens * 0.0001, 4),
    })
```

### Key Metrics Dashboard

| Metric | What to Track | Alert If |
|--------|-------------|----------|
| Response time | Average latency | > 5 seconds |
| Error rate | Failed requests / total | > 5% |
| Daily cost | Token usage * price | Exceeds budget |
| Cache hit rate | Cached / total | < 20% (cache not working) |
| Escalation rate | Escalated / total | > 10% (bot not helpful enough) |

---

## Content Filtering

Prevent the chatbot from generating harmful or off-topic content:

```python
BLOCKED_TOPICS = [
    "hack", "crack", "pirate", "illegal",
    "personal opinion", "political",
]

def content_filter(message: str) -> bool:
    """Check if the message should be blocked."""
    message_lower = message.lower()
    for topic in BLOCKED_TOPICS:
        if topic in message_lower:
            return True
    return False

@app.post("/chat")
async def chat(message: str):
    if content_filter(message):
        return {"reply": "I can only help with questions about TechPath Institute courses and services."}
    # Process normally...
```

---

## Production Checklist

Before deploying your chatbot:

| Category | Check | Status |
|----------|-------|--------|
| **Rate Limiting** | Max requests per user per minute configured | |
| **Token Budget** | Daily token limit per user set | |
| **Caching** | Common questions cached | |
| **Error Handling** | Retry logic with exponential backoff | |
| **Fallback** | Response for when LLM is unavailable | |
| **Logging** | Every question, response, and cost tracked | |
| **Content Filter** | Off-topic and harmful content blocked | |
| **Model Routing** | Cheap model for simple queries | |
| **Monitoring** | Alerts on high costs and errors | |
| **User Feedback** | Thumbs up/down on responses | |
| **Escalation** | Path to human agent when bot fails | |

---

## Cost Control Summary

| Strategy | Implementation | Savings |
|----------|---------------|---------|
| Caching | Store frequent answers | 30-50% |
| Model routing | Haiku for simple, Sonnet for complex | 40-60% |
| Rate limiting | Cap requests per user | Prevents abuse |
| Token budgets | Limit tokens per user/day | Predictable costs |
| Intent routing | Keyword match before LLM | Skip LLM for 30% of queries |

---

## Summary

| Concern | Solution | Why It Matters |
|---------|---------|---------------|
| Too many requests | Rate limiting | Prevents abuse, controls costs |
| High API costs | Token budgets + caching + model routing | Keeps costs predictable |
| API failures | Retry with backoff + fallback responses | Users always get an answer |
| Harmful content | Content filtering | Protects users and your brand |
| Debugging | Logging every conversation | Find and fix problems |
| Monitoring | Track latency, errors, costs | Catch issues before users complain |

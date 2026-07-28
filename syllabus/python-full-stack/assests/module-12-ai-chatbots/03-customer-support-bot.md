# Customer Support Bot

**Module 12 -- AI Chatbots | Topic 3**

---

## What is a Customer Support Bot?

A customer support bot handles common student inquiries automatically -- questions about courses, fees, timings, and placements. It uses a combination of intent detection, FAQ search, and LLM generation to answer questions quickly and accurately.

**Analogy:** Think of a support bot like a smart reception desk at TechPath Institute. For common questions ("What are your timings?"), it answers instantly from a FAQ sheet. For unusual questions, it checks the knowledge base. If it still cannot help, it connects the student to a human staff member.

---

## The Three-Layer Approach

```
User Message
     |
     v
[1. INTENT DETECTION]    -- Quick keyword check (free, fast)
     |                        "What is the fee?" --> fee_inquiry
     |                        "Hello" --> greeting
     v
[2. FAQ RAG SEARCH]      -- Search FAQ database (if needed)
     |                        Find the closest FAQ answer
     v
[3. LLM GENERATION]      -- Generate response (if FAQ misses)
     |                        Use context from FAQ + LLM
     v
[4. ESCALATION CHECK]    -- Should we transfer to human?
     |                        "I want to speak to manager" --> YES
     v
Response to User
```

This layered approach saves money -- you only call the expensive LLM when simpler methods fail.

---

## Layer 1: Intent Detection

Before calling any AI model, check if the user's intent can be detected from keywords:

```python
INTENTS = {
    "greeting": ["hello", "hi", "hey", "good morning", "namaste", "hii"],
    "fee_inquiry": ["fee", "cost", "price", "kitna", "charge", "payment", "emi"],
    "course_info": ["course", "syllabus", "subjects", "duration", "batch", "module"],
    "placement": ["placement", "job", "internship", "career", "salary", "package"],
    "timing": ["timing", "schedule", "time", "when", "class", "batch time"],
    "location": ["location", "address", "where", "campus", "office"],
    "complaint": ["problem", "issue", "not working", "complaint", "bad", "worst"],
    "goodbye": ["bye", "thank you", "thanks", "goodbye", "ok bye"],
}

def detect_intent(message: str) -> str:
    """Detect user intent from keywords. Returns intent name or 'general'."""
    message_lower = message.lower()
    for intent, keywords in INTENTS.items():
        if any(keyword in message_lower for keyword in keywords):
            return intent
    return "general"   # Fallback to LLM
```

### Quick Responses for Simple Intents

```python
QUICK_RESPONSES = {
    "greeting": "Namaste! Welcome to TechPath Institute. How can I help you today?",
    "goodbye": "Thank you for contacting TechPath Institute! Have a great day.",
    "location": "TechPath Institute is located near MP Nagar Zone-II, Bhopal. We also offer online batches for students in Delhi, Pune, and other cities.",
}

def get_quick_response(intent: str) -> str | None:
    """Return a quick response if available, else None."""
    return QUICK_RESPONSES.get(intent)
```

---

## Layer 2: FAQ RAG Search

For questions about fees, courses, and timings, search a FAQ database instead of calling the LLM every time:

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# TechPath FAQ database
faqs = [
    {"q": "What is the fee for Python Full Stack?", "a": "The fee is Rs 49,999 for the 6-month program. EMI options are available starting at Rs 8,333/month."},
    {"q": "What are the batch timings?", "a": "Morning: 10 AM - 1 PM, Afternoon: 2 PM - 5 PM, Weekend: Sat-Sun 10 AM - 4 PM."},
    {"q": "Do you provide placement assistance?", "a": "Yes, TechPath provides 100% placement assistance. Average package is Rs 4-6 LPA."},
    {"q": "Where is TechPath located?", "a": "Our campus is in MP Nagar Zone-II, Bhopal. Online batches also available."},
    {"q": "Can I pay in installments?", "a": "Yes, we offer 3-month and 6-month EMI options. No interest charged."},
    {"q": "What courses do you offer?", "a": "Python Full Stack, Data Science, AI/ML, Web Development, and ADCA courses."},
    {"q": "What is the course duration?", "a": "Python Full Stack: 6 months. Data Science: 8 months. Web Development: 4 months."},
    {"q": "Do you offer online classes?", "a": "Yes, online batches are available for all courses. Same curriculum and projects."},
    {"q": "What are the prerequisites?", "a": "No prior coding experience needed. We start from the basics."},
    {"q": "How do I enroll?", "a": "Visit our campus or call us at 9876543210. Online enrollment also available on our website."},
]

# Create FAQ vector store
faq_texts = [f"Q: {faq['q']}\nA: {faq['a']}" for faq in faqs]
faq_store = FAISS.from_texts(faq_texts, OpenAIEmbeddings())

def search_faq(question: str, threshold: float = 0.7) -> str | None:
    """Search FAQ database. Returns answer if found, None if not."""
    results = faq_store.similarity_search_with_score(question, k=1)
    if results:
        doc, score = results[0]
        if score < threshold:    # Lower score = more similar in FAISS
            return doc.page_content.split("A: ")[1]
    return None
```

---

## Layer 3: LLM Fallback

If intent detection and FAQ search both miss, use the LLM:

```python
import anthropic

client = anthropic.Anthropic()

def llm_response(question: str, context: str = "") -> str:
    """Generate a response using the LLM."""
    system_prompt = """You are a helpful customer support assistant for TechPath Institute, Bhopal.
    Be friendly, professional, and concise.
    If you don't know something, say "Let me connect you with our team for more details."
    Never make up information about fees, dates, or policies."""
    
    user_content = question
    if context:
        user_content = f"Context: {context}\n\nStudent's question: {question}"
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    return response.content[0].text
```

---

## Layer 4: Escalation Logic

When the bot cannot handle a query, it should hand off to a human:

```python
ESCALATION_TRIGGERS = [
    "speak to human", "talk to person", "manager", "call me",
    "refund", "legal", "not satisfied", "complaint", "worst",
]

def should_escalate(message: str, failed_attempts: int = 0) -> bool:
    """Check if we should transfer to a human agent."""
    message_lower = message.lower()
    
    # Explicit request for human
    if any(trigger in message_lower for trigger in ESCALATION_TRIGGERS):
        return True
    
    # Too many failed attempts
    if failed_attempts >= 3:
        return True
    
    return False

def escalation_response() -> str:
    return ("I understand you need more help. Let me connect you with our team. "
            "Please call us at 9876543210 or email support@techpath.biz. "
            "Our team is available Mon-Sat, 10 AM to 6 PM.")
```

---

## Putting It All Together

```python
def handle_message(message: str, conversation: dict) -> str:
    """Main message handler -- routes through all layers."""
    
    # Track failed attempts
    failed = conversation.get("failed_attempts", 0)
    
    # Layer 4: Check escalation first
    if should_escalate(message, failed):
        return escalation_response()
    
    # Layer 1: Intent detection
    intent = detect_intent(message)
    
    quick = get_quick_response(intent)
    if quick:
        return quick
    
    # Layer 2: FAQ search
    faq_answer = search_faq(message)
    if faq_answer:
        return faq_answer
    
    # Layer 3: LLM fallback
    try:
        return llm_response(message)
    except Exception:
        conversation["failed_attempts"] = failed + 1
        return "I'm sorry, I couldn't process your question. Could you rephrase it?"
```

### Cost Savings from Layered Approach

| Layer | Cost per Query | Handles |
|-------|---------------|---------|
| Intent detection | Free (keyword match) | 30% of queries (greetings, simple intents) |
| FAQ RAG search | ~Rs 0.01 (embedding only) | 40% of queries (common questions) |
| LLM generation | ~Rs 0.50 (API call) | 25% of queries (complex questions) |
| Escalation | Free | 5% of queries (complaints, complex issues) |

**Without layering:** 100% of queries go to LLM = Rs 50/day for 100 queries
**With layering:** Only 25% go to LLM = Rs 12.50/day for 100 queries (75% savings)

---

## Conversation Memory

The bot should remember what the student said earlier in the conversation:

```python
from collections import deque

class ConversationMemory:
    def __init__(self, max_messages: int = 20):
        self.messages = deque(maxlen=max_messages)
    
    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
    
    def get_messages(self) -> list:
        return list(self.messages)
    
    def get_context_string(self) -> str:
        return "\n".join(f"{m['role']}: {m['content']}" for m in self.messages)
```

---

## Summary

| Layer | What It Does | Cost |
|-------|-------------|------|
| Intent detection | Keyword-based quick routing | Free |
| FAQ RAG | Searches stored FAQs by meaning | Very cheap |
| LLM generation | Generates custom responses | Moderate |
| Escalation | Transfers to human agent | Free |

| Best Practice | Why |
|--------------|-----|
| Layer your approach | Saves 50-75% on LLM costs |
| Keep FAQs updated | Reduces LLM fallback calls |
| Track failed attempts | Know when to escalate |
| Never make up info | Direct students to humans for unknown answers |

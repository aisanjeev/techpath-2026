"""
RAG Chatbot Backend -- TechPath Institute Course FAQ Bot
========================================================

A complete Retrieval-Augmented Generation (RAG) chatbot backend built with
FastAPI. This bot answers questions about TechPath Institute courses by
searching a knowledge base and generating responses using Claude.

INSTALL INSTRUCTIONS:
    pip install fastapi uvicorn anthropic chromadb pydantic

RUN:
    uvicorn code-rag-chatbot-backend:app --reload --port 8000

    Then open http://localhost:8000/docs to test the API.

SETUP:
    Set your Anthropic API key as an environment variable:
    - Windows:  set ANTHROPIC_API_KEY=sk-ant-...
    - Mac/Linux: export ANTHROPIC_API_KEY=sk-ant-...

    Or create a .env file with:
    ANTHROPIC_API_KEY=sk-ant-your-key-here
"""

# ============================================================
# IMPORTS
# ============================================================

import os
import json
import hashlib
import time
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Anthropic SDK for Claude API calls
import anthropic

# ChromaDB for vector search (stores document embeddings locally)
import chromadb
from chromadb.utils import embedding_functions

# ============================================================
# APP SETUP
# ============================================================

app = FastAPI(
    title="TechPath RAG Chatbot API",
    description="AI-powered course FAQ chatbot for TechPath Institute, Bhopal",
    version="1.0.0",
)

# Allow frontend to connect from any origin (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# CONFIGURATION
# ============================================================

# Claude API client -- reads ANTHROPIC_API_KEY from environment
client = anthropic.Anthropic()

# Model to use for chat responses
CHAT_MODEL = "claude-sonnet-4-20250514"

# Maximum tokens the LLM can generate per response
MAX_TOKENS = 1024

# How many document chunks to retrieve per question
TOP_K_RESULTS = 3

# Rate limiting: max requests per user per minute
RATE_LIMIT_MAX = 10
RATE_LIMIT_WINDOW = 60  # seconds

# Token budget: max tokens per user per day
DAILY_TOKEN_BUDGET = 100_000

# ============================================================
# KNOWLEDGE BASE -- TechPath Institute FAQ Data
# ============================================================
# In production, you would load this from a database or PDF files.
# Here we use a list of FAQ entries as the knowledge base.

TECHPATH_FAQ_DATA = [
    # Course Information
    {
        "text": "TechPath Institute offers a Python Full Stack Developer course. The duration is 6 months. The fee is ₹49,999. EMI options are available starting at ₹8,333 per month for 6 months.",
        "category": "courses",
        "source": "brochure",
    },
    {
        "text": "TechPath Institute offers an Advanced Diploma in Computer Applications (ADCA) course. The duration is 12 months. The fee is ₹35,999. This covers computer fundamentals, MS Office, web development, Python, databases, and AI tools.",
        "category": "courses",
        "source": "brochure",
    },
    {
        "text": "TechPath Institute offers a Web Development Bootcamp. The duration is 3 months. The fee is ₹24,999. This covers HTML, CSS, JavaScript, React, Node.js, and deployment.",
        "category": "courses",
        "source": "brochure",
    },
    {
        "text": "The Python Full Stack course syllabus covers 18 modules: Python Core, Advanced Python, Python Libraries, Database Design, Git & GitHub, FastAPI, Django & DRF, Frontend (React), GenAI Fundamentals, LangChain, LangGraph, AI Chatbots, Docker, CI/CD, Cloud Deployment, Spec Kit, Capstone Project, and Career Launch.",
        "category": "syllabus",
        "source": "website",
    },
    # Batch Timings
    {
        "text": "TechPath Institute batch timings: Morning batch 10:00 AM to 1:00 PM, Afternoon batch 2:00 PM to 5:00 PM, Evening batch 6:00 PM to 8:00 PM (online only), Weekend batch Saturday-Sunday 10:00 AM to 4:00 PM. Students can switch batches with 2 days advance notice.",
        "category": "schedule",
        "source": "website",
    },
    # Location
    {
        "text": "TechPath Institute is located in MP Nagar Zone-II, Bhopal, Madhya Pradesh. The campus is near the DB Mall and easily accessible by city bus routes 9 and 12. Free parking is available for two-wheeler vehicles.",
        "category": "location",
        "source": "website",
    },
    # Placement
    {
        "text": "TechPath Institute provides 100% placement assistance. Partner companies include TCS, Infosys, Wipro, Tech Mahindra, and several startups in Pune, Bhopal, and Indore. Average starting salary for Python Full Stack graduates is ₹4-6 LPA. Students also get help with resume building, mock interviews, and LinkedIn profile optimization.",
        "category": "placement",
        "source": "placement_report",
    },
    {
        "text": "TechPath placement statistics for 2025: 87% of eligible students placed within 3 months of course completion. Top recruiters: TCS (12 students), Infosys (8 students), startups (25 students). Highest package offered: ₹8.5 LPA for a Python Full Stack graduate placed at a Pune-based fintech startup.",
        "category": "placement",
        "source": "placement_report",
    },
    # Admission
    {
        "text": "Admission process at TechPath Institute: Step 1 - Fill the online enquiry form or visit the campus. Step 2 - Counselling session with a faculty member. Step 3 - Pay the registration fee of ₹2,000 (adjusted in total fee). Step 4 - Get your login credentials for the student portal. No entrance exam required. Minimum qualification is 12th pass for ADCA and graduation for Python Full Stack.",
        "category": "admission",
        "source": "website",
    },
    # Infrastructure
    {
        "text": "TechPath Institute has 3 computer labs with 30 workstations each, all running Windows 11 and Ubuntu dual-boot. High-speed 100 Mbps internet. Each student gets a personal cloud workspace. The campus also has a library, cafeteria, and a seminar hall for guest lectures and hackathons.",
        "category": "infrastructure",
        "source": "brochure",
    },
    # Trainers
    {
        "text": "TechPath Institute trainers have 5+ years of industry experience. Lead Python trainer Vikram Malhotra previously worked at Wipro and has built production applications using FastAPI and Django. The AI/ML module is taught by Sneha Iyer who has published research papers on LLM applications.",
        "category": "faculty",
        "source": "website",
    },
    # Certification
    {
        "text": "Upon completing any course at TechPath Institute, students receive an industry-recognized certificate. The certificate includes a QR code that links to a verification page. TechPath certificates are accepted by most IT companies in India for skill validation.",
        "category": "certification",
        "source": "website",
    },
]


# ============================================================
# VECTOR DATABASE SETUP (ChromaDB)
# ============================================================

def initialize_vector_db():
    """
    Create a ChromaDB collection and load the FAQ knowledge base.
    ChromaDB automatically generates embeddings using its default model.
    In production, you would use OpenAI or Cohere embeddings for better quality.
    """
    # Create an in-memory ChromaDB client (use PersistentClient for production)
    chroma_client = chromadb.Client()

    # Use the default embedding function (all-MiniLM-L6-v2)
    ef = embedding_functions.DefaultEmbeddingFunction()

    # Create or get the collection
    collection = chroma_client.get_or_create_collection(
        name="techpath_faq",
        embedding_function=ef,
        metadata={"description": "TechPath Institute FAQ knowledge base"},
    )

    # Only add documents if collection is empty
    if collection.count() == 0:
        print("Loading FAQ data into vector database...")
        collection.add(
            documents=[item["text"] for item in TECHPATH_FAQ_DATA],
            ids=[f"faq_{i}" for i in range(len(TECHPATH_FAQ_DATA))],
            metadatas=[
                {"category": item["category"], "source": item["source"]}
                for item in TECHPATH_FAQ_DATA
            ],
        )
        print(f"Loaded {len(TECHPATH_FAQ_DATA)} FAQ entries.")

    return collection


# Initialize the vector DB when the app starts
faq_collection = initialize_vector_db()


# ============================================================
# CONVERSATION MEMORY
# ============================================================
# Stores recent messages per session so the chatbot can refer
# to earlier parts of the conversation.

class ConversationMemory:
    """
    Sliding window memory -- keeps the last N messages per session.
    Old messages are automatically dropped to control token usage.
    """

    def __init__(self, max_messages: int = 20):
        # Each session gets its own deque (double-ended queue)
        self.sessions: dict[str, deque] = defaultdict(
            lambda: deque(maxlen=max_messages)
        )

    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to the session history."""
        self.sessions[session_id].append({
            "role": role,
            "content": content,
        })

    def get_history(self, session_id: str) -> list[dict]:
        """Get all messages in the session as a list."""
        return list(self.sessions[session_id])

    def clear_session(self, session_id: str):
        """Clear all messages for a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]


# Create a global memory instance
memory = ConversationMemory(max_messages=20)


# ============================================================
# RATE LIMITER
# ============================================================
# Prevents a single user from sending too many requests and
# running up the API bill.

class RateLimiter:
    """
    Limits each user to a maximum number of requests within a time window.
    Example: 10 requests per 60 seconds.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        # Stores timestamps of recent requests per user
        self.request_log: dict[str, list[datetime]] = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        """Check if the user can make another request."""
        now = datetime.now()

        # Remove timestamps older than the window
        self.request_log[user_id] = [
            t for t in self.request_log[user_id]
            if now - t < self.window
        ]

        # Check if under the limit
        if len(self.request_log[user_id]) >= self.max_requests:
            return False

        # Record this request
        self.request_log[user_id].append(now)
        return True

    def remaining(self, user_id: str) -> int:
        """How many requests the user has left in the current window."""
        now = datetime.now()
        recent = [
            t for t in self.request_log[user_id]
            if now - t < self.window
        ]
        return max(0, self.max_requests - len(recent))


# Create a global rate limiter
rate_limiter = RateLimiter(
    max_requests=RATE_LIMIT_MAX,
    window_seconds=RATE_LIMIT_WINDOW,
)


# ============================================================
# RESPONSE CACHE
# ============================================================
# If multiple users ask the exact same question, return the
# cached answer instead of calling the LLM again.

class ResponseCache:
    """
    Simple in-memory cache for chatbot responses.
    Uses MD5 hash of the question as the cache key.
    Entries expire after a configurable TTL (time-to-live).
    """

    def __init__(self, ttl_seconds: int = 3600):
        self.cache: dict[str, dict] = {}
        self.ttl = ttl_seconds

    def _make_key(self, question: str) -> str:
        """Create a cache key by hashing the normalized question."""
        normalized = question.strip().lower()
        return hashlib.md5(normalized.encode()).hexdigest()

    def get(self, question: str) -> Optional[str]:
        """Look up a cached response. Returns None if not found or expired."""
        key = self._make_key(question)
        entry = self.cache.get(key)
        if entry is None:
            return None
        # Check if expired
        if time.time() - entry["timestamp"] > self.ttl:
            del self.cache[key]
            return None
        return entry["response"]

    def set(self, question: str, response: str):
        """Store a response in the cache."""
        key = self._make_key(question)
        self.cache[key] = {
            "response": response,
            "timestamp": time.time(),
        }


# Create a global cache (1 hour TTL)
response_cache = ResponseCache(ttl_seconds=3600)


# ============================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================

class ChatRequest(BaseModel):
    """What the frontend sends when a user asks a question."""
    message: str = Field(..., min_length=1, max_length=2000,
                         description="The user's question")
    session_id: str = Field(default="default",
                            description="Session ID for conversation memory")

class ChatResponse(BaseModel):
    """What the API returns after generating an answer."""
    answer: str
    sources: list[dict] = Field(default_factory=list,
                                description="Retrieved document sources")
    cached: bool = Field(default=False,
                         description="Whether this was a cached response")
    session_id: str

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    faq_count: int
    uptime: str


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def retrieve_context(question: str) -> tuple[str, list[dict]]:
    """
    Search the vector database for chunks relevant to the user's question.
    Returns the combined context text and source metadata.
    """
    results = faq_collection.query(
        query_texts=[question],
        n_results=TOP_K_RESULTS,
    )

    # Combine retrieved chunks into a single context string
    context_parts = []
    sources = []

    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            context_parts.append(doc)
            # Include metadata about where the info came from
            meta = results["metadatas"][0][i] if results["metadatas"] else {}
            sources.append({
                "text_preview": doc[:100] + "..." if len(doc) > 100 else doc,
                "category": meta.get("category", "unknown"),
                "source": meta.get("source", "unknown"),
            })

    context = "\n\n".join(context_parts)
    return context, sources


def build_prompt(question: str, context: str, history: list[dict]) -> list[dict]:
    """
    Build the message list for the Claude API call.
    Includes conversation history, retrieved context, and the current question.
    """
    # System message sets the chatbot's personality and rules
    system_prompt = """You are the TechPath Institute AI Assistant, a helpful and friendly chatbot
for TechPath Institute, an IT training center located in Bhopal, Madhya Pradesh, India.

RULES:
1. Answer questions using ONLY the provided context. Do not make up information.
2. If the context does not contain the answer, say: "I don't have that information.
   Please contact our office at +91-755-XXXXXXX or visit our campus in MP Nagar."
3. Be friendly, professional, and concise.
4. Use Indian Rupee (₹) for all prices.
5. If asked about something unrelated to TechPath, politely redirect the conversation.
6. Keep answers short (2-4 sentences) unless the user asks for details."""

    # Build the messages list
    messages = []

    # Add conversation history (for context)
    for msg in history:
        messages.append(msg)

    # Add the current question with retrieved context
    user_message = f"""Use the following context to answer the student's question.
If the answer is not in the context, say you don't have that information.

CONTEXT:
{context}

STUDENT'S QUESTION: {question}"""

    messages.append({"role": "user", "content": user_message})

    return messages


# Track app start time for uptime calculation
APP_START_TIME = datetime.now()


# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/", tags=["General"])
async def home():
    """Root endpoint -- confirms the API is running."""
    return {
        "message": "TechPath RAG Chatbot API is running!",
        "docs": "/docs",
        "endpoints": {
            "chat": "POST /chat",
            "chat_stream": "POST /chat/stream",
            "health": "GET /health",
            "clear_history": "DELETE /history/{session_id}",
        },
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Check if the API and vector database are working."""
    uptime = datetime.now() - APP_START_TIME
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    return HealthResponse(
        status="healthy",
        faq_count=faq_collection.count(),
        uptime=f"{hours}h {minutes}m {seconds}s",
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest, req: Request):
    """
    Main chat endpoint -- takes a question and returns an AI-generated answer.

    Flow:
    1. Check rate limit
    2. Check cache for existing answer
    3. Retrieve relevant context from vector DB
    4. Build prompt with context and conversation history
    5. Call Claude API for the answer
    6. Store in memory and cache
    7. Return the answer with sources
    """
    # Use IP address as user ID for rate limiting (in production, use auth tokens)
    user_id = req.client.host if req.client else "unknown"

    # STEP 1: Check rate limit
    if not rate_limiter.is_allowed(user_id):
        remaining = rate_limiter.remaining(user_id)
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. You can make {RATE_LIMIT_MAX} requests "
                   f"per {RATE_LIMIT_WINDOW} seconds. Please wait and try again.",
        )

    # STEP 2: Check cache
    cached_answer = response_cache.get(request.message)
    if cached_answer:
        return ChatResponse(
            answer=cached_answer,
            sources=[],
            cached=True,
            session_id=request.session_id,
        )

    # STEP 3: Retrieve relevant context from vector DB
    context, sources = retrieve_context(request.message)

    # STEP 4: Build prompt with history and context
    history = memory.get_history(request.session_id)
    messages = build_prompt(request.message, context, history)

    # STEP 5: Call Claude API
    try:
        response = client.messages.create(
            model=CHAT_MODEL,
            max_tokens=MAX_TOKENS,
            system="""You are the TechPath Institute AI Assistant, a helpful chatbot
for TechPath Institute in Bhopal. Answer using only the provided context.
Be friendly, concise, and use ₹ for prices.""",
            messages=messages,
        )
        answer = response.content[0].text
    except anthropic.APIError as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI service temporarily unavailable. Please try again. Error: {str(e)}",
        )

    # STEP 6: Store in memory and cache
    memory.add_message(request.session_id, "user", request.message)
    memory.add_message(request.session_id, "assistant", answer)
    response_cache.set(request.message, answer)

    # STEP 7: Return the answer
    return ChatResponse(
        answer=answer,
        sources=sources,
        cached=False,
        session_id=request.session_id,
    )


@app.post("/chat/stream", tags=["Chat"])
async def chat_stream(request: ChatRequest, req: Request):
    """
    Streaming chat endpoint -- returns the answer word-by-word using
    Server-Sent Events (SSE). This is how ChatGPT shows responses
    appearing gradually instead of all at once.

    The frontend reads this using the EventSource API or fetch + ReadableStream.
    """
    # Rate limit check
    user_id = req.client.host if req.client else "unknown"
    if not rate_limiter.is_allowed(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    # Retrieve context
    context, sources = retrieve_context(request.message)

    # Build prompt
    history = memory.get_history(request.session_id)
    messages = build_prompt(request.message, context, history)

    async def generate():
        """
        Generator function that yields response chunks as SSE events.
        Each chunk is a small piece of the answer (a few words or a sentence).
        The frontend reads these chunks and displays them one by one.
        """
        full_response = ""

        try:
            # Use Claude's streaming API
            with client.messages.stream(
                model=CHAT_MODEL,
                max_tokens=MAX_TOKENS,
                system="""You are the TechPath Institute AI Assistant, a helpful chatbot
for TechPath Institute in Bhopal. Answer using only the provided context.
Be friendly, concise, and use ₹ for prices.""",
                messages=messages,
            ) as stream:
                for text_chunk in stream.text_stream:
                    full_response += text_chunk
                    # Send each chunk as an SSE event
                    # Format: "data: <text>\n\n"
                    yield f"data: {json.dumps({'text': text_chunk})}\n\n"

        except anthropic.APIError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

        # Send a final event to signal the stream is complete
        yield f"data: {json.dumps({'done': True, 'sources': sources})}\n\n"

        # Store the complete response in memory
        memory.add_message(request.session_id, "user", request.message)
        memory.add_message(request.session_id, "assistant", full_response)

    # Return as a streaming response with SSE content type
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.delete("/history/{session_id}", tags=["Chat"])
async def clear_history(session_id: str):
    """Clear conversation history for a session."""
    memory.clear_session(session_id)
    return {"success": True, "message": f"History cleared for session '{session_id}'."}


@app.get("/stats", tags=["Admin"])
async def get_stats():
    """
    Get chatbot statistics (for admin dashboard).
    In production, this would be behind authentication.
    """
    return {
        "faq_entries": faq_collection.count(),
        "active_sessions": len(memory.sessions),
        "cache_entries": len(response_cache.cache),
        "uptime_seconds": (datetime.now() - APP_START_TIME).total_seconds(),
    }


# ============================================================
# MAIN -- Run with: python code-rag-chatbot-backend.py
# ============================================================

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("  TechPath RAG Chatbot API")
    print("  Open http://localhost:8000/docs for Swagger UI")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)

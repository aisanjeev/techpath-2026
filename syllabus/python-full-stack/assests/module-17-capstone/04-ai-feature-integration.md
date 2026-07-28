# AI Feature Integration: RAG, Chatbots, and AI Workflows

**Module 17 — Full-Stack AI Product: Capstone Development | Topic 4**

---

## What AI Feature Should You Add?

Adding an AI feature to your capstone is what separates a good project from a great one. But the key is choosing the RIGHT AI feature — one that genuinely improves the user experience, not one that is glued on as an afterthought.

Think of AI features like spices in cooking. The right spice enhances the dish. Too much spice, or the wrong spice, ruins it. Your AI feature should feel natural and useful, not forced.

### AI Feature Options for Capstone Projects

| AI Feature | What It Does | Best For | Difficulty |
|-----------|-------------|----------|------------|
| **Chatbot (RAG)** | Answers questions using your app's data | Knowledge bases, course portals, documentation | Medium |
| **Text Summarizer** | Condenses long text into key points | Document management, news aggregator | Low |
| **Recommendation Engine** | Suggests items based on user behavior | E-commerce, course platforms, job boards | Medium |
| **Content Generator** | Creates descriptions, emails, reports | Invoice tools, product catalogs | Low |
| **Code Review Assistant** | Reviews code and suggests improvements | Coding platforms, learning apps | Medium-High |
| **Smart Search** | Semantic search (understands meaning, not just keywords) | Any app with search functionality | Medium |

**Recommendation**: For your capstone, build a RAG-based chatbot. It is impressive, demonstrates multiple skills (vector databases, LLM integration, prompt engineering), and works with any domain.

---

## Understanding RAG Architecture

RAG stands for Retrieval-Augmented Generation. It is a technique that makes AI answers accurate and grounded in your actual data, instead of making things up (hallucinating).

### How RAG Works — The Library Analogy

Imagine you are a librarian in a huge library (your database). A student (the user) asks you a question. Here is what you do:

1. **Retrieve**: You go to the relevant shelf and pull out 3-5 books that might have the answer
2. **Augment**: You open those books to the relevant pages and read the key passages
3. **Generate**: You use those passages to craft a clear, accurate answer for the student

Without RAG, the AI would just guess the answer from its general knowledge. With RAG, it always references your actual data.

### RAG Architecture Diagram

```
User Question
    |
    v
[1. Embed Question] --> Convert question to a vector (numbers)
    |
    v
[2. Search Vector DB] --> Find similar documents/chunks
    |
    v
[3. Retrieve Top Results] --> Get 3-5 most relevant text chunks
    |
    v
[4. Build Prompt] --> Combine: System instruction + Context chunks + User question
    |
    v
[5. Send to LLM] --> GPT generates answer using the context
    |
    v
[6. Return Answer] --> Show answer to user with source references
```

---

## Setting Up RAG with LangChain

LangChain is a framework that makes building RAG pipelines much easier. It handles the heavy lifting of document loading, splitting, embedding, and retrieval.

### Installing Dependencies

```bash
poetry add langchain langchain-openai langchain-community chromadb tiktoken
```

### Step 1: Load and Split Documents

```python
# app/services/rag_service.py
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_and_split_documents(file_path: str) -> list:
    """Load a document and split it into chunks."""

    # Choose loader based on file type
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()

    # Split into chunks of 500 characters with 50 character overlap
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    print(f"Split {file_path} into {len(chunks)} chunks")
    return chunks
```

### Step 2: Create a Vector Database with ChromaDB

ChromaDB is a lightweight vector database that stores your document chunks as numerical vectors, making similarity search fast and efficient.

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import settings


# Create embeddings model
embeddings = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    model="text-embedding-3-small",
)


def create_vector_store(chunks: list, collection_name: str = "capstone_docs"):
    """Create a ChromaDB vector store from document chunks."""
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory="./data/chroma_db",
    )
    print(f"Created vector store with {len(chunks)} documents")
    return vector_store


def get_vector_store(collection_name: str = "capstone_docs"):
    """Load an existing vector store."""
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory="./data/chroma_db",
    )
```

### Step 3: Build the RAG Chain

```python
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def create_rag_chain(vector_store):
    """Create a RAG chain that answers questions using retrieved context."""

    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a helpful assistant for TechPath Institute students.
Answer the question based ONLY on the following context. If the context does not
contain enough information, say "I do not have enough information to answer this."

Context:
{context}

Question: {question}

Answer in simple, clear language suitable for beginner students:""",
    )

    # Create the LLM
    llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model="gpt-3.5-turbo",
        temperature=0.2,
    )

    # Create the RAG chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Puts all retrieved docs into one prompt
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt_template},
        return_source_documents=True,
    )

    return chain
```

### Step 4: Create the API Endpoint

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import get_vector_store, create_rag_chain


router = APIRouter(prefix="/chat", tags=["AI Chat"])


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/ask", response_model=ChatResponse)
async def ask_chatbot(request: ChatRequest):
    """Ask the RAG chatbot a question."""
    try:
        vector_store = get_vector_store()
        chain = create_rag_chain(vector_store)

        result = chain.invoke({"query": request.question})

        # Extract source document references
        sources = []
        for doc in result.get("source_documents", []):
            source = doc.metadata.get("source", "Unknown")
            if source not in sources:
                sources.append(source)

        return ChatResponse(
            answer=result["result"],
            sources=sources,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")
```

---

## Prompt Engineering for Your AI Feature

The quality of your AI feature depends heavily on how you write your prompts. Bad prompts give bad answers.

### Prompt Engineering Best Practices

| Principle | Bad Prompt | Good Prompt |
|-----------|-----------|-------------|
| Be specific | "Answer this question" | "Answer based ONLY on the provided context" |
| Set a role | (no role) | "You are a course advisor for engineering students" |
| Limit scope | "Tell me everything about Python" | "Explain Python lists in 3 bullet points" |
| Handle unknowns | (no instruction) | "If you do not know, say 'I need more information'" |
| Set format | (no format) | "Respond in JSON with keys: answer, confidence" |

### Example Prompts for Common AI Features

**For a Course Recommendation Chatbot:**
```python
system_prompt = """You are a course advisor at TechPath Institute, Bhopal.
You help students choose the right courses based on their goals and background.

Rules:
1. Only recommend courses that exist in the provided course catalog
2. Ask about the student's current skill level before recommending
3. Suggest a learning path (which course to take first, second, etc.)
4. Keep responses under 200 words
5. Use simple English suitable for beginners"""
```

**For a Resume Review Assistant:**
```python
system_prompt = """You are a resume reviewer for fresh graduates in India.
Review the resume and provide feedback in this exact format:

SCORE: [1-10]
STRENGTHS:
- [Point 1]
- [Point 2]
IMPROVEMENTS:
- [Point 1 with specific suggestion]
- [Point 2 with specific suggestion]
MISSING SECTIONS:
- [Any important sections not present]

Be encouraging but honest. Focus on what matters for entry-level jobs in India."""
```

---

## Testing AI Features

AI features are tricky to test because the output is non-deterministic (the same input can give different outputs). Here is how to handle it.

### Testing Strategies

| What to Test | How to Test | Example |
|-------------|-------------|---------|
| API endpoint works | Call endpoint, check 200 status | `assert response.status_code == 200` |
| Response has correct format | Validate response schema | `assert "answer" in response.json()` |
| Context retrieval works | Check that relevant docs are retrieved | `assert len(sources) > 0` |
| Empty input handling | Send empty question | `assert response.status_code == 422` |
| Long input handling | Send very long text | Should not crash, may truncate |
| API key missing | Remove API key from env | Should return clear error message |

### Example Test

```python
# tests/test_ai_chat.py
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_chat_endpoint_returns_answer():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/chat/ask",
            json={"question": "What Python courses are available?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert isinstance(data["answer"], str)
        assert len(data["answer"]) > 10


@pytest.mark.asyncio
async def test_chat_endpoint_rejects_empty_question():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/chat/ask",
            json={"question": ""},
        )
        # Should either reject or handle gracefully
        assert response.status_code in [200, 422]
```

---

## Common AI Integration Mistakes

| Mistake | Why It Is Bad | Solution |
|---------|-------------|----------|
| No rate limiting on AI endpoints | Users can drain your API credits in minutes | Add rate limiting (e.g., 10 requests per minute per user) |
| Not caching AI responses | Same question costs money every time | Cache responses in Redis for identical queries |
| Sending entire documents to LLM | Exceeds token limits, costs more | Use RAG to send only relevant chunks |
| No fallback when AI fails | App crashes if OpenAI is down | Return a helpful error message |
| Exposing API keys in frontend | Anyone can steal your key | Always call AI from backend, never from frontend |

---

*TechPath Institute — Full-Stack AI Product: Capstone Development*

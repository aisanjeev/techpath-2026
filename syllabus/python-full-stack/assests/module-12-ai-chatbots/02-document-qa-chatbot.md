# Document Q&A Chatbot

**Module 12 -- AI Chatbots | Topic 2**

---

## What is a Document Q&A Chatbot?

A Document Q&A chatbot lets users upload a PDF or text file, then ask questions about it. The chatbot finds relevant sections in the document and generates answers based on those sections.

**Analogy:** Imagine giving your textbook to a very fast reader. They read the entire book, and then you can ask them any question about it. They flip to the right page, read the relevant paragraph, and answer in their own words. That is exactly what a document Q&A chatbot does.

### The Flow

```
Step 1: UPLOAD
  User uploads "techpath_syllabus.pdf"
       |
       v
  Split PDF into chunks --> Generate embeddings --> Store in vector DB

Step 2: ASK QUESTIONS
  User: "What is the Python course fee?"
       |
       v
  Search vector DB --> Find relevant chunks --> Send to LLM --> Answer
```

---

## Building the Backend

### Step 1: File Upload Endpoint

```python
from fastapi import FastAPI, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import shutil
import os

app = FastAPI()
embeddings = OpenAIEmbeddings()
vector_stores = {}   # Store per-document indexes

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Load and split the PDF
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(pages)
    
    # Create vector store
    doc_id = file.filename.replace(".", "_")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vector_stores[doc_id] = vectorstore
    
    return {
        "message": f"Uploaded {file.filename}",
        "chunks": len(chunks),
        "doc_id": doc_id,
    }
```

### Step 2: Chat Endpoint with RAG

```python
from fastapi.responses import StreamingResponse
import anthropic

client = anthropic.Anthropic()

@app.post("/chat")
async def chat_with_document(question: str, doc_id: str):
    # Get the vector store for this document
    vectorstore = vector_stores.get(doc_id)
    if not vectorstore:
        return {"error": "Document not found. Please upload first."}
    
    # Search for relevant chunks
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)
    
    # Generate answer with streaming
    async def generate():
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system="You are a helpful assistant. Answer based ONLY on the provided context. If the answer is not in the context, say 'This information is not in the document.'",
            messages=[{
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }],
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {text}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### Step 3: Chat with Sources

Users want to know where the answer came from:

```python
@app.post("/chat-with-sources")
async def chat_with_sources(question: str, doc_id: str):
    vectorstore = vector_stores.get(doc_id)
    if not vectorstore:
        return {"error": "Document not found"}
    
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)
    sources = [
        {"page": doc.metadata.get("page", "?"), "preview": doc.page_content[:100]}
        for doc in docs
    ]
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer based only on the context."
        }],
    )
    
    return {
        "answer": response.content[0].text,
        "sources": sources,
    }
```

---

## The Frontend

### Simple Chat UI

```html
<!DOCTYPE html>
<html>
<head>
    <title>TechPath Document Chat</title>
    <style>
        body { font-family: Arial; background: #0f172a; color: #e2e8f0; margin: 0; padding: 20px; }
        .container { max-width: 700px; margin: 0 auto; }
        h1 { color: #38bdf8; }
        .upload-area { background: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .chat-box { background: #1e293b; border-radius: 8px; padding: 20px; height: 400px; overflow-y: auto; }
        .user-msg { background: #334155; padding: 10px; border-radius: 8px; margin: 8px 0; }
        .bot-msg { background: #0f4c75; padding: 10px; border-radius: 8px; margin: 8px 0; }
        input[type="text"] { width: 70%; padding: 10px; background: #334155; border: none; color: white; border-radius: 4px; }
        button { padding: 10px 20px; background: #38bdf8; color: #0f172a; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TechPath Document Chat</h1>
        <div class="upload-area">
            <input type="file" id="fileInput" accept=".pdf,.txt">
            <button onclick="uploadFile()">Upload</button>
            <span id="uploadStatus"></span>
        </div>
        <div class="chat-box" id="chatBox"></div>
        <div style="margin-top: 10px">
            <input type="text" id="questionInput" placeholder="Ask a question about the document...">
            <button onclick="askQuestion()">Send</button>
        </div>
    </div>
</body>
</html>
```

---

## Handling Multiple File Types

| File Type | Loader | What to Install |
|-----------|--------|-----------------|
| PDF | `PyPDFLoader` | `pip install pypdf` |
| Text | `TextLoader` | Built-in |
| Word (.docx) | `Docx2txtLoader` | `pip install docx2txt` |
| CSV | `CSVLoader` | Built-in |
| Markdown | `TextLoader` | Built-in |

```python
def get_loader(file_path: str):
    """Pick the right loader based on file extension."""
    ext = file_path.split(".")[-1].lower()
    loaders = {
        "pdf": PyPDFLoader,
        "txt": TextLoader,
        "csv": CSVLoader,
        "docx": Docx2txtLoader,
        "md": TextLoader,
    }
    loader_class = loaders.get(ext)
    if not loader_class:
        raise ValueError(f"Unsupported file type: .{ext}")
    return loader_class(file_path)
```

---

## Improving Answer Quality

| Technique | How | When to Use |
|-----------|-----|-------------|
| Increase k (retrieve more chunks) | `k=5` instead of `k=3` | Answers are incomplete |
| Reduce chunk size | `chunk_size=300` | Answers include irrelevant info |
| Add overlap | `chunk_overlap=100` | Context is lost at boundaries |
| Better prompt | Add "be specific" or "include numbers" | Answers are too vague |
| MMR retrieval | `search_type="mmr"` | Results are too similar |

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Document Q&A | Upload a file, ask questions, get answers from the content |
| Upload flow | Load file -> split into chunks -> embed -> store in vector DB |
| Query flow | Question -> search vector DB -> get chunks -> LLM generates answer |
| Sources | Include page numbers and previews so users can verify |
| Streaming | Use SSE for word-by-word response display |
| Multiple formats | Use different loaders for PDF, DOCX, CSV, TXT |

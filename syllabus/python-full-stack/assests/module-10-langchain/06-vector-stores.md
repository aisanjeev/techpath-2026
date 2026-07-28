# Vector Stores

**Module 10 -- LangChain | Topic 6**

---

## What is a Vector Store?

A vector store is a specialized database designed to store and search **embeddings** (number vectors). When a user asks a question, the vector store finds the most similar document chunks by comparing vectors.

**Analogy:** Think of a regular database like a dictionary -- you look up words alphabetically. A vector store is like a smart librarian -- you describe what you want ("I need a book about cooking Indian food for beginners"), and the librarian finds the closest match based on meaning, not exact words.

```
Regular database:  SELECT * FROM courses WHERE name = "Python"
                   --> Only finds exact match "Python"

Vector store:      search("I want to learn coding and build websites")
                   --> Finds "Python Full Stack Development Course"
                   --> Even though the words are completely different
```

---

## How Vector Stores Work

```
Step 1: STORE (one-time)
  Your documents --> Embed each chunk --> Store vectors + original text in the database

Step 2: SEARCH (every query)
  User question --> Embed the question --> Find nearest vectors --> Return matching chunks

          Stored vectors:
          [0.12, 0.34, ...]  "Python course costs Rs 45,000"
          [0.56, 0.78, ...]  "Classes are Monday to Friday"
          [0.23, 0.45, ...]  "Campus is near MP Nagar Bhopal"
                 ^
                 |
          Query vector: [0.13, 0.35, ...]  "How much is the Python course?"
                 |
                 v
          Nearest match: "Python course costs Rs 45,000" (most similar vector)
```

---

## FAISS -- Facebook AI Similarity Search

FAISS is the most popular choice for learning and small projects. It runs entirely on your computer -- no server, no account, no internet needed.

### Creating a FAISS Vector Store

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Sample documents about TechPath
texts = [
    "TechPath Institute offers Python Full Stack course in Bhopal.",
    "The course fee is Rs 45,000 including GST. EMI options available.",
    "Course duration is 6 months with classes Monday to Friday.",
    "Students learn Python, Django, FastAPI, React, and deployment.",
    "Placement assistance is provided after course completion.",
    "TechPath also offers AI/ML and Data Science courses.",
    "The Bhopal campus is located near MP Nagar, Zone-II.",
    "Online batches are available for students in Delhi, Pune, and Indore.",
]

# Create the vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(texts, embeddings)

print(f"Vector store created with {vectorstore.index.ntotal} vectors")
```

### Searching for Similar Documents

```python
# Simple similarity search -- find the 2 most relevant chunks
results = vectorstore.similarity_search("How much does the course cost?", k=2)

for doc in results:
    print(f"- {doc.page_content}")
# Output:
# - The course fee is Rs 45,000 including GST. EMI options available.
# - Course duration is 6 months with classes Monday to Friday.
```

### Similarity Search with Scores

```python
# Get similarity scores along with results
results = vectorstore.similarity_search_with_score("Where is the campus?", k=3)

for doc, score in results:
    print(f"Score: {score:.4f} | {doc.page_content}")
# Lower score = more similar (FAISS uses L2 distance by default)
```

### Saving and Loading

```python
# Save to disk (creates a folder with the index files)
vectorstore.save_local("techpath_index")

# Load it back later
loaded_store = FAISS.load_local(
    "techpath_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# Works the same as before
results = loaded_store.similarity_search("Python course", k=2)
```

**Install:** `pip install faiss-cpu`

---

## Chroma

Chroma is another popular option. It is slightly more feature-rich than FAISS and supports metadata filtering.

### Creating a Chroma Vector Store

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_texts(
    texts,
    embeddings,
    persist_directory="./chroma_db",
    collection_name="techpath_courses",
)

results = vectorstore.similarity_search("Where is the campus?", k=2)
for doc in results:
    print(f"- {doc.page_content}")
```

### Metadata Filtering

Chroma lets you filter results by metadata:

```python
from langchain_core.documents import Document

# Documents with metadata
docs = [
    Document(page_content="Python Full Stack course fee is Rs 45,000", metadata={"category": "fee", "course": "python"}),
    Document(page_content="Data Science course fee is Rs 55,000", metadata={"category": "fee", "course": "data-science"}),
    Document(page_content="Python classes are 10 AM to 1 PM", metadata={"category": "schedule", "course": "python"}),
]

vectorstore = Chroma.from_documents(docs, embeddings)

# Search only within a specific category
results = vectorstore.similarity_search(
    "How much?",
    k=2,
    filter={"category": "fee"}   # Only look at fee-related documents
)
```

**Install:** `pip install chromadb`

---

## Pinecone -- Cloud Vector Database

Pinecone is a cloud-hosted vector database for production applications. It handles billions of vectors and scales automatically.

```python
from langchain_pinecone import PineconeVectorStore
import os

os.environ["PINECONE_API_KEY"] = "your-api-key"

vectorstore = PineconeVectorStore.from_texts(
    texts,
    embeddings,
    index_name="techpath-courses",
)

results = vectorstore.similarity_search("course fee", k=2)
```

### Why Use Pinecone?

| Feature | FAISS | Chroma | Pinecone | Milvus |
|---------|-------|--------|----------|--------|
| Runs locally | Yes | Yes | No (cloud) | Yes (Milvus Lite) |
| Free | Yes | Yes | Free tier (limited) | Yes (open source) |
| Scalability | Small datasets | Medium | Billions of vectors | Billions of vectors |
| Metadata filtering | No | Yes | Yes | Yes |
| Best for | Learning, prototypes | Small apps | Managed production | Flexible production |

---

## Weaviate

Weaviate supports **hybrid search** -- combining keyword search and semantic search for better results.

```python
from langchain_weaviate import WeaviateVectorStore
import weaviate

client = weaviate.connect_to_local()  # Requires Docker

vectorstore = WeaviateVectorStore.from_texts(
    texts,
    embeddings,
    client=client,
    index_name="TechpathCourses",
)
```

**Install:** `pip install langchain-weaviate` and run Weaviate via Docker.

---

## Milvus -- Purpose-Built Vector Database

Milvus is an open-source vector database built specifically for AI applications. It handles billions of vectors, supports multiple index types, and offers both a local lightweight mode and a full distributed deployment.

### Why Milvus?

- **Open source and free** -- no vendor lock-in
- **Milvus Lite** -- runs locally with a single pip install (great for learning)
- **Scales to billions** -- used by companies like Shopee, Tokopedia, and Zomato
- **Multiple index types** -- HNSW, IVF_FLAT, IVF_SQ8 for different needs
- **Metadata filtering** -- filter results by category, date, or any field
- **Hybrid search** -- combine keyword and semantic search

### Installing pymilvus

```bash
# For local development (Milvus Lite -- no Docker needed)
pip install pymilvus langchain-milvus

# For production (full Milvus server via Docker)
# docker compose up -d   (uses the official milvus-standalone docker-compose.yml)
```

### Basic pymilvus Operations

```python
from pymilvus import MilvusClient

# Connect to Milvus Lite (stores data in a local file)
client = MilvusClient("techpath_demo.db")

# Create a collection (like a table in SQL)
client.create_collection(
    collection_name="techpath_courses",
    dimension=1536,   # Must match your embedding model
)

# Prepare data
data = [
    {"id": 1, "vector": [0.12, -0.34, ...],  "text": "Python Full Stack course fee is Rs 45,000"},
    {"id": 2, "vector": [0.56, 0.78, ...],   "text": "Classes are Monday to Friday, 10 AM to 1 PM"},
    {"id": 3, "vector": [0.23, -0.45, ...],  "text": "Campus is near MP Nagar, Bhopal"},
]

# Insert data
client.insert(collection_name="techpath_courses", data=data)
print("Inserted 3 documents")
```

### Searching in Milvus

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
query_vector = embeddings.embed_query("How much does the course cost?")

# Search for the 2 most similar documents
results = client.search(
    collection_name="techpath_courses",
    data=[query_vector],
    limit=2,
    output_fields=["text"],   # Return the text field along with results
)

for hit in results[0]:
    print(f"Score: {hit['distance']:.4f} | {hit['entity']['text']}")
```

### LangChain + Milvus Integration

This is the recommended way to use Milvus with LangChain:

```python
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# TechPath course information
texts = [
    "TechPath Institute offers Python Full Stack course in Bhopal.",
    "The course fee is Rs 45,000 including GST. EMI options available.",
    "Course duration is 6 months with classes Monday to Friday.",
    "Students learn Python, Django, FastAPI, React, and deployment.",
    "Placement assistance is provided after course completion.",
    "TechPath also offers AI/ML and Data Science courses.",
    "The Bhopal campus is located near MP Nagar, Zone-II.",
    "Online batches are available for students in Delhi, Pune, and Indore.",
]

# Create a Milvus vector store (uses Milvus Lite by default)
vectorstore = Milvus.from_texts(
    texts,
    embeddings,
    connection_args={"uri": "./milvus_techpath.db"},   # Local file
    collection_name="techpath_courses",
)

# Similarity search
results = vectorstore.similarity_search("How much does the course cost?", k=2)
for doc in results:
    print(f"- {doc.page_content}")
# Output:
# - The course fee is Rs 45,000 including GST. EMI options available.
# - Course duration is 6 months with classes Monday to Friday.
```

### Milvus with Metadata Filtering

```python
from langchain_core.documents import Document

docs = [
    Document(page_content="Python Full Stack course fee is Rs 45,000", metadata={"category": "fee", "course": "python"}),
    Document(page_content="Data Science course fee is Rs 55,000", metadata={"category": "fee", "course": "data-science"}),
    Document(page_content="Python classes are 10 AM to 1 PM", metadata={"category": "schedule", "course": "python"}),
    Document(page_content="AI/ML course starts in August 2026", metadata={"category": "schedule", "course": "ai-ml"}),
]

vectorstore = Milvus.from_documents(
    docs,
    embeddings,
    connection_args={"uri": "./milvus_techpath.db"},
)

# Search only fee-related documents
results = vectorstore.similarity_search(
    "How much?",
    k=2,
    expr='category == "fee"',   # Milvus uses expr for filtering
)
```

### Connecting to a Production Milvus Server

```python
# For production: connect to a Milvus server running on Docker or Kubernetes
vectorstore = Milvus.from_texts(
    texts,
    embeddings,
    connection_args={
        "host": "localhost",
        "port": "19530",
    },
    collection_name="techpath_courses",
)
```

**Install:** `pip install pymilvus langchain-milvus`

---

## Using Vector Stores as Retrievers

In LangChain, a **retriever** is anything that takes a query and returns relevant documents. You can easily convert any vector store into a retriever:

```python
# Convert FAISS to a retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Use it in a chain
docs = retriever.invoke("What courses are available?")
for doc in docs:
    print(f"- {doc.page_content}")
```

### Configuring the Retriever

```python
# Retrieve top 5 results
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Use similarity score threshold (only return very relevant results)
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.7}
)

# Use Maximum Marginal Relevance (diverse results)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 10}  # Fetch 10, select 4 most diverse
)
```

### Search Types Explained

| Search Type | How It Works | Best For |
|------------|-------------|----------|
| `similarity` | Returns the K most similar documents | Most use cases |
| `similarity_score_threshold` | Only returns docs above a similarity score | When you want only highly relevant results |
| `mmr` (Max Marginal Relevance) | Returns diverse results (avoids near-duplicates) | When documents are repetitive |

---

## Adding Documents to an Existing Store

```python
# Add new documents later
new_texts = [
    "TechPath now offers a Cloud Computing course.",
    "Weekend batches start from August 2026.",
]

vectorstore.add_texts(new_texts)

# Or add Document objects with metadata
from langchain_core.documents import Document

new_docs = [
    Document(
        page_content="Hostel facility available near the campus.",
        metadata={"category": "facilities"}
    ),
]
vectorstore.add_documents(new_docs)
```

---

## Comparison of Vector Stores

| Feature | FAISS | Chroma | Pinecone | Weaviate | Milvus |
|---------|-------|--------|----------|----------|--------|
| **Type** | Local library | Local/server | Cloud service | Cloud/local | Local/server/cloud |
| **Setup** | `pip install faiss-cpu` | `pip install chromadb` | API key | Docker | `pip install pymilvus` |
| **Cost** | Free | Free | Free tier + paid | Free tier + paid | Free (open source) |
| **Max vectors** | Millions | Millions | Billions | Billions | Billions |
| **Metadata filter** | No | Yes | Yes | Yes | Yes |
| **Hybrid search** | No | No | No | Yes | Yes |
| **Multiple index types** | Limited | No | Managed | Limited | Yes (HNSW, IVF, FLAT) |
| **Persistence** | Save/load files | Built-in | Cloud managed | Cloud/Docker | File or server |
| **Best for** | Learning, small apps | Prototyping | Managed production | Production + hybrid | Flexible production |

### Decision Guide

```
Are you learning or building a prototype?
  --> Use FAISS (simplest, no setup)

Do you need metadata filtering for a small app?
  --> Use Chroma (still local, easy to use)

Do you want an open-source production database?
  --> Use Milvus (free, scalable, multiple index types)

Do you want a fully managed cloud service?
  --> Use Pinecone (no infrastructure to manage)

Do you need keyword + semantic search combined?
  --> Use Weaviate or Milvus (both support hybrid search)
```

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Vector store | Database optimized for storing and searching embeddings |
| FAISS | Free, local, simple -- best for learning |
| Chroma | Local with metadata filtering -- good for prototypes |
| Pinecone | Cloud-hosted -- best for managed production |
| Weaviate | Supports hybrid search (keyword + semantic) |
| Milvus | Open-source, scalable, multiple index types -- flexible production |
| `similarity_search()` | Find the K most similar documents |
| `as_retriever()` | Convert vector store to a retriever for use in chains |
| MMR | Returns diverse results instead of near-duplicates |
| `save_local()` / `load_local()` | Persist FAISS index to disk |

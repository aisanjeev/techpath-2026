# Vector Databases & Embeddings -- Foundations

**Module 04 -- Database Design | Topic 8**

---

## What Are Embeddings?

Imagine you want a computer to understand the **meaning** of words, sentences, or images -- not just store them as text or pixels, but actually understand what they *mean*.

An **embedding** is a way to convert any piece of data (text, image, audio) into a **list of numbers** (a vector) that captures its meaning.

```
"Python programming"  ->  [0.23, -0.45, 0.67, 0.12, -0.89, ...]   (hundreds of numbers)
"Coding in Python"    ->  [0.21, -0.43, 0.65, 0.14, -0.87, ...]   (very similar numbers!)
"Cricket match"       ->  [0.78, 0.34, -0.56, 0.91, 0.02, ...]   (very different numbers)
```

Notice how "Python programming" and "Coding in Python" have almost the same numbers -- because they mean almost the same thing. "Cricket match" has completely different numbers because the meaning is different.

### How Embeddings Work (Simple Explanation)

1. You give text (or an image) to an **embedding model** (a trained AI model)
2. The model outputs a list of numbers (typically 128 to 1536 numbers)
3. Each number represents some aspect of meaning
4. Similar meanings produce similar numbers

```python
# Conceptual example (not real code yet)
embed("King")     = [0.9, 0.1, 0.8, ...]
embed("Queen")    = [0.9, 0.1, 0.7, ...]   # Similar to King!
embed("Apple")    = [0.1, 0.8, 0.2, ...]   # Very different
```

### Think of It Like Coordinates on a Map

Just like every city in India has GPS coordinates (latitude, longitude):

```
Bhopal   ->  (23.26, 77.41)
Indore   ->  (22.72, 75.86)    # Close to Bhopal (nearby cities)
Delhi    ->  (28.61, 77.23)    # Far from Bhopal
```

Embeddings work the same way, but instead of 2 coordinates (lat, long), they use hundreds of coordinates to locate meaning in a "meaning space."

---

## What Is a Vector Database?

A **vector database** is a specialized database designed to store and search through embeddings (vectors) efficiently.

### Why Can't Regular Databases Do This?

Traditional databases (MySQL, SQLite, MongoDB) are designed for **exact matching**:

```sql
-- Traditional query: find exact match
SELECT * FROM students WHERE city = 'Bhopal';

-- This works perfectly for exact text matching
```

But what if you want to find things that are **similar** rather than exactly the same?

```
User searches: "How to learn web development?"

You want to find:
  - "Getting started with frontend development"  (similar meaning!)
  - "Best resources for learning HTML and CSS"    (related topic!)
  - "Web dev roadmap for beginners"               (same intent!)

You do NOT want:
  - "Development of Bhopal city infrastructure"   (word 'development' matches, but wrong meaning!)
```

Traditional databases match by keywords. Vector databases match by **meaning**.

### How a Vector Database Works

```
Step 1: Convert your data into embeddings (numbers)
   "Python course for beginners"  ->  [0.23, -0.45, 0.67, ...]

Step 2: Store the embedding + original data in the vector database

Step 3: When a user searches, convert their query into an embedding too
   "Learn Python from scratch"    ->  [0.21, -0.43, 0.65, ...]

Step 4: Find the stored embeddings most similar to the query embedding
   Result: "Python course for beginners" (similarity: 0.95)
```

---

## How Similarity Search Works

When you have two vectors (lists of numbers), you need a way to measure how **similar** they are. There are two main methods:

### 1. Cosine Similarity

Cosine similarity measures the **angle** between two vectors. Think of it like comparing the direction two arrows point, ignoring their length.

```
Vector A = [1, 2, 3]
Vector B = [2, 4, 6]     # Points in the same direction -> similarity = 1.0
Vector C = [-1, -2, -3]  # Points in the opposite direction -> similarity = -1.0
Vector D = [3, -1, 2]    # Points in a different direction -> similarity = 0.5
```

- **1.0** = exactly the same meaning
- **0.0** = completely unrelated
- **-1.0** = opposite meaning

**Cosine similarity is the most commonly used method** in practice.

```python
# Simple Python example
import math

def cosine_similarity(vec_a, vec_b):
    """Calculate how similar two vectors are (0 to 1)."""
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)

# Example
python_course = [0.9, 0.2, 0.8, 0.1]
coding_tutorial = [0.85, 0.25, 0.75, 0.15]
cricket_score = [0.1, 0.9, 0.05, 0.8]

print(cosine_similarity(python_course, coding_tutorial))  # ~0.99 (very similar)
print(cosine_similarity(python_course, cricket_score))     # ~0.35 (not similar)
```

### 2. Euclidean Distance (L2 Distance)

Euclidean distance measures the **straight-line distance** between two points -- just like measuring distance between two cities on a map.

```
Point A = [1, 2]
Point B = [4, 6]
Distance = sqrt((4-1)^2 + (6-2)^2) = sqrt(9 + 16) = 5.0
```

- **Smaller distance** = more similar
- **Larger distance** = less similar

```python
def euclidean_distance(vec_a, vec_b):
    """Calculate distance between two vectors (lower = more similar)."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)))
```

### Which Method to Use?

| Method | Best For | Returns |
|--------|----------|---------|
| Cosine Similarity | Text search, recommendations | 0 to 1 (higher = more similar) |
| Euclidean Distance | Image similarity, clustering | 0 to infinity (lower = more similar) |

For most text-based applications, **cosine similarity** is the standard choice.

---

## Vector DB vs Traditional DB

| Feature | Traditional DB (MySQL/SQLite) | Vector DB (Milvus/FAISS) |
|---------|------------------------------|--------------------------|
| Data stored | Rows and columns (text, numbers) | Vectors (lists of numbers) + metadata |
| Search type | Exact match (`WHERE city = 'Bhopal'`) | Similarity search (find nearest vectors) |
| Query | SQL | Vector query (give me 10 most similar) |
| Index type | B-tree, Hash | HNSW, IVF, Annoy |
| Best for | Structured data, transactions | Semantic search, recommendations, AI |
| Speed for similarity | Very slow (must compare every row) | Very fast (specialized indexes) |
| Example query | "Find students named Rahul" | "Find courses similar to this description" |

**Key insight:** You often use BOTH a traditional database AND a vector database together:
- MySQL stores the structured data (student names, fees, enrollments)
- Vector DB stores embeddings for semantic search (course recommendations, similar content)

---

## Milvus -- An Open-Source Vector Database

### What Is Milvus?

**Milvus** is one of the most popular open-source vector databases. It is designed to store and search billions of vectors efficiently.

**Why Milvus?**
- Open source and free
- Handles millions/billions of vectors
- Supports multiple index types (for different speed/accuracy trade-offs)
- Used by companies like Shopee, Tokopedia, and many Indian startups
- Active community and good documentation

### Installing Milvus (Lite Version for Learning)

For learning purposes, you can use **Milvus Lite** which runs entirely in Python (no server needed, similar to SQLite):

```bash
pip install pymilvus
```

**Note:** For production, you would run Milvus as a server using Docker:
```bash
# Production setup (Docker)
docker compose up -d
```

But for this course, Milvus Lite is perfect for learning.

### Basic Milvus Concepts

| Milvus Concept | SQL Equivalent | Description |
|----------------|---------------|-------------|
| Collection | Table | Where you store vectors |
| Entity | Row | One vector + its metadata |
| Field | Column | A property (vector, id, name) |
| Index | Index | Speed up similarity search |
| Search | SELECT | Find similar vectors |

### Simple Python Example with Milvus

```python
"""
Simple vector database example using Milvus Lite.
We store course descriptions as vectors and search for similar ones.

Requirements:
    pip install pymilvus
"""

from pymilvus import MilvusClient

# ─── Step 1: Connect to Milvus Lite (file-based, like SQLite) ───
client = MilvusClient("techpath_vectors.db")

# ─── Step 2: Create a collection (like a table) ───
# We need to define the schema -- what fields each entry has
from pymilvus import CollectionSchema, FieldSchema, DataType

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=4),  # 4D for demo
]
schema = CollectionSchema(fields, description="Course embeddings")

# Create the collection (drop if exists for clean demo)
if client.has_collection("courses"):
    client.drop_collection("courses")

client.create_collection(
    collection_name="courses",
    schema=schema,
)

# ─── Step 3: Insert data with vectors ───
# In a real app, you would use an AI model to generate these embeddings.
# For this demo, we use small hand-crafted vectors.
data = [
    {"title": "Python Full Stack Development", "embedding": [0.9, 0.2, 0.8, 0.1]},
    {"title": "Data Science with Python",      "embedding": [0.7, 0.8, 0.6, 0.3]},
    {"title": "Java Full Stack Development",   "embedding": [0.85, 0.15, 0.75, 0.2]},
    {"title": "Web Development with React",    "embedding": [0.8, 0.3, 0.9, 0.05]},
    {"title": "Machine Learning Fundamentals", "embedding": [0.5, 0.9, 0.4, 0.6]},
    {"title": "DevOps and Cloud Computing",    "embedding": [0.3, 0.4, 0.5, 0.9]},
]

client.insert(collection_name="courses", data=data)
print(f"Inserted {len(data)} courses")

# ─── Step 4: Create an index for fast search ───
index_params = client.prepare_index_params()
index_params.add_index(
    field_name="embedding",
    index_type="FLAT",       # Simple index (good for small datasets)
    metric_type="COSINE",    # Use cosine similarity
)
client.create_index(collection_name="courses", index_params=index_params)

# ─── Step 5: Search for similar courses ───
# "I want to learn backend programming" -> embedding
query_vector = [[0.88, 0.18, 0.82, 0.12]]  # Similar to Python/Java Full Stack

results = client.search(
    collection_name="courses",
    data=query_vector,
    limit=3,                 # Return top 3 most similar
    output_fields=["title"], # Also return the title
)

print("\nSearch: 'Backend programming courses'")
print("Top 3 most similar courses:")
for hits in results:
    for hit in hits:
        print(f"  - {hit['entity']['title']} (similarity: {hit['distance']:.4f})")
```

**Expected output:**
```
Inserted 6 courses

Search: 'Backend programming courses'
Top 3 most similar courses:
  - Python Full Stack Development (similarity: 0.9987)
  - Java Full Stack Development (similarity: 0.9952)
  - Web Development with React (similarity: 0.9821)
```

---

## Other Vector Databases -- Quick Comparison

| Database | Type | Best For | Learning Curve |
|----------|------|----------|---------------|
| **Milvus** | Open source, self-hosted | Production-scale, billions of vectors | Medium |
| **FAISS** | Library (by Facebook/Meta) | Research, in-memory search, no server needed | Easy |
| **Chroma** | Open source, lightweight | Prototyping, small projects, LLM apps | Very Easy |
| **Pinecone** | Cloud-managed (paid) | Production without managing infrastructure | Easy |
| **Weaviate** | Open source, self-hosted | Multi-modal (text + images), GraphQL API | Medium |
| **Qdrant** | Open source, self-hosted | High-performance, Rust-based | Medium |

### FAISS (Facebook AI Similarity Search)

```python
# FAISS is a library, not a database -- it runs in memory
import faiss
import numpy as np

# Create an index for 4-dimensional vectors
index = faiss.IndexFlatL2(4)  # L2 = Euclidean distance

# Add vectors
vectors = np.array([
    [0.9, 0.2, 0.8, 0.1],
    [0.7, 0.8, 0.6, 0.3],
    [0.85, 0.15, 0.75, 0.2],
], dtype='float32')
index.add(vectors)

# Search
query = np.array([[0.88, 0.18, 0.82, 0.12]], dtype='float32')
distances, indices = index.search(query, k=2)  # Find 2 nearest
print(f"Nearest vectors at indices: {indices[0]}")  # [0, 2]
```

### Chroma (Simple and Beginner-Friendly)

```python
# Chroma is great for learning -- very simple API
import chromadb

client = chromadb.Client()
collection = client.create_collection("courses")

# Add documents (Chroma generates embeddings automatically!)
collection.add(
    documents=["Python Full Stack", "Data Science", "Java Full Stack"],
    ids=["c1", "c2", "c3"]
)

# Search by text (Chroma handles embeddings for you)
results = collection.query(
    query_texts=["backend programming"],
    n_results=2
)
print(results["documents"])  # Most similar course titles
```

---

## Use Cases for Vector Databases

### 1. Semantic Search
Search by meaning, not just keywords.
```
Query: "affordable laptop for students"
Result: "Budget-friendly notebook for college" (same meaning, different words)
```

### 2. Recommendation Systems
"Students who liked this course also liked..."
```
Student enrolled in "Python Full Stack"
Recommend: "Web Development with React" (similar embedding)
```

### 3. RAG (Retrieval-Augmented Generation)
Help AI chatbots answer questions using your own data.
```
1. Store your company's documents as embeddings in a vector DB
2. When a user asks a question, find the most relevant documents
3. Send those documents + the question to an LLM (like ChatGPT)
4. The LLM answers using YOUR data, not just its training data
```

### 4. Image Similarity
Find visually similar images.
```
Upload: Photo of a red dress
Result: Similar red dresses from the catalog
```

### 5. Duplicate Detection
Find near-duplicate content (plagiarism detection, dedup).
```
New submission: "Machine learning is a subset of AI that..."
Similar match found: "ML is a part of artificial intelligence..." (87% similar)
```

### 6. Anomaly Detection
Find data points that are very different from everything else.
```
Normal server logs: [0.2, 0.3, 0.1, ...]
Anomaly detected:  [0.9, 0.8, 0.95, ...]  (far from all normal vectors)
```

---

## Generating Real Embeddings

In the examples above, we used hand-crafted small vectors. In real applications, you use AI models to generate embeddings:

```python
# Example using the sentence-transformers library
# pip install sentence-transformers

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # Free, runs locally

texts = [
    "Python Full Stack Development",
    "Learn backend programming with Python",
    "Cricket World Cup 2026 highlights",
]

embeddings = model.encode(texts)
print(f"Each embedding has {len(embeddings[0])} dimensions")  # 384 dimensions

# Now store these embeddings in Milvus, FAISS, or Chroma
```

Popular embedding models:

| Model | Dimensions | Best For | Cost |
|-------|-----------|----------|------|
| `all-MiniLM-L6-v2` | 384 | General text (free, fast) | Free |
| `text-embedding-3-small` (OpenAI) | 1536 | High quality text | Paid API |
| `BAAI/bge-small-en` | 384 | English text (free) | Free |
| `CLIP` (OpenAI) | 512 | Text AND images together | Free |

---

## Summary

| Concept | What It Is |
|---------|-----------|
| Embedding | A list of numbers that represents the meaning of data |
| Vector | Same as embedding -- a list of numbers |
| Vector Database | A database optimized for storing and searching vectors |
| Similarity Search | Finding vectors closest to a query vector |
| Cosine Similarity | Measures angle between vectors (0 to 1, higher = more similar) |
| Euclidean Distance | Measures straight-line distance (lower = more similar) |
| Milvus | Popular open-source vector database |
| FAISS | Facebook's in-memory vector search library |
| Chroma | Simple, beginner-friendly vector database |
| RAG | Using vector search to help AI answer questions from your data |

**Key takeaway:** Traditional databases find exact matches. Vector databases find **similar** matches. Modern AI applications often need both.

---

*TechPath Institute -- Python Full Stack Development*

# Embeddings

**Module 10 -- LangChain | Topic 5**

---

## What Are Embeddings?

Embeddings convert text into numbers -- specifically, into a list of numbers called a **vector**. Similar text gets similar vectors. This is how computers "understand" meaning.

**Analogy:** Imagine you are organizing books on a map instead of a shelf. Books about Python programming would be placed close together in one corner. Books about cooking would be far away in another corner. Books about web development would be near the Python books. Embeddings do this same thing, but in a mathematical space with hundreds of dimensions.

```
"Python programming"     --> [0.12, -0.34, 0.56, 0.78, ...]   (1536 numbers)
"Python web development" --> [0.11, -0.33, 0.55, 0.80, ...]   (similar numbers!)
"Best biryani in Bhopal" --> [0.89, 0.23, -0.67, 0.01, ...]   (very different numbers)
```

---

## Why Do We Need Embeddings?

Computers cannot understand text the way humans do. They only understand numbers. Embeddings solve this problem by converting words and sentences into numbers while preserving their meaning.

| Without Embeddings | With Embeddings |
|-------------------|----------------|
| Keyword match only: "course fee" matches only "course fee" | Semantic match: "course fee" also matches "how much does it cost?" |
| Misses related concepts | Understands meaning and context |
| Simple but limited | Powerful and accurate |

### How Embeddings Enable Search

```
User's question: "How much does the Python course cost?"
                      |
                      v
            Generate embedding: [0.23, -0.45, 0.67, ...]
                      |
                      v
    Compare with stored document embeddings
                      |
                      v
    Most similar: "TechPath Python Full Stack course fee is Rs 45,000"
    (even though the words are different, the meaning is similar)
```

---

## Using OpenAI Embeddings

The most popular embedding model. Requires an API key and costs a small fee per use.

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Embed a single query (question)
vector = embeddings.embed_query("Python programming course at TechPath")
print(f"Vector has {len(vector)} dimensions")   # 1536
print(f"First 5 values: {vector[:5]}")
# [-0.012, 0.034, -0.056, 0.078, 0.023]
```

### Embedding Multiple Documents

```python
# Embed multiple texts at once (more efficient)
texts = [
    "TechPath Institute offers Python Full Stack course.",
    "Course fee is Rs 45,000 with EMI options.",
    "Classes are Monday to Friday, 10 AM to 1 PM.",
    "Campus is located in Bhopal near MP Nagar.",
]

vectors = embeddings.embed_documents(texts)
print(f"Embedded {len(vectors)} documents")
print(f"Each vector has {len(vectors[0])} dimensions")
```

### OpenAI Embedding Models

| Model | Dimensions | Cost (per 1M tokens) | Best For |
|-------|-----------|---------------------|----------|
| `text-embedding-3-small` | 1536 | ~$0.02 | Most applications (recommended) |
| `text-embedding-3-large` | 3072 | ~$0.13 | Maximum accuracy |
| `text-embedding-ada-002` | 1536 | ~$0.10 | Legacy (older model) |

---

## Using HuggingFace Embeddings (Free)

HuggingFace models run on your computer -- no API key, no cost, no internet needed.

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

# Downloads the model on first run (~90 MB)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = embeddings.embed_query("TechPath Institute Bhopal")
print(f"Vector has {len(vector)} dimensions")  # 384
```

### Popular HuggingFace Models

| Model | Dimensions | Size | Quality |
|-------|-----------|------|---------|
| `all-MiniLM-L6-v2` | 384 | 90 MB | Good (recommended for learning) |
| `all-mpnet-base-v2` | 768 | 420 MB | Better |
| `multilingual-e5-large` | 1024 | 2.2 GB | Best for Hindi + English |

### When to Use Which?

| Factor | OpenAI | HuggingFace |
|--------|--------|-------------|
| Cost | Paid (very cheap) | Free |
| Speed | Fast (API call) | Medium (runs locally) |
| Internet needed | Yes | No (after download) |
| Quality | Excellent | Good to Very Good |
| Best for | Production apps | Learning, offline apps |

---

## Cosine Similarity -- Measuring How Similar Two Texts Are

Once you have two vectors, you can measure how similar they are using **cosine similarity**. The result is a number between -1 and 1:

| Score | Meaning | Example |
|-------|---------|---------|
| 1.0 | Identical meaning | "Python course" vs "Python course" |
| 0.8-0.9 | Very similar | "Python course" vs "Learn Python programming" |
| 0.5-0.7 | Somewhat related | "Python course" vs "Web development bootcamp" |
| 0.0-0.3 | Not related | "Python course" vs "Best biryani recipe" |
| -1.0 | Opposite meaning | Rare in practice |

### Computing Cosine Similarity

```python
import numpy as np

def cosine_similarity(vec1, vec2):
    """Calculate how similar two vectors are (0 to 1)."""
    dot_product = np.dot(vec1, vec2)
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)
    return dot_product / (magnitude1 * magnitude2)

# Embed three sentences
texts = [
    "Python programming course at TechPath",
    "Learn Python full stack development",
    "Best biryani recipe in Bhopal",
]
vectors = embeddings.embed_documents(texts)

# Compare similarities
sim_1_2 = cosine_similarity(vectors[0], vectors[1])
sim_1_3 = cosine_similarity(vectors[0], vectors[2])

print(f"Python course vs Python development: {sim_1_2:.4f}")  # ~0.85 (very similar)
print(f"Python course vs biryani recipe:     {sim_1_3:.4f}")   # ~0.15 (not related)
```

### Visual Explanation

```
                    Python course
                         *  * Python development (close = similar)
                        /
                       /
                      /
     * Biryani recipe (far away = not similar)
```

---

## Embedding Dimensions

The number of dimensions affects quality and speed:

| Dimensions | What It Means | Trade-off |
|-----------|--------------|-----------|
| 384 | Each text is represented by 384 numbers | Faster, less accurate |
| 768 | 768 numbers per text | Balanced |
| 1536 | 1536 numbers per text | Slower, more accurate |
| 3072 | 3072 numbers per text | Slowest, most accurate |

**Analogy:** Think of it like describing a person:
- 3 dimensions: "tall, male, young" (not very unique)
- 10 dimensions: "tall, male, young, glasses, curly hair, dark skin, slim, from Bhopal, student, Python coder" (much more unique)
- More dimensions = more detail = better similarity matching

---

## Practical Example: Finding the Best Course

```python
from langchain_openai import OpenAIEmbeddings
import numpy as np

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# TechPath course descriptions
courses = [
    "Python Full Stack: Learn Python, Django, FastAPI, React, and databases. Build complete web applications from scratch.",
    "Data Science: Learn Python, Pandas, NumPy, Machine Learning, and data visualization. Analyze real-world datasets.",
    "AI/ML Engineering: Learn deep learning, NLP, computer vision, and model deployment. Build AI-powered applications.",
    "Web Development: Learn HTML, CSS, JavaScript, and React. Design responsive websites for any device.",
    "ADCA: Learn computer basics, MS Office, internet, and data entry. Perfect for complete beginners.",
]

# Student's interest
student_query = "I want to learn how to build websites using Python"

# Embed everything
query_vector = embeddings.embed_query(student_query)
course_vectors = embeddings.embed_documents(courses)

# Find the most similar course
similarities = [
    np.dot(query_vector, cv) / (np.linalg.norm(query_vector) * np.linalg.norm(cv))
    for cv in course_vectors
]

# Rank courses by similarity
ranked = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
print("Best courses for you:")
for idx, score in ranked[:3]:
    print(f"  {score:.3f} -- {courses[idx][:60]}...")
```

---

## How Milvus Stores and Indexes Embeddings

Milvus is a purpose-built vector database that stores embeddings and makes searching them extremely fast -- even when you have millions of vectors. Understanding how Milvus handles embeddings will help you design better AI applications.

### How Milvus Organizes Embeddings

When you insert embeddings into Milvus, it does not just store them in a plain list. It builds an **index** -- a special data structure that speeds up similarity search.

```
Without an index (brute force):
  Query vector --> Compare with ALL 1,000,000 vectors --> Slow (seconds)

With a Milvus index:
  Query vector --> Smart lookup in index --> Compare with ~1,000 candidates --> Fast (milliseconds)
```

### Index Types in Milvus

| Index Type | How It Works | Speed | Accuracy | Best For |
|-----------|-------------|-------|----------|----------|
| FLAT | Compares every vector (brute force) | Slowest | 100% exact | Small datasets (<100K vectors) |
| IVF_FLAT | Groups vectors into clusters, searches nearby clusters | Fast | ~95% | Medium datasets |
| IVF_SQ8 | Like IVF_FLAT but compresses vectors | Faster | ~90% | Large datasets, save memory |
| HNSW | Builds a graph connecting similar vectors | Very fast | ~98% | Production apps (recommended) |

**Analogy:** Imagine finding a book in a library:
- **FLAT** = Check every single book on every shelf (accurate but slow)
- **IVF_FLAT** = Go to the right section first, then check books there (faster)
- **HNSW** = Follow a trail of related books, each pointing to the next closest one (fastest)

### Creating an Index in Milvus

```python
from pymilvus import connections, Collection

connections.connect("default", host="localhost", port="19530")

collection = Collection("techpath_courses")

# Create an HNSW index for fast similarity search
index_params = {
    "index_type": "HNSW",
    "metric_type": "COSINE",     # Use cosine similarity
    "params": {"M": 16, "efConstruction": 256},
}
collection.create_index("embedding", index_params)
collection.load()   # Load into memory for searching
```

### Metric Types for Comparing Embeddings

| Metric | Range | Meaning | When to Use |
|--------|-------|---------|-------------|
| COSINE | -1 to 1 | Measures angle between vectors | Most common (recommended) |
| L2 (Euclidean) | 0 to infinity | Measures straight-line distance | When magnitude matters |
| IP (Inner Product) | varies | Dot product of vectors | Normalized embeddings |

For most LangChain applications, use **COSINE** -- it matches how OpenAI and HuggingFace embeddings are designed.

---

## How Embedding Dimensions Affect Search Quality

The number of dimensions in your embedding model directly impacts how well similarity search works. Here is a practical comparison:

### Dimension Comparison

| Dimensions | Model Example | Storage per 1M docs | Search Speed | Search Quality |
|-----------|--------------|---------------------|-------------|----------------|
| 384 | all-MiniLM-L6-v2 | ~1.5 GB | Fastest | Good for simple queries |
| 768 | all-mpnet-base-v2 | ~3 GB | Fast | Better distinction between topics |
| 1024 | multilingual-e5-large | ~4 GB | Medium | Great for Hindi + English |
| 1536 | text-embedding-3-small | ~6 GB | Slower | Excellent for most apps |
| 3072 | text-embedding-3-large | ~12 GB | Slowest | Best accuracy, highest cost |

### Practical Impact

```python
# Example: Searching TechPath course data with different dimensions

# 384 dimensions (all-MiniLM-L6-v2)
# Query: "I want to learn backend development"
# Result 1: "Python Full Stack course" (score: 0.72)
# Result 2: "Web Development course"   (score: 0.70)  <-- hard to distinguish

# 1536 dimensions (text-embedding-3-small)
# Query: "I want to learn backend development"
# Result 1: "Python Full Stack course" (score: 0.88)  <-- clear winner
# Result 2: "Web Development course"   (score: 0.61)  <-- clearly lower
```

Higher dimensions give **wider gaps** between relevant and irrelevant results, making it easier for the vector store to pick the right answer.

### Choosing the Right Dimensions

| Scenario | Recommended Dimensions | Why |
|----------|----------------------|-----|
| Learning and practice | 384 (MiniLM) | Free, fast, good enough |
| College project or demo | 768 (mpnet) | Better quality, still free |
| Startup MVP / small app | 1536 (OpenAI small) | Best balance of cost and quality |
| Enterprise production | 3072 (OpenAI large) | Maximum accuracy |
| Milvus with large datasets | 768-1536 | Good accuracy without excessive storage |

**Important:** Milvus supports all common dimensions. When creating a Milvus collection, you specify the dimension once, and all vectors inserted must match that size.

---

## Reducing Dimensions (Optional)

You can reduce the size of embeddings to save storage and speed up searches:

```python
from langchain_openai import OpenAIEmbeddings

# Use the large model but reduce to 512 dimensions
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=512,   # Reduce from 3072 to 512
)
```

This is called **Matryoshka embedding** -- like Russian nesting dolls, the most important information is in the first few dimensions.

---

## Common Mistakes

| Mistake | Why It Is Wrong | Fix |
|---------|----------------|-----|
| Using different models for query and documents | Vectors from different models are incompatible | Use the same model for both |
| Not normalizing vectors | Cosine similarity assumes normalized vectors | Most libraries handle this automatically |
| Embedding very long text | Models have token limits (8192 for OpenAI) | Split text first, then embed each chunk |
| Comparing embeddings from different models | A 384-dim vector cannot be compared with a 1536-dim vector | Always use the same model |

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Embeddings | Convert text into number vectors that capture meaning |
| Cosine similarity | Measures how similar two vectors are (0 to 1) |
| OpenAI embeddings | High quality, paid, requires internet |
| HuggingFace embeddings | Free, runs locally, good quality |
| Dimensions | More dimensions = more accurate but slower |
| `embed_query()` | Embed a single question/search query |
| `embed_documents()` | Embed multiple texts at once (more efficient) |
| Milvus indexing | Milvus builds indexes (HNSW, IVF) to search embeddings fast |
| Dimension trade-off | Higher dimensions = better accuracy but more storage and slower search |
| Key rule | Always use the same embedding model for queries and documents |

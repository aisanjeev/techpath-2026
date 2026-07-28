# Advanced RAG Techniques

**Module 10 -- LangChain | Topic 8**

---

## Why Advanced RAG?

Basic RAG works well for simple questions, but it struggles with:
- Complex questions that need information from multiple places
- Poorly worded questions that do not match the stored documents
- Long documents where many chunks are retrieved but few are relevant

Advanced RAG techniques solve these problems by adding intelligence to the retrieval and generation process.

| Basic RAG | Advanced RAG |
|----------|-------------|
| One search query | Multiple search queries |
| Returns whatever it finds | Filters out irrelevant results |
| Single search method | Combines keyword + semantic search |
| No quality check | Ranks and verifies results |

---

## Multi-Query Retrieval

### The Problem

Sometimes a single query misses relevant documents because the wording does not match.

```
User question:  "Tell me about TechPath fees and duration"

This is really TWO questions:
  1. "What is the course fee?"
  2. "How long is the course?"

A single search might find one but miss the other.
```

### The Solution

Multi-query retrieval generates multiple versions of the question and searches with each one:

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm,
)

# This generates multiple query phrasings internally
docs = multi_retriever.invoke("Tell me about TechPath fees and duration")
```

### How It Works Internally

```
Original question: "Tell me about TechPath fees and duration"
                      |
                      v
              LLM generates variations:
                1. "What is the course fee at TechPath?"
                2. "How long is the TechPath course?"
                3. "What are the pricing and schedule details?"
                      |
                      v
              Each query searches the vector store
                      |
                      v
              Results are combined and deduplicated
                      |
                      v
              Final set of relevant documents
```

**When to use:** When users ask broad or multi-part questions.

---

## Contextual Compression

### The Problem

Retrieved chunks often contain extra information that is not relevant to the question. This wastes tokens and can confuse the LLM.

```
Question: "What is the course fee?"

Retrieved chunk: "TechPath Institute Bhopal was founded in 2020.
We offer Python Full Stack, Data Science, and Web Development courses.
The Python Full Stack course fee is Rs 45,000 including GST.
EMI options are available for 3 and 6 months."

Only the last two sentences are relevant.
```

### The Solution

Contextual compression uses an LLM to extract only the relevant parts:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(ChatOpenAI(model="gpt-4o-mini"))

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(),
)

docs = compression_retriever.invoke("What is the course fee?")
# Returns only the relevant parts:
# "The Python Full Stack course fee is Rs 45,000 including GST.
#  EMI options are available for 3 and 6 months."
```

### Before vs After Compression

| | Without Compression | With Compression |
|-|--------------------|--------------------|
| Chunk size | Full 500 chars | Only relevant sentences |
| Tokens used | More | Fewer (cheaper) |
| Answer quality | May include noise | More focused |
| Speed | Faster retrieval | Slightly slower (extra LLM call) |

**When to use:** When your chunks are large and contain mixed information.

---

## Hybrid Search

### The Problem

Semantic search (embeddings) is great at understanding meaning but can miss exact keywords. Keyword search (BM25) finds exact matches but does not understand meaning.

```
Semantic search for "Rs 45000":
  --> Might find "course pricing and fees" (understands meaning)
  --> Might miss "Rs 45,000" (exact number match)

Keyword search for "Rs 45000":
  --> Finds "Rs 45,000" (exact match)
  --> Misses "course pricing" (different words)
```

### The Solution

Combine both methods with an **Ensemble Retriever**:

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Keyword-based retriever (BM25)
bm25_retriever = BM25Retriever.from_texts(texts)
bm25_retriever.k = 3

# Semantic retriever (embeddings)
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Combine both with weights
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.4, 0.6],   # 40% keyword, 60% semantic
)

docs = hybrid_retriever.invoke("TechPath Bhopal campus Rs 45000")
```

### How Weights Work

| Weight Setting | Behavior |
|---------------|----------|
| `[0.5, 0.5]` | Equal importance to keywords and meaning |
| `[0.3, 0.7]` | Prefer semantic (meaning-based) results |
| `[0.7, 0.3]` | Prefer keyword (exact match) results |

**When to use:** When your data contains specific numbers, names, or codes that semantic search might miss.

**Install:** `pip install rank_bm25`

---

## Reranking

### The Problem

The initial retrieval might return 10 documents, but they are not always in the best order. Document #5 might be more relevant than document #1.

### The Solution

After retrieval, use a **reranker** to reorder the results by relevance:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import CohereRerank

# Step 1: Retrieve more documents than needed
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Step 2: Rerank and keep the best 3
reranker = CohereRerank(top_n=3)

reranking_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever,
)

# Retrieves 10 documents, reranks them, returns top 3
docs = reranking_retriever.invoke("course details and placement info")
```

### How Reranking Works

```
Step 1: Retrieve 10 documents (fast, approximate)
  [Doc A (score 0.82)]
  [Doc B (score 0.79)]
  [Doc C (score 0.75)]
  ... (7 more)

Step 2: Reranker scores each document against the question (slower, accurate)
  [Doc C (rerank score 0.95)]  <-- moved to #1
  [Doc A (rerank score 0.88)]
  [Doc F (rerank score 0.85)]  <-- jumped from #6 to #3

Step 3: Return top 3 reranked documents
```

**When to use:** When you need the highest accuracy and can afford a small speed penalty.

---

## Parent Document Retriever

### The Problem

Small chunks are great for precise search but lose context. Large chunks have context but are less precise.

### The Solution

Store both! Search with **small chunks** (precise) but return the **parent document** (full context):

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Small chunks for searching
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)

# Large chunks for context
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# Create parent document retriever
store = InMemoryStore()
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# Add documents
retriever.add_documents(pages)

# Search finds small chunks, returns large parent chunks
docs = retriever.invoke("course fee")
```

```
Search:  Small chunk matches: "Fee is Rs 45,000"
Return:  Parent chunk: "TechPath offers Python Full Stack for Rs 45,000.
         Duration is 6 months with Mon-Fri classes. EMI available.
         Placement assistance provided after completion."
```

---

## Self-Query Retriever

Automatically extracts filters from natural language questions:

```python
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

# Define what metadata fields exist
metadata_field_info = [
    AttributeInfo(name="course", description="The course name", type="string"),
    AttributeInfo(name="category", description="Type: fee, schedule, placement", type="string"),
]

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="Information about TechPath Institute courses",
    metadata_field_info=metadata_field_info,
)

# The retriever automatically extracts filters from the question
docs = retriever.invoke("What is the fee for the Python course?")
# Internally: searches for "fee" with filter {"course": "python"}
```

---

## Combining Techniques

In production, you often combine multiple advanced techniques:

```python
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever

# Step 1: Multi-query for better coverage
multi_query = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    llm=llm,
)

# Step 2: Hybrid search for keyword + semantic
hybrid = EnsembleRetriever(
    retrievers=[bm25_retriever, multi_query],
    weights=[0.3, 0.7],
)

# Step 3: Compression to remove noise
final_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=hybrid,
)

# Use in your RAG chain
rag_chain = (
    {"context": final_retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | parser
)
```

---

## When to Use Each Technique

| Technique | Problem It Solves | Cost | Complexity |
|-----------|------------------|------|------------|
| Multi-Query | Broad or multi-part questions | Extra LLM call | Low |
| Contextual Compression | Noisy, large chunks | Extra LLM call | Low |
| Hybrid Search | Missing exact keywords | None (free) | Medium |
| Reranking | Results in wrong order | API call (Cohere) | Low |
| Parent Document | Need both precision and context | More storage | Medium |
| Self-Query | Natural language filters | Extra LLM call | Medium |

### Decision Flowchart

```
Start with basic RAG
  |
  +--> Answers are incomplete?
  |      --> Add Multi-Query Retrieval
  |
  +--> Answers include irrelevant info?
  |      --> Add Contextual Compression
  |
  +--> Missing exact matches (numbers, names)?
  |      --> Add Hybrid Search (BM25 + Semantic)
  |
  +--> Wrong results ranked higher?
  |      --> Add Reranking
  |
  +--> All of the above?
         --> Combine techniques
```

---

## Summary

| Technique | One-Line Summary |
|-----------|-----------------|
| Multi-Query | Generates multiple search queries from one question |
| Contextual Compression | Removes irrelevant parts from retrieved chunks |
| Hybrid Search | Combines keyword (BM25) and semantic (embedding) search |
| Reranking | Reorders results by relevance using a separate model |
| Parent Document | Searches small chunks, returns large parent chunks |
| Self-Query | Extracts metadata filters from natural language |
| Key rule | Start simple, add complexity only when basic RAG is not enough |

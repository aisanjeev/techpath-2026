# Cheat Sheet: LangChain -- Building LLM Applications

**Module 10 -- Quick Reference**

---

## Installation

```bash
pip install langchain langchain-openai langchain-community langchain-core
pip install faiss-cpu chromadb pymilvus langchain-milvus pypdf tiktoken
```

---

## Core Imports

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
```

---

## LLM Setup

```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
response = llm.invoke("What is Python?")
print(response.content)
```

| Temperature | Behavior |
|-------------|----------|
| 0.0 | Deterministic, factual |
| 0.7 | Balanced (default) |
| 1.0 | Very creative |

---

## Prompt Templates

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a TechPath Institute assistant."),
    ("human", "Explain {topic} simply."),
])
```

---

## LCEL -- Pipe Operator

```python
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"topic": "REST APIs"})
```

| Method | Purpose |
|--------|---------|
| `invoke()` | Process one input |
| `batch()` | Process multiple inputs |
| `stream()` | Word-by-word output |

---

## Parallel Chains

```python
parallel = RunnableParallel(
    summary=summary_prompt | llm | parser,
    details=details_prompt | llm | parser,
)
result = parallel.invoke({"topic": "Python"})
```

---

## Document Loaders

| Loader | Source | Install |
|--------|--------|---------|
| `TextLoader` | `.txt` | Built-in |
| `PyPDFLoader` | PDF | `pypdf` |
| `CSVLoader` | CSV | Built-in |
| `WebBaseLoader` | Web | `beautifulsoup4` |

```python
loader = PyPDFLoader("file.pdf")
pages = loader.load()
```

---

## Text Splitters

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = splitter.split_documents(pages)
```

| Chunk Size | Use Case |
|-----------|----------|
| 200-500 | Precise Q&A |
| 500-1000 | General (recommended) |
| 1000-2000 | Summaries |

---

## Embeddings

```python
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector = embeddings.embed_query("Python course")
```

| Model | Dims | Cost |
|-------|------|------|
| `text-embedding-3-small` | 1536 | Cheap |
| `all-MiniLM-L6-v2` (HuggingFace) | 384 | Free |

---

## Vector Stores

```python
# FAISS (local, simple)
vectorstore = FAISS.from_texts(texts, embeddings)
results = vectorstore.similarity_search("query", k=3)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
vectorstore.save_local("index_folder")

# Milvus (local via Milvus Lite, or connect to server)
from langchain_milvus import Milvus
vectorstore = Milvus.from_texts(
    texts, embeddings,
    connection_args={"uri": "./milvus_demo.db"},   # Milvus Lite (local file)
    collection_name="my_collection",
)
results = vectorstore.similarity_search("query", k=3)
```

| Store | Type | Best For |
|-------|------|----------|
| FAISS | Local | Learning |
| Chroma | Local | Prototyping |
| Milvus | Local/server | Flexible production |
| Pinecone | Cloud | Managed production |

---

## RAG Chain (Complete)

```python
def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)
answer = rag_chain.invoke("What is the fee?")
```

---

## Advanced RAG

| Technique | What It Does |
|-----------|-------------|
| Multi-Query | Generates multiple search queries |
| Compression | Removes irrelevant parts from chunks |
| Hybrid Search | BM25 (keyword) + Semantic (embedding) |
| Reranking | Reorders results by relevance |

```python
# Hybrid Search
hybrid = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.4, 0.6],
)
```

---

## Memory

```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(return_messages=True)
memory.save_context({"input": "Hi"}, {"output": "Hello!"})
```

---

## Cosine Similarity Formula

```python
import numpy as np
similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
# 1.0 = identical, 0.0 = unrelated
```

---

## Complete RAG Flow

```
Documents --> Loader --> Splitter --> Embeddings --> Vector Store
                                                         |
User Question --> Retriever --> Chunks --> Prompt --> LLM --> Answer
```

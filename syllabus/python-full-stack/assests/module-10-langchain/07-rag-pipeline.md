# RAG Pipeline -- Retrieval Augmented Generation

**Module 10 -- LangChain | Topic 7**

---

## What is RAG?

RAG stands for **Retrieval-Augmented Generation**. It is the most important pattern in LangChain and the backbone of most AI applications today.

The idea is simple: instead of asking the LLM to answer from its training data (which may be outdated or wrong), you first **retrieve** relevant documents from your own data, then **augment** the prompt with those documents, so the LLM **generates** an accurate answer.

**Analogy:** Imagine you are giving an open-book exam at TechPath Institute.
- Without RAG: You close the book and answer from memory. You might forget details or make things up.
- With RAG: You open the textbook, find the relevant page, read it, then write your answer. Your answer is accurate because you are looking at the source.

---

## How RAG Works -- The Flow

```
User Question: "What is the Python course fee?"
       |
       v
[1. RETRIEVER]  -- Searches the vector store for relevant chunks
       |         -- Returns: "Python Full Stack course fee is Rs 45,000"
       v
[2. PROMPT]     -- Combines the question + retrieved context
       |         -- "Based on this context: [fee is Rs 45,000]
       |            Answer this question: What is the course fee?"
       v
[3. LLM]        -- Reads the context and generates an answer
       |         -- "The Python Full Stack course at TechPath costs Rs 45,000."
       v
[4. OUTPUT]     -- Returns the answer (optionally with source citations)
```

---

## Building a RAG Pipeline Step by Step

### Step 1: Prepare Your Documents

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load documents
loader = PyPDFLoader("techpath_brochure.pdf")
pages = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)

print(f"Split into {len(chunks)} chunks")
```

### Step 2: Create the Vector Store

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# Save for later use
vectorstore.save_local("techpath_knowledge_base")
```

### Step 3: Create the Retriever

```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Test it
test_docs = retriever.invoke("What is the course fee?")
for doc in test_docs:
    print(f"- {doc.page_content[:100]}...")
```

### Step 4: Create the RAG Prompt

```python
from langchain_core.prompts import ChatPromptTemplate

rag_prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant for TechPath Institute, Bhopal.
Answer the question based ONLY on the following context.
If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:""")
```

### Step 5: Build the Chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

def format_docs(docs):
    """Convert document objects to a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | parser
)
```

### Step 6: Ask Questions

```python
# Ask questions about your documents
answer = rag_chain.invoke("What is the Python course fee?")
print(answer)
# "The Python Full Stack course at TechPath Institute costs Rs 45,000 including GST."

answer = rag_chain.invoke("What are the class timings?")
print(answer)
# "Classes are held Monday to Friday from 10 AM to 1 PM."

answer = rag_chain.invoke("What is the weather in Delhi?")
print(answer)
# "I don't have that information."
```

---

## Understanding Each Component

### The Retriever

The retriever searches the vector store and returns the most relevant document chunks.

```python
# How the retriever works internally:
# 1. Takes the user's question
# 2. Converts it to an embedding vector
# 3. Searches the vector store for similar vectors
# 4. Returns the top K matching documents

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke("course fee")
# Returns the 3 most relevant chunks about course fees
```

### The Prompt

The prompt tells the LLM how to use the retrieved context:

```python
# Key parts of a good RAG prompt:
# 1. Role: "You are a helpful assistant for TechPath Institute"
# 2. Instruction: "Answer based ONLY on the context"
# 3. Fallback: "If not in context, say I don't know"
# 4. Context: The retrieved documents
# 5. Question: The user's actual question
```

### Why "Answer ONLY from context"?

Without this instruction, the LLM might:
- Make up information (hallucinate)
- Use outdated information from its training data
- Give answers that contradict your actual data

With this instruction, the LLM stays grounded in your documents.

---

## Adding Source Citations

Users want to know where the answer came from. Here is how to include sources:

```python
from langchain_core.runnables import RunnablePassthrough

def retrieve_with_sources(question):
    """Retrieve documents and include their sources."""
    docs = retriever.invoke(question)
    return {
        "context": "\n\n".join(doc.page_content for doc in docs),
        "sources": [doc.metadata.get("source", "unknown") for doc in docs],
        "question": question,
    }

# Modified prompt that asks for citations
citation_prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below.
Include the source at the end of your answer.

Context:
{context}

Sources: {sources}

Question: {question}

Answer (include source citations):""")

# Chain with sources
rag_with_sources = (
    RunnablePassthrough()
    | RunnableLambda(retrieve_with_sources)
    | citation_prompt
    | llm
    | parser
)

result = rag_with_sources.invoke("What is the course fee?")
print(result)
# "The Python Full Stack course costs Rs 45,000 (Source: techpath_brochure.pdf, page 2)"
```

---

## Streaming RAG Responses

Show the answer word by word, like ChatGPT:

```python
# Stream the response
for chunk in rag_chain.stream("Tell me about the Python course"):
    print(chunk, end="", flush=True)
```

---

## Using RAG from Plain Text (Without PDFs)

You do not always need PDF files. You can create a RAG system from plain text:

```python
# Knowledge base as simple text
knowledge = [
    "TechPath Institute is located in Bhopal, Madhya Pradesh.",
    "Python Full Stack course fee is Rs 45,000 with 6-month EMI available.",
    "Course duration is 6 months. Classes: Mon-Fri, 10 AM to 1 PM.",
    "Students learn Python, Django, FastAPI, React, SQL, and Git.",
    "Placement assistance provided. Average package: Rs 4-6 LPA.",
    "Online batches available for students in Delhi, Pune, and Indore.",
    "Weekend batches start every month. Timing: Sat-Sun, 10 AM to 4 PM.",
    "Hostel facility available near campus. Rent: Rs 5,000/month.",
]

# Create vector store from text
vectorstore = FAISS.from_texts(knowledge, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Build the same RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | parser
)

print(rag_chain.invoke("Is hostel available?"))
# "Yes, hostel facility is available near the TechPath campus. The rent is Rs 5,000 per month."
```

---

## Common RAG Mistakes and Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Wrong or irrelevant answers | Chunks are too large or too small | Adjust chunk_size (try 500, then 300 or 800) |
| LLM makes up information | Prompt does not restrict to context | Add "Answer ONLY from the context" |
| Misses relevant documents | Only retrieving 1-2 chunks | Increase k to 3-5 |
| Slow responses | Large chunks sent to LLM | Reduce chunk_size or k |
| Duplicate information | Overlapping chunks | Use MMR retrieval for diversity |

---

## RAG Pipeline Checklist

Before deploying a RAG system, verify:

1. **Document loading** -- Are all documents loaded correctly?
2. **Chunking** -- Are chunks the right size? (500-1000 chars is a good start)
3. **Embedding** -- Is the embedding model the same for indexing and querying?
4. **Retrieval** -- Does `retriever.invoke("test question")` return relevant results?
5. **Prompt** -- Does the prompt tell the LLM to answer only from context?
6. **Fallback** -- Does the system say "I don't know" for out-of-scope questions?
7. **Citations** -- Can users see where the answer came from?

---

## The Complete RAG Flow Diagram

```
[Your Documents]
       |
  [Document Loader]  -- PyPDFLoader, TextLoader, WebBaseLoader
       |
  [Text Splitter]    -- RecursiveCharacterTextSplitter (chunk_size=500)
       |
  [Embeddings]       -- OpenAIEmbeddings / HuggingFace
       |
  [Vector Store]     -- FAISS / Chroma / Pinecone
       |
       +----> [Retriever] <---- User Question
                  |
                  v
            [Retrieved Chunks]
                  |
                  v
           [Prompt Template]  -- "Answer from this context: {context}"
                  |
                  v
              [LLM]          -- ChatOpenAI / Claude
                  |
                  v
          [Output Parser]    -- StrOutputParser
                  |
                  v
             [Answer]        -- "The course fee is Rs 45,000"
```

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| RAG | Retrieve relevant docs, augment prompt, generate answer |
| Retriever | Searches vector store for relevant chunks |
| `format_docs()` | Converts Document objects to a text string for the prompt |
| `RunnablePassthrough()` | Passes the question through while retriever runs |
| Citations | Include source metadata so users know where the answer came from |
| Fallback | Always tell the LLM to say "I don't know" if answer is not in context |
| Streaming | Use `chain.stream()` for word-by-word output |
| Key rule | Always test retrieval separately before building the full chain |

# Module 10: LangChain -- Building LLM Applications

## 1. What is LangChain?

LangChain is a Python framework that makes it easy to build applications powered by Large Language Models (LLMs). Think of it like this: an LLM (such as OpenAI's GPT) is a powerful engine, but LangChain gives you a full car -- steering wheel, seats, dashboard -- so you can actually drive somewhere useful.

Without LangChain, you would have to write a lot of code yourself to connect an LLM to your documents, manage conversation history, or chain multiple steps together. LangChain handles all of this for you.

### Installation

```bash
pip install langchain langchain-openai langchain-community langchain-core
pip install faiss-cpu chromadb       # Vector stores
pip install pypdf tiktoken           # PDF loading and tokenization
```

### Setting Up Your API Key

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Or load from a .env file (recommended)
from dotenv import load_dotenv
load_dotenv()
```

---

## 2. LangChain Architecture

LangChain has several core building blocks. Here is how they fit together:

| Component       | What It Does                                      | Analogy                           |
|-----------------|---------------------------------------------------|-----------------------------------|
| **LLM / ChatModel** | Sends text to an AI model, gets a response     | The brain                         |
| **Prompt Template**  | Formats your question before sending to LLM    | A fill-in-the-blank form          |
| **Output Parser**    | Converts the LLM's raw text into structured data | A translator                   |
| **Chain**            | Connects multiple steps together                 | An assembly line                  |
| **Memory**           | Remembers previous messages in a conversation    | A notebook for the AI             |
| **Retriever**        | Finds relevant documents from a knowledge base   | A librarian searching for books   |

### LLMs and Chat Models

```python
from langchain_openai import ChatOpenAI

# Create a chat model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Simple call
response = llm.invoke("What is Python used for?")
print(response.content)
```

**Temperature** controls creativity:
- `0.0` = Focused, deterministic (good for factual answers)
- `0.7` = Balanced (good for general use)
- `1.0` = Very creative (good for brainstorming)

### Prompt Templates

Instead of writing the full prompt every time, use templates:

```python
from langchain_core.prompts import ChatPromptTemplate

# Create a template with a variable
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful teaching assistant at TechPath Institute."),
    ("human", "Explain {topic} in simple words for a beginner student."),
])

# Fill in the variable
formatted = prompt.invoke({"topic": "machine learning"})
print(formatted)
```

### Output Parsers

LLMs return plain text. Parsers convert that into Python objects:

```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Simple string parser
parser = StrOutputParser()

# JSON parser -- gets structured data from LLM
from langchain_core.pydantic_v1 import BaseModel, Field

class CourseInfo(BaseModel):
    name: str = Field(description="Course name")
    duration: str = Field(description="Course duration")
    fee: int = Field(description="Course fee in rupees")

json_parser = JsonOutputParser(pydantic_object=CourseInfo)
```

### Memory

Memory lets the LLM remember what was said earlier in a conversation:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)

# Save a conversation exchange
memory.save_context(
    {"input": "My name is Rahul"},
    {"output": "Hello Rahul! How can I help you today?"}
)

# Later, the LLM can recall this
history = memory.load_memory_variables({})
print(history)
# {'history': [HumanMessage(content='My name is Rahul'),
#              AIMessage(content='Hello Rahul! How can I help you today?')]}
```

**Types of Memory:**

| Memory Type                 | Behavior                                    | Best For                |
|-----------------------------|---------------------------------------------|-------------------------|
| `ConversationBufferMemory`  | Stores everything                           | Short conversations     |
| `ConversationSummaryMemory` | Summarizes old messages                     | Long conversations      |
| `ConversationWindowMemory`  | Keeps only the last N exchanges             | Medium conversations    |

---

## 3. LCEL -- LangChain Expression Language

LCEL is the modern way to build chains in LangChain. It uses the pipe operator (`|`) to connect components, just like Unix pipes.

### Basic Chain with the Pipe Operator

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Define components
prompt = ChatPromptTemplate.from_template(
    "You are a TechPath Institute trainer. Explain {topic} in 3 bullet points."
)
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Connect them with pipes
chain = prompt | llm | parser

# Run the chain
result = chain.invoke({"topic": "REST APIs"})
print(result)
```

**How the pipe works:**
1. `prompt` formats the input into a message
2. `|` passes the output to `llm`
3. `llm` sends it to OpenAI and gets a response
4. `|` passes the response to `parser`
5. `parser` extracts the text string

### Runnable Sequences

Under the hood, `|` creates a `RunnableSequence`. You can also build one explicitly:

```python
from langchain_core.runnables import RunnableSequence

chain = RunnableSequence(prompt, llm, parser)
result = chain.invoke({"topic": "Django"})
```

### Parallel Chains

Run multiple chains at the same time with `RunnableParallel`:

```python
from langchain_core.runnables import RunnableParallel

# Two different prompts for the same topic
beginner_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} for a complete beginner."
)
advanced_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} for someone with programming experience."
)

# Run both in parallel
parallel_chain = RunnableParallel(
    beginner=beginner_prompt | llm | parser,
    advanced=advanced_prompt | llm | parser,
)

results = parallel_chain.invoke({"topic": "Python decorators"})
print("Beginner:", results["beginner"])
print("Advanced:", results["advanced"])
```

### Streaming

LCEL chains support streaming (output appears word by word):

```python
chain = prompt | llm | parser

for chunk in chain.stream({"topic": "LangChain"}):
    print(chunk, end="", flush=True)
```

---

## 4. Document Loaders

Document loaders bring data into LangChain from different sources -- PDFs, websites, CSVs, and more.

### Loading Text Files

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("techpath_courses.txt")
documents = loader.load()

print(f"Loaded {len(documents)} document(s)")
print(documents[0].page_content[:200])  # First 200 characters
```

### Loading PDFs

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("syllabus.pdf")
pages = loader.load()

print(f"Total pages: {len(pages)}")
print(f"Page 1 content: {pages[0].page_content[:300]}")
print(f"Page 1 metadata: {pages[0].metadata}")  # {'source': 'syllabus.pdf', 'page': 0}
```

### Loading Web Pages

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://docs.python.org/3/tutorial/")
docs = loader.load()

print(docs[0].page_content[:500])
```

### Loading CSVs

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("students.csv")
docs = loader.load()

# Each row becomes a separate document
for doc in docs[:3]:
    print(doc.page_content)
    print("---")
```

### Comparison of Document Loaders

| Loader           | Source         | Install                     | Output              |
|------------------|---------------|-----------------------------|--------------------|
| `TextLoader`     | `.txt` files   | Built-in                   | 1 document          |
| `PyPDFLoader`    | PDF files      | `pip install pypdf`        | 1 doc per page      |
| `CSVLoader`      | CSV files      | Built-in                   | 1 doc per row       |
| `WebBaseLoader`  | Web URLs       | `pip install beautifulsoup4` | 1 doc per page    |
| `NotionDBLoader` | Notion pages   | `pip install notion-client` | 1 doc per page     |
| `GitHubLoader`   | GitHub repos   | Built-in                   | 1 doc per file      |

---

## 5. Text Splitters

Documents are often too long to send to an LLM at once. Text splitters break them into smaller, overlapping chunks.

### Why Overlap?

Imagine splitting a paragraph right in the middle of a sentence. The meaning is lost. Overlap ensures that the end of one chunk and the start of the next share some text, so no context is lost at the boundaries.

```
Original:  [............sentence A.........|...sentence B.............]
Chunk 1:   [............sentence A.........|...sent]
Chunk 2:                                   [...sentence B.............]
                                           ^^^^^^^^ overlap
```

### Recursive Character Splitter

The most commonly used splitter. It tries to split by paragraphs first, then sentences, then words:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Max characters per chunk
    chunk_overlap=50,     # Overlap between chunks
    separators=["\n\n", "\n", ". ", " ", ""],  # Split priority
)

text = """TechPath Institute offers a Python Full Stack course.
The course covers Python basics, web development with Django and FastAPI,
database design, and deployment. Students learn by building real projects.

The course duration is 6 months. Fee is Rs 45,000 including GST.
Classes are held Monday to Friday from 10 AM to 1 PM at the Bhopal campus.
Online batches are also available for students in Delhi, Pune, and Indore."""

chunks = splitter.split_text(text)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} ({len(chunk)} chars): {chunk[:80]}...")
```

### Choosing Chunk Size

| Chunk Size | Good For                           | Trade-Off                     |
|------------|------------------------------------|------------------------------ |
| 200-500    | Precise retrieval, FAQ bots        | May lose context              |
| 500-1000   | General purpose (recommended)      | Balanced                      |
| 1000-2000  | Long documents, summaries          | Less precise retrieval        |

**Rule of thumb:** Start with `chunk_size=500` and `chunk_overlap=50`. Adjust based on results.

---

## 6. Embeddings

Embeddings convert text into numbers (vectors). Similar text gets similar numbers. This is how the computer "understands" meaning.

### How Embeddings Work

Think of it like placing books on a shelf by topic. Books about Python would be close together, and books about cooking would be far away. Embeddings do the same thing, but in a mathematical space with hundreds of dimensions.

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Embed a single text
vector = embeddings.embed_query("Python programming course")
print(f"Vector length: {len(vector)}")   # 1536 dimensions
print(f"First 5 values: {vector[:5]}")   # [-0.012, 0.034, ...]
```

### Measuring Similarity with Cosine Similarity

```python
import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

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

print(f"Python course vs Python development: {sim_1_2:.4f}")  # High (~0.85)
print(f"Python course vs biryani recipe: {sim_1_3:.4f}")       # Low (~0.15)
```

### HuggingFace Embeddings (Free, Local)

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

# Runs locally -- no API key needed
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = embeddings.embed_query("TechPath Institute Bhopal")
print(f"Vector length: {len(vector)}")  # 384 dimensions
```

| Embedding Model                  | Dimensions | Cost          | Speed     |
|----------------------------------|------------|---------------|-----------|
| OpenAI `text-embedding-3-small`  | 1536       | Paid (cheap)  | Fast      |
| OpenAI `text-embedding-3-large`  | 3072       | Paid          | Fast      |
| HuggingFace `all-MiniLM-L6-v2`  | 384        | Free          | Medium    |
| HuggingFace `all-mpnet-base-v2` | 768        | Free          | Slower    |

---

## 7. Vector Stores

A vector store is a database optimized for storing and searching embeddings. When you ask a question, it finds the most similar document chunks.

### FAISS (Local, No Server Needed)

FAISS (Facebook AI Similarity Search) runs entirely on your computer:

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

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

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(texts, embeddings)

# Search for similar documents
results = vectorstore.similarity_search("How much does the course cost?", k=2)
for doc in results:
    print(f"- {doc.page_content}")
# Output:
# - The course fee is Rs 45,000 including GST. EMI options available.
# - Course duration is 6 months with classes Monday to Friday.
```

### Saving and Loading FAISS

```python
# Save to disk
vectorstore.save_local("techpath_index")

# Load later
loaded_store = FAISS.load_local(
    "techpath_index", embeddings, allow_dangerous_deserialization=True
)
```

### Chroma (Another Popular Option)

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_texts(
    texts,
    embeddings,
    persist_directory="./chroma_db",
    collection_name="techpath_courses",
)

results = vectorstore.similarity_search("Where is the campus?", k=2)
```

### Comparison of Vector Stores

| Vector Store | Type         | Setup         | Best For                    |
|-------------|--------------|---------------|-----------------------------|
| **FAISS**   | Local        | `pip install faiss-cpu` | Learning, small projects |
| **Chroma**  | Local/Server | `pip install chromadb`  | Prototyping, medium apps |
| **Pinecone**| Cloud        | API key needed          | Production, large scale  |
| **Weaviate**| Cloud/Local  | Docker or API key       | Production, hybrid search|

---

## 8. RAG Pipeline -- Retrieval Augmented Generation

RAG is the most important pattern in LangChain. It lets an LLM answer questions using YOUR documents, not just its training data.

### How RAG Works

```
User Question
     |
     v
[1. Retriever] -- Finds relevant document chunks from vector store
     |
     v
[2. Prompt] -- Combines question + retrieved context
     |
     v
[3. LLM] -- Generates answer based on the context
     |
     v
[4. Output] -- Answer with source citations
```

**Analogy:** Imagine you are a student and the teacher asks you a question. Instead of guessing, you quickly look through your textbook (retriever), find the relevant pages (context), read them, and then answer the question in your own words (LLM). That is RAG.

### Building a Complete RAG Chain

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. Create vector store with your documents
texts = [
    "TechPath Institute Python Full Stack course costs Rs 45,000.",
    "Course duration is 6 months. Classes are Monday to Friday, 10 AM to 1 PM.",
    "The course covers Python, Django, FastAPI, React, databases, and deployment.",
    "TechPath Bhopal campus is near MP Nagar. Online batches also available.",
    "Placement assistance provided. Average package is Rs 4-6 LPA.",
]

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(texts, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 2. Create the RAG prompt
rag_prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant for TechPath Institute.
Answer the question based ONLY on the following context.
If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:""")

# 3. Build the chain
def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

# 4. Ask questions
answer = rag_chain.invoke("What is the course fee?")
print(answer)
# "The Python Full Stack course at TechPath Institute costs Rs 45,000."
```

### Adding Source Citations

```python
from langchain_core.runnables import RunnablePassthrough

def retrieve_with_sources(question):
    docs = retriever.invoke(question)
    return {
        "context": "\n".join(doc.page_content for doc in docs),
        "sources": [doc.metadata.get("source", "unknown") for doc in docs],
        "question": question,
    }

# Modified chain that returns sources
rag_with_sources = (
    RunnablePassthrough()
    | retrieve_with_sources
)

result = rag_with_sources("What is the course fee?")
print(f"Answer context: {result['context']}")
print(f"Sources: {result['sources']}")
```

---

## 9. Advanced RAG Techniques

### Multi-Query Retrieval

Sometimes a single query misses relevant documents. Multi-query generates multiple versions of the question:

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=ChatOpenAI(model="gpt-4o-mini"),
)

# This generates multiple phrasings of the question internally
docs = multi_retriever.invoke("Tell me about TechPath fees and duration")
```

**How it works:** For "Tell me about TechPath fees and duration", the LLM might generate:
1. "What is the course fee at TechPath?"
2. "How long is the TechPath course?"
3. "What are the pricing and duration details?"

Each query retrieves documents, and the results are combined (deduplicated).

### Contextual Compression

Removes irrelevant parts from retrieved documents before sending to the LLM:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(ChatOpenAI(model="gpt-4o-mini"))

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(),
)

docs = compression_retriever.invoke("What is the course fee?")
# Returns only the relevant parts of each document
```

### Hybrid Search

Combines keyword search (BM25) with semantic search (embeddings) for better results:

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Keyword-based retriever
bm25_retriever = BM25Retriever.from_texts(texts)
bm25_retriever.k = 3

# Semantic retriever
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Combine both
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.4, 0.6],  # 40% keyword, 60% semantic
)

docs = hybrid_retriever.invoke("TechPath Bhopal campus location")
```

### Reranking

After retrieving documents, rerank them by relevance to improve quality:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import CohereRerank

# Rerank the top results
reranker = CohereRerank(top_n=3)

reranking_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
)

# Retrieves 10, reranks, returns top 3
docs = reranking_retriever.invoke("course details")
```

---

## 10. Summary -- Putting It All Together

Here is the complete flow of building an LLM application with LangChain:

```
[Your Documents] --> [Document Loader] --> [Text Splitter] --> [Embeddings]
                                                                    |
                                                                    v
                                                            [Vector Store]
                                                                    |
User Question --> [Retriever] --> [Retrieved Chunks]                |
                                        |                          |
                                        v                          |
                               [Prompt Template] <-----------------+
                                        |
                                        v
                                      [LLM]
                                        |
                                        v
                                [Output Parser]
                                        |
                                        v
                                    [Answer]
```

### Key Takeaways

1. **LangChain** simplifies building LLM apps by providing reusable components.
2. **LCEL** (pipe operator) is the modern way to chain components together.
3. **Document Loaders** bring your data in; **Text Splitters** break it into chunks.
4. **Embeddings** convert text to vectors; **Vector Stores** enable fast similarity search.
5. **RAG** is the most important pattern -- it lets LLMs answer from YOUR data.
6. **Advanced RAG** (multi-query, compression, hybrid search, reranking) improves accuracy.
7. Start simple (FAISS + basic RAG), then add complexity as needed.

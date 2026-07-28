# Quiz: LangChain -- Building LLM Applications

**Module 10 | 15 Questions | Pass Mark: 60%**

---

## Q1. What is LangChain?
- A) A JavaScript framework for web apps
- B) A Python framework for building LLM-powered applications ✅
- C) A database management tool
- D) A CSS library for styling

> **Explanation:** LangChain is a Python framework that provides reusable components (prompts, chains, memory, retrievers) for building applications powered by Large Language Models.

---

## Q2. What does the pipe operator (|) do in LCEL?
- A) Adds two numbers together
- B) Connects components so output of one becomes input of the next ✅
- C) Creates a new file on disk
- D) Splits text into chunks

> **Explanation:** In LCEL, the pipe operator connects components in sequence -- the output of the left side flows as input to the right side, like `prompt | llm | parser`.

---

## Q3. What does a Prompt Template do?
- A) Stores data in a database
- B) Formats a question with variables before sending to the LLM ✅
- C) Converts text to numbers
- D) Searches for similar documents

> **Explanation:** A Prompt Template is like a fill-in-the-blank form. You define the structure once with variables like {topic}, then fill in different values each time.

---

## Q4. What does temperature=0.0 mean when configuring an LLM?
- A) The model runs faster
- B) The model gives creative, random responses
- C) The model gives focused, deterministic responses ✅
- D) The model uses less memory

> **Explanation:** Temperature 0.0 makes the LLM deterministic -- it gives the same focused answer every time. Higher temperature makes responses more creative.

---

## Q5. What is the purpose of an Output Parser?
- A) To send prompts to the LLM
- B) To convert raw LLM text into structured Python data ✅
- C) To load PDF files
- D) To store conversation history

> **Explanation:** Output Parsers convert the LLM's plain text into structured data like JSON objects, dictionaries, or lists that your code can easily use.

---

## Q6. Which document loader would you use to load a PDF file?
- A) TextLoader
- B) CSVLoader
- C) PyPDFLoader ✅
- D) WebBaseLoader

> **Explanation:** PyPDFLoader is designed for PDF files. It loads each page as a separate Document with metadata including the page number.

---

## Q7. Why do text splitters use chunk_overlap?
- A) To make files larger
- B) To prevent information loss at chunk boundaries ✅
- C) To speed up processing
- D) To reduce the number of chunks

> **Explanation:** Overlap ensures that text at the boundary between two chunks is included in both, so important information at split points is not lost.

---

## Q8. What are embeddings?
- A) HTML elements embedded in a page
- B) Number vectors that represent the meaning of text ✅
- C) Images inserted into documents
- D) Database table relationships

> **Explanation:** Embeddings convert text into lists of numbers (vectors) that capture meaning. Similar text gets similar vectors, enabling semantic search.

---

## Q9. What does cosine similarity measure?
- A) The length of a text
- B) How similar two embedding vectors are ✅
- C) The speed of an API call
- D) The cost of an LLM query

> **Explanation:** Cosine similarity measures how similar two vectors are, returning a value between -1 and 1. A score close to 1 means the texts have very similar meaning.

---

## Q10. Which vector store is best for learning and small projects?
- A) Pinecone
- B) Weaviate
- C) FAISS ✅
- D) MongoDB

> **Explanation:** FAISS is free, runs locally without any server setup, and is the simplest option for learning and small projects.

---

## Q11. What does RAG stand for?
- A) Random Access Generation
- B) Retrieval-Augmented Generation ✅
- C) Real-time API Gateway
- D) Recursive Algorithm Graph

> **Explanation:** RAG = Retrieval-Augmented Generation. It retrieves relevant documents first, then augments the prompt with context so the LLM generates accurate answers.

---

## Q12. In a RAG pipeline, what does the retriever do?
- A) Generates the final answer
- B) Searches the vector store for relevant document chunks ✅
- C) Formats the prompt template
- D) Converts text to embeddings

> **Explanation:** The retriever takes the user's question, searches the vector store for the most similar document chunks, and returns them for the LLM to use as context.

---

## Q13. What is the recommended starting chunk_size for text splitting?
- A) 50 characters
- B) 500 characters ✅
- C) 5000 characters
- D) 50000 characters

> **Explanation:** 500 characters is a good starting point for most applications. It balances precision with context. Adjust based on your results.

---

## Q14. What is Multi-Query Retrieval?
- A) Searching multiple databases at once
- B) Generating multiple versions of a question for better search coverage ✅
- C) Running multiple LLMs in parallel
- D) Loading multiple documents at once

> **Explanation:** Multi-Query Retrieval uses an LLM to generate multiple phrasings of the user's question, searches with each, and combines results for better coverage.

---

## Q15. What does hybrid search combine?
- A) Two different LLMs
- B) Keyword search (BM25) and semantic search (embeddings) ✅
- C) PDF loading and web scraping
- D) Memory and prompt templates

> **Explanation:** Hybrid search combines keyword-based search (BM25, exact matching) with semantic search (embeddings, meaning matching) for more comprehensive results.

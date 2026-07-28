# Module 10 -- Assignment: LangChain & RAG Applications

**Deadline:** End of Week 20
**Submission:** Python files (.py) + screenshots of output + a short write-up (PDF or text) explaining your approach

---

## Task 1: TechPath FAQ Bot with RAG -- 30 marks

Build a question-answering bot for TechPath Institute using LangChain's RAG pipeline.

**Requirements:**

1. Create a text file (`techpath_info.txt`) with at least 15 paragraphs of information about TechPath Institute -- courses offered, fees, schedule, placement details, campus facilities, admission process, faculty, contact info, and student reviews (use realistic Indian names and details)
2. Load the file using `TextLoader`
3. Split the text using `RecursiveCharacterTextSplitter` with `chunk_size=500` and `chunk_overlap=50`
4. Create embeddings using OpenAI or HuggingFace sentence-transformers
5. Store embeddings in a FAISS vector store
6. Build a RAG chain using LCEL (pipe operator): `retriever | prompt | llm | parser`
7. The bot should answer at least 10 different questions correctly based on the document
8. Include source citations in the answer (show which chunks were used)

**Test your bot with these questions:**
- "What is the fee for the Python course?"
- "Where is TechPath located?"
- "What is the placement rate?"
- "Do you offer online classes?"
- "What are the scholarship options?"

**Submit:** `task1_faq_bot.py` + `techpath_info.txt` + screenshot of 5 Q&A outputs

---

## Task 2: Multi-Document RAG System -- 35 marks

Build a RAG system that can answer questions from multiple document types.

**Requirements:**

1. Create three different source files:
   - `courses.txt` -- Course names, durations, fees, and schedules
   - `students.csv` -- At least 10 student records with columns: Name, City, Course, Batch, Fee Paid, Placement Status, Company, Package (LPA)
   - `faqs.txt` -- At least 15 frequently asked questions and their answers

2. Load all three files using the appropriate LangChain loaders (`TextLoader`, `CSVLoader`)
3. Split all documents into chunks
4. Store all chunks in a single FAISS vector store
5. Build a RAG chain that:
   - Answers questions from any of the three sources
   - Shows which source file the answer came from
   - Handles questions where the answer is not in the documents (says "I don't have that information")

6. Implement at least TWO of these advanced features:
   - **Multi-query retrieval:** Generate multiple versions of the question for better retrieval
   - **Conversation memory:** Remember previous questions in the same session
   - **Custom prompt:** Use a system prompt that makes the bot respond as a TechPath counselor

7. Add an interactive loop where the user can keep asking questions until they type "quit"

**Submit:** All Python files + all data files + screenshot of a 5-question conversation

---

## Task 3: Document Chunking Analyzer -- 20 marks

Build a tool that helps you understand how text splitting works.

**Requirements:**

1. Create a Python script that:
   - Takes a text file as input
   - Splits it using `RecursiveCharacterTextSplitter` with THREE different configurations:
     - Small: `chunk_size=200, chunk_overlap=20`
     - Medium: `chunk_size=500, chunk_overlap=50`
     - Large: `chunk_size=1000, chunk_overlap=100`

2. For each configuration, print:
   - Number of chunks created
   - Average chunk size (characters)
   - Smallest and largest chunk sizes
   - Total characters across all chunks
   - Overlap ratio (total chars / original text length)

3. Print the results in a formatted comparison table

4. Show the first chunk from each configuration side by side so the user can see the difference

5. Write a short paragraph (5-6 lines) at the end of your script (as a comment or print statement) explaining which configuration you would recommend for a TechPath FAQ bot and why

**Sample output format:**
```
Configuration       Chunks   Avg Size   Min   Max    Total   Overlap Ratio
Small (200/20)          18       175     45    200     3150       1.25x
Medium (500/50)          8       420    120    500     3360       1.33x
Large (1000/100)         4       630    250   1000     2520       1.00x
```

**Submit:** `task3_chunking_analyzer.py` + screenshot of output

---

## Task 4: Embedding Similarity Explorer -- 15 marks

Build a script that demonstrates how embeddings capture meaning.

**Requirements:**

1. Create a list of at least 12 sentences about TechPath courses, using a mix of:
   - Similar sentences (e.g., "Python course fee is Rs 45,000" and "The cost of the Python program is forty-five thousand rupees")
   - Different topics (e.g., course details vs. campus location vs. placement stats)

2. Generate embeddings for all sentences using HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (free, no API key needed)

3. Calculate cosine similarity between every pair of sentences

4. Display a similarity matrix showing which sentences are most/least similar

5. Find and print:
   - The 3 most similar pairs (highest cosine similarity)
   - The 3 least similar pairs (lowest cosine similarity)

6. Explain in comments why certain pairs are similar or different

**Submit:** `task4_embedding_explorer.py` + screenshot of similarity results

---

## Rubric

| Criteria | Excellent (Full Marks) | Good (75%) | Needs Work (50%) |
|----------|----------------------|------------|------------------|
| **Code Quality** | Clean code, proper comments, good variable names, follows Python conventions | Code works but has minor style issues, some comments missing | Code works but messy, no comments, poor naming |
| **Functionality** | All features work correctly, handles edge cases, error handling present | Most features work, minor bugs, basic error handling | Core feature works but missing several requirements |
| **RAG Pipeline** (Tasks 1-2) | Complete pipeline with retriever, prompt, LLM, parser. Answers are accurate and cite sources | Pipeline works but answers are sometimes inaccurate or sources missing | Pipeline partially works, many incorrect answers |
| **Data Quality** | Realistic Indian context data, comprehensive coverage, well-organized | Good data but incomplete or lacking variety | Minimal data, placeholder content |
| **Documentation** | Clear write-up explaining approach, challenges faced, and learnings | Brief write-up with basic explanation | No write-up or very minimal |

**Total: 100 marks**

**Note:** You can use either OpenAI API (paid, needs API key) or HuggingFace models (free, runs locally) for embeddings. If using OpenAI, include instructions in your code for setting up the API key. Never commit your actual API key to any file.

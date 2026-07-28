# Text Splitters

**Module 10 -- LangChain | Topic 4**

---

## Why Split Text?

LLMs have a **context window** -- a maximum number of tokens they can process at once. If your document is longer than this limit, you cannot send it all at once. You need to split it into smaller pieces called **chunks**.

**Analogy:** Imagine you are a student studying for exams. You cannot read a 500-page textbook in one sitting. Instead, you break it into chapters, then sections, then paragraphs. Text splitting works the same way -- it breaks large documents into manageable pieces.

### The Problem with Naive Splitting

You might think: "Just split every 500 characters." But that can cut words and sentences in half:

```
Original:  "TechPath Institute is located in Bhopal. The campus is near MP Nagar."

Bad split at character 40:
  Chunk 1: "TechPath Institute is located in Bhopal"
  Chunk 2: ". The campus is near MP Nagar."

The period and sentence are split awkwardly.
```

Smart splitters try to break at natural boundaries -- paragraphs, sentences, and words.

---

## Chunk Size and Overlap

Two key parameters control how text is split:

| Parameter | What It Means | Typical Value |
|-----------|--------------|---------------|
| `chunk_size` | Maximum characters (or tokens) per chunk | 500-1000 |
| `chunk_overlap` | How many characters are shared between adjacent chunks | 50-200 |

### Why Overlap?

Overlap prevents information loss at chunk boundaries.

```
Without overlap:
  Chunk 1: [......sentence A........]
  Chunk 2:                            [......sentence B........]
  --> If a question spans both sentences, neither chunk has full context.

With overlap:
  Chunk 1: [......sentence A......|..se]
  Chunk 2:                     [..sentence B........]
                                ^^^^ shared text (overlap)
  --> The shared region ensures context is not lost at the boundary.
```

**Rule of thumb:** Set overlap to about 10% of chunk_size. For `chunk_size=500`, use `chunk_overlap=50`.

---

## Recursive Character Text Splitter

This is the **most commonly used** splitter in LangChain. It tries to split at the most natural boundary first:

1. First tries to split by **double newlines** (`\n\n`) -- paragraph breaks
2. If chunks are still too big, splits by **single newlines** (`\n`)
3. Then by **sentences** (`. `)
4. Then by **spaces** (` `)
5. Finally by **individual characters** (`""`)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)

text = """TechPath Institute offers a Python Full Stack course.
The course covers Python basics, web development with Django and FastAPI,
database design, and deployment. Students learn by building real projects.

The course duration is 6 months. Fee is Rs 45,000 including GST.
Classes are held Monday to Friday from 10 AM to 1 PM at the Bhopal campus.
Online batches are also available for students in Delhi, Pune, and Indore.

After completing the course, students receive placement assistance.
Many students have been placed at companies like TCS, Infosys, and Wipro
with packages ranging from Rs 4 LPA to Rs 8 LPA."""

chunks = splitter.split_text(text)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} ({len(chunk)} chars):")
    print(chunk)
    print("---")
```

### How Separators Work

```
Priority order: ["\n\n", "\n", ". ", " ", ""]

Step 1: Try splitting by paragraphs (\n\n)
  --> If each paragraph is under chunk_size, done!

Step 2: If a paragraph is too big, split by lines (\n)
  --> If each section is under chunk_size, done!

Step 3: If still too big, split by sentences (. )
Step 4: If still too big, split by words ( )
Step 5: Last resort: split by characters ("")
```

---

## Character Text Splitter

Splits by a single separator. Simpler but less intelligent than the recursive version.

```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=500,
    chunk_overlap=50,
)

chunks = splitter.split_text(text)
```

**When to use:** When your text has a consistent structure (like log files where each line is a record).

---

## Token-Based Text Splitter

Instead of counting characters, this splitter counts **tokens** (the units that LLMs actually process).

Why does this matter? The word "TechPath" is 1 word but might be 2 tokens. Counting characters can be misleading -- a 500-character chunk might use 100 tokens or 200 tokens depending on the content.

```python
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=200,        # 200 tokens per chunk (not characters)
    chunk_overlap=20,
)

chunks = splitter.split_text(text)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk[:80]}...")
```

**Install:** `pip install tiktoken`

### Characters vs Tokens

| Text | Characters | Tokens (approx) |
|------|-----------|-----------------|
| "Hello" | 5 | 1 |
| "TechPath Institute" | 18 | 3 |
| "Python Full Stack Development Course" | 36 | 5 |
| A full paragraph (100 words) | ~500 | ~130 |

**Rule of thumb:** 1 token is roughly 4 characters or 0.75 words in English.

---

## Markdown Text Splitter

Specifically designed for Markdown files. It splits at headings, code blocks, and other Markdown elements.

```python
from langchain.text_splitter import MarkdownTextSplitter

splitter = MarkdownTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

markdown_text = """# Python Full Stack Course

## Module 1: Python Basics

Learn variables, data types, loops, and functions.
Build simple programs like a calculator and a student grade tracker.

## Module 2: Web Development

Learn HTML, CSS, JavaScript, and React.
Build responsive websites that work on mobile and desktop.

## Module 3: Backend with FastAPI

Learn to build REST APIs using FastAPI.
Connect to databases using SQLAlchemy.
"""

chunks = splitter.split_text(markdown_text)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:")
    print(chunk)
    print("---")
```

This splitter preserves the heading structure, so each chunk starts with its relevant heading.

---

## Code Splitter

For splitting programming code. It understands code structure and splits at function/class boundaries.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

# Python code splitter
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=500,
    chunk_overlap=50,
)

code = """
class Student:
    def __init__(self, name, city):
        self.name = name
        self.city = city
    
    def display(self):
        print(f"Student: {self.name} from {self.city}")

class Course:
    def __init__(self, name, fee):
        self.name = name
        self.fee = fee
    
    def get_emi(self, months):
        return self.fee / months
"""

chunks = python_splitter.split_text(code)
```

Supported languages: Python, JavaScript, TypeScript, Java, Go, Ruby, C, C++, and many more.

---

## Semantic Text Splitter

The most advanced approach. Instead of splitting by character count, it splits by **meaning**. Sentences about the same topic stay together.

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# Uses embeddings to detect topic changes
splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
)

chunks = splitter.split_text(text)
```

**How it works:**
1. Splits text into sentences
2. Generates embeddings for each sentence
3. Measures similarity between consecutive sentences
4. Splits where the similarity drops (topic changes)

**When to use:** When your documents cover multiple topics and you want each chunk to be about one topic.

---

## Choosing the Right Splitter

| Splitter | Best For | Complexity |
|----------|---------|------------|
| `RecursiveCharacterTextSplitter` | General purpose (default choice) | Simple |
| `CharacterTextSplitter` | Text with consistent structure | Simple |
| `TokenTextSplitter` | When you need precise token counts | Medium |
| `MarkdownTextSplitter` | Markdown documents | Medium |
| `RecursiveCharacterTextSplitter.from_language()` | Source code | Medium |
| `SemanticChunker` | Mixed-topic documents | Advanced |

---

## Choosing Chunk Size

| Chunk Size | Good For | Trade-off |
|-----------|---------|-----------|
| 200-500 chars | FAQ bots, precise answers | May lose context from longer passages |
| 500-1000 chars | General purpose (recommended) | Balanced accuracy and context |
| 1000-2000 chars | Summaries, long-form content | Less precise retrieval |

### How to Decide

Start with these defaults and adjust based on your results:

```python
# Good starting point for most applications
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
```

If your chatbot gives incomplete answers, **increase chunk_size**.
If your chatbot retrieves irrelevant content, **decrease chunk_size**.

---

## Splitting Documents (Not Just Text)

The splitters work with Document objects too, preserving metadata:

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load a PDF
loader = PyPDFLoader("syllabus.pdf")
pages = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)

# Each chunk keeps the original metadata (source, page number)
for chunk in chunks[:3]:
    print(f"Source: {chunk.metadata['source']}, Page: {chunk.metadata['page']}")
    print(f"Content: {chunk.page_content[:100]}...")
    print("---")
```

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Text splitting | Breaking large documents into smaller chunks for LLM processing |
| `chunk_size` | Maximum size of each chunk (characters or tokens) |
| `chunk_overlap` | Shared text between adjacent chunks to prevent context loss |
| `RecursiveCharacterTextSplitter` | Default choice -- splits by paragraphs, then sentences, then words |
| `TokenTextSplitter` | Splits by token count (what the LLM actually processes) |
| `MarkdownTextSplitter` | Splits Markdown by headings and structure |
| Code splitter | Splits code at function and class boundaries |
| `SemanticChunker` | Splits by meaning -- keeps related sentences together |
| Start with | `chunk_size=500`, `chunk_overlap=50`, adjust based on results |

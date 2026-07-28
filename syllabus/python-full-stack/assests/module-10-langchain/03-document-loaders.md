# Document Loaders

**Module 10 -- LangChain | Topic 3**

---

## What Are Document Loaders?

Document loaders are LangChain components that bring external data into your application. They read files from different sources -- PDFs, websites, CSVs, databases -- and convert them into a standard format that LangChain can work with.

**Analogy:** Think of document loaders like a librarian who can read books in any language. Whether you give them a PDF, a web page, or a spreadsheet, they read it and write it down in a standard format (a LangChain `Document` object) so the rest of your application can use it.

### The Document Object

Every loader returns a list of `Document` objects. Each document has:

```python
from langchain_core.documents import Document

doc = Document(
    page_content="TechPath Institute offers Python Full Stack course in Bhopal.",
    metadata={"source": "brochure.pdf", "page": 1}
)

print(doc.page_content)   # The actual text
print(doc.metadata)        # Information about where the text came from
```

| Property | What It Contains | Why It Matters |
|----------|-----------------|---------------|
| `page_content` | The actual text from the file | This is what gets embedded and searched |
| `metadata` | Source file, page number, URL, etc. | Helps you cite sources in your answers |

---

## Loading Text Files

The simplest loader -- reads a plain `.txt` file.

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("techpath_courses.txt")
documents = loader.load()

print(f"Loaded {len(documents)} document(s)")
print(documents[0].page_content[:200])
print(documents[0].metadata)
# {'source': 'techpath_courses.txt'}
```

**When to use:** Configuration files, plain text content, simple notes.

---

## Loading PDF Files

PDFs are the most common document format in business and education. LangChain can load them page by page.

### PyPDFLoader (Most Common)

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("techpath_syllabus.pdf")
pages = loader.load()

print(f"Total pages: {len(pages)}")
print(f"Page 1 text: {pages[0].page_content[:300]}")
print(f"Metadata: {pages[0].metadata}")
# {'source': 'techpath_syllabus.pdf', 'page': 0}
```

**Install:** `pip install pypdf`

### Loading Multiple PDFs from a Folder

```python
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

# Load all PDFs from a folder
loader = DirectoryLoader(
    "study_materials/",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
)
all_pages = loader.load()
print(f"Loaded {len(all_pages)} pages from all PDFs")
```

### Handling Scanned PDFs (OCR)

Some PDFs are scanned images, not real text. You need OCR (Optical Character Recognition) for these.

```python
# pip install unstructured pdf2image pytesseract
from langchain_community.document_loaders import UnstructuredPDFLoader

loader = UnstructuredPDFLoader("scanned_document.pdf", mode="elements")
docs = loader.load()
```

---

## Loading Web Pages

Pull content from websites directly into your application.

### Single Web Page

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://docs.python.org/3/tutorial/")
docs = loader.load()

print(f"Loaded {len(docs)} document(s)")
print(docs[0].page_content[:500])
```

**Install:** `pip install beautifulsoup4`

### Multiple Web Pages

```python
loader = WebBaseLoader([
    "https://docs.python.org/3/tutorial/classes.html",
    "https://docs.python.org/3/tutorial/errors.html",
    "https://docs.python.org/3/tutorial/modules.html",
])
docs = loader.load()
print(f"Loaded {len(docs)} pages")
```

### Recursive Web Loader (Crawl a Whole Site)

```python
from langchain_community.document_loaders import RecursiveUrlLoader

loader = RecursiveUrlLoader(
    url="https://docs.python.org/3/tutorial/",
    max_depth=2,        # How deep to crawl
    prevent_outside=True  # Stay on the same domain
)
docs = loader.load()
```

---

## Loading CSV Files

Each row in the CSV becomes a separate document.

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("students.csv")
docs = loader.load()

# Each row is a document
for doc in docs[:3]:
    print(doc.page_content)
    print("---")
```

**Example output for a student CSV:**

```
Name: Rahul Sharma
City: Bhopal
Course: Python Full Stack
Fee Paid: 45000
---
Name: Priya Patel
City: Indore
Course: Web Development
Fee Paid: 30000
---
```

### Custom CSV Loading

```python
loader = CSVLoader(
    "students.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
    },
    source_column="Name",      # Use this column as the source in metadata
)
```

---

## Loading from Notion

If your team uses Notion for documentation, you can load pages directly.

```python
from langchain_community.document_loaders import NotionDBLoader

loader = NotionDBLoader(
    integration_token="your-notion-token",
    database_id="your-database-id",
)
docs = loader.load()
```

**Install:** `pip install notion-client`

---

## Loading from GitHub

Load code files from a GitHub repository.

```python
from langchain_community.document_loaders import GitHubLoader

loader = GitHubLoader(
    repo="techpath/python-course",
    access_token="your-github-token",
    file_filter=lambda file_path: file_path.endswith(".py"),
)
docs = loader.load()
```

---

## Loading JSON Files

```python
from langchain_community.document_loaders import JSONLoader

# Load a JSON file -- specify which field contains the text
loader = JSONLoader(
    file_path="courses.json",
    jq_schema=".courses[].description",   # Extract course descriptions
    text_content=False,
)
docs = loader.load()
```

---

## Custom Document Loader

If none of the built-in loaders fit your needs, you can create your own.

```python
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader

class TechPathCourseLoader(BaseLoader):
    """Custom loader for TechPath course data."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load(self) -> list[Document]:
        documents = []
        with open(self.file_path, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    name, fee, duration = parts
                    doc = Document(
                        page_content=f"Course: {name}. Fee: Rs {fee}. Duration: {duration}.",
                        metadata={"source": self.file_path, "course": name.strip()},
                    )
                    documents.append(doc)
        return documents

# Usage
loader = TechPathCourseLoader("courses.txt")
docs = loader.load()
```

---

## Comparison of All Loaders

| Loader | Source | Install | One Doc or Many? | Metadata |
|--------|--------|---------|-----------------|----------|
| `TextLoader` | `.txt` files | Built-in | 1 document | source |
| `PyPDFLoader` | PDF files | `pip install pypdf` | 1 per page | source, page |
| `CSVLoader` | CSV files | Built-in | 1 per row | source, row |
| `WebBaseLoader` | Web URLs | `pip install beautifulsoup4` | 1 per page | source, title |
| `JSONLoader` | JSON files | `pip install jq` | Depends on schema | source |
| `NotionDBLoader` | Notion | `pip install notion-client` | 1 per page | source |
| `GitHubLoader` | GitHub repos | Built-in | 1 per file | source, path |
| `DirectoryLoader` | Folders | Built-in | Multiple | source |

---

## Best Practices

| Practice | Why |
|----------|-----|
| Always check `len(docs)` after loading | Make sure your loader actually found content |
| Print `docs[0].page_content[:200]` | Verify the content looks correct before processing |
| Check `docs[0].metadata` | Make sure source information is captured for citations |
| Use `DirectoryLoader` for bulk loading | Loads all files from a folder matching a pattern |
| Handle encoding errors | Use `TextLoader("file.txt", encoding="utf-8")` |
| Filter large files | Some PDFs have hundreds of pages -- load only what you need |

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Document Loader | Reads data from files/URLs into LangChain Document objects |
| Document object | Has `page_content` (text) and `metadata` (source info) |
| PyPDFLoader | Loads PDFs, one document per page |
| WebBaseLoader | Loads web pages, extracts text |
| CSVLoader | Loads CSVs, one document per row |
| DirectoryLoader | Loads all matching files from a folder |
| Custom Loader | Extend `BaseLoader` for your own formats |

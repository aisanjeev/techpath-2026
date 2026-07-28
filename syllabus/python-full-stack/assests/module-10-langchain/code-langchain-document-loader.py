"""
TechPath Institute -- LangChain Document Loaders & Text Splitters
==================================================================
Demonstrates loading documents from different sources (text, CSV, web)
and splitting them into chunks using various text splitters.

Install required packages:
    pip install langchain langchain-community beautifulsoup4 pypdf

Run this file:
    python code-langchain-document-loader.py
"""

import os
import csv
import tempfile

print("=" * 60)
print("TechPath Institute -- Document Loaders & Text Splitters")
print("=" * 60)


# ──────────────────────────────────────────────
# 1. LOADING TEXT FILES
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("1. LOADING TEXT FILES")
print("=" * 60)

# First, create a sample text file with TechPath course information
sample_text = """TechPath Institute - Python Full Stack Course

About TechPath:
TechPath Institute is a leading IT training center based in Bhopal, Madhya Pradesh.
We specialize in industry-aligned courses that prepare students for real-world jobs
in software development, AI, and data science. Our campus is located near MP Nagar,
Zone-II, the commercial hub of Bhopal.

Course Overview:
The Python Full Stack course is a 6-month intensive program designed for beginners.
No prior programming experience is required. Students learn everything from Python
basics to building and deploying full-stack web applications.

What You Will Learn:
- Python programming (core + advanced)
- Web development with Django and FastAPI
- Frontend with HTML, CSS, JavaScript, and React
- Database design with SQL and SQLAlchemy
- REST API development and testing
- Git and GitHub for version control
- GenAI and LangChain for building AI applications
- Docker and CI/CD for deployment

Fee Structure:
The course fee is Rs 45,000 (including GST).
EMI options: 3-month or 6-month no-cost EMI available through partner banks.
Early bird discount: Rs 5,000 off for enrollments before batch start date.
Women in Tech scholarship: 15% fee waiver for female students.

Placement Support:
TechPath has a dedicated placement cell with connections to top IT companies.
Our placement rate is 85% within 3 months of course completion.
Average starting package for freshers: Rs 4-6 LPA.
Top recruiters include TCS, Infosys, Wipro, HCL, and various startups.

Contact:
Email: info@techpath.biz
Phone: +91 98765 43210
Address: 2nd Floor, Tech Tower, MP Nagar Zone-II, Bhopal, MP 462011
"""

# Save the sample text to a file
text_file_path = os.path.join(tempfile.gettempdir(), "techpath_courses.txt")
with open(text_file_path, "w", encoding="utf-8") as f:
    f.write(sample_text)

print(f"Created sample text file: {text_file_path}")

# Load using LangChain's TextLoader
from langchain_community.document_loaders import TextLoader

loader = TextLoader(text_file_path, encoding="utf-8")
documents = loader.load()

print(f"\nLoaded {len(documents)} document(s) from text file")
print(f"Document length: {len(documents[0].page_content)} characters")
print(f"Metadata: {documents[0].metadata}")
print(f"\nFirst 200 characters:")
print(f"  \"{documents[0].page_content[:200]}...\"")


# ──────────────────────────────────────────────
# 2. LOADING CSV FILES
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("2. LOADING CSV FILES")
print("=" * 60)

# Create a sample CSV with student data
csv_file_path = os.path.join(tempfile.gettempdir(), "techpath_students.csv")

students = [
    ["Name", "City", "Course", "Batch", "Fee Paid (Rs)", "Status"],
    ["Rahul Sharma", "Bhopal", "Python Full Stack", "Jan 2026", "45000", "Active"],
    ["Priya Patel", "Indore", "Python Full Stack", "Jan 2026", "38250", "Active"],
    ["Amit Verma", "Delhi", "AI/ML", "Feb 2026", "35000", "Active"],
    ["Neha Gupta", "Pune", "Python Full Stack", "Jan 2026", "45000", "Completed"],
    ["Ananya Singh", "Bhopal", "Data Science", "Mar 2026", "40000", "Active"],
    ["Vikram Joshi", "Bhopal", "Python Full Stack", "Jan 2026", "40000", "Active"],
    ["Deepika Rao", "Indore", "AI/ML", "Feb 2026", "29750", "Active"],
    ["Arjun Malhotra", "Delhi", "Python Full Stack", "Mar 2026", "45000", "Enrolled"],
]

with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(students)

print(f"Created sample CSV file: {csv_file_path}")

# Load using LangChain's CSVLoader
from langchain_community.document_loaders import CSVLoader

csv_loader = CSVLoader(csv_file_path, encoding="utf-8")
csv_documents = csv_loader.load()

print(f"\nLoaded {len(csv_documents)} documents from CSV (one per row)")
print("\nFirst 3 documents:")
for i, doc in enumerate(csv_documents[:3]):
    print(f"\n  Document {i + 1}:")
    print(f"  {doc.page_content}")
    print(f"  Metadata: {doc.metadata}")


# ──────────────────────────────────────────────
# 3. LOADING WEB PAGES
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("3. LOADING WEB PAGES")
print("=" * 60)

# WebBaseLoader fetches a web page and extracts text
# Note: This requires internet access and beautifulsoup4
try:
    from langchain_community.document_loaders import WebBaseLoader

    # Load the Python official tutorial page
    url = "https://docs.python.org/3/tutorial/index.html"
    print(f"Loading web page: {url}")
    print("(This requires internet access...)")

    web_loader = WebBaseLoader(url)
    web_docs = web_loader.load()

    print(f"\nLoaded {len(web_docs)} document(s) from web")
    print(f"Content length: {len(web_docs[0].page_content)} characters")
    print(f"Metadata: {web_docs[0].metadata}")
    print(f"\nFirst 300 characters:")
    # Clean up whitespace for display
    clean_text = " ".join(web_docs[0].page_content.split())
    print(f"  \"{clean_text[:300]}...\"")

except Exception as e:
    print(f"  Web loading skipped (requires internet): {e}")
    print("  Install: pip install beautifulsoup4")


# ──────────────────────────────────────────────
# 4. TEXT SPLITTERS -- Breaking documents into chunks
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("4. TEXT SPLITTERS")
print("=" * 60)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)

# Use our TechPath course text for splitting demos
text = sample_text

# ── 4a. RecursiveCharacterTextSplitter (most common) ──

print("\n--- 4a. RecursiveCharacterTextSplitter ---")
print("Tries to split by paragraphs, then sentences, then words.")

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=30,
    separators=["\n\n", "\n", ". ", " ", ""],
)

recursive_chunks = recursive_splitter.split_text(text)

print(f"\nSettings: chunk_size=300, chunk_overlap=30")
print(f"Result: {len(recursive_chunks)} chunks\n")

for i, chunk in enumerate(recursive_chunks):
    print(f"  Chunk {i + 1} ({len(chunk)} chars):")
    # Show first and last 50 characters
    if len(chunk) > 100:
        print(f"    Start: \"{chunk[:60]}...\"")
        print(f"    End:   \"...{chunk[-60:]}\"")
    else:
        print(f"    \"{chunk}\"")
    print()

# ── 4b. CharacterTextSplitter (splits on a single separator) ──

print("\n--- 4b. CharacterTextSplitter ---")
print("Splits on a single character/separator.")

char_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separator="\n\n",  # Split only on double newlines (paragraphs)
)

char_chunks = char_splitter.split_text(text)

print(f"\nSettings: chunk_size=500, chunk_overlap=50, separator='\\n\\n'")
print(f"Result: {len(char_chunks)} chunks\n")

for i, chunk in enumerate(char_chunks):
    first_line = chunk.split("\n")[0]
    print(f"  Chunk {i + 1} ({len(chunk)} chars): \"{first_line}...\"")


# ──────────────────────────────────────────────
# 5. COMPARING CHUNK SIZES AND OVERLAPS
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("5. CHUNK SIZE AND OVERLAP COMPARISON")
print("=" * 60)

# Test different configurations
configs = [
    {"chunk_size": 200, "chunk_overlap": 0,   "label": "Small chunks, no overlap"},
    {"chunk_size": 200, "chunk_overlap": 50,  "label": "Small chunks, 50 overlap"},
    {"chunk_size": 500, "chunk_overlap": 50,  "label": "Medium chunks, 50 overlap"},
    {"chunk_size": 500, "chunk_overlap": 100, "label": "Medium chunks, 100 overlap"},
    {"chunk_size": 1000, "chunk_overlap": 100, "label": "Large chunks, 100 overlap"},
]

print(f"\nOriginal text length: {len(text)} characters\n")
print(f"{'Configuration':<40} {'Chunks':>8} {'Avg Size':>10} {'Total Chars':>12}")
print("-" * 72)

for config in configs:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunk_size"],
        chunk_overlap=config["chunk_overlap"],
    )
    chunks = splitter.split_text(text)

    total_chars = sum(len(c) for c in chunks)
    avg_size = total_chars // len(chunks) if chunks else 0

    print(f"{config['label']:<40} {len(chunks):>8} {avg_size:>10} {total_chars:>12}")

print("\nKey observations:")
print("  - Smaller chunk_size = more chunks (more precise retrieval)")
print("  - Larger chunk_size = fewer chunks (more context per chunk)")
print("  - Overlap increases total characters but prevents information loss")
print("  - Recommended starting point: chunk_size=500, chunk_overlap=50")


# ──────────────────────────────────────────────
# 6. SPLITTING DOCUMENTS (not just text)
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("6. SPLITTING DOCUMENT OBJECTS (preserves metadata)")
print("=" * 60)

from langchain_core.documents import Document

# Create Document objects with metadata (like a real loader would)
documents_with_metadata = [
    Document(
        page_content="""TechPath Institute offers Python Full Stack, AI/ML, and
Data Science courses. All courses include placement assistance and certificate.
The Bhopal campus has modern computer labs with high-speed internet.""",
        metadata={"source": "brochure.txt", "page": 1},
    ),
    Document(
        page_content="""Student reviews for TechPath Institute:
Rahul from Bhopal: "Excellent trainers, practical approach, got placed at Rs 5.2 LPA."
Priya from Indore: "Zero to hero in 6 months. Now working as a Django developer."
Ananya from Delhi: "Online batch was smooth. Good support from the team."
Amit from Pune: "The AI modules are world-class. Worth every rupee." """,
        metadata={"source": "reviews.txt", "page": 1},
    ),
]

# Split documents (metadata is preserved in each chunk)
doc_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
)

split_docs = doc_splitter.split_documents(documents_with_metadata)

print(f"\nOriginal: {len(documents_with_metadata)} documents")
print(f"After splitting: {len(split_docs)} chunks\n")

for i, doc in enumerate(split_docs):
    print(f"  Chunk {i + 1}:")
    print(f"    Source: {doc.metadata['source']}, Page: {doc.metadata['page']}")
    print(f"    Content ({len(doc.page_content)} chars): \"{doc.page_content[:80]}...\"")
    print()

print("Notice: Each chunk keeps the metadata from the original document.")
print("This is important for RAG -- you can cite which source an answer came from.")


# ──────────────────────────────────────────────
# 7. SUMMARY
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
Document Loaders -- Bring data into LangChain:
  - TextLoader:     Load .txt files
  - CSVLoader:      Load CSV files (one document per row)
  - PyPDFLoader:    Load PDF files (one document per page)
  - WebBaseLoader:  Load web pages (requires beautifulsoup4)

Text Splitters -- Break documents into smaller chunks:
  - RecursiveCharacterTextSplitter:  Best for most use cases
  - CharacterTextSplitter:          Simple, splits on one separator

Key Settings:
  - chunk_size:    Maximum characters per chunk (start with 500)
  - chunk_overlap: Characters shared between chunks (start with 50)

Next Steps:
  - Use these chunks with embeddings and vector stores
  - See code-langchain-rag-pipeline.py for the full RAG pipeline
""")

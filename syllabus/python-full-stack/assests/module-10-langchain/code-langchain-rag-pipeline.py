"""
TechPath Institute -- LangChain RAG Pipeline
==============================================
A complete Retrieval Augmented Generation (RAG) pipeline that:
  1. Loads sample documents about TechPath courses
  2. Splits text into chunks
  3. Creates embeddings and stores them in FAISS
  4. Builds a retrieval chain
  5. Answers questions with source citations

Install required packages:
    pip install langchain langchain-openai langchain-community faiss-cpu python-dotenv

Set your OpenAI API key:
    Option A: Create a .env file with OPENAI_API_KEY=sk-your-key-here
    Option B: Set environment variable: export OPENAI_API_KEY=sk-your-key-here

Run this file:
    python code-langchain-rag-pipeline.py
"""

import os
from dotenv import load_dotenv

# ──────────────────────────────────────────────
# 0. SETUP -- Load API key from .env file
# ──────────────────────────────────────────────

load_dotenv()

# Check that the API key is set
if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: Please set OPENAI_API_KEY in your .env file or environment.")
    print("Create a .env file with this line:")
    print("  OPENAI_API_KEY=sk-your-key-here")
    exit(1)

print("=" * 60)
print("TechPath Institute -- RAG Pipeline Demo")
print("=" * 60)


# ──────────────────────────────────────────────
# 1. SAMPLE DATA -- TechPath course information
# ──────────────────────────────────────────────
# In a real project, you would load this from PDFs, databases,
# or web pages. Here we use sample text for demonstration.

print("\n[Step 1] Preparing sample documents...")

techpath_documents = [
    {
        "content": """TechPath Institute is a premier IT training center located in Bhopal,
Madhya Pradesh. Founded in 2024, TechPath offers industry-aligned courses in
software development, AI/ML, and data science. The institute is located near
MP Nagar, Zone-II, which is the commercial hub of Bhopal. Online batches are
available for students in Delhi, Pune, Indore, and other cities across India.""",
        "source": "about-techpath.txt",
    },
    {
        "content": """Python Full Stack Course at TechPath Institute:
- Duration: 6 months (24 weeks)
- Fee: Rs 45,000 (including GST). EMI options available.
- Schedule: Monday to Friday, 10:00 AM to 1:00 PM
- Mode: Classroom (Bhopal campus) or Online (live classes)
- Batch Size: Maximum 20 students per batch
- Prerequisites: Basic computer knowledge. No programming experience needed.
- Certificate: TechPath Institute Completion Certificate provided.""",
        "source": "python-course-details.txt",
    },
    {
        "content": """Python Full Stack Course Curriculum:
Module 1-2: Python Core and Advanced Python
Module 3: Python Libraries (NumPy, Pandas, Matplotlib)
Module 4: Database Design with SQL and SQLAlchemy
Module 5: Git and GitHub for version control
Module 6: FastAPI -- Building REST APIs
Module 7: Django and Django REST Framework
Module 8: Frontend with HTML, CSS, JavaScript, React
Module 9: GenAI Fundamentals
Module 10: LangChain -- Building LLM Applications
Module 11: LangGraph -- Multi-Agent Systems
Module 12-17: Advanced topics and Capstone Project""",
        "source": "curriculum.txt",
    },
    {
        "content": """Placement Assistance at TechPath Institute:
- Dedicated placement cell with industry connections
- Resume building and LinkedIn profile optimization
- Mock interviews conducted by industry professionals
- Average starting package: Rs 4-6 LPA for freshers
- Top recruiters: TCS, Infosys, Wipro, HCL, and startups
- 85% placement rate within 3 months of course completion
- Internship opportunities during the last 2 months of the course""",
        "source": "placements.txt",
    },
    {
        "content": """TechPath Institute AI/ML Course:
- Duration: 4 months
- Fee: Rs 35,000 (including GST)
- Covers: Machine Learning, Deep Learning, NLP, Computer Vision
- Tools: Python, TensorFlow, PyTorch, Scikit-learn
- Projects: Sentiment analysis, image classification, chatbot
- Schedule: Saturday and Sunday, 10:00 AM to 2:00 PM (weekend batch)""",
        "source": "aiml-course.txt",
    },
    {
        "content": """Student Testimonials:
Rahul Sharma (Batch 2025): "The Python Full Stack course at TechPath was
excellent. The trainers explain concepts in simple Hindi and English. I got
placed at an IT company in Pune with Rs 5.2 LPA package."

Priya Patel (Batch 2025): "I had zero coding experience before joining.
The step-by-step teaching style helped me learn at my own pace. Now I work
as a Django developer in Indore."

Amit Verma (Batch 2026): "The LangChain and AI modules are the best part.
Building real AI applications gave me confidence for interviews." """,
        "source": "testimonials.txt",
    },
    {
        "content": """TechPath Institute Contact Information:
- Address: 2nd Floor, Tech Tower, MP Nagar Zone-II, Bhopal, MP 462011
- Phone: +91 98765 43210
- Email: info@techpath.biz
- Website: https://techpath.biz
- Office Hours: Monday to Saturday, 9:00 AM to 6:00 PM
- Admission Process: Fill online form -> Counseling call -> Fee payment -> Batch allotment""",
        "source": "contact.txt",
    },
    {
        "content": """Scholarship and Fee Concession at TechPath Institute:
- Early bird discount: Rs 5,000 off for enrollments before batch start date
- Sibling discount: 10% off for second sibling enrolling
- Women in Tech scholarship: 15% fee waiver for female students
- Merit scholarship: Top 3 students in each batch get Rs 5,000 cashback
- EMI available: 3-month and 6-month no-cost EMI through partner banks""",
        "source": "scholarships.txt",
    },
]

print(f"   Loaded {len(techpath_documents)} documents")
for doc in techpath_documents:
    print(f"   - {doc['source']} ({len(doc['content'])} characters)")


# ──────────────────────────────────────────────
# 2. TEXT SPLITTING -- Break documents into chunks
# ──────────────────────────────────────────────

print("\n[Step 2] Splitting documents into chunks...")

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Create a text splitter
# chunk_size=500 means each chunk will be at most 500 characters
# chunk_overlap=50 means chunks share 50 characters at boundaries
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)

# Split each document and keep track of the source
from langchain_core.documents import Document

all_chunks = []
for doc_info in techpath_documents:
    chunks = splitter.split_text(doc_info["content"])
    for chunk in chunks:
        all_chunks.append(
            Document(
                page_content=chunk,
                metadata={"source": doc_info["source"]},
            )
        )

print(f"   Split into {len(all_chunks)} chunks")
print(f"   Average chunk size: {sum(len(c.page_content) for c in all_chunks) // len(all_chunks)} characters")

# Show a sample chunk
print(f"\n   Sample chunk (from {all_chunks[0].metadata['source']}):")
print(f"   \"{all_chunks[0].page_content[:100]}...\"")


# ──────────────────────────────────────────────
# 3. EMBEDDINGS + VECTOR STORE -- Store chunks in FAISS
# ──────────────────────────────────────────────

print("\n[Step 3] Creating embeddings and storing in FAISS...")

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Create the embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create FAISS vector store from our chunks
# This converts each chunk into a vector and stores it
vectorstore = FAISS.from_documents(all_chunks, embeddings)

print(f"   Vector store created with {len(all_chunks)} vectors")

# Save to disk so we can reuse it later without re-embedding
save_path = "techpath_faiss_index"
vectorstore.save_local(save_path)
print(f"   Saved to disk at: ./{save_path}/")

# Test: search for similar documents
print("\n   Quick test -- searching for 'course fee':")
test_results = vectorstore.similarity_search("course fee", k=2)
for i, doc in enumerate(test_results, 1):
    print(f"   Result {i} (from {doc.metadata['source']}):")
    print(f"     \"{doc.page_content[:120]}...\"")


# ──────────────────────────────────────────────
# 4. RAG CHAIN -- Retriever + Prompt + LLM
# ──────────────────────────────────────────────

print("\n[Step 4] Building the RAG chain...")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Create a retriever (searches the vector store)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},  # Return top 3 most relevant chunks
)

# Create the RAG prompt template
rag_prompt = ChatPromptTemplate.from_template("""You are a helpful assistant
for TechPath Institute in Bhopal. Answer the student's question based ONLY
on the context provided below. If the answer is not in the context, say
"I don't have that information. Please contact TechPath at info@techpath.biz."

Keep your answer concise and friendly. Use simple English.

Context:
{context}

Student's Question: {question}

Answer:""")

# Create the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Helper: format retrieved documents into a single string
def format_docs(docs):
    """Join document contents with source labels."""
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        formatted.append(f"[Source: {source}]\n{doc.page_content}")
    return "\n\n".join(formatted)

# Build the RAG chain using LCEL (pipe operator)
# Step by step:
#   1. retriever finds relevant chunks for the question
#   2. format_docs converts them to a string
#   3. The prompt template fills in {context} and {question}
#   4. The LLM generates an answer
#   5. The parser extracts the text string
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)

print("   RAG chain built successfully!")


# ──────────────────────────────────────────────
# 5. ASK QUESTIONS -- Test the RAG pipeline
# ──────────────────────────────────────────────

print("\n[Step 5] Testing the RAG pipeline with sample questions...\n")

# Sample questions that students might ask
questions = [
    "What is the fee for the Python Full Stack course?",
    "Where is TechPath Institute located?",
    "What is the placement record at TechPath?",
    "Do you offer any scholarships or discounts?",
    "What programming languages are taught in the curriculum?",
]

for i, question in enumerate(questions, 1):
    print(f"Q{i}: {question}")
    answer = rag_chain.invoke(question)
    print(f"A{i}: {answer}")
    print("-" * 60)


# ──────────────────────────────────────────────
# 6. RAG WITH SOURCE CITATIONS
# ──────────────────────────────────────────────

print("\n[Step 6] RAG with source citations...\n")

def answer_with_sources(question):
    """Answer a question and show which documents were used."""
    # Retrieve relevant documents
    docs = retriever.invoke(question)

    # Format context
    context = format_docs(docs)

    # Get answer from LLM
    answer = rag_chain.invoke(question)

    # Collect unique sources
    sources = list(set(doc.metadata.get("source", "unknown") for doc in docs))

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "num_chunks_used": len(docs),
    }

# Test with source citations
question = "Tell me about EMI options and discounts at TechPath."
result = answer_with_sources(question)

print(f"Question: {result['question']}")
print(f"Answer: {result['answer']}")
print(f"Sources used: {', '.join(result['sources'])}")
print(f"Chunks retrieved: {result['num_chunks_used']}")


# ──────────────────────────────────────────────
# 7. INTERACTIVE MODE (Optional)
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("INTERACTIVE MODE")
print("Type your questions about TechPath Institute.")
print("Type 'quit' to exit.")
print("=" * 60)

while True:
    question = input("\nYour question: ").strip()
    if question.lower() in ("quit", "exit", "q"):
        print("Thank you for using TechPath AI Assistant!")
        break
    if not question:
        print("Please enter a question.")
        continue

    result = answer_with_sources(question)
    print(f"\nAnswer: {result['answer']}")
    print(f"(Sources: {', '.join(result['sources'])})")

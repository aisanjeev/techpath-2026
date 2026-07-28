# Agentic RAG

**Module 11 -- LangGraph | Topic 8**

---

## What is Agentic RAG?

Regular RAG (Retrieval-Augmented Generation) does a one-shot search: get documents, generate answer, done. **Agentic RAG** adds intelligence -- the agent can decide whether to search, rewrite the query if results are poor, search multiple times, and verify the answer quality before responding.

**Analogy:** 
- **Regular RAG** = A student who looks up one page in the textbook and writes the answer, even if the page was wrong.
- **Agentic RAG** = A student who checks the answer, realizes the page was not quite right, tries a different chapter, finds better information, and then writes a confident answer.

| Feature | Regular RAG | Agentic RAG |
|---------|------------|-------------|
| Query | Single fixed query | Rewrites query if needed |
| Search | One-shot | Multiple attempts |
| Quality check | None | Grades document relevance |
| Answer check | None | Verifies answer quality |
| Fallback | Returns whatever it gets | Retries or says "I don't know" |

---

## The Agentic RAG Flow

```
User Question
     |
     v
  +--+---+        +----------+
  | Route |------->| Direct   |  (Agent already knows the answer)
  +--+---+        | Answer   |
     |             +----------+
     v
  +--+--------+
  | Rewrite   |  (Improve the search query)
  | Query     |
  +--+--------+
     |
     v
  +--+--------+
  | Search    |  (Query the vector store)
  | Documents |
  +--+--------+
     |
     v
  +--+--------+      +----------+
  | Grade     |--NO-->| Rewrite  |  (Documents not relevant? Try different query)
  | Documents |       | & Retry  |
  +--+--------+       +----------+
     |
     YES
     v
  +--+--------+
  | Generate  |  (Create the answer from documents)
  | Answer    |
  +--+--------+
     |
     v
  +--+-----------+      +----------+
  | Check Answer |--NO-->| Retry    |  (Answer not good? Search again)
  | Quality      |       | Search   |
  +--+-----------+       +----------+
     |
     YES
     v
  Final Answer
```

---

## Building Agentic RAG with LangGraph

### Step 1: Define the State

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class RAGState(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    documents: list
    generation: str
    retry_count: int
```

### Step 2: Create the Nodes

#### Route Node -- Decide Whether to Search

```python
def route_node(state):
    """Decide if we need to search or can answer directly."""
    question = state["question"]
    
    response = llm.invoke([
        ("system", """You are a router. Decide if the question needs document search.
        Reply ONLY with "search" or "direct".
        - "search" if the question is about TechPath courses, fees, schedules, etc.
        - "direct" if it is a greeting or general knowledge question."""),
        ("human", question),
    ])
    
    decision = response.content.strip().lower()
    return {"route": decision}
```

#### Retrieve Node -- Search the Vector Store

```python
def retrieve_node(state):
    """Search the document store for relevant information."""
    question = state["question"]
    docs = vector_store.similarity_search(question, k=4)
    return {"documents": docs}
```

#### Grade Documents Node -- Check Relevance

```python
def grade_documents_node(state):
    """Check if retrieved documents are actually relevant to the question."""
    docs = state["documents"]
    question = state["question"]
    
    graded_docs = []
    for doc in docs:
        score = llm.invoke([
            ("system", "You are a relevance grader. Reply ONLY 'yes' or 'no'."),
            ("human", f"Is this document relevant to the question '{question}'?\n\nDocument: {doc.page_content}"),
        ])
        if "yes" in score.content.lower():
            graded_docs.append(doc)
    
    return {"documents": graded_docs}
```

#### Rewrite Query Node -- Improve the Search

```python
def rewrite_query_node(state):
    """Rewrite the query for better search results."""
    question = state["question"]
    
    rewritten = llm.invoke([
        ("system", "Rewrite this search query to get better results from a course information database. Return only the rewritten query."),
        ("human", question),
    ])
    
    return {
        "question": rewritten.content,
        "retry_count": state.get("retry_count", 0) + 1,
    }
```

#### Generate Node -- Create the Answer

```python
def generate_node(state):
    """Generate an answer using the relevant documents."""
    docs = state["documents"]
    question = state["question"]
    context = "\n\n".join([doc.page_content for doc in docs])
    
    answer = llm.invoke([
        ("system", """Answer the question based ONLY on the context provided.
        If the context does not contain the answer, say "I don't have that information."
        Be specific and include relevant details like fees, durations, etc."""),
        ("human", f"Context:\n{context}\n\nQuestion: {question}"),
    ])
    
    return {"generation": answer.content}
```

#### Check Answer Quality Node

```python
def check_answer_node(state):
    """Verify the generated answer is good enough."""
    answer = state["generation"]
    question = state["question"]
    
    check = llm.invoke([
        ("system", """You are an answer quality checker. 
        Reply ONLY 'pass' or 'fail'.
        - 'pass' if the answer addresses the question with specific information
        - 'fail' if the answer is vague, says "I don't know", or is incomplete"""),
        ("human", f"Question: {question}\nAnswer: {answer}"),
    ])
    
    return {"quality": check.content.strip().lower()}
```

### Step 3: Define Routing Logic

```python
def route_after_grading(state) -> str:
    """After grading documents: generate answer or retry search."""
    if not state["documents"]:
        if state.get("retry_count", 0) < 3:
            return "rewrite"      # No good docs -- try a different query
        return "give_up"          # Tried 3 times -- give up gracefully
    return "generate"             # Good docs found -- generate answer

def route_after_quality(state) -> str:
    """After checking answer quality: return or retry."""
    if state.get("quality") == "pass":
        return "end"
    if state.get("retry_count", 0) < 3:
        return "rewrite"
    return "end"                  # Return what we have after 3 tries
```

### Step 4: Build the Graph

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(RAGState)

# Add nodes
graph.add_node("retrieve", retrieve_node)
graph.add_node("grade", grade_documents_node)
graph.add_node("rewrite", rewrite_query_node)
graph.add_node("generate", generate_node)
graph.add_node("check", check_answer_node)

# Add edges
graph.add_edge("retrieve", "grade")
graph.add_edge("rewrite", "retrieve")
graph.add_edge("generate", "check")

# Conditional edges
graph.add_conditional_edges("grade", route_after_grading, {
    "generate": "generate",
    "rewrite": "rewrite",
    "give_up": END,
})
graph.add_conditional_edges("check", route_after_quality, {
    "end": END,
    "rewrite": "rewrite",
})

graph.set_entry_point("retrieve")
app = graph.compile()
```

### Step 5: Run It

```python
result = app.invoke({
    "question": "What is the Python course fee and EMI option?",
    "documents": [],
    "generation": "",
    "retry_count": 0,
    "messages": [],
})

print(result["generation"])
```

---

## Execution Example

```
Question: "What is the placement record at TechPath?"

Attempt 1:
  RETRIEVE: Searches for "placement record at TechPath"
  GRADE: 0 of 4 documents are relevant (about fees, not placement)
  REWRITE: "TechPath Institute placement statistics packages salary"

Attempt 2:
  RETRIEVE: Searches with rewritten query
  GRADE: 2 of 4 documents are relevant
  GENERATE: "TechPath provides placement assistance. Average package is Rs 4-6 LPA."
  CHECK: PASS

Final Answer: "TechPath provides placement assistance. Average package is Rs 4-6 LPA."
```

---

## Retry Limits

Always set a maximum number of retries to prevent infinite loops:

```python
MAX_RETRIES = 3

def route_after_grading(state) -> str:
    if not state["documents"]:
        if state.get("retry_count", 0) < MAX_RETRIES:
            return "rewrite"
        return "give_up"
    return "generate"
```

What happens at each retry count:

| Retry | Action | Why |
|-------|--------|-----|
| 0 | First search | Original query |
| 1 | Rewrite and search again | Original query did not find good results |
| 2 | Rewrite differently and search | Second query also missed |
| 3 | Give up gracefully | Say "I don't have that information" |

---

## When to Use Agentic RAG

| Scenario | Regular RAG | Agentic RAG |
|----------|------------|-------------|
| Simple FAQ ("What is the fee?") | Good enough | Overkill |
| Complex question ("Compare Python and Data Science courses") | May miss info | Better coverage |
| Vague question ("Tell me about everything") | Poor results | Rewrites to specific queries |
| Critical accuracy needed | May hallucinate | Quality checks catch errors |
| High query volume (1000/day) | Cheaper | More expensive (extra LLM calls) |

### Decision Guide

Use **Regular RAG** when:
- Questions are simple and specific
- Speed matters more than accuracy
- Budget is tight

Use **Agentic RAG** when:
- Questions are complex or vague
- Accuracy is critical
- Users expect high-quality answers

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| Agentic RAG | RAG with intelligence -- search, grade, rewrite, verify |
| Route node | Decides if search is needed or agent can answer directly |
| Grade documents | Checks if retrieved documents are actually relevant |
| Rewrite query | Rephrases the search query for better results |
| Quality check | Verifies the generated answer before returning it |
| Retry loop | Searches again with different queries if first attempt fails |
| Max retries | Always limit retries (3 is a good default) to prevent loops |
| Key advantage | Much higher answer quality than basic RAG |

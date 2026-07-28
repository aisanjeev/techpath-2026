# Chatbot Evaluation

**Module 12 -- AI Chatbots | Topic 7**

---

## Why Evaluate Your Chatbot?

Building a chatbot is easy. Building a **good** chatbot is hard. Without evaluation, you have no way to know if your chatbot is:
- Giving accurate answers
- Staying true to the source documents (not hallucinating)
- Actually answering the question that was asked
- Finding the right information from its knowledge base

**Analogy:** Imagine TechPath Institute hires a new receptionist. Before they start answering calls alone, you test them: "What is the Python course fee?" If they say the right answer, great. If they make up a number, that is a problem. Evaluation is this testing process, but automated.

---

## The RAGAS Framework

RAGAS (Retrieval-Augmented Generation Assessment) is the most popular framework for evaluating RAG chatbots. It measures four key qualities:

### The Four Metrics

| Metric | What It Measures | Example (Good) | Example (Bad) |
|--------|-----------------|-----------------|----------------|
| **Faithfulness** | Does the answer stick to the context? | "Fee is Rs 49,999" (context says 49,999) | "Fee is Rs 30,000" (made up) |
| **Answer Relevancy** | Does the answer address the question? | Q: "What is the fee?" A: "Rs 49,999" | Q: "What is the fee?" A: "We are in Bhopal" |
| **Context Precision** | Are the retrieved chunks relevant? | Retrieved chunks about fees | Retrieved chunks about weather |
| **Context Recall** | Did retrieval find ALL needed info? | Found both fee AND EMI info | Found fee but missed EMI options |

### Score Interpretation

| Score Range | Quality | Action |
|-------------|---------|--------|
| 0.9 - 1.0 | Excellent | No changes needed |
| 0.7 - 0.9 | Good | Minor improvements |
| 0.5 - 0.7 | Fair | Needs work on prompts or retrieval |
| Below 0.5 | Poor | Major issues -- rethink approach |

---

## Building Your Own Evaluation (Without RAGAS Library)

You can evaluate your chatbot using an LLM as a judge:

### Faithfulness Evaluator

Check if the answer is supported by the context (no hallucination):

```python
import anthropic

client = anthropic.Anthropic()

def evaluate_faithfulness(question: str, context: str, answer: str) -> float:
    """Check if the answer is fully supported by the context."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"""Rate from 0.0 to 1.0: Is this answer fully supported by the context?
            
            Context: {context}
            Question: {question}
            Answer: {answer}
            
            1.0 = Every claim in the answer is in the context
            0.5 = Some claims are in the context, some are not
            0.0 = The answer has no basis in the context
            
            Reply with ONLY a number between 0.0 and 1.0."""
        }],
    )
    return float(response.content[0].text.strip())
```

### Answer Relevancy Evaluator

Check if the answer actually addresses the question:

```python
def evaluate_relevancy(question: str, answer: str) -> float:
    """Check if the answer is relevant to the question."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"""Rate from 0.0 to 1.0: Does this answer address the question?
            
            Question: {question}
            Answer: {answer}
            
            1.0 = Answer directly and completely addresses the question
            0.5 = Answer partially addresses the question
            0.0 = Answer is completely off-topic
            
            Reply with ONLY a number between 0.0 and 1.0."""
        }],
    )
    return float(response.content[0].text.strip())
```

### Context Precision Evaluator

Check if the retrieved documents are actually relevant:

```python
def evaluate_context_precision(question: str, contexts: list[str]) -> float:
    """Check what fraction of retrieved contexts are relevant."""
    relevant_count = 0
    for ctx in contexts:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": f"Is this text relevant to the question '{question}'?\nText: {ctx}\nReply YES or NO."
            }],
        )
        if "yes" in response.content[0].text.lower():
            relevant_count += 1
    return relevant_count / len(contexts) if contexts else 0.0
```

---

## Building a Test Suite

Create a set of test questions with expected answers:

```python
test_cases = [
    {
        "question": "What is the Python Full Stack course fee?",
        "expected_answer": "Rs 49,999",
        "expected_context_topic": "fee",
    },
    {
        "question": "What are the batch timings?",
        "expected_answer": "10 AM to 1 PM",
        "expected_context_topic": "schedule",
    },
    {
        "question": "Do you provide placement assistance?",
        "expected_answer": "Yes",
        "expected_context_topic": "placement",
    },
    {
        "question": "Where is TechPath located?",
        "expected_answer": "Bhopal",
        "expected_context_topic": "location",
    },
    {
        "question": "What is the weather in Delhi?",
        "expected_answer": "I don't have that information",
        "expected_context_topic": "out_of_scope",
    },
]
```

### Running the Test Suite

```python
def run_evaluation(chatbot_fn, test_cases: list) -> dict:
    """Run all test cases and calculate scores."""
    results = []
    
    for test in test_cases:
        # Get chatbot response
        response = chatbot_fn(test["question"])
        answer = response["answer"]
        context = response.get("context", "")
        
        # Evaluate
        faith = evaluate_faithfulness(test["question"], context, answer)
        relevancy = evaluate_relevancy(test["question"], answer)
        
        results.append({
            "question": test["question"],
            "answer": answer,
            "faithfulness": faith,
            "relevancy": relevancy,
        })
    
    # Calculate averages
    avg_faith = sum(r["faithfulness"] for r in results) / len(results)
    avg_relevancy = sum(r["relevancy"] for r in results) / len(results)
    
    return {
        "results": results,
        "average_faithfulness": round(avg_faith, 2),
        "average_relevancy": round(avg_relevancy, 2),
    }

# Run evaluation
scores = run_evaluation(my_chatbot, test_cases)
print(f"Faithfulness: {scores['average_faithfulness']}")
print(f"Relevancy: {scores['average_relevancy']}")
```

---

## Common Evaluation Patterns

### Pattern 1: Golden Dataset

Create a "golden" dataset of correct question-answer pairs from a human expert:

```python
golden_dataset = [
    {"q": "Fee?", "a": "Rs 49,999", "source": "brochure page 2"},
    {"q": "Duration?", "a": "6 months", "source": "brochure page 1"},
]
```

### Pattern 2: A/B Testing

Compare two versions of your chatbot:

```python
def ab_test(question, chatbot_a, chatbot_b):
    answer_a = chatbot_a(question)
    answer_b = chatbot_b(question)
    
    # Judge which is better
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""Which answer is better for: "{question}"?
            Answer A: {answer_a}
            Answer B: {answer_b}
            Reply "A" or "B"."""
        }],
    )
    return response.content[0].text.strip()
```

### Pattern 3: User Feedback

The simplest evaluation -- let users rate responses:

```python
@app.post("/feedback")
async def save_feedback(conversation_id: str, rating: int, comment: str = ""):
    """Save user feedback (thumbs up/down)."""
    # rating: 1 = good, 0 = bad
    feedback_db.save({
        "conversation_id": conversation_id,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now(),
    })
    return {"message": "Thank you for your feedback!"}
```

---

## Improving Based on Evaluation

| Low Score In | Possible Cause | Fix |
|-------------|---------------|-----|
| Faithfulness | LLM making up info | Strengthen "answer only from context" prompt |
| Relevancy | Wrong docs retrieved | Improve embeddings or chunk size |
| Context Precision | Irrelevant chunks retrieved | Add metadata filtering, reduce k |
| Context Recall | Missing information | Add more documents, increase k |

---

## Summary

| Metric | What It Checks | Target Score |
|--------|---------------|-------------|
| Faithfulness | No hallucination -- answer is in the context | > 0.8 |
| Answer Relevancy | Answer addresses the actual question | > 0.7 |
| Context Precision | Retrieved documents are relevant | > 0.7 |
| Context Recall | All needed information was retrieved | > 0.7 |

| Evaluation Method | Cost | Accuracy |
|------------------|------|----------|
| LLM-as-judge | Moderate (API calls) | Good |
| Golden dataset comparison | Free (after creation) | High |
| User feedback | Free | Real-world but biased |
| A/B testing | Moderate | Very good for comparisons |

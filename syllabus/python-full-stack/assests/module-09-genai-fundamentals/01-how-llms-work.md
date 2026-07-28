# How Large Language Models Work

**Module 09 — Generative AI Fundamentals & Prompt Engineering | Topic 1**

---

## What is an LLM?

A Large Language Model (LLM) is a computer program that has read so much text that it can understand and generate human language. Think of it as a **super-smart autocomplete** that was trained on most of the internet.

When you type a message on WhatsApp and your phone suggests the next word — that is autocomplete. Now imagine that autocomplete read every book, every Wikipedia article, every StackOverflow answer, and every blog post ever written. That is an LLM.

**Examples of LLMs you may already know:**
- ChatGPT (by OpenAI)
- Claude (by Anthropic)
- Gemini (by Google)
- Llama (by Meta, open-source)

**Analogy:** Imagine Rahul is preparing for a competitive exam. He reads thousands of textbooks, previous year papers, and notes. After all that reading, he can answer questions on many topics — not because he memorized every answer, but because he understood the patterns. An LLM works the same way, except it has read billions of pages instead of thousands.

---

## The Transformer Architecture

Every modern LLM is built on an architecture called the **Transformer**, invented by Google researchers in 2017. Before Transformers, AI models read text one word at a time (left to right), like reading a sentence with a magnifying glass that shows only one word.

The Transformer changed everything with a concept called **attention**.

### The Attention Mechanism

**Analogy:** Imagine Priya is reading this sentence: "The bank of the river was covered in mud." When she sees the word "bank," she looks at the surrounding words ("river," "mud") to understand that "bank" means the side of a river, not a financial bank.

The attention mechanism does exactly this — **the model looks at ALL the words in a sentence simultaneously** to understand the meaning of each word based on its context.

```
Input:  "Amit went to the bank to deposit money"
                         ^^^^
The model looks at "deposit" and "money" to decide:
    bank = financial institution (not riverbank)
```

Without attention, the model would not know which meaning of "bank" to use. With attention, it connects related words no matter how far apart they are in the sentence.

### Why Transformers are Fast

Older models (RNNs) processed words one by one — like reading a book one word at a time. Transformers process all words at once — like seeing the whole page at a glance. This is why Transformers can be trained on massive datasets using powerful GPUs.

| Feature | Old Models (RNN/LSTM) | Transformers |
|---------|----------------------|-------------|
| Reads text | One word at a time | All words at once |
| Speed | Slow | Very fast (parallelizable) |
| Long text handling | Forgets early words | Remembers everything in context |
| Training time | Weeks | Days (with enough GPUs) |

---

## Tokens: The Language of LLMs

LLMs do not read words the way we do. They break text into smaller pieces called **tokens**. A token can be a whole word, part of a word, or even a single character.

### How Tokenization Works

```
Input:   "Sneha is learning Python programming"

Tokens:  ["Sne", "ha", " is", " learning", " Python", " programming"]
          (1)    (2)   (3)      (4)           (5)         (6)
```

Notice how "Sneha" became two tokens ("Sne" + "ha") because it is an uncommon name. Common English words like "learning" stay as one token.

**Rule of thumb:** 1 token is approximately 4 characters in English, or about 0.75 words.

| Text | Approximate Tokens |
|------|-------------------|
| "Hello" | 1 token |
| "Hello, how are you?" | 5 tokens |
| One paragraph (100 words) | ~130 tokens |
| One page (500 words) | ~650 tokens |
| A full novel (80,000 words) | ~100,000 tokens |

### Why Token Limits Matter

Every LLM has a **context window** — the maximum number of tokens it can handle in one conversation (input + output combined).

| Model | Context Window |
|-------|---------------|
| GPT-4o | 128,000 tokens (~96,000 words) |
| Claude 4 Sonnet | 200,000 tokens (~150,000 words) |
| Gemini 2.5 Pro | 1,000,000 tokens (~750,000 words) |

If your conversation exceeds the context window, the model starts "forgetting" the earliest messages. This is like having a notebook with limited pages — once it is full, you have to tear out old pages to write new ones.

**Pricing is also based on tokens.** When you use the API, you pay per token — both for what you send (input tokens) and what the model generates (output tokens). So understanding tokens helps you control costs.

---

## Embeddings: Words as Numbers

Computers cannot understand words directly. They need numbers. An **embedding** is a way to represent a word (or sentence) as a list of numbers — a point in a high-dimensional space.

**Analogy:** Think of a map of India. Delhi is at one location, and nearby cities like Noida and Gurgaon are close to it on the map. Similarly, in embedding space, words with similar meanings are "close" to each other.

```
"king"    → [0.21, 0.85, 0.43, 0.11, ...]   (768 numbers)
"queen"   → [0.23, 0.82, 0.45, 0.09, ...]   (very close to "king")
"bicycle" → [0.91, 0.12, 0.67, 0.55, ...]   (far from "king")
```

### Why Embeddings Matter

Because similar words have similar numbers, the model can understand relationships:

```
"king" - "man" + "woman" ≈ "queen"
"Delhi" - "India" + "Japan" ≈ "Tokyo"
```

This is how LLMs "understand" meaning — not by reading dictionaries, but by learning which words appear in similar contexts. If "chai" and "tea" appear in the same kind of sentences, the model learns they are related.

---

## How LLMs Are Trained

Training an LLM happens in three stages. Think of it like training a new employee at TechPath Institute.

### Stage 1: Pre-training (Learning Everything)

The model reads billions of pages from the internet — books, articles, code, conversations — and learns to predict the next word in a sentence.

```
Training example:
Input:  "The capital of India is ___"
Target: "New Delhi"

The model adjusts its internal numbers to get better at this prediction.
Repeated billions of times across millions of documents.
```

**Analogy:** This is like Ananya joining a library and reading every book. She does not have a specific job yet — she is just absorbing knowledge.

**Cost:** Pre-training GPT-4 reportedly cost over $100 million in compute. This is why only big companies can build LLMs from scratch.

### Stage 2: Fine-tuning (Learning a Specific Job)

After pre-training, the model knows a lot but is not good at following instructions. Fine-tuning trains it on curated question-answer pairs to make it helpful.

```
Question: "Write a Python function to add two numbers"
Expected answer: "def add(a, b):\n    return a + b"

Thousands of such examples teach the model to follow instructions.
```

**Analogy:** Ananya has read everything in the library. Now she joins TechPath Institute as a teaching assistant. She is trained specifically on how to answer student questions clearly.

### Stage 3: RLHF (Learning to Be Safe and Helpful)

RLHF stands for **Reinforcement Learning from Human Feedback**. Human reviewers rate the model's responses, and the model learns to generate responses that humans prefer.

```
Prompt: "How do I hack someone's WiFi?"

Response A: "Here are the steps to hack WiFi..."  ← Bad (harmful)
Response B: "I can't help with that. Instead, here's how to secure your own WiFi..." ← Good (safe)

Human reviewers mark Response B as better → model learns to prefer safe answers.
```

**Analogy:** Ananya's supervisor reviews her answers to students and gives feedback: "This answer was too technical — simplify it." Over time, Ananya learns to give better answers.

| Stage | What It Does | Analogy |
|-------|-------------|---------|
| Pre-training | Read the internet, learn language | Reading every book in the library |
| Fine-tuning | Learn to follow instructions | Training for a specific job |
| RLHF | Learn to be helpful and safe | Getting feedback from a supervisor |

---

## Inference: How the Model Generates Text

When you send a message to ChatGPT or Claude, the model generates its response **one token at a time**. This process is called **inference**.

```
Your prompt: "Write a greeting in Hindi"

Step 1: Model predicts first token  → "Nam"
Step 2: Model predicts next token   → "aste"
Step 3: Model predicts next token   → ","
Step 4: Model predicts next token   → " aap"
Step 5: Model predicts next token   → " kaise"
Step 6: Model predicts next token   → " hain"
Step 7: Model predicts next token   → "?"
Step 8: Model predicts [STOP]       → Generation complete

Final output: "Namaste, aap kaise hain?"
```

This is why you see text appearing word by word when you use ChatGPT — the model is literally generating one token at a time. Each new token is predicted based on everything that came before it (your prompt + all previously generated tokens).

### Why Responses Vary

At each step, the model does not just pick the single most likely next token. It considers multiple options with different probabilities:

```
After "The best programming language is":
  "Python"     → 35% probability
  "JavaScript" → 20% probability
  "it"         → 10% probability
  "subjective" → 8% probability
  ...
```

A setting called **temperature** controls how the model chooses among these options. We will cover temperature and other parameters in Topic 4.

---

## Key Takeaways

| Concept | One-Line Summary |
|---------|-----------------|
| LLM | A program trained on internet text to understand and generate language |
| Transformer | Architecture that looks at all words simultaneously using attention |
| Token | The smallest unit of text an LLM processes (roughly 4 characters) |
| Embedding | Words represented as numbers — similar words have similar numbers |
| Pre-training | Reading billions of pages to learn language patterns |
| Fine-tuning | Training on specific examples to follow instructions |
| RLHF | Learning from human feedback to be safe and helpful |
| Inference | Generating text one token at a time |

---

*TechPath Institute -- Python Full Stack with Gen AI*

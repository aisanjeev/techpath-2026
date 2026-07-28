# LLM Providers Comparison

**Module 09 — Generative AI Fundamentals & Prompt Engineering | Topic 2**

---

## Why Multiple Providers?

There is no single "best" LLM. Different models have different strengths, pricing, and limits. Choosing the right model for your project is like choosing the right vehicle — you would not use an auto-rickshaw to move furniture, and you would not hire a truck to go to the grocery store.

As a developer, you need to know what options exist so you can pick the best fit for your budget and use case.

---

## The Major LLM Providers

### 1. OpenAI (GPT Models)

OpenAI created ChatGPT and is the most popular LLM provider. Their models are known for strong general-purpose performance and excellent code generation.

**Key Models:**

| Model | Best For | Context Window | Notes |
|-------|---------|---------------|-------|
| GPT-4o | General tasks, coding, analysis | 128K tokens | Their flagship model — fast and capable |
| GPT-4o-mini | Simple tasks, high volume | 128K tokens | Cheap and quick — great for chatbots |
| o3 | Complex reasoning, math, code | 200K tokens | Reasoning model — thinks before answering |
| o4-mini | Reasoning on a budget | 200K tokens | Cheaper reasoning model |

**API Setup:**

```python
# Install: pip install openai
from openai import OpenAI

client = OpenAI(api_key="sk-...")  # Your API key

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain Python decorators simply"}
    ]
)
print(response.choices[0].message.content)
```

**Get your API key:** Go to [platform.openai.com](https://platform.openai.com), sign up, and navigate to API Keys. New accounts get $5 free credits (enough for thousands of API calls with GPT-4o-mini).

---

### 2. Anthropic (Claude Models)

Anthropic builds Claude, known for being especially good at long documents, careful reasoning, and following complex instructions. Claude has the largest standard context window among major providers.

**Key Models:**

| Model | Best For | Context Window | Notes |
|-------|---------|---------------|-------|
| Claude 4 Opus | Hardest tasks, deep analysis | 200K tokens | Most capable Claude model |
| Claude 4 Sonnet | Balanced performance and speed | 200K tokens | Best value for most tasks |
| Claude 4 Haiku | Quick responses, high volume | 200K tokens | Fast and affordable |

**API Setup:**

```python
# Install: pip install anthropic
from anthropic import Anthropic

client = Anthropic(api_key="sk-ant-...")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain Python decorators simply"}
    ]
)
print(message.content[0].text)
```

**Get your API key:** Go to [console.anthropic.com](https://console.anthropic.com), sign up, and create an API key. New accounts get $5 free credits.

---

### 3. Google (Gemini Models)

Google's Gemini models are built into Google's ecosystem (Search, Workspace, Android). They excel at multimodal tasks — handling text, images, video, and audio together. Gemini 2.5 Pro holds the record for the largest context window.

**Key Models:**

| Model | Best For | Context Window | Notes |
|-------|---------|---------------|-------|
| Gemini 2.5 Pro | Complex tasks, long documents | 1M tokens | Massive context window |
| Gemini 2.5 Flash | Fast responses, multimodal | 1M tokens | Very fast, good value |

**API Setup:**

```python
# Install: pip install google-genai
from google import genai

client = genai.Client(api_key="AIza...")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain Python decorators simply"
)
print(response.text)
```

**Get your API key:** Go to [aistudio.google.com](https://aistudio.google.com), sign in with your Google account. You get a generous free tier — great for students.

---

### 4. Mistral (European Provider)

Mistral is a French AI company known for efficient, high-quality models. Their open-weight models are popular for self-hosting — useful if you need to run an LLM on your own server for data privacy.

**Key Models:**

| Model | Best For | Context Window | Notes |
|-------|---------|---------------|-------|
| Mistral Large | Complex tasks, multilingual | 128K tokens | Their most capable model |
| Mistral Small | Simple tasks, fast | 32K tokens | Good for chatbots |

**API Setup:**

```python
# Install: pip install mistralai
from mistralai import Mistral

client = Mistral(api_key="...")

response = client.chat.complete(
    model="mistral-large-latest",
    messages=[
        {"role": "user", "content": "Explain Python decorators simply"}
    ]
)
print(response.choices[0].message.content)
```

**Get your API key:** Go to [console.mistral.ai](https://console.mistral.ai) and sign up.

---

### 5. Open-Source Models

Open-source models are free to download and run on your own hardware. This means no API costs and full control over your data. The trade-off is that you need a powerful computer (or rent GPU servers).

| Model | Creator | Parameters | Notes |
|-------|---------|-----------|-------|
| Llama 3.1 (405B) | Meta | 405 billion | Rivals GPT-4o on many tasks |
| Llama 3.1 (8B) | Meta | 8 billion | Runs on a good laptop |
| Qwen 2.5 (72B) | Alibaba | 72 billion | Strong multilingual, great at code |
| Gemma 2 (27B) | Google | 27 billion | Efficient, good for fine-tuning |

**Running locally with Ollama:**

```bash
# Install Ollama from ollama.com, then:
ollama pull llama3.1:8b
ollama run llama3.1:8b
# Now you have a local chatbot running on your machine!
```

```python
# Use from Python (works like any API)
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

## Provider Comparison Table

This is the table you will refer to when choosing a model for your projects.

| Provider | Flagship Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) | Context Window | Strengths |
|----------|---------------|---------------------------|----------------------------|---------------|-----------|
| OpenAI | GPT-4o | $2.50 | $10.00 | 128K | General purpose, coding, ecosystem |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 | 128K | Cheapest quality option |
| Anthropic | Claude 4 Sonnet | $3.00 | $15.00 | 200K | Long docs, instruction following |
| Anthropic | Claude 4 Haiku | $0.80 | $4.00 | 200K | Fast, affordable |
| Google | Gemini 2.5 Flash | $0.15 | $0.60 | 1M | Multimodal, huge context, free tier |
| Mistral | Mistral Large | $2.00 | $6.00 | 128K | Multilingual, European data privacy |
| Local | Llama 3.1 8B | Free (your hardware) | Free | 128K | No API cost, full data control |

> **Note:** Prices change frequently. Always check the provider's pricing page before starting a project. Prices listed are as of mid-2025.

---

## Which Model Should You Pick?

Here is a simple decision guide for common use cases:

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| Learning & experimenting | Gemini 2.5 Flash | Generous free tier, easy setup |
| Building a chatbot | GPT-4o-mini | Cheap, fast, good quality |
| Analyzing long documents | Claude 4 Sonnet | 200K context, great at careful reading |
| Code generation | GPT-4o or Claude 4 Sonnet | Both excel at writing code |
| Student project (no budget) | Ollama + Llama 3.1 8B | Completely free, runs locally |
| Multilingual app (Hindi, Tamil, etc.) | Gemini 2.5 Pro | Strong in Indian languages |
| Data privacy required | Ollama + Llama/Qwen | Data never leaves your machine |
| Production app in India | GPT-4o-mini or Gemini Flash | Low cost per request |

---

## Free Tiers and Student-Friendly Options

As a fresher learning AI development, you do not need to spend money. Here are the free options:

| Option | What You Get | Best For |
|--------|-------------|---------|
| Google AI Studio | Free Gemini API with generous limits | Best free API for students |
| OpenAI free credits | $5 on signup (enough for ~33,000 GPT-4o-mini calls) | Trying the most popular API |
| Anthropic free credits | $5 on signup | Trying Claude |
| Ollama (local) | Unlimited, completely free | Running models offline, no internet needed |
| Hugging Face | Free access to thousands of open-source models | Experimenting with many models |
| GitHub Models | Free access to GPT-4o, Llama, Mistral via GitHub | Students with GitHub accounts |

**Amit's tip:** Start with Google AI Studio (free Gemini API) for your coursework. When you build your capstone project, use GPT-4o-mini or Gemini Flash — they cost less than a cup of chai per hundred API calls.

---

## Setting Up Multiple Providers (Best Practice)

In real projects, you often use different models for different tasks. Here is a clean way to manage API keys:

```python
# .env file (NEVER commit this to GitHub!)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
MISTRAL_API_KEY=...
```

```python
# config.py — Load all keys from environment
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
```

> **Important:** Add `.env` to your `.gitignore` file. If you accidentally push API keys to GitHub, bots will find them within minutes and use your credits. Sneha from the previous batch once pushed her OpenAI key to a public repo — her account was charged Rs 3,200 overnight before she noticed.

---

## Key Takeaways

| Lesson | Details |
|--------|---------|
| No single best model | Each provider has different strengths and pricing |
| Start free | Use Google AI Studio or Ollama for learning |
| Match model to task | Use cheap models for simple tasks, capable models for complex ones |
| Protect your API keys | Use `.env` files, never commit keys to GitHub |
| Pricing is per token | Both input and output tokens count toward your bill |

---

*TechPath Institute -- Python Full Stack with Gen AI*

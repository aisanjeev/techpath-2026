# Generative AI & Large Language Models

**Module 06 — Fundamentals of AI | Topic 2**

---

## What is Generative AI?

**Generative AI** = AI that creates NEW content — text, images, code, music, video.

| What It Generates | Tool Examples |
|-------------------|--------------|
| **Text** | ChatGPT, Claude, Gemini |
| **Images** | DALL-E, Midjourney, Stable Diffusion |
| **Code** | GitHub Copilot, Claude Code |
| **Music** | Suno AI, Udio |
| **Video** | Sora (OpenAI), Runway |
| **Voice** | ElevenLabs, Play.ht |
| **Presentations** | Gamma, Beautiful.ai |

> **Before GenAI:** AI could classify (cat or dog?), predict (will it rain?), detect (is this spam?)
>
> **With GenAI:** AI can CREATE (write an essay, paint a picture, compose music)

---

## How Does ChatGPT / Claude Actually Work?

### Large Language Models (LLMs)

ChatGPT and Claude are **Large Language Models (LLMs)**. Here's the simple version:

1. **Trained on massive text data** — books, websites, articles (trillions of words)
2. **Learned language patterns** — grammar, facts, logic, style
3. **Predicts the next word** — Given "The capital of France is...", it predicts "Paris"
4. **Does this billions of times** — to generate full responses

> **Think of it like a super auto-complete.** Your phone predicts the next word in texts — LLMs do the same but millions of times better.

### Key Facts about LLMs

| Fact | Detail |
|------|--------|
| **Training data** | Trillions of words from internet, books, papers |
| **Parameters** | Billions of adjustable numbers (GPT-4 has ~1.8 trillion) |
| **Training cost** | $50-100 million+ per large model |
| **Training time** | Months on thousands of GPUs |
| **Knowledge cutoff** | Models know up to their training date, not real-time |

---

## Popular AI Models (2024-2026)

| Model | Company | Best For |
|-------|---------|---------|
| **GPT-4o / GPT-5** | OpenAI | General text, coding, analysis |
| **Claude 5 / Opus** | Anthropic | Long documents, careful reasoning, coding |
| **Gemini** | Google | Integration with Google services |
| **Llama** | Meta | Open-source, run locally |
| **Mistral** | Mistral AI | Fast, efficient, European |
| **Copilot** | Microsoft | Built into Windows, Office, VS Code |

---

## Prompt Engineering — How to Talk to AI

A **prompt** is what you type to tell AI what to do. Better prompts = better results.

### Bad vs Good Prompts

| Bad Prompt | Good Prompt |
|-----------|------------|
| "Write about AI" | "Write a 200-word explanation of AI for high school students with 3 examples" |
| "Fix my code" | "I have a Python function that should add numbers but returns None. Here's the code: [code]. What's wrong?" |
| "Make a resume" | "Create a resume for a fresh graduate in Computer Science applying for a web developer role. Include skills: HTML, CSS, JavaScript, React" |

### Prompt Tips

| Tip | Example |
|-----|---------|
| **Be specific** | "Write 5 bullet points" not "Write about" |
| **Give context** | "You are a teacher explaining to beginners..." |
| **Set format** | "Respond as a table / list / JSON" |
| **Give examples** | "Like this example: [example]" |
| **Set length** | "In 100 words" or "In 3 paragraphs" |
| **Iterate** | If first answer isn't right, refine your prompt |

### Advanced Prompt Techniques

| Technique | What It Means | Example |
|-----------|-------------|---------|
| **Zero-shot** | Ask directly, no examples | "Translate to Hindi: Hello" |
| **Few-shot** | Give 2-3 examples first | "Happy → Positive. Angry → Negative. Excited → ?" |
| **Chain-of-Thought** | Ask AI to think step by step | "Solve this math problem step by step..." |
| **Role prompting** | Give AI a role | "Act as a senior Python developer and review this code" |
| **System prompts** | Set behavior rules | "Always respond in bullet points, use simple English" |

---

## AI Can Be Wrong — Hallucinations

**Hallucination** = When AI confidently gives wrong information.

| AI Says | Reality |
|---------|---------|
| "The Eiffel Tower is 500m tall" | Actually 330m |
| "This Python function exists: `str.reverse()`" | No such function in Python |
| "Research paper by Dr. Smith (2023) proves..." | Paper doesn't exist |

### How to Avoid Hallucinations

- **Always verify facts** from AI with a reliable source
- **Don't trust AI for** medical, legal, or financial advice
- **Ask AI to cite sources** — then check if they exist
- **Use AI as a starting point**, not the final answer

---

## AI Limitations — What AI Cannot Do

| AI Can | AI Cannot |
|--------|-----------|
| Generate text and code | Truly understand meaning |
| Answer questions from training data | Know current events (knowledge cutoff) |
| Translate languages | Feel emotions or have consciousness |
| Summarize documents | Replace human judgment for important decisions |
| Write creative content | Guarantee 100% accuracy |
| Help learn faster | Replace actual learning and practice |

---

## Tokens — How AI Measures Text

AI doesn't read "words" — it reads **tokens** (word pieces).

| Text | Approximate Tokens |
|------|-------------------|
| "Hello" | 1 token |
| "artificial intelligence" | 2-3 tokens |
| 1 page of text | ~250-300 tokens |
| A full novel | ~100,000 tokens |

**Why tokens matter:**
- AI models have a **context window** (max tokens they can handle)
- GPT-4: ~128K tokens, Claude: ~200K tokens
- More tokens = higher cost when using paid APIs

---

## AI Safety and Responsible Use

| Do | Don't |
|----|-------|
| Use AI to learn faster | Use AI to cheat on exams |
| Verify AI-generated facts | Blindly trust everything AI says |
| Give credit when using AI | Claim AI-generated work as 100% yours |
| Use AI as a coding assistant | Let AI write code you don't understand |
| Understand AI limitations | Assume AI is always right |

---

## Summary

- **Generative AI** creates new content (text, images, code, music)
- **LLMs** (like ChatGPT, Claude) predict the next word based on training data
- **Better prompts** = better AI responses (be specific, give context)
- AI **hallucinates** — always verify important facts
- **Tokens** = how AI measures text, models have context window limits
- Use AI **responsibly** — as a tool, not a replacement for learning

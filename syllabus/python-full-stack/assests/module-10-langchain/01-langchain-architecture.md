# LangChain Architecture

**Module 10 -- LangChain | Topic 1**

---

## What is LangChain?

LangChain is a Python framework that helps you build applications powered by Large Language Models (LLMs) like GPT-4, Claude, or Gemini.

**Analogy:** Think of an LLM like a powerful car engine. By itself, the engine just sits there. LangChain gives you the steering wheel, brakes, dashboard, and seats -- so you can actually drive somewhere useful.

Without LangChain, you would need to write hundreds of lines of code to:
- Format prompts correctly
- Parse AI responses into usable data
- Remember previous messages in a conversation
- Connect the AI to your documents or databases

LangChain provides ready-made building blocks for all of this.

### Installation

```bash
pip install langchain langchain-openai langchain-community langchain-core
pip install faiss-cpu chromadb       # Vector stores
pip install pypdf tiktoken           # PDF loading and tokenization
```

### Setting Up Your API Key

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Or load from a .env file (recommended for real projects)
from dotenv import load_dotenv
load_dotenv()
```

> **Never hardcode API keys in your code.** Always use environment variables or `.env` files. If you accidentally push your key to GitHub, someone can use it and you will get a huge bill.

---

## The Six Building Blocks

LangChain is made up of six core components. Here is how they fit together:

| Component | What It Does | Analogy |
|-----------|-------------|---------|
| **LLM / ChatModel** | Sends text to an AI model and gets a response | The brain |
| **Prompt Template** | Formats your question before sending to the LLM | A fill-in-the-blank form |
| **Output Parser** | Converts raw AI text into structured Python data | A translator |
| **Chain** | Connects multiple steps together in sequence | An assembly line |
| **Memory** | Remembers previous messages in a conversation | A notebook for the AI |
| **Retriever** | Finds relevant documents from a knowledge base | A librarian searching for books |

```
User Question --> [Prompt Template] --> [LLM] --> [Output Parser] --> Structured Answer
                                         ^
                                         |
                                    [Memory] (remembers past messages)
                                    [Retriever] (finds relevant docs)
```

---

## LLMs and Chat Models

An LLM is the AI model that generates text. In LangChain, you interact with LLMs through a **ChatModel** object.

```python
from langchain_openai import ChatOpenAI

# Create a chat model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Simple call -- ask a question, get an answer
response = llm.invoke("What is Python used for?")
print(response.content)
```

### Temperature -- Controlling Creativity

Temperature is a number between 0 and 1 that controls how creative the AI's responses are.

| Temperature | Behavior | Best For |
|-------------|----------|----------|
| `0.0` | Focused, always gives the same answer | Factual Q&A, data extraction |
| `0.3` | Mostly consistent with slight variation | Customer support bots |
| `0.7` | Balanced creativity and accuracy | General chatbots |
| `1.0` | Very creative, unpredictable | Brainstorming, creative writing |

**Analogy:** Temperature is like asking a chef to cook biryani:
- Temperature 0.0 = "Follow the exact recipe, no changes"
- Temperature 0.7 = "Follow the recipe but feel free to add your own touch"
- Temperature 1.0 = "Surprise me! Make it however you want"

### Using Different Providers

```python
# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

# Anthropic (Claude)
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-sonnet-4-20250514")

# Google (Gemini)
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
```

---

## Prompt Templates

Instead of writing the full prompt every time, you create a **template** with variables that get filled in.

### Basic Template

```python
from langchain_core.prompts import ChatPromptTemplate

# Create a template with a variable {topic}
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful teaching assistant at TechPath Institute."),
    ("human", "Explain {topic} in simple words for a beginner student."),
])

# Fill in the variable
formatted = prompt.invoke({"topic": "machine learning"})
print(formatted)
```

### Template with Multiple Variables

```python
prompt = ChatPromptTemplate.from_template(
    "Write a {length} explanation of {topic} for a student in {city}."
)

result = prompt.invoke({
    "topic": "REST APIs",
    "length": "3-sentence",
    "city": "Bhopal",
})
```

### System vs Human Messages

| Message Type | Purpose | Example |
|-------------|---------|---------|
| **System** | Sets the AI's personality and rules | "You are a Python tutor. Be patient and use simple language." |
| **Human** | The user's actual question | "What is a function?" |
| **AI** | The AI's previous response (for conversation history) | "A function is a reusable block of code..." |

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a TechPath Institute counselor. Be helpful and friendly."),
    ("human", "I want to learn web development. What course should I join?"),
])
```

---

## Output Parsers

LLMs return plain text. But in real applications, you often need structured data -- like a Python dictionary, a list, or a JSON object. Output parsers handle this conversion.

### String Output Parser (Simplest)

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
# Just extracts the text content from the AI's response
```

### JSON Output Parser

```python
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# Define the structure you want
class CourseInfo(BaseModel):
    name: str = Field(description="Course name")
    duration: str = Field(description="Course duration")
    fee: int = Field(description="Course fee in rupees")

json_parser = JsonOutputParser(pydantic_object=CourseInfo)

# The parser automatically adds format instructions to your prompt
print(json_parser.get_format_instructions())
```

### List Output Parser

```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser

list_parser = CommaSeparatedListOutputParser()
# Converts "Python, JavaScript, Java" into ["Python", "JavaScript", "Java"]
```

### Why Use Parsers?

| Without Parser | With Parser |
|---------------|-------------|
| `"The fee is Rs 45,000"` (plain text) | `{"fee": 45000}` (structured data) |
| Hard to use in code | Easy to use -- `result["fee"]` |
| Inconsistent format | Always the same format |

---

## Memory -- Remembering Conversations

Without memory, every message to the LLM is independent. The AI does not know what you said 10 seconds ago.

### Conversation Buffer Memory

Stores every message in the conversation.

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)

# Save a conversation exchange
memory.save_context(
    {"input": "My name is Rahul"},
    {"output": "Hello Rahul! How can I help you today?"}
)

# Later, load the history
history = memory.load_memory_variables({})
print(history)
# The AI now knows the user's name is Rahul
```

### Types of Memory

| Memory Type | How It Works | Best For | Downside |
|------------|-------------|----------|----------|
| `ConversationBufferMemory` | Stores every message | Short chats (5-10 messages) | Uses lots of tokens for long chats |
| `ConversationSummaryMemory` | Summarizes old messages | Long conversations | Loses details |
| `ConversationWindowMemory` | Keeps only last N messages | Medium conversations | Forgets old messages |

**Analogy:** Think of memory types like note-taking styles:
- **Buffer** = writing down every single word the teacher says (accurate but your notebook fills up fast)
- **Summary** = writing only the key points (saves space but you lose details)
- **Window** = using sticky notes that fall off when you add new ones (only recent notes survive)

---

## Chains -- Connecting Steps

A chain connects multiple components together. The output of one step becomes the input to the next.

### Simple Chain Example

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Define each component
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in 3 bullet points for a beginner."
)
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Connect them into a chain using the pipe operator
chain = prompt | llm | parser

# Run the chain
result = chain.invoke({"topic": "Python dictionaries"})
print(result)
```

**How the chain flows:**

```
{"topic": "Python dictionaries"}
        |
   [Prompt Template]  -->  "Explain Python dictionaries in 3 bullet points..."
        |
      [LLM]           -->  AI generates the response
        |
   [Output Parser]    -->  Extracts the text string
        |
   Final Answer
```

---

## Summary

| Concept | One-Line Summary |
|---------|-----------------|
| LangChain | Framework to build LLM-powered apps with reusable components |
| LLM/ChatModel | The AI brain -- sends text, gets response |
| Prompt Template | Fill-in-the-blank form for formatting questions |
| Output Parser | Converts AI text into structured Python data |
| Memory | Remembers past conversation messages |
| Chain | Connects steps together (prompt -> LLM -> parser) |
| Temperature | Controls how creative vs deterministic the AI is |

### What's Next?

In the next topic, we will learn about **LCEL (LangChain Expression Language)** -- the modern way to build powerful chains with pipes, parallel execution, and streaming.

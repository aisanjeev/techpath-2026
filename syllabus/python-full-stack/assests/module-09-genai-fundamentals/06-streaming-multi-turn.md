# Streaming Responses and Multi-Turn Conversations

**Module 09 — Generative AI Fundamentals & Prompt Engineering | Topic 6**

*TechPath Institute — Python Full Stack Development Program*

---

## Why Streaming Matters

Imagine you order food at a restaurant. In the normal (non-streaming) way, you wait 20 minutes and then the waiter brings the entire meal at once. With streaming, the waiter starts bringing dishes one by one as they are ready -- you can start eating the salad while the main course is still being prepared.

**Streaming** in AI works the same way. Instead of waiting for the entire response to be generated (which can take several seconds for long answers), the text appears word by word as it is being created.

| Without Streaming | With Streaming |
|---|---|
| User waits 5-10 seconds, sees nothing | Text starts appearing in under 1 second |
| Feels slow and unresponsive | Feels fast and interactive |
| All-or-nothing (if connection drops, you get nothing) | Partial response is still visible |
| Simple to implement | Slightly more code, but worth it |

Think about how ChatGPT works -- the text appears word by word. That is streaming in action. Without it, you would stare at a blank screen for seconds before the entire answer popped up at once.

---

## Implementing Streaming with OpenAI

### Basic Streaming Example

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Create a streaming response
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain Python lists in simple words"}
    ],
    stream=True  # This one parameter enables streaming
)

# Print each chunk as it arrives
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)

print()  # New line at the end
```

**What happens here:**
1. We set `stream=True` in the API call.
2. Instead of getting one big response, we get many small **chunks**.
3. Each chunk contains a small piece of text (sometimes just one word or even one character).
4. We print each piece immediately with `end=""` so they appear on the same line.
5. `flush=True` forces the output to display immediately without buffering.

### Collecting the Full Response While Streaming

Often you want to both show the text to the user AND keep a copy of the full response:

```python
def stream_and_collect(prompt):
    """Stream the response to console and return the full text."""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    full_response = []

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="", flush=True)
            full_response.append(content)

    print()  # New line
    return "".join(full_response)

# Use it
response_text = stream_and_collect("What are the top 3 IT companies in Pune?")
# Now response_text has the complete answer
```

---

## Implementing Streaming with Anthropic

Anthropic's Claude uses a similar but slightly different approach:

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Streaming with Claude
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain Python dictionaries simply"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()
```

### Anthropic Streaming with Event Details

If you need more control over what is happening during streaming:

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "List 5 Python tips for beginners"}]
) as stream:
    for event in stream:
        # Different event types give different information
        if event.type == "content_block_delta":
            print(event.delta.text, end="", flush=True)
        elif event.type == "message_stop":
            print("\n[Response complete]")
```

### Comparison: OpenAI vs Anthropic Streaming

| Feature | OpenAI | Anthropic |
|---|---|---|
| Enable streaming | `stream=True` parameter | `client.messages.stream()` context manager |
| Iterate chunks | `for chunk in stream` | `for text in stream.text_stream` |
| Access text | `chunk.choices[0].delta.content` | `text` (directly) |
| Get final message | Collect chunks manually | `stream.get_final_message()` |

---

## Multi-Turn Conversations

A **multi-turn conversation** is a back-and-forth chat where the AI remembers what was said before. Without this, every message would be like talking to someone with no memory.

### How Message History Works

LLMs do not actually "remember" anything. They are stateless -- each API call is independent. To create the illusion of memory, we send the **entire conversation history** with every request.

Think of it like this: imagine Ananya is writing letters to a friend. Each letter, she includes a copy of all previous letters so her friend can follow the conversation. That is exactly what we do with LLMs.

```python
# The conversation is just a list of messages
conversation = [
    {"role": "system", "content": "You are a helpful Python tutor at TechPath Institute."},
    {"role": "user", "content": "What is a variable?"},
    {"role": "assistant", "content": "A variable is like a labelled box..."},
    {"role": "user", "content": "Can you give me an example?"},
    # The AI sees ALL of the above and knows "example" refers to variables
]
```

### Message Roles Explained

| Role | Who Is Speaking | Purpose |
|---|---|---|
| `system` | The developer (you) | Sets the AI's personality and rules |
| `user` | The end user | Questions and requests |
| `assistant` | The AI | The AI's previous responses |

---

## Token Counting and Context Windows

Every LLM has a **context window** -- the maximum number of tokens it can process in one request. This includes both the input (your messages) and the output (the AI's response).

### What Are Tokens?

Tokens are pieces of words. Roughly:
- 1 word is about 1.3 tokens in English
- 1 word is about 1.5-2 tokens in Hindi (Devanagari text uses more tokens)
- 100 tokens is about 75 English words

### Context Window Sizes

| Model | Context Window | Approx. Words |
|---|---|---|
| GPT-4o-mini | 128,000 tokens | ~96,000 words |
| GPT-4o | 128,000 tokens | ~96,000 words |
| Claude Sonnet | 200,000 tokens | ~150,000 words |

### Counting Tokens with OpenAI

```python
import tiktoken

def count_tokens(text, model="gpt-4o-mini"):
    """Count how many tokens a text will use."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Example
text = "TechPath Institute is located in Bhopal, Madhya Pradesh."
tokens = count_tokens(text)
print(f"This text uses {tokens} tokens")

def count_conversation_tokens(messages, model="gpt-4o-mini"):
    """Count total tokens in a conversation."""
    encoding = tiktoken.encoding_for_model(model)
    total = 0
    for message in messages:
        total += len(encoding.encode(message["content"]))
        total += 4  # Every message has overhead tokens
    total += 2  # Conversation overhead
    return total
```

---

## Conversation Memory Strategies

As a conversation grows longer, it will eventually exceed the context window. You need strategies to manage this.

### Strategy 1: Sliding Window

Keep only the last N messages. Simple but loses early context.

```python
def sliding_window(messages, max_messages=20):
    """Keep system message + last N messages."""
    system_messages = [m for m in messages if m["role"] == "system"]
    other_messages = [m for m in messages if m["role"] != "system"]

    # Keep system message + last max_messages exchanges
    if len(other_messages) > max_messages:
        other_messages = other_messages[-max_messages:]

    return system_messages + other_messages
```

### Strategy 2: Summarization

When the conversation gets long, summarize older messages and keep the summary.

```python
def summarize_old_messages(client, messages, keep_recent=6):
    """Summarize old messages, keep recent ones."""
    if len(messages) <= keep_recent + 1:  # +1 for system message
        return messages

    system_msg = messages[0]  # System message
    old_messages = messages[1:-keep_recent]
    recent_messages = messages[-keep_recent:]

    # Ask the LLM to summarize the old conversation
    old_text = "\n".join(
        f"{m['role']}: {m['content']}" for m in old_messages
    )

    summary_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Summarize this conversation in 2-3 sentences:\n{old_text}"
        }]
    )

    summary = summary_response.choices[0].message.content

    # Build new message list with summary
    return [
        system_msg,
        {"role": "system", "content": f"Previous conversation summary: {summary}"},
        *recent_messages
    ]
```

### Strategy 3: Token-Based Trimming

More precise -- trim based on actual token count rather than message count.

```python
import tiktoken

def trim_by_tokens(messages, max_tokens=4000, model="gpt-4o-mini"):
    """Remove oldest messages until under the token limit."""
    encoding = tiktoken.encoding_for_model(model)

    # Always keep the system message
    system_msg = messages[0] if messages[0]["role"] == "system" else None
    other_messages = messages[1:] if system_msg else messages[:]

    # Count tokens from newest to oldest, keep what fits
    kept = []
    total = 0
    if system_msg:
        total = len(encoding.encode(system_msg["content"])) + 4

    for msg in reversed(other_messages):
        msg_tokens = len(encoding.encode(msg["content"])) + 4
        if total + msg_tokens > max_tokens:
            break
        kept.insert(0, msg)
        total += msg_tokens

    result = [system_msg] + kept if system_msg else kept
    return result
```

### Comparison of Memory Strategies

| Strategy | Pros | Cons | Best For |
|---|---|---|---|
| Sliding Window | Simple, fast | Loses old context | Quick chatbots |
| Summarization | Preserves key information | Costs extra API calls | Important conversations |
| Token-Based Trimming | Precise control | More complex code | Production applications |

---

## Building a Complete Chat Loop

Here is a full chatbot that streams responses and remembers conversation history:

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

def chat():
    """A complete streaming chatbot with memory."""
    print("=" * 50)
    print("  TechPath Student Assistant")
    print("  Type 'quit' to exit, 'clear' to reset")
    print("=" * 50)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly student assistant at TechPath Institute, Bhopal. "
                "You help students with Python programming questions. "
                "Keep answers short and use simple language. "
                "Use Indian examples when possible."
            )
        }
    ]

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye! Happy coding!")
            break
        if user_input.lower() == "clear":
            messages = messages[:1]  # Keep only system message
            print("[Conversation cleared]")
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        # Trim if conversation is getting too long
        if len(messages) > 22:  # system + 10 exchanges (user + assistant each)
            messages = [messages[0]] + messages[-20:]
            print("[Older messages trimmed to save memory]")

        # Stream the response
        print("\nAssistant: ", end="")
        full_response = []

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                full_response.append(content)

        print()  # New line after response

        # Add assistant response to history
        assistant_text = "".join(full_response)
        messages.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    chat()
```

### Sample Conversation

```
==================================================
  TechPath Student Assistant
  Type 'quit' to exit, 'clear' to reset
==================================================

You: What is a list in Python?
Assistant: A list in Python is like a tiffin box with multiple
compartments. You can store different items in each compartment
-- numbers, strings, even other lists. You create a list using
square brackets: my_list = [1, 2, 3, "hello"]

You: How do I add items to it?
Assistant: You can use the .append() method! For example:
fruits = ["apple", "banana"]
fruits.append("mango")
Now fruits is ["apple", "banana", "mango"]. The AI remembers
we were talking about lists because the full conversation
history is sent with every request.

You: quit
Goodbye! Happy coding!
```

Notice how the AI knew "it" referred to a list -- because the entire conversation history was sent with the second question.

---

## Common Mistakes to Avoid

| Mistake | Why It Is Wrong | Fix |
|---|---|---|
| Forgetting `flush=True` | Text buffers and appears in bursts | Always use `flush=True` with `end=""` |
| Not saving streamed text | You lose the response after printing | Collect chunks in a list |
| Sending unlimited history | Exceeds context window, API errors | Use a memory strategy |
| No system message | AI has no personality or rules | Always start with a system message |
| Ignoring token costs | Long histories cost more money | Trim or summarize old messages |

---

## Key Takeaways

1. **Streaming** makes your chatbot feel fast by showing text as it is generated, word by word.
2. **OpenAI** uses `stream=True`; **Anthropic** uses `client.messages.stream()` -- different syntax, same idea.
3. **Multi-turn conversations** work by sending the entire message history with every API call.
4. **LLMs have no memory** -- you must manage conversation history yourself.
5. **Context windows** have limits -- use sliding window, summarization, or token trimming to stay within bounds.
6. **Always collect** the streamed response so you can add it to the conversation history.

---

*Next Topic: AI Safety and Guardrails*

---
*TechPath Institute | Python Full Stack Development Program | Module 09*

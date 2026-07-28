# Streaming AI Responses

**Module 08 — Front-End for Python Developers | Topic 7**

---

## What Is Streaming?

Imagine you are watching a cricket match on TV. You see each ball live as it is bowled — you do not wait for the entire match to finish and then watch a recording. That is streaming.

Now compare two ways of watching a movie:
- **Downloading first:** You wait 30 minutes for the file to download, then you watch it. (Non-streaming)
- **Streaming (Netflix/Hotstar):** You click play and start watching immediately while the rest loads in the background. (Streaming)

AI responses work the same way. When you chat with ChatGPT or any AI assistant, the response appears **word by word** — you do not wait for the entire answer to be generated. This is streaming. The server sends tokens (words or parts of words) as they are generated, and the browser displays them in real time.

**Why streaming matters for AI applications:**
- Users see the first words instantly instead of waiting 5-10 seconds for the full response
- The experience feels interactive, like talking to a person
- Users can stop generation early if they see the answer going in the wrong direction
- It reduces perceived latency — the app feels faster even though total time is similar

---

## Server-Sent Events (SSE) Explained

Before we build anything, you need to understand how the server sends data to the browser continuously.

### Three Ways to Get Live Data

| Method | How It Works | Best For |
|--------|-------------|----------|
| Polling | Browser asks server every 2 seconds: "Any update?" | Simple notifications |
| WebSocket | Two-way permanent connection (both sides can talk) | Chat apps, games, collaboration |
| Server-Sent Events (SSE) | One-way: server pushes data to browser | AI streaming, live feeds, dashboards |

**Think of it this way:**
- **Polling** = Rahul calling the delivery person every 2 minutes: "Where is my food?"
- **WebSocket** = A phone call that stays connected — both people can talk anytime
- **SSE** = A live cricket score ticker — the server keeps sending updates, you just watch

For AI streaming, SSE is perfect because:
- The server sends data (AI tokens) one way to the browser
- The browser only needs to listen and display
- SSE automatically reconnects if the connection drops
- It works over regular HTTP — no special protocol needed

### SSE Data Format

SSE messages follow a simple text format:

```
data: Hello

data: , how

data:  are

data:  you?

data: [DONE]
```

Each line starts with `data: ` followed by the content. The browser receives these one by one and can display them as they arrive.

---

## Building an SSE Endpoint in FastAPI

Let us build a **TechPath AI Tutor** — a chatbot that explains programming concepts to students. The response streams word by word.

### The FastAPI Streaming Endpoint

```python
# app/api/v1/endpoints/ai_tutor.py
import asyncio
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

router = APIRouter()

async def generate_tutor_response(question: str):
    """
    Simulate an AI generating a response token by token.
    In production, this would call OpenAI/Claude API with stream=True.
    """
    # Simulated AI response (in production, call OpenAI/Claude API)
    responses = {
        "what is a variable": (
            "A variable is like a labelled box where you store data. "
            "For example, `name = 'Priya'` creates a box labelled 'name' "
            "and puts the value 'Priya' inside it."
        ),
    }
    answer = responses.get(
        question.lower().strip(),
        "That is a great question! Let me explain step by step..."
    )

    # Stream word by word with a small delay (simulating AI generation)
    words = answer.split(" ")
    for i, word in enumerate(words):
        separator = "" if i == 0 else " "
        yield f"data: {separator}{word}\n\n"
        await asyncio.sleep(0.05)  # 50ms per token

    yield "data: [DONE]\n\n"


@router.get("/ai-tutor/ask")
async def ask_tutor(question: str = Query(..., min_length=3)):
    """
    Stream an AI tutor response using Server-Sent Events.
    """
    return StreamingResponse(
        generate_tutor_response(question),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )
```

**Key points:**
- `StreamingResponse` sends data as it is generated — it does not wait for the full response
- `media_type="text/event-stream"` tells the browser this is an SSE stream
- `yield` sends each chunk immediately; `await asyncio.sleep(0.05)` simulates AI generation time
- `X-Accel-Buffering: no` prevents reverse proxies (Nginx) from buffering the stream
- The `[DONE]` token tells the browser the stream is finished

---

## Consuming SSE in the Browser

### Method 1: EventSource (Simple)

The browser has a built-in `EventSource` API specifically for SSE:

```javascript
function askTutor(question) {
    const outputDiv = document.getElementById("response");
    outputDiv.textContent = "";

    const url = `/api/v1/ai-tutor/ask?question=${encodeURIComponent(question)}`;
    const source = new EventSource(url);

    source.onmessage = function(event) {
        if (event.data === "[DONE]") {
            source.close();
            return;
        }
        // Append each token to the output
        outputDiv.textContent += event.data;
    };

    source.onerror = function(error) {
        console.error("SSE connection error:", error);
        source.close();
        outputDiv.textContent += "\n\n[Connection lost. Please try again.]";
    };
}
```

**Limitation:** `EventSource` only supports GET requests. If you need to send a long message or POST data, use `fetch` with `ReadableStream` instead.

### Method 2: Fetch with ReadableStream (Flexible)

This method works with POST requests and gives you more control:

```javascript
async function askTutorPost(question) {
    const outputDiv = document.getElementById("response");
    outputDiv.textContent = "";

    try {
        const response = await fetch("/api/v1/ai-tutor/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question })
        });

        if (!response.ok) {
            outputDiv.textContent = "Error: " + response.statusText;
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            // Decode the chunk from bytes to text
            const text = decoder.decode(value, { stream: true });

            // Parse SSE lines
            const lines = text.split("\n");
            for (const line of lines) {
                if (line.startsWith("data: ")) {
                    const data = line.slice(6);  // Remove "data: "
                    if (data === "[DONE]") return;
                    outputDiv.textContent += data;
                }
            }
        }
    } catch (error) {
        console.error("Streaming failed:", error);
        outputDiv.textContent += "\n\n[Connection lost. Please try again.]";
    }
}
```

### EventSource vs Fetch ReadableStream

| Feature | EventSource | Fetch + ReadableStream |
|---------|-------------|----------------------|
| HTTP method | GET only | GET, POST, PUT, etc. |
| Auto-reconnect | Yes (built-in) | No (you must handle it) |
| Custom headers | No | Yes |
| Send request body | No | Yes |
| Browser support | All modern browsers | All modern browsers |
| Best for | Simple SSE streams | POST-based AI chat |

---

## Building a Chat UI — TechPath AI Tutor

Let us put it all together and build a complete chat interface where students can ask questions and see the AI response appear token by token.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechPath AI Tutor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5;
               display: flex; flex-direction: column; height: 100vh; }
        .header { background: #1a237e; color: white;
                  padding: 12px 20px; text-align: center; }
        .chat-area { flex: 1; overflow-y: auto; padding: 20px; }
        .message { max-width: 80%; margin-bottom: 16px;
                  padding: 12px 16px; border-radius: 12px; line-height: 1.6; }
        .user-message { background: #1a237e; color: white; margin-left: auto; }
        .ai-message { background: white; color: #333; border: 1px solid #ddd; }
        .typing-indicator { color: #999; font-style: italic; }
        .input-area { display: flex; gap: 10px; padding: 16px 20px;
                     background: white; border-top: 1px solid #ddd; }
        .input-area input { flex: 1; padding: 12px; border: 1px solid #ddd;
                           border-radius: 8px; font-size: 16px; }
        .input-area button { padding: 12px 24px; background: #1a237e;
                            color: white; border: none; border-radius: 8px;
                            cursor: pointer; font-size: 16px; }
        .input-area button:disabled { background: #999; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="header">
        <h2>TechPath AI Tutor</h2>
        <small>Ask any Python question — your personal coding mentor</small>
    </div>

    <div class="chat-area" id="chatArea">
        <div class="message ai-message">
            Namaste! I am your TechPath AI Tutor. Ask me anything about
            Python, web development, or databases. Try: "What is a variable?"
        </div>
    </div>

    <div class="input-area">
        <input type="text" id="questionInput"
               placeholder="Type your question here..."
               onkeypress="if(event.key==='Enter') sendQuestion()">
        <button id="sendBtn" onclick="sendQuestion()">Ask</button>
    </div>

    <script>
    async function sendQuestion() {
        const input = document.getElementById("questionInput");
        const chatArea = document.getElementById("chatArea");
        const sendBtn = document.getElementById("sendBtn");
        const question = input.value.trim();

        if (!question) return;

        // Show user message
        chatArea.innerHTML += `
            <div class="message user-message">${escapeHtml(question)}</div>
        `;
        input.value = "";
        sendBtn.disabled = true;

        // Create AI message container
        const aiMessage = document.createElement("div");
        aiMessage.className = "message ai-message";
        aiMessage.innerHTML = '<span class="typing-indicator">Thinking...</span>';
        chatArea.appendChild(aiMessage);
        chatArea.scrollTop = chatArea.scrollHeight;

        try {
            const url = `/api/v1/ai-tutor/ask?question=${
                encodeURIComponent(question)
            }`;
            const response = await fetch(url);
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            aiMessage.textContent = "";  // Clear "Thinking..."
            let fullResponse = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const text = decoder.decode(value, { stream: true });
                const lines = text.split("\n");

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        const data = line.slice(6);
                        if (data === "[DONE]") break;
                        fullResponse += data;
                        aiMessage.textContent = fullResponse;
                        chatArea.scrollTop = chatArea.scrollHeight;
                    }
                }
            }
        } catch (error) {
            aiMessage.textContent += "\n\n[Connection error. Please try again.]";
        }

        sendBtn.disabled = false;
        input.focus();
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
    </script>
</body>
</html>
```

**What happens when Ananya asks "What is a variable?":**
1. Her question appears as a blue bubble on the right
2. A "Thinking..." indicator appears on the left
3. The browser opens a connection to `/api/v1/ai-tutor/ask?question=What+is+a+variable`
4. FastAPI starts generating the response and yields each word
5. The browser reads each chunk, parses the `data:` lines, and appends words to the AI message
6. Words appear one by one — just like ChatGPT
7. When `[DONE]` arrives, the stream is complete
8. The Send button is re-enabled

---

## Handling Connection Errors and Reconnection

Networks are unreliable — especially in India where mobile connections can drop. Your chat must handle errors gracefully.

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server is down | Show "Server unavailable" message, retry button |
| Network timeout | Slow internet | Set a timeout, show retry option |
| Stream interrupted | Wi-Fi switched | Auto-reconnect with a delay |
| HTTP 429 | Too many requests | Show "Please wait" with countdown |
| HTTP 500 | Server crash | Show "Something went wrong" with a retry |

### Reconnection with Exponential Backoff

If the connection drops, do not retry immediately — wait longer each time (1s, 2s, 4s). This is called exponential backoff. Think of it like calling a friend who is not picking up — you wait a bit longer between each call instead of dialing non-stop.

```javascript
async function askWithRetry(question, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            await sendQuestion(question);
            return;
        } catch (error) {
            if (attempt >= maxRetries) {
                showError("Unable to connect. Please check your internet.");
                return;
            }
            const delay = Math.pow(2, attempt) * 1000;
            showStatus(`Retrying in ${delay / 1000} seconds...`);
            await new Promise(r => setTimeout(r, delay));
        }
    }
}
```

---

## Quick Reference Card

```
Server (FastAPI):
  StreamingResponse(generator, media_type="text/event-stream")
  yield "data: token_text\n\n"     → Send one token
  yield "data: [DONE]\n\n"         → Signal stream end
  Headers: Cache-Control: no-cache, X-Accel-Buffering: no

Browser (EventSource — GET only):
  const source = new EventSource(url);
  source.onmessage = (e) => { /* e.data */ }
  source.onerror = (e) => { source.close(); }

Browser (fetch + ReadableStream — GET/POST):
  const reader = response.body.getReader();
  const { done, value } = await reader.read();
  new TextDecoder().decode(value, { stream: true });
```

---

## Key Takeaways

1. Streaming shows AI responses word by word — like ChatGPT — instead of making users wait for the full answer
2. Server-Sent Events (SSE) are the simplest way to stream data from server to browser
3. FastAPI's `StreamingResponse` with an async generator makes SSE endpoints easy to build
4. Use `EventSource` for simple GET-based streams; use `fetch` with `ReadableStream` for POST requests
5. Always handle connection errors with retry logic and exponential backoff
6. The `[DONE]` token is a convention to signal the end of the stream — always check for it on the client

---

*TechPath Institute — Python Full Stack Development Program*

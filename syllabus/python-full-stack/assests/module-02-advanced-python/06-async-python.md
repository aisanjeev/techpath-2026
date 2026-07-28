# Async Python

**Module 02 — Advanced Python | Topic 6**

---

## The Problem: Waiting

Many programs spend most of their time **waiting** — waiting for an API response, waiting for a file to download, waiting for a database query. During this wait, your program sits idle doing nothing.

**Real-world analogy:** Imagine you are at a restaurant and order food. Synchronous = you stand at the counter staring until your food is ready. Asynchronous = you sit down, check your phone, chat with friends, and the waiter brings your food when it is ready.

### Sync vs Async

```
Synchronous (blocking):
Task 1: ████████████████░░░░░░░░░░░░░░░░  (waiting...)
Task 2: ░░░░░░░░░░░░░░░░████████████████  (starts after Task 1)
Total: ████████████████████████████████  (sum of both)

Asynchronous (non-blocking):
Task 1: ████░░░░░░░░████░░░░░░░░████
Task 2: ░░░░████░░░░░░░░████░░░░░░░░████
Total: ████████████████████████████  (overlapped)
```

---

## async and await — The Basics

```python
import asyncio

# Regular (sync) function
def greet_sync(name):
    return f"Hello, {name}!"

# Async function (coroutine)
async def greet_async(name):
    return f"Hello, {name}!"

# You cannot call an async function normally
# greet_async("Rahul")  ← This returns a coroutine object, not the result!

# You must "await" it inside another async function, or use asyncio.run()
async def main():
    result = await greet_async("Rahul")
    print(result)

asyncio.run(main())    # Hello, Rahul!
```

### Key Rules

1. An `async def` function is a **coroutine** — it can be paused and resumed
2. Use `await` to wait for an async operation to complete
3. `await` can only be used inside an `async def` function
4. Use `asyncio.run()` to start the async event loop from sync code

---

## asyncio.sleep() — Simulating Async Work

```python
import asyncio
import time

async def fetch_data(source, delay):
    """Simulate fetching data from a source."""
    print(f"Fetching from {source}...")
    await asyncio.sleep(delay)    # Non-blocking wait
    print(f"Got data from {source}!")
    return f"{source}_data"

async def main():
    start = time.time()

    # Sequential — one after another (slow)
    data1 = await fetch_data("Database", 2)
    data2 = await fetch_data("API", 3)
    # Total time: ~5 seconds

    print(f"Sequential: {time.time() - start:.1f}s")

asyncio.run(main())
```

---

## asyncio.gather() — Run Tasks Concurrently

```python
import asyncio
import time

async def fetch_data(source, delay):
    print(f"Fetching from {source}...")
    await asyncio.sleep(delay)
    print(f"Got data from {source}!")
    return f"{source}_data"

async def main():
    start = time.time()

    # Concurrent — all at once (fast!)
    results = await asyncio.gather(
        fetch_data("Database", 2),
        fetch_data("API", 3),
        fetch_data("Cache", 1),
    )
    # Total time: ~3 seconds (the longest task)

    print(f"Results: {results}")
    print(f"Concurrent: {time.time() - start:.1f}s")

asyncio.run(main())
# Fetching from Database...
# Fetching from API...
# Fetching from Cache...
# Got data from Cache!
# Got data from Database!
# Got data from API!
# Results: ['Database_data', 'API_data', 'Cache_data']
# Concurrent: 3.0s
```

---

## The Event Loop

The event loop is the engine that runs async code. It keeps track of all tasks and switches between them when one is waiting.

```
Event Loop:
┌─────────────────────────────────────────┐
│ Task A: fetch_data("DB")                │
│   → starts → awaits sleep(2) → PAUSED  │
│                                         │
│ Task B: fetch_data("API")               │
│   → starts → awaits sleep(3) → PAUSED  │
│                                         │
│ (2 seconds later)                       │
│ Task A: → RESUMED → completes          │
│                                         │
│ (1 second later)                        │
│ Task B: → RESUMED → completes          │
└─────────────────────────────────────────┘
```

```python
# asyncio.run() creates and manages the event loop
asyncio.run(main())

# You can also manage it manually (rarely needed)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

---

## Async with httpx — Real API Calls

`httpx` is an async-capable HTTP client (unlike `requests`, which is sync-only).

```bash
pip install httpx
```

```python
import asyncio
import httpx
import time

async def fetch_url(client, url):
    """Fetch a URL asynchronously."""
    response = await client.get(url)
    return {
        "url": url,
        "status": response.status_code,
        "size": len(response.text),
    }

async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/users/1",
        "https://jsonplaceholder.typicode.com/todos/1",
    ]

    start = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url) for url in urls]
        results = await asyncio.gather(*tasks)

    for r in results:
        print(f"{r['url']}: {r['status']} ({r['size']} bytes)")

    print(f"\nFetched {len(urls)} URLs in {time.time() - start:.2f}s")

asyncio.run(main())
```

---

## asyncio.create_task() — Fire and Forget

```python
import asyncio

async def background_job(name, duration):
    print(f"Starting {name}...")
    await asyncio.sleep(duration)
    print(f"Finished {name}!")

async def main():
    # Create tasks — they start running immediately
    task1 = asyncio.create_task(background_job("Backup", 3))
    task2 = asyncio.create_task(background_job("Email", 2))

    print("Tasks started, doing other work...")
    await asyncio.sleep(1)
    print("Still working...")

    # Wait for both tasks to complete
    await task1
    await task2
    print("All done!")

asyncio.run(main())
# Tasks started, doing other work...
# Starting Backup...
# Starting Email...
# Still working...
# Finished Email!
# Finished Backup!
# All done!
```

---

## Async Context Managers

```python
import asyncio

class AsyncDatabase:
    async def __aenter__(self):
        print("Connecting to database...")
        await asyncio.sleep(0.5)
        print("Connected!")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection...")
        await asyncio.sleep(0.2)
        print("Connection closed.")

    async def query(self, sql):
        await asyncio.sleep(0.3)
        return [{"name": "Rahul", "marks": 85}]

async def main():
    async with AsyncDatabase() as db:
        results = await db.query("SELECT * FROM students")
        print(f"Got {len(results)} results")

asyncio.run(main())
```

---

## Async Iterators and for Loops

```python
import asyncio

class AsyncStudentLoader:
    """Load students in batches asynchronously."""
    def __init__(self, total, batch_size=3):
        self.total = total
        self.batch_size = batch_size
        self.loaded = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.loaded >= self.total:
            raise StopAsyncIteration
        
        await asyncio.sleep(0.5)    # Simulate network delay
        batch = list(range(self.loaded, min(self.loaded + self.batch_size, self.total)))
        self.loaded += self.batch_size
        return batch

async def main():
    async for batch in AsyncStudentLoader(10, batch_size=3):
        print(f"Loaded batch: {batch}")

asyncio.run(main())
# Loaded batch: [0, 1, 2]
# Loaded batch: [3, 4, 5]
# Loaded batch: [6, 7, 8]
# Loaded batch: [9]
```

---

## Error Handling in Async Code

```python
import asyncio

async def risky_fetch(url):
    await asyncio.sleep(0.5)
    if "error" in url:
        raise ConnectionError(f"Failed to fetch {url}")
    return f"Data from {url}"

async def main():
    # Option 1: try/except
    try:
        result = await risky_fetch("https://api.error.com")
    except ConnectionError as e:
        print(f"Error: {e}")

    # Option 2: gather with return_exceptions
    results = await asyncio.gather(
        risky_fetch("https://api.good.com/data"),
        risky_fetch("https://api.error.com/bad"),
        risky_fetch("https://api.good.com/more"),
        return_exceptions=True,    # Don't crash, return exceptions
    )

    for r in results:
        if isinstance(r, Exception):
            print(f"Failed: {r}")
        else:
            print(f"Success: {r}")

asyncio.run(main())
```

---

## When to Use Async

| Use Async When | Use Sync When |
|----------------|---------------|
| Multiple I/O operations (API calls, DB queries) | CPU-heavy computation |
| Web servers handling many requests | Simple scripts |
| Chat applications, real-time feeds | File processing (usually) |
| Calling multiple external services | Single sequential task |

**Important:** Async does NOT make CPU-bound work faster. It helps with I/O-bound work (network, files, databases) by not wasting time waiting.

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Coroutine | `async def func():` | Define async function |
| Await | `await coroutine` | Wait for async result |
| Run | `asyncio.run(main())` | Start event loop |
| Gather | `asyncio.gather(t1, t2)` | Run tasks concurrently |
| Create task | `asyncio.create_task(coro)` | Fire-and-forget |
| Sleep | `await asyncio.sleep(n)` | Non-blocking wait |
| Async with | `async with resource:` | Async context manager |
| Async for | `async for item in aiterable:` | Async iteration |

---

## Practice Tasks

1. Write two async functions that simulate API calls with different delays and run them concurrently
2. Use `httpx` to fetch 5 URLs concurrently and compare time with sequential fetching
3. Create an async context manager for a simulated database connection
4. Write a function that uses `asyncio.gather()` with `return_exceptions=True` to handle partial failures
5. Build a simple async task queue that processes tasks concurrently with a limit

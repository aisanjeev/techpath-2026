# HTTP Requests — requests & httpx

**Module 03 — Python Libraries: Data, Automation & APIs | Topic 4**

---

## What is an HTTP Request?

When you open a website, your browser sends an **HTTP request** to a server and gets back a **response**. Python lets you do the same thing in code — call APIs, download data, and interact with web services.

**Real-world analogy:** An HTTP request is like ordering food at a restaurant. You (client) give your order (request) to the waiter (internet), who delivers it to the kitchen (server). The kitchen prepares your food (processes request) and the waiter brings it back (response).

### HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Fetch data | Get a list of students |
| **POST** | Create data | Add a new student |
| **PUT** | Replace data | Update entire student record |
| **PATCH** | Update data | Update student's marks only |
| **DELETE** | Remove data | Delete a student |

---

## requests Library (Synchronous)

```bash
pip install requests
```

### GET — Fetch Data

```python
import requests

# Simple GET request
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print(response.status_code)    # 200 (success)
print(response.headers["Content-Type"])    # application/json

# Parse JSON response
data = response.json()
print(data["title"])
print(data["body"])
```

### Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK — Success |
| 201 | Created — New resource created |
| 204 | No Content — Success but nothing to return |
| 400 | Bad Request — Invalid data |
| 401 | Unauthorized — Authentication required |
| 403 | Forbidden — No permission |
| 404 | Not Found — Resource does not exist |
| 500 | Internal Server Error — Server crashed |

### Checking Response Status

```python
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

if response.ok:    # True for 200-299 status codes
    data = response.json()
    print(f"Title: {data['title']}")
else:
    print(f"Error: {response.status_code}")

# Or raise an exception on error
response.raise_for_status()    # Raises HTTPError for 4xx/5xx
```

### GET with Query Parameters

```python
# Instead of: requests.get("https://api.com/users?page=2&limit=10")
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1, "_limit": 3},
)

posts = response.json()
print(f"Got {len(posts)} posts")
for post in posts:
    print(f"  - {post['title'][:50]}")
```

### POST — Send Data

```python
# Create a new post
new_post = {
    "title": "Learning Python at TechPath",
    "body": "Python Full Stack course is amazing!",
    "userId": 1,
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post,    # Automatically sets Content-Type: application/json
)

print(response.status_code)    # 201 (Created)
print(response.json())         # Returns the created post with an ID
```

### PUT and PATCH — Update Data

```python
# PUT — replace entire resource
updated_post = {
    "id": 1,
    "title": "Updated Title",
    "body": "Updated body content",
    "userId": 1,
}
response = requests.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json=updated_post,
)

# PATCH — update specific fields only
response = requests.patch(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"title": "Only Title Changed"},
)
```

### DELETE — Remove Data

```python
response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)    # 200 (OK)
```

---

## Authentication

### Bearer Token (Most Common for APIs)

```python
headers = {
    "Authorization": "Bearer your-api-token-here",
    "Content-Type": "application/json",
}

response = requests.get(
    "https://api.example.com/students",
    headers=headers,
)
```

### Basic Auth

```python
response = requests.get(
    "https://api.example.com/data",
    auth=("username", "password"),
)
```

### API Key in Headers

```python
response = requests.get(
    "https://api.example.com/data",
    headers={"X-API-Key": "your-api-key"},
)
```

---

## Handling JSON Responses

```python
response = requests.get("https://jsonplaceholder.typicode.com/users")
users = response.json()    # Parse JSON to Python list/dict

# Process the data
for user in users[:3]:
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"City: {user['address']['city']}")
    print("---")
```

---

## Sessions — Reuse Connection

```python
# Session reuses the connection and cookies
session = requests.Session()
session.headers.update({
    "Authorization": "Bearer my-token",
    "Accept": "application/json",
})

# All requests through this session have the headers
response1 = session.get("https://api.example.com/students")
response2 = session.get("https://api.example.com/courses")
```

---

## Error Handling

```python
import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    HTTPError,
    RequestException,
)

def fetch_data(url, timeout=10):
    """Fetch data from an API with proper error handling."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except ConnectionError:
        print("Could not connect to the server. Check your internet.")
    except Timeout:
        print(f"Request timed out after {timeout} seconds.")
    except HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
    except RequestException as e:
        print(f"Request failed: {e}")
    return None

data = fetch_data("https://jsonplaceholder.typicode.com/posts/1")
if data:
    print(data["title"])
```

---

## httpx — Modern Async HTTP Client

`httpx` is a modern alternative to `requests`. Its main advantage is **async support**.

```bash
pip install httpx
```

### Synchronous Usage (Same as requests)

```python
import httpx

response = httpx.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)
print(response.json()["title"])
```

### Async Usage — Concurrent Requests

```python
import asyncio
import httpx
import time

async def fetch_post(client, post_id):
    response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    return response.json()

async def main():
    start = time.time()

    async with httpx.AsyncClient() as client:
        # Fetch 10 posts concurrently
        tasks = [fetch_post(client, i) for i in range(1, 11)]
        posts = await asyncio.gather(*tasks)

    for post in posts:
        print(f"Post {post['id']}: {post['title'][:40]}")

    print(f"\nFetched {len(posts)} posts in {time.time() - start:.2f}s")

asyncio.run(main())
```

### httpx vs requests

| Feature | requests | httpx |
|---------|----------|-------|
| Sync support | Yes | Yes |
| Async support | No | Yes |
| HTTP/2 | No | Yes |
| Type hints | No | Yes |
| Speed (sync) | Similar | Similar |
| Speed (async) | N/A | Much faster for multiple requests |

---

## Practical Example: Weather API

```python
import requests

def get_weather(city):
    """Get weather for a city (using a free API)."""
    url = "https://wttr.in"
    params = {"format": "j1"}
    
    response = requests.get(f"{url}/{city}", params=params)
    
    if response.ok:
        data = response.json()
        current = data["current_condition"][0]
        return {
            "city": city,
            "temp_c": current["temp_C"],
            "description": current["weatherDesc"][0]["value"],
            "humidity": current["humidity"],
        }
    return None

# Get weather for Indian cities
for city in ["Bhopal", "Delhi", "Pune"]:
    weather = get_weather(city)
    if weather:
        print(f"{weather['city']}: {weather['temp_c']}°C, {weather['description']}")
```

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| GET | `requests.get(url)` | Fetch data |
| POST | `requests.post(url, json=data)` | Send data |
| PUT/PATCH | `requests.put(url, json=data)` | Update data |
| DELETE | `requests.delete(url)` | Remove data |
| JSON parsing | `response.json()` | Convert response to dict |
| Auth | `headers={"Authorization": "Bearer token"}` | Authenticate |
| Timeout | `requests.get(url, timeout=10)` | Prevent hanging |
| Session | `requests.Session()` | Reuse connection |
| Async | `httpx.AsyncClient()` | Concurrent requests |

---

## Practice Tasks

1. Fetch 5 posts from JSONPlaceholder and print their titles
2. POST a new resource to JSONPlaceholder and print the response
3. Build a function that fetches user data with proper error handling
4. Use httpx to fetch 10 URLs concurrently and compare time with sequential
5. Build a simple CLI that fetches weather for a city entered by the user

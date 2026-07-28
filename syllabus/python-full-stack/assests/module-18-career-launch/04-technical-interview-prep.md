# Technical Interview Preparation: Cracking the Code

**Module 18 -- Career Launch & Professional Portfolio | Topic 4**

---

## Understanding Interview Rounds in India

Think of a technical interview as a multi-level game. Each level tests a different skill. Knowing what to expect at each level lets you prepare strategically instead of randomly.

| Round | What Is Tested | Duration | Format |
|---|---|---|---|
| HR Screening | Communication, salary expectations, basic fit | 15-20 min | Phone/Video call |
| Online Test | Coding ability, MCQs, aptitude | 60-90 min | HackerRank, Codility, or similar |
| Technical Round 1 | DSA, Python, problem solving | 45-60 min | Live coding + questions |
| Technical Round 2 | System design, framework knowledge | 45-60 min | Whiteboard + discussion |
| HR Final | Offer discussion, joining date, salary negotiation | 20-30 min | Video/In-person |

Not all companies follow all five rounds. Startups often combine rounds or skip the online test. Large companies like TCS, Infosys, and Wipro usually have all five.

---

## Python DSA Essentials

Data Structures and Algorithms (DSA) questions appear in almost every technical interview. You do not need to master competitive programming, but you must be comfortable with the basics.

### Core Data Structures You Must Know

| Data Structure | Key Operations | When to Use |
|---|---|---|
| List (Array) | append, pop, index, slice | Ordered collection, random access |
| Dictionary (HashMap) | get, set, delete, keys | Fast lookups by key, counting |
| Set | add, remove, intersection, union | Unique elements, membership testing |
| String | slice, split, join, replace | Text processing |
| Stack (list) | append, pop | Last-in-first-out problems |
| Queue (deque) | append, popleft | First-in-first-out, BFS |
| Tuple | index, count | Immutable ordered data |

### Essential Algorithms

| Algorithm | Concept | Complexity |
|---|---|---|
| Linear Search | Check each element one by one | O(n) |
| Binary Search | Divide sorted array in half each time | O(log n) |
| Bubble Sort | Compare adjacent pairs, swap if needed | O(n^2) |
| Merge Sort | Divide, sort halves, merge | O(n log n) |
| Two Pointers | Two indices moving toward each other | O(n) |
| Sliding Window | Fixed/variable window over array | O(n) |
| Recursion | Function calls itself with smaller input | Varies |
| Hashing | Map keys to values for fast lookup | O(1) average |

---

## Top 10 DSA Problems with Python Solutions

### Problem 1: Two Sum

Given a list of numbers and a target, find two numbers that add up to the target.

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Example
print(two_sum([2, 7, 11, 15], 9))  # Output: [0, 1]
```

### Problem 2: Reverse a String

```python
def reverse_string(s):
    return s[::-1]

# Without slicing
def reverse_string_manual(s):
    chars = list(s)
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return "".join(chars)
```

### Problem 3: Check if a String Is a Palindrome

```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(is_palindrome("madam"))   # True
print(is_palindrome("hello"))   # False
```

### Problem 4: Find the Maximum Subarray Sum (Kadane's Algorithm)

```python
def max_subarray_sum(nums):
    current_sum = max_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum

print(max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # Output: 6
```

### Problem 5: Count Character Frequency

```python
def char_frequency(s):
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq

# Using Counter (preferred in interviews)
from collections import Counter
print(Counter("banana"))  # Counter({'a': 3, 'n': 2, 'b': 1})
```

### Problem 6: Remove Duplicates from a Sorted List

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

### Problem 7: Valid Parentheses (Stack)

```python
def is_valid_parentheses(s):
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0

print(is_valid_parentheses("({[]})"))  # True
print(is_valid_parentheses("({[})"))   # False
```

### Problem 8: Binary Search

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### Problem 9: Fibonacci Series (Recursion + Memoization)

```python
# Simple recursion (slow for large n)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# With memoization (fast)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_fast(n):
    if n <= 1:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)
```

### Problem 10: Merge Two Sorted Lists

```python
def merge_sorted(list1, list2):
    result = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result
```

---

## 20 Common Python Interview Questions with Answers

### Language Fundamentals

**Q1: What is the difference between a list and a tuple?**
A list is mutable (can be changed after creation), while a tuple is immutable (cannot be changed). Lists use square brackets `[]`, tuples use parentheses `()`. Tuples are faster and use less memory.

**Q2: What are *args and **kwargs?**
`*args` allows a function to accept any number of positional arguments as a tuple. `**kwargs` allows any number of keyword arguments as a dictionary.

```python
def greet(*args, **kwargs):
    for name in args:
        print(f"Hello {name}")
    for key, value in kwargs.items():
        print(f"{key}: {value}")
```

**Q3: What is a decorator?**
A decorator is a function that takes another function as input and extends its behavior without modifying it. The `@` syntax is used.

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b
```

**Q4: What is the difference between `==` and `is`?**
`==` checks value equality. `is` checks identity (same object in memory).

**Q5: What are list comprehensions?**
A concise way to create lists. `[x**2 for x in range(10) if x % 2 == 0]` creates a list of squares of even numbers.

### Web Development

**Q6: What is FastAPI and how is it different from Flask?**
FastAPI is an async Python web framework with automatic API documentation, type validation using Pydantic, and high performance. Flask is simpler but lacks built-in async support and automatic validation.

**Q7: What is an ORM?**
Object-Relational Mapping. It lets you interact with databases using Python objects instead of raw SQL. SQLAlchemy is the most popular Python ORM.

**Q8: What is a REST API?**
A REST API follows rules: uses HTTP methods (GET, POST, PUT, DELETE), is stateless (no session stored on server), returns JSON, and uses meaningful URL paths.

**Q9: What is JWT authentication?**
JSON Web Token. A token containing encoded user information signed with a secret key. The server generates it on login, the client sends it with each request, and the server verifies it without needing a database lookup.

**Q10: What is CORS?**
Cross-Origin Resource Sharing. A security feature that controls which domains can access your API. If your frontend is on `localhost:3000` and API on `localhost:8000`, you need CORS middleware.

### Database

**Q11: What is the difference between SQL and NoSQL?**
SQL databases (PostgreSQL, MySQL) use tables with fixed schemas and relationships. NoSQL databases (MongoDB, Redis) use flexible document/key-value formats. SQL is better for structured data with relationships.

**Q12: What is database indexing?**
An index is like a book's table of contents -- it helps the database find rows faster without scanning the entire table. Add indexes on columns used in WHERE, JOIN, and ORDER BY clauses.

**Q13: What are database migrations?**
Migrations track changes to your database schema in code. Alembic (for SQLAlchemy) generates migration files when you change models, letting you apply or rollback schema changes safely.

### DevOps

**Q14: What is Docker?**
Docker packages your application and its dependencies into a container that runs the same way on any machine. Think of it as a lightweight virtual machine.

**Q15: What is CI/CD?**
Continuous Integration (CI) automatically runs tests when you push code. Continuous Deployment (CD) automatically deploys code that passes tests. GitHub Actions is a popular CI/CD tool.

### AI/ML

**Q16: What is LangChain?**
A Python framework for building applications powered by large language models (LLMs). It provides tools for prompt management, chains, agents, memory, and retrieval.

**Q17: What is RAG?**
Retrieval-Augmented Generation. Instead of relying only on the LLM's training data, RAG retrieves relevant documents from a knowledge base and includes them in the prompt for more accurate answers.

### General

**Q18: What is version control and why is Git important?**
Version control tracks changes to code over time. Git lets multiple developers work on the same project, create branches for features, and merge changes safely.

**Q19: What is the difference between synchronous and asynchronous programming?**
Synchronous code runs one task at a time, waiting for each to finish. Asynchronous code (using `async/await`) can start a task and move to the next one while waiting, making it faster for I/O operations like API calls and database queries.

**Q20: What is test-driven development (TDD)?**
Write tests before writing code. Red (test fails) then Green (write code to pass) then Refactor (clean up). It ensures your code works correctly from the start.

---

## System Design Basics: Design a URL Shortener

System design questions test whether you can think about building real systems. Here is a beginner-friendly example.

### The Problem

Design a service like bit.ly that takes a long URL and returns a short URL.

### Step 1: Requirements

- Given a long URL, generate a short URL (e.g., `short.ly/abc123`).
- When someone visits the short URL, redirect to the original.
- Handle millions of URLs.

### Step 2: API Design

```
POST /shorten
Body: { "url": "https://very-long-url.com/page/123" }
Response: { "short_url": "https://short.ly/abc123" }

GET /{short_code}
Response: 301 Redirect to original URL
```

### Step 3: Database Schema

```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    click_count INTEGER DEFAULT 0
);
```

### Step 4: Short Code Generation

Use Base62 encoding (a-z, A-Z, 0-9) to convert an auto-increment ID to a short string. ID 1000 becomes "g8" in Base62.

### Step 5: Architecture

```
Client --> Load Balancer --> FastAPI Server --> PostgreSQL
                                           --> Redis (cache popular URLs)
```

This level of system design knowledge is sufficient for fresher interviews. You do not need to design distributed systems at this stage.

---

## Framework-Specific Questions

### FastAPI Questions

- How do you define a path parameter vs a query parameter?
- What is dependency injection in FastAPI?
- How do you handle authentication with FastAPI?
- What is the difference between `async def` and `def` in FastAPI routes?

### SQL Questions

- Write a query to find the second highest salary.
- What is the difference between INNER JOIN and LEFT JOIN?
- What is a subquery? Give an example.
- How do you optimize a slow query?

Practice answering these questions out loud, not just in your head. Speaking your thought process clearly is half the battle in a technical interview.

---

*TechPath Institute -- Building Careers in Technology*

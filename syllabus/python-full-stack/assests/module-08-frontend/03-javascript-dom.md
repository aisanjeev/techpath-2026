# JavaScript and DOM Manipulation

**Module 08 — Front-End for Python Developers | Topic 3**

---

## Why JavaScript Matters for Python Developers

You know Python. You can build APIs, process data, and work with databases. But Python runs on the **server**. Once your HTML reaches the user's browser, Python cannot touch it anymore.

JavaScript is the **only** programming language that runs inside a web browser. If you want a button click to show a message, a form to validate in real time, or a table to load data without refreshing the page — you need JavaScript.

> **Analogy:** Think of a restaurant in Delhi. Python is the kitchen staff — they prepare the food (data). HTML is the plate and table setup. But JavaScript is the waiter — it serves the food to the customer, takes new orders, and handles complaints, all without going back to the kitchen every time.

---

## Python vs JavaScript — A Quick Comparison

If you know Python, you already understand most programming concepts. JavaScript just writes them differently.

| Concept | Python | JavaScript |
|---|---|---|
| Variable | `name = "Rahul"` | `let name = "Rahul";` |
| Constant | `NAME = "Rahul"` (convention) | `const NAME = "Rahul";` |
| Print | `print("Hello")` | `console.log("Hello");` |
| String format | `f"Hello {name}"` | `` `Hello ${name}` `` |
| List / Array | `[1, 2, 3]` | `[1, 2, 3]` |
| Dictionary / Object | `{"name": "Rahul"}` | `{name: "Rahul"}` |
| Function | `def greet(name):` | `function greet(name) { }` |
| Arrow function | `lambda x: x * 2` | `(x) => x * 2` |
| If | `if age >= 18:` | `if (age >= 18) { }` |
| For loop | `for item in list:` | `for (let item of list) { }` |
| None / null | `None` | `null` or `undefined` |
| Boolean | `True`, `False` | `true`, `false` |
| Comments | `# comment` | `// comment` |

### Key Differences to Remember

1. **Semicolons**: JavaScript lines end with `;` (optional but recommended)
2. **Curly braces**: JavaScript uses `{ }` instead of indentation for code blocks
3. **let vs const**: Use `const` by default, `let` only when the value will change. Avoid `var`.
4. **===**: Always use `===` (strict equality), not `==` (loose equality that does type conversion)

---

## The DOM — Your Page as a Tree

When a browser loads your HTML, it creates an in-memory tree structure called the **DOM** (Document Object Model). Every HTML tag becomes a **node** in this tree. JavaScript interacts with this tree to read, change, add, or remove elements.

```
document
  └── html
       ├── head
       │    └── title
       └── body
            ├── header
            │    └── h1 ("TechPath Institute")
            ├── main
            │    ├── p ("Welcome, Ananya")
            │    └── ul
            │         ├── li ("Python")
            │         ├── li ("Django")
            │         └── li ("FastAPI")
            └── footer
```

### Selecting Elements

| Method | Returns | Example |
|---|---|---|
| `document.getElementById("id")` | Single element | `document.getElementById("name")` |
| `document.querySelector(".class")` | First matching element | `document.querySelector(".card")` |
| `document.querySelectorAll(".class")` | All matching elements (NodeList) | `document.querySelectorAll(".card")` |
| `document.querySelector("tag")` | First matching tag | `document.querySelector("h1")` |

```javascript
// Get a single element by ID
const nameInput = document.getElementById("student-name");

// Get the first element with class "course-card"
const firstCard = document.querySelector(".course-card");

// Get ALL elements with class "course-card"
const allCards = document.querySelectorAll(".course-card");

// Loop through all cards (like Python's for loop)
allCards.forEach((card) => {
    console.log(card.textContent);
});
```

---

## Event Handling — Responding to User Actions

Events are things that happen in the browser — clicks, key presses, form submissions, page loads. You "listen" for events and run code when they happen.

### Common Events

| Event | Triggers When |
|---|---|
| `click` | User clicks an element |
| `submit` | A form is submitted |
| `input` | User types in a text field |
| `change` | A dropdown or checkbox value changes |
| `keydown` | A key is pressed |
| `mouseover` | Mouse moves over an element |
| `DOMContentLoaded` | HTML is fully loaded (place scripts here) |

### Adding Event Listeners

```html
<button id="enroll-btn">Enroll Now</button>
<p id="message"></p>
```

```javascript
const button = document.getElementById("enroll-btn");
const message = document.getElementById("message");

button.addEventListener("click", () => {
    message.textContent = "You have been enrolled! Welcome to TechPath.";
});
```

### Form Submission Example

```html
<form id="search-form">
    <input type="text" id="search-input" placeholder="Search courses...">
    <button type="submit">Search</button>
</form>
<div id="results"></div>
```

```javascript
const form = document.getElementById("search-form");

form.addEventListener("submit", (event) => {
    event.preventDefault();   // Stop the page from reloading

    const query = document.getElementById("search-input").value;
    const results = document.getElementById("results");

    if (query.trim() === "") {
        results.textContent = "Please enter a search term.";
    } else {
        results.textContent = `Searching for: "${query}"...`;
    }
});
```

> **Important:** `event.preventDefault()` stops the form's default behaviour (reloading the page). Without it, the page refreshes and your JavaScript result disappears.

---

## Manipulating Elements

### Changing Text and HTML

```javascript
const heading = document.querySelector("h1");

// Change text content (safe, no HTML parsing)
heading.textContent = "Welcome to TechPath Institute, Bhopal";

// Change inner HTML (can include HTML tags — use with caution)
heading.innerHTML = "Welcome to <strong>TechPath</strong> Institute";
```

> **Security warning:** Never put user-supplied text into `innerHTML`. If Rahul types `<script>alert('hacked')</script>` in a form and you insert it with `innerHTML`, the script runs. This is called **XSS** (Cross-Site Scripting). Use `textContent` for user data.

### Changing CSS Classes

```javascript
const card = document.querySelector(".student-card");

// Add a class
card.classList.add("highlighted");

// Remove a class
card.classList.remove("highlighted");

// Toggle a class (add if missing, remove if present)
card.classList.toggle("highlighted");

// Check if a class exists
if (card.classList.contains("highlighted")) {
    console.log("Card is highlighted");
}
```

### Changing Inline Styles

```javascript
const notification = document.getElementById("notification");

notification.style.backgroundColor = "#d4edda";
notification.style.color = "#155724";
notification.style.padding = "15px";
notification.style.display = "block";
```

> **Tip:** Prefer adding/removing CSS classes over changing styles directly. Classes keep your styling in the CSS file where it belongs.

---

## Creating and Removing Elements

### Creating New Elements

```javascript
// Create a new student card
const card = document.createElement("div");
card.classList.add("student-card");
card.innerHTML = `
    <h3>Priya Sharma</h3>
    <p>Course: Python Full Stack</p>
    <p>City: Pune</p>
`;

// Add it to the page
const container = document.getElementById("student-list");
container.appendChild(card);
```

### Removing Elements

```javascript
const oldCard = document.getElementById("student-42");
oldCard.remove();
```

### Building a List from Data

```javascript
const students = [
    { name: "Rahul", course: "Python Full Stack", city: "Bhopal" },
    { name: "Ananya", course: "Data Science", city: "Delhi" },
    { name: "Amit", course: "DevOps", city: "Pune" },
    { name: "Sneha", course: "Python Full Stack", city: "Hyderabad" },
];

const table = document.getElementById("student-table-body");

students.forEach((student) => {
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${student.name}</td>
        <td>${student.course}</td>
        <td>${student.city}</td>
    `;
    table.appendChild(row);
});
```

---

## Fetch API — Talking to Your Python Backend

The Fetch API lets JavaScript send HTTP requests to your FastAPI or Django backend — without reloading the page. This is how modern web applications work.

### Basic GET Request

```javascript
// Fetch list of students from FastAPI backend
fetch("http://localhost:8000/api/v1/students")
    .then((response) => response.json())
    .then((result) => {
        console.log(result.data);  // Array of student objects
    })
    .catch((error) => {
        console.error("Failed to fetch students:", error);
    });
```

### The Same Request with async/await

The `.then()` chain works, but `async/await` reads more like Python and is easier to follow.

```javascript
async function loadStudents() {
    try {
        const response = await fetch("http://localhost:8000/api/v1/students");

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const result = await response.json();
        console.log(result.data);

    } catch (error) {
        console.error("Failed to load students:", error);
    }
}

// Call the function
loadStudents();
```

### Python vs JavaScript Comparison

```python
# Python (using httpx)
import httpx

async def load_students():
    response = await httpx.AsyncClient().get("http://localhost:8000/api/v1/students")
    data = response.json()
    print(data)
```

```javascript
// JavaScript (using fetch)
async function loadStudents() {
    const response = await fetch("http://localhost:8000/api/v1/students");
    const data = await response.json();
    console.log(data);
}
```

The structure is almost identical. If you can write `async/await` in Python, you can write it in JavaScript.

### POST Request — Sending Data to the Backend

```javascript
async function registerStudent() {
    const studentData = {
        name: "Priya Sharma",
        email: "priya@example.com",
        course: "python-fullstack",
        city: "Pune",
    };

    try {
        const response = await fetch("http://localhost:8000/api/v1/students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(studentData),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Registration failed");
        }

        const result = await response.json();
        console.log("Registered:", result.data);
        alert("Registration successful!");

    } catch (error) {
        console.error("Registration error:", error);
        alert("Failed to register. Please try again.");
    }
}
```

---

## Error Handling with try/catch

Just like Python's `try/except`, JavaScript uses `try/catch` to handle errors gracefully.

| Python | JavaScript |
|---|---|
| `try:` | `try {` |
| `except Exception as e:` | `} catch (error) {` |
| `finally:` | `} finally {` |

```javascript
async function fetchCourseDetails(courseId) {
    try {
        const response = await fetch(`http://localhost:8000/api/v1/courses/${courseId}`);

        if (!response.ok) {
            if (response.status === 404) {
                throw new Error("Course not found");
            }
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();
        displayCourse(result.data);

    } catch (error) {
        // Show a user-friendly message
        document.getElementById("course-detail").innerHTML = `
            <div class="error-message">
                <p>Could not load course details.</p>
                <p>${error.message}</p>
            </div>
        `;

    } finally {
        // Runs whether the request succeeded or failed
        document.getElementById("loading-spinner").style.display = "none";
    }
}
```

---

## Putting It Together — Live Search Example

Here is a complete example that connects to a FastAPI backend: a search box that filters students as you type.

```html
<div class="search-container">
    <input type="text" id="search-box"
           placeholder="Search students by name...">
    <div id="loading" style="display: none;">Searching...</div>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Course</th>
                <th>City</th>
            </tr>
        </thead>
        <tbody id="student-table"></tbody>
    </table>
    <p id="no-results" style="display: none;">No students found.</p>
</div>
```

```javascript
const searchBox = document.getElementById("search-box");
const tableBody = document.getElementById("student-table");
const loading = document.getElementById("loading");
const noResults = document.getElementById("no-results");

let searchTimeout;

searchBox.addEventListener("input", () => {
    // Debounce: wait 300ms after user stops typing
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        searchStudents(searchBox.value);
    }, 300);
});

async function searchStudents(query) {
    loading.style.display = "block";
    noResults.style.display = "none";
    tableBody.innerHTML = "";

    try {
        const response = await fetch(
            `http://localhost:8000/api/v1/students?search=${encodeURIComponent(query)}`
        );
        const result = await response.json();
        const students = result.data;

        if (students.length === 0) {
            noResults.style.display = "block";
            return;
        }

        students.forEach((student) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${student.name}</td>
                <td>${student.email}</td>
                <td>${student.course}</td>
                <td>${student.city}</td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        tableBody.innerHTML = `
            <tr><td colspan="4">Failed to load students. Is the server running?</td></tr>
        `;
    } finally {
        loading.style.display = "none";
    }
}

// Load all students when the page opens
searchStudents("");
```

---

## Summary

| Concept | What You Learned |
|---|---|
| Python vs JS syntax | Similar concepts, slightly different syntax (`let`, `const`, `=>`, `{}`) |
| DOM selection | `getElementById`, `querySelector`, `querySelectorAll` |
| Event handling | `addEventListener` for `click`, `submit`, `input` events |
| Element manipulation | `textContent`, `innerHTML`, `classList`, `style` |
| Creating elements | `createElement`, `appendChild`, `remove` |
| Fetch API | `fetch()` with `async/await` to call your Python backend |
| Error handling | `try/catch/finally` — just like Python's `try/except/finally` |

---

**Next Topic:** Consuming REST APIs from Frontend — CORS, tokens, CRUD operations, and building a full data-driven page.

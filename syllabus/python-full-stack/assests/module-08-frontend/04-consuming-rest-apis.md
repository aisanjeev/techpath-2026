# Consuming REST APIs from Frontend

**Module 08 — Front-End for Python Developers | Topic 4**

---

## The Big Picture

In the previous topics, you learned HTML (structure), CSS (style), and JavaScript (behaviour). Now you will combine all three to build a **data-driven frontend** — a page that talks to your Python backend, fetches real data, and displays it.

This is how every modern web application works. Swiggy fetches restaurant data from an API. Razorpay fetches payment status from an API. Your TechPath student portal will fetch student records from a FastAPI or Django REST Framework (DRF) API.

> **Analogy:** Imagine a bank in Bhopal. The frontend is the customer-facing counter. The backend is the vault and the database of accounts. The API is the set of forms and procedures the counter clerk follows to talk to the vault. CORS is the security guard who checks whether the clerk is authorized to access the vault from this particular branch.

---

## CORS — The Most Common Frontend-Backend Error

### What Is CORS?

CORS stands for **Cross-Origin Resource Sharing**. When your frontend (running at `http://localhost:3000`) tries to fetch data from your backend (running at `http://localhost:8000`), the browser blocks the request by default. This is a security feature.

An **origin** is the combination of protocol + domain + port:

| URL | Origin |
|---|---|
| `http://localhost:3000` | `http://localhost:3000` |
| `http://localhost:8000` | `http://localhost:8000` |
| `https://techpath.biz` | `https://techpath.biz` |
| `https://api.techpath.biz` | `https://api.techpath.biz` |

If the origin of your frontend does not match the origin of your backend, you have a **cross-origin** request, and the browser enforces CORS.

### The Error You Will See

Open your browser console (F12 > Console) and you will see:

```
Access to fetch at 'http://localhost:8000/api/v1/students'
from origin 'http://localhost:3000' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### How to Fix CORS in FastAPI

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Next.js / React dev server
        "http://localhost:4321",      # Astro dev server
        "https://techpath.biz",      # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Authorization, Content-Type, etc.
)
```

### How to Fix CORS in Django (DRF)

First install the package:

```bash
pip install django-cors-headers
```

Then configure it:

```python
# settings.py
INSTALLED_APPS = [
    ...
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",   # Must be near the top
    "django.middleware.common.CommonMiddleware",
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://techpath.biz",
]
```

### Quick CORS Troubleshooting Guide

| Problem | Solution |
|---|---|
| CORS error in browser console | Add your frontend origin to the backend's allowed origins |
| Works in Postman but not in browser | Postman does not enforce CORS — only browsers do |
| Error only on POST/PUT/DELETE | Ensure `allow_methods=["*"]` is set |
| Error mentions "preflight" | The browser sends an OPTIONS request first — your backend must handle it (FastAPI CORS middleware does this automatically) |
| Error only when sending Authorization header | Ensure `allow_headers=["*"]` includes Authorization |

---

## Authentication — Storing and Sending Tokens

Most APIs require authentication. After a user logs in, the backend returns a **token** (JWT or Firebase token). The frontend must store this token and send it with every subsequent request.

### Storing the Token

```javascript
// After successful login, store the token
function handleLogin(response) {
    const token = response.data.access_token;

    // Store in localStorage (persists across page refreshes)
    localStorage.setItem("auth_token", token);
}

// Retrieve the token later
function getToken() {
    return localStorage.getItem("auth_token");
}

// Remove on logout
function handleLogout() {
    localStorage.removeItem("auth_token");
    window.location.href = "/login";
}
```

### Sending the Token with Requests

```javascript
async function fetchProtectedData() {
    const token = localStorage.getItem("auth_token");

    if (!token) {
        window.location.href = "/login";
        return;
    }

    const response = await fetch("http://localhost:8000/api/v1/students", {
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
        },
    });

    if (response.status === 401) {
        // Token expired or invalid — redirect to login
        localStorage.removeItem("auth_token");
        window.location.href = "/login";
        return;
    }

    const result = await response.json();
    return result.data;
}
```

### localStorage vs sessionStorage

| Feature | `localStorage` | `sessionStorage` |
|---|---|---|
| Persists after closing browser | Yes | No |
| Shared across tabs | Yes | No |
| Storage limit | ~5 MB | ~5 MB |
| Use case | "Remember me" login | Sensitive one-time sessions |

> **Security note:** Storing tokens in `localStorage` is convenient but vulnerable to XSS attacks. For production applications, consider using httpOnly cookies instead. For learning purposes and internal tools, `localStorage` is acceptable.

---

## Making CRUD Requests with Fetch

CRUD stands for Create, Read, Update, Delete — the four basic operations of any data-driven application. Each maps to an HTTP method:

| Operation | HTTP Method | Example URL |
|---|---|---|
| Create | POST | `/api/v1/students` |
| Read (list) | GET | `/api/v1/students` |
| Read (single) | GET | `/api/v1/students/42` |
| Update | PUT | `/api/v1/students/42` |
| Delete | DELETE | `/api/v1/students/42` |

### Helper Function for API Calls

Writing `fetch` with headers every time is repetitive. Create a helper function:

```javascript
const API_BASE = "http://localhost:8000/api/v1";

async function apiCall(endpoint, method = "GET", body = null) {
    const token = localStorage.getItem("auth_token");

    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
    };

    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE}${endpoint}`, options);

    if (response.status === 401) {
        localStorage.removeItem("auth_token");
        window.location.href = "/login";
        return;
    }

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Request failed: ${response.status}`);
    }

    return response.json();
}
```

### Using the Helper — All Four CRUD Operations

```javascript
// CREATE — Register a new student
async function createStudent() {
    const result = await apiCall("/students", "POST", {
        name: "Priya Sharma",
        email: "priya@example.com",
        course: "python-fullstack",
        city: "Pune",
    });
    console.log("Created:", result.data);
}

// READ — Get all students
async function getStudents() {
    const result = await apiCall("/students");
    console.log("Students:", result.data);
    return result.data;
}

// READ — Get one student
async function getStudent(id) {
    const result = await apiCall(`/students/${id}`);
    console.log("Student:", result.data);
    return result.data;
}

// UPDATE — Change student details
async function updateStudent(id) {
    const result = await apiCall(`/students/${id}`, "PUT", {
        city: "Delhi",
        course: "data-science",
    });
    console.log("Updated:", result.data);
}

// DELETE — Remove a student
async function deleteStudent(id) {
    const result = await apiCall(`/students/${id}`, "DELETE");
    console.log("Deleted:", result);
}
```

---

## Handling JSON Responses

Your FastAPI backend returns responses in this format:

```json
{
    "success": true,
    "data": [
        { "id": 1, "name": "Rahul Verma", "email": "rahul@example.com", "course": "Python Full Stack", "city": "Bhopal" },
        { "id": 2, "name": "Ananya Joshi", "email": "ananya@example.com", "course": "Data Science", "city": "Delhi" }
    ],
    "timestamp": "2026-07-25T10:30:00Z"
}
```

### Displaying Data in an HTML Table

```javascript
async function displayStudentTable() {
    const tableBody = document.getElementById("student-table-body");
    tableBody.innerHTML = "";  // Clear existing rows

    try {
        const result = await apiCall("/students");
        const students = result.data;

        if (students.length === 0) {
            tableBody.innerHTML = `
                <tr><td colspan="5" class="text-center">No students found.</td></tr>
            `;
            return;
        }

        students.forEach((student) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.email}</td>
                <td>${student.course}</td>
                <td>${student.city}</td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        tableBody.innerHTML = `
            <tr><td colspan="5" class="text-danger">
                Error: ${error.message}
            </td></tr>
        `;
    }
}
```

### Displaying Data as Cards

```javascript
async function displayStudentCards() {
    const container = document.getElementById("student-cards");
    container.innerHTML = "";

    try {
        const result = await apiCall("/students");

        result.data.forEach((student) => {
            const card = document.createElement("div");
            card.classList.add("student-card");
            card.innerHTML = `
                <h3>${student.name}</h3>
                <p><strong>Email:</strong> ${student.email}</p>
                <p><strong>Course:</strong> ${student.course}</p>
                <p><strong>City:</strong> ${student.city}</p>
                <div class="card-actions">
                    <button onclick="editStudent(${student.id})" class="btn-edit">Edit</button>
                    <button onclick="removeStudent(${student.id})" class="btn-delete">Delete</button>
                </div>
            `;
            container.appendChild(card);
        });

    } catch (error) {
        container.innerHTML = `<p class="error">Failed to load students: ${error.message}</p>`;
    }
}
```

---

## Error Handling and Loading States

A professional application does not just show data. It also tells the user when data is loading and when something goes wrong.

### The Three States of Every Data Request

| State | What the User Sees |
|---|---|
| **Loading** | A spinner or "Loading..." text |
| **Success** | The actual data (table, cards, etc.) |
| **Error** | A helpful error message |

### Implementation Pattern

```html
<div id="loading" class="loading-spinner" style="display: none;">
    Loading students...
</div>
<div id="error-message" class="error-box" style="display: none;"></div>
<div id="student-list"></div>
```

```javascript
async function loadStudents() {
    const loading = document.getElementById("loading");
    const errorBox = document.getElementById("error-message");
    const studentList = document.getElementById("student-list");

    // Show loading, hide others
    loading.style.display = "block";
    errorBox.style.display = "none";
    studentList.innerHTML = "";

    try {
        const result = await apiCall("/students");
        displayStudents(result.data, studentList);

    } catch (error) {
        errorBox.textContent = `Could not load students: ${error.message}`;
        errorBox.style.display = "block";

    } finally {
        loading.style.display = "none";
    }
}
```

---

## Using Axios as an Alternative to Fetch

**Axios** is a popular JavaScript library that makes HTTP requests simpler than `fetch`. Many companies and frameworks (including our TechPath admin panel) use Axios.

### Why Use Axios Over Fetch?

| Feature | Fetch | Axios |
|---|---|---|
| Built into browser | Yes | No (needs install) |
| Auto JSON parsing | No (need `.json()`) | Yes |
| Request interceptors | No | Yes |
| Automatic error for 4xx/5xx | No | Yes |
| Timeout support | Manual | Built-in |
| Request cancellation | AbortController | Built-in |

### Installing Axios

```html
<!-- Via CDN (for quick projects) -->
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
```

```bash
# Via npm (for React, Next.js, or Node projects)
npm install axios
```

### Axios Examples

```javascript
// Create a reusable Axios instance
const api = axios.create({
    baseURL: "http://localhost:8000/api/v1",
    timeout: 10000,  // 10 second timeout
});

// Add token to every request automatically (interceptor)
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("auth_token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle 401 errors globally
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem("auth_token");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);

// GET — no need to call .json()
async function getStudents() {
    const response = await api.get("/students");
    return response.data.data;   // Axios auto-parses JSON
}

// POST
async function createStudent(studentData) {
    const response = await api.post("/students", studentData);
    return response.data.data;
}

// PUT
async function updateStudent(id, updates) {
    const response = await api.put(`/students/${id}`, updates);
    return response.data.data;
}

// DELETE
async function deleteStudent(id) {
    await api.delete(`/students/${id}`);
}
```

> Notice how Axios interceptors handle the token automatically. You set it up once and every request includes the token. This is exactly how the TechPath admin panel works (see `src/lib/api-client.ts` in the admin project).

---

## Complete Example — Student Management Page

Here is a full working page that talks to a FastAPI backend. It lists students, lets you add new ones, and delete existing ones.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Management — TechPath Institute</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
          rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>Student Management</h1>
        <p class="text-muted">TechPath Institute, Bhopal</p>

        <!-- Add Student Form -->
        <div class="card mb-4">
            <div class="card-header">Add New Student</div>
            <div class="card-body">
                <form id="add-student-form">
                    <div class="row g-3">
                        <div class="col-md-3">
                            <input type="text" class="form-control" id="name"
                                   placeholder="Full Name" required>
                        </div>
                        <div class="col-md-3">
                            <input type="email" class="form-control" id="email"
                                   placeholder="Email" required>
                        </div>
                        <div class="col-md-2">
                            <select class="form-select" id="course">
                                <option value="python-fullstack">Python Full Stack</option>
                                <option value="data-science">Data Science</option>
                                <option value="devops">DevOps</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <select class="form-select" id="city">
                                <option value="Bhopal">Bhopal</option>
                                <option value="Delhi">Delhi</option>
                                <option value="Pune">Pune</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <button type="submit" class="btn btn-primary w-100">
                                Add Student
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <!-- Status Messages -->
        <div id="loading" class="alert alert-info" style="display:none;">
            Loading students...
        </div>
        <div id="error" class="alert alert-danger" style="display:none;"></div>
        <div id="success" class="alert alert-success" style="display:none;"></div>

        <!-- Student Table -->
        <table class="table table-striped">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Course</th>
                    <th>City</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody id="student-table"></tbody>
        </table>
    </div>

    <script>
        const API_BASE = "http://localhost:8000/api/v1";

        // ---- Helper Function ----
        async function apiCall(endpoint, method = "GET", body = null) {
            const options = {
                method,
                headers: { "Content-Type": "application/json" },
            };
            const token = localStorage.getItem("auth_token");
            if (token) options.headers["Authorization"] = `Bearer ${token}`;
            if (body) options.body = JSON.stringify(body);

            const response = await fetch(`${API_BASE}${endpoint}`, options);
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || `Error ${response.status}`);
            }
            return response.json();
        }

        // ---- Display Functions ----
        function showMessage(type, text) {
            const el = document.getElementById(type);
            el.textContent = text;
            el.style.display = "block";
            if (type === "success") {
                setTimeout(() => { el.style.display = "none"; }, 3000);
            }
        }

        function hideMessage(type) {
            document.getElementById(type).style.display = "none";
        }

        // ---- Load Students ----
        async function loadStudents() {
            const tableBody = document.getElementById("student-table");
            showMessage("loading", "Loading students...");
            hideMessage("error");

            try {
                const result = await apiCall("/students");
                tableBody.innerHTML = "";

                result.data.forEach((s) => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${s.id}</td>
                        <td>${s.name}</td>
                        <td>${s.email}</td>
                        <td>${s.course}</td>
                        <td>${s.city}</td>
                        <td>
                            <button class="btn btn-sm btn-danger"
                                    onclick="deleteStudent(${s.id})">
                                Delete
                            </button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });

            } catch (error) {
                showMessage("error", `Failed to load: ${error.message}`);
            } finally {
                hideMessage("loading");
            }
        }

        // ---- Add Student ----
        document.getElementById("add-student-form")
            .addEventListener("submit", async (e) => {
                e.preventDefault();

                try {
                    await apiCall("/students", "POST", {
                        name: document.getElementById("name").value,
                        email: document.getElementById("email").value,
                        course: document.getElementById("course").value,
                        city: document.getElementById("city").value,
                    });

                    showMessage("success", "Student added successfully!");
                    e.target.reset();
                    loadStudents();   // Refresh the table

                } catch (error) {
                    showMessage("error", `Failed to add: ${error.message}`);
                }
            });

        // ---- Delete Student ----
        async function deleteStudent(id) {
            if (!confirm("Are you sure you want to delete this student?")) return;

            try {
                await apiCall(`/students/${id}`, "DELETE");
                showMessage("success", "Student deleted.");
                loadStudents();
            } catch (error) {
                showMessage("error", `Failed to delete: ${error.message}`);
            }
        }

        // ---- Initialize ----
        loadStudents();
    </script>
</body>
</html>
```

---

## Summary

| Concept | What You Learned |
|---|---|
| CORS | What it is, why browsers block cross-origin requests, how to fix it in FastAPI and Django |
| Token storage | `localStorage.setItem` / `getItem` for auth tokens |
| Sending tokens | `Authorization: Bearer <token>` header on every request |
| CRUD with fetch | GET, POST, PUT, DELETE using `fetch()` with `async/await` |
| JSON handling | `response.json()` to parse, `JSON.stringify()` to send |
| Data display | Rendering API data as HTML tables and cards |
| Loading and error states | Show spinners while loading, show messages on failure |
| Axios | Simpler syntax, auto JSON parsing, interceptors for tokens |

---

**Module 08 Complete.** You now know how to build a frontend that talks to your Python backend. In the next module, you will explore GenAI fundamentals and how to integrate AI capabilities into your applications.

# Quiz — FastAPI: Modern API Development

**Module 06 | 15 Questions**

---

### Q1. What is the main advantage of FastAPI over Flask?

- A) FastAPI uses JavaScript instead of Python
- B) FastAPI has built-in data validation, async support, and auto-generated docs ✅
- C) FastAPI does not require any installation
- D) FastAPI can only build REST APIs, not websites

> **Explanation:** FastAPI provides automatic data validation via Pydantic, native async/await support for high concurrency, and auto-generated Swagger/ReDoc documentation — features that Flask requires additional libraries to achieve.

---

### Q2. What server does FastAPI use to run, and what interface does it implement?

- A) Gunicorn, WSGI
- B) Apache, CGI
- C) Uvicorn, ASGI ✅
- D) Nginx, HTTP

> **Explanation:** FastAPI is an ASGI (Asynchronous Server Gateway Interface) framework and runs on Uvicorn, an ASGI server. ASGI supports async operations and WebSockets, unlike the older WSGI standard.

---

### Q3. In FastAPI, how does a path parameter differ from a query parameter?

- A) Path parameters are optional, query parameters are required
- B) Path parameters are part of the URL path (/students/{id}), query parameters come after ? (/students?city=Bhopal) ✅
- C) Path parameters are for POST requests only, query parameters are for GET only
- D) There is no difference between them

> **Explanation:** Path parameters are embedded in the URL path (e.g., /students/5 where 5 is the id). Query parameters come after the ? character (e.g., /students?city=Bhopal&limit=10). Path params identify a resource, query params filter or modify the request.

---

### Q4. What does `response_model=StudentResponse` do in a FastAPI endpoint?

- A) It validates the incoming request body
- B) It filters the response to only include fields defined in StudentResponse ✅
- C) It creates a database table called StudentResponse
- D) It redirects to another endpoint

> **Explanation:** response_model tells FastAPI to filter the response data through the specified Pydantic model. Only fields defined in that model are included in the response — even if the database object has extra fields like password.

---

### Q5. What is the purpose of `model_dump(exclude_unset=True)` in Pydantic?

- A) It removes all None values from the dictionary
- B) It returns only the fields that were explicitly provided by the client ✅
- C) It deletes the model from memory
- D) It converts the model to a JSON string

> **Explanation:** exclude_unset=True returns only fields that were explicitly set by the client. This is essential for partial updates (PATCH) — if the client sends only {"city": "Pune"}, you update only the city without overwriting other fields with None.

---

### Q6. Which Pydantic configuration is needed to read data from SQLAlchemy ORM objects?

- A) model_config = ConfigDict(strict=True)
- B) model_config = ConfigDict(from_attributes=True) ✅
- C) model_config = ConfigDict(json_mode=True)
- D) model_config = ConfigDict(orm_mode=True)

> **Explanation:** from_attributes=True (Pydantic v2) allows the model to read data from ORM objects by accessing their attributes. The older Pydantic v1 used orm_mode=True, which is now deprecated.

---

### Q7. What does `Depends(get_db)` do in a FastAPI endpoint?

- A) It downloads the database
- B) It automatically creates, injects, and closes a database session ✅
- C) It checks if the database exists
- D) It creates a new database table

> **Explanation:** Depends() is FastAPI's dependency injection system. get_db is a generator function that creates a database session, yields it to the endpoint function, and automatically handles commit/rollback/close after the request.

---

### Q8. Why should you NEVER store passwords as plain text?

- A) Plain text passwords take more storage space
- B) If the database is compromised, all user passwords are exposed ✅
- C) Python cannot compare plain text strings
- D) FastAPI does not allow plain text fields

> **Explanation:** If an attacker gains access to the database, plain text passwords expose all user accounts immediately. Hashed passwords (using bcrypt) are one-way — even if stolen, the original password cannot be recovered.

---

### Q9. What is the difference between authentication and authorization?

- A) They are the same thing
- B) Authentication verifies who you are; authorization determines what you can do ✅
- C) Authentication is for APIs; authorization is for websites
- D) Authentication uses tokens; authorization uses passwords

> **Explanation:** Authentication answers "Who are you?" (login with email/password). Authorization answers "What can you do?" (admin can delete users, students can only view their own data). Both are needed for secure APIs.

---

### Q10. What does CORS middleware do in a FastAPI application?

- A) Compresses response data for faster transfer
- B) Allows a frontend on a different domain/port to make API requests ✅
- C) Encrypts all API communication
- D) Caches API responses for better performance

> **Explanation:** CORS (Cross-Origin Resource Sharing) allows requests from different origins. Without CORS middleware, a React frontend on localhost:3000 cannot call a FastAPI backend on localhost:8000 — the browser blocks it.

---

### Q11. When should you use `BackgroundTasks` in FastAPI?

- A) For database queries that take more than 1 second
- B) For tasks like sending emails or logging that should not delay the response ✅
- C) For all POST requests
- D) For handling file uploads

> **Explanation:** BackgroundTasks run after the response is sent to the client. They are perfect for non-critical tasks like sending emails, push notifications, logging, and cache warming that should not slow down the API response.

---

### Q12. What is the purpose of `dependency_overrides` in FastAPI testing?

- A) To skip authentication in production
- B) To replace real dependencies (like the database) with test versions ✅
- C) To override endpoint functions
- D) To change the API URL

> **Explanation:** dependency_overrides lets you replace dependencies during testing. The most common use is replacing the real database session (get_db) with a test database session that uses an in-memory SQLite database.

---

### Q13. In a WebSocket connection, what is the key difference from HTTP?

- A) WebSocket only works with JavaScript
- B) WebSocket maintains an open connection for bidirectional real-time communication ✅
- C) WebSocket is faster but less secure
- D) WebSocket can only send text, not JSON

> **Explanation:** HTTP is request-response: the client asks, the server answers, the connection closes. WebSocket keeps the connection open, allowing both client and server to send messages at any time — perfect for chat, live notifications, and real-time updates.

---

### Q14. What is the correct HTTP status code to return when creating a new resource?

- A) 200 OK
- B) 201 Created ✅
- C) 204 No Content
- D) 301 Moved Permanently

> **Explanation:** 201 Created indicates that a new resource was successfully created. 200 OK is for general success, 204 is for successful operations with no response body (like DELETE), and 301 is for URL redirects.

---

### Q15. What does the `--reload` flag do when running `uvicorn main:app --reload`?

- A) Reloads the database on every request
- B) Automatically restarts the server when you save code changes ✅
- C) Reloads all dependencies from pip
- D) Clears the server cache

> **Explanation:** --reload enables auto-reload: the server watches your Python files and restarts automatically when you save changes. This is for development only — do not use in production as it adds overhead.

---

**Score Guide:**
- 13-15 correct: Excellent — you are ready to build production APIs
- 10-12 correct: Good — review the topics you missed
- 7-9 correct: Fair — revisit the notes and practice building endpoints
- Below 7: Needs improvement — go through each topic again carefully

---

*TechPath Institute — Python Full Stack Development*

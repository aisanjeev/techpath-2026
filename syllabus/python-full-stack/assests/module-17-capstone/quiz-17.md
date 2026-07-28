# Quiz: Full-Stack AI Product — Capstone Development

**Module 17 | 15 Questions | Pass Mark: 60%**

---

## Q1. What does MVP stand for in the context of product development?
- A) Most Valuable Product
- B) Minimum Viable Product ✓
- C) Maximum Version Product
- D) Minimum Version Plan

> **Explanation:** MVP stands for Minimum Viable Product — the smallest version of your product that delivers value and can be tested with real users.

---

## Q2. Which of the following is the BEST first step when choosing a capstone project idea?
- A) Pick the most complex technology stack available
- B) Copy a popular app like Instagram or Amazon
- C) Identify a real problem that people face and validate it ✓
- D) Start coding immediately and decide the idea later

> **Explanation:** The best approach is problem-first thinking — identify a real problem, validate that people actually face it, and then design a solution around it.

---

## Q3. In a FastAPI project, what is the purpose of the `async_sessionmaker` in database.py?
- A) It creates HTML templates for the frontend
- B) It generates API documentation automatically
- C) It creates async database sessions for handling DB operations ✓
- D) It manages user authentication tokens

> **Explanation:** async_sessionmaker creates asynchronous database session factories that provide AsyncSession instances for performing database operations without blocking the event loop.

---

## Q4. Why is Redis commonly used alongside PostgreSQL in a capstone project?
- A) Redis replaces PostgreSQL for all database operations
- B) Redis provides caching, reducing repeated database queries and AI API calls ✓
- C) Redis is required by FastAPI to function properly
- D) Redis is used only for storing user passwords securely

> **Explanation:** Redis is an in-memory data store used for caching frequently accessed data, storing session information, and reducing expensive database queries or AI API calls.

---

## Q5. What does the HTMX attribute `hx-target` do?
- A) It specifies the URL to send the request to
- B) It specifies which HTML element should be updated with the response ✓
- C) It defines when the request should be triggered
- D) It sets the HTTP method (GET, POST, etc.)

> **Explanation:** hx-target specifies the CSS selector of the HTML element where the server's response HTML should be inserted, allowing partial page updates without a full reload.

---

## Q6. When connecting a vanilla JavaScript frontend to a FastAPI backend on different ports, what must be configured on the backend?
- A) A WebSocket connection
- B) CORS (Cross-Origin Resource Sharing) middleware ✓
- C) A reverse proxy server
- D) HTTPS certificates

> **Explanation:** When the frontend and backend run on different ports (origins), browsers block cross-origin requests by default. CORS middleware must be added to FastAPI to allow the frontend to make API calls.

---

## Q7. What does RAG stand for in the context of AI features?
- A) Rapid Application Generation
- B) Retrieval-Augmented Generation ✓
- C) Random Answer Generator
- D) Recursive Algorithm Graph

> **Explanation:** RAG stands for Retrieval-Augmented Generation. It retrieves relevant documents from a knowledge base and uses them as context for the LLM to generate accurate, grounded answers.

---

## Q8. In a RAG pipeline, what is the role of ChromaDB?
- A) It serves as the main relational database for user data
- B) It stores document chunks as vectors for similarity search ✓
- C) It handles user authentication and session management
- D) It renders the frontend user interface

> **Explanation:** ChromaDB is a vector database that stores document embeddings (numerical representations) and enables fast similarity search to find the most relevant document chunks for a given query.

---

## Q9. In a GitHub Actions workflow, what does the `needs` keyword do in a job definition?
- A) It lists the packages that need to be installed
- B) It specifies that this job must wait for another job to complete successfully before running ✓
- C) It defines the required environment variables
- D) It sets the minimum hardware requirements for the runner

> **Explanation:** The 'needs' keyword creates a dependency between jobs. For example, 'needs: test' means the deploy job will only run after the test job completes successfully.

---

## Q10. Where should sensitive values like API keys and database passwords be stored in a GitHub Actions workflow?
- A) Directly in the workflow YAML file
- B) In the README.md file
- C) In GitHub repository Secrets (Settings > Secrets > Actions) ✓
- D) In a public .env file committed to the repository

> **Explanation:** Sensitive values must be stored in GitHub repository Secrets, which are encrypted and accessible in workflows via the syntax ${{ secrets.SECRET_NAME }}. Never commit secrets to the repository.

---

## Q11. In FastAPI, what is the automatic benefit of using Pydantic schemas for your endpoint parameters?
- A) It automatically creates a frontend UI
- B) It generates interactive Swagger/OpenAPI documentation at /docs ✓
- C) It automatically deploys the application
- D) It creates database tables from the schemas

> **Explanation:** FastAPI uses Pydantic schemas and type hints to automatically generate interactive Swagger UI documentation at /docs, where developers can test API endpoints directly in the browser.

---

## Q12. Which section should come FIRST in a professional README file?
- A) License information
- B) Project structure and folder layout
- C) Project name, one-sentence description, and a screenshot ✓
- D) Detailed API endpoint documentation

> **Explanation:** The README should open with the project name, a clear one-sentence description, and a screenshot or demo GIF. This gives readers an immediate understanding of what the project does.

---

## Q13. During a 15-minute capstone demo, what should you show FIRST?
- A) The code editor with all your source files
- B) The CI/CD pipeline configuration
- C) The problem statement — what problem your project solves and for whom ✓
- D) The tech stack and architecture diagram

> **Explanation:** Always open with the problem statement. The audience needs to understand WHY your project exists before they care about HOW you built it. Start with the problem, then show the solution.

---

## Q14. What is the 'happy path' in the context of a live demo?
- A) The path through the code that has the most comments
- B) The main use case working perfectly with no errors or edge cases ✓
- C) The most complex feature in the application
- D) The deployment pipeline from local to production

> **Explanation:** The happy path is the primary use case working exactly as intended, with valid inputs and no error conditions. Always demo the happy path first to show the core value of your product.

---

## Q15. Sneha is building a Freelancer Invoice Manager for her capstone. Which AI feature is MOST appropriate for this project?
- A) An AI chatbot that writes poetry about invoices
- B) An AI expense categorizer that classifies transactions into categories like travel, food, and office supplies ✓
- C) An AI that generates random invoice amounts
- D) An AI that automatically pays all invoices without user approval

> **Explanation:** An AI expense categorizer is the most practical and useful AI feature for an invoice manager. It solves a real problem (manually categorizing expenses) and demonstrates meaningful AI integration.

---

*TechPath Institute — Full-Stack AI Product: Capstone Development*

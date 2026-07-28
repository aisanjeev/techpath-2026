# Quiz: Spec-Kit Development Methodology

**Module 16 | 15 Questions | Pass Mark: 60%**

---

## Q1. What is the primary purpose of a Spec-Kit in software development?

- A) To write the final code for the application
- B) To plan and document what to build, how to build it, and how to deliver it before coding begins ✓
- C) To test the application after deployment
- D) To create marketing materials for the product

> **Explanation:** A Spec-Kit is a collection of planning documents (PRD, system design, API spec, DB schema, sprint plan, deployment plan) created before coding begins to ensure clarity and alignment.

---

## Q2. Which section of a PRD explicitly lists features that will NOT be included in the current version?

- A) Problem Statement
- B) User Stories
- C) Out of Scope ✓
- D) Success Metrics

> **Explanation:** The Out of Scope section prevents scope creep by clearly listing features that are excluded from the current version of the product.

---

## Q3. In Gherkin syntax, what does the 'Given' keyword represent?

- A) The action the user performs
- B) The expected outcome after the action
- C) The initial context or precondition before the action ✓
- D) The error message when something goes wrong

> **Explanation:** In Gherkin syntax, 'Given' describes the precondition or initial state, 'When' describes the action, and 'Then' describes the expected outcome.

---

## Q4. In the C4 model, which diagram level shows the major applications, databases, and message queues inside your system?

- A) Level 1 - Context Diagram
- B) Level 2 - Container Diagram ✓
- C) Level 3 - Component Diagram
- D) Level 4 - Code Diagram

> **Explanation:** The Container Diagram (Level 2) shows the major containers such as web apps, APIs, databases, and message queues within the system boundary.

---

## Q5. What is the main benefit of API-First design?

- A) It eliminates the need for testing
- B) It allows frontend and backend teams to work in parallel using a shared contract ✓
- C) It automatically generates the entire application code
- D) It replaces the need for a database

> **Explanation:** API-First design defines the contract before code is written, enabling frontend and backend teams to work simultaneously since both agree on the interface upfront.

---

## Q6. In an OpenAPI specification, what does the '$ref' keyword do?

- A) Defines a new API endpoint
- B) References a reusable schema or response definition to avoid duplication ✓
- C) Sets the API version number
- D) Specifies the server URL

> **Explanation:** The $ref keyword references a reusable component (schema, response, parameter) defined in the components section, avoiding repetition and maintaining a single source of truth.

---

## Q7. A many-to-many relationship between 'products' and 'categories' is implemented using:

- A) A foreign key in the products table only
- B) A foreign key in the categories table only
- C) A junction table with foreign keys to both products and categories ✓
- D) Storing category names as a comma-separated list in the products table

> **Explanation:** Many-to-many relationships require a junction (bridge) table that contains foreign keys referencing both related tables. Storing comma-separated values violates First Normal Form.

---

## Q8. What does First Normal Form (1NF) require?

- A) Every table must have a primary key and a foreign key
- B) Each column must contain only a single atomic value, not lists or arrays ✓
- C) All non-key columns must depend on the entire primary key
- D) No column should depend on another non-key column

> **Explanation:** First Normal Form requires that each column contains a single, atomic value. Multi-valued columns (like comma-separated phone numbers) must be split into separate rows or a related table.

---

## Q9. What is the correct Alembic command to roll back the most recent database migration?

- A) alembic rollback last
- B) alembic downgrade -1 ✓
- C) alembic undo head
- D) alembic revert --latest

> **Explanation:** The command 'alembic downgrade -1' rolls back exactly one migration. Each migration has an upgrade() and downgrade() function for applying and reversing changes.

---

## Q10. In Scrum, what are 'story points' used to measure?

- A) The number of hours a task will take
- B) The complexity and effort of a task, not its duration ✓
- C) The number of lines of code to be written
- D) The priority level of a task

> **Explanation:** Story points measure the complexity and effort required for a task using the Fibonacci sequence (1, 2, 3, 5, 8, 13). They are not a direct measure of time because different developers work at different speeds.

---

## Q11. During a daily stand-up meeting, each team member answers three questions. Which of the following is NOT one of them?

- A) What did I do yesterday?
- B) What will I do today?
- C) How many story points did I complete? ✓
- D) Is anything blocking me?

> **Explanation:** The three stand-up questions are: What did I do yesterday? What will I do today? Is anything blocking me? Story point tracking happens at the sprint level, not daily stand-ups.

---

## Q12. Which of the following is a security vulnerability that should be caught during code review?

- A) Using snake_case for Python variable names
- B) Writing SQL queries with f-string interpolation of user input ✓
- C) Using descriptive variable names instead of single letters
- D) Adding comments that explain why a piece of code exists

> **Explanation:** Using f-string interpolation to build SQL queries with user input creates SQL injection vulnerabilities. Always use parameterized queries or an ORM like SQLAlchemy.

---

## Q13. What is the recommended maximum size for a pull request to ensure effective code review?

- A) Under 50 lines
- B) Under 400 lines ✓
- C) Under 2000 lines
- D) There is no recommended limit

> **Explanation:** Pull requests under 400 lines get thorough reviews. Large PRs tend to be rubber-stamped because reviewers lose focus and miss issues in large diffs.

---

## Q14. What is the difference between a liveness health check (/health) and a readiness health check (/health/ready)?

- A) There is no difference; they check the same thing
- B) Liveness checks if the process is running; readiness checks if it can serve requests (database connected, etc.) ✓
- C) Liveness checks the database; readiness checks the CPU usage
- D) Liveness is for frontend apps; readiness is for backend apps

> **Explanation:** A liveness check confirms the application process is running. A readiness check goes further to verify the app can actually serve requests by checking dependencies like database connectivity.

---

## Q15. After a production incident, what is the primary purpose of writing a post-mortem?

- A) To assign blame to the developer who caused the issue
- B) To document what happened, identify the root cause, and define action items to prevent recurrence ✓
- C) To calculate the financial loss caused by the incident
- D) To update the product's marketing page

> **Explanation:** A post-mortem is a blameless document that records the timeline, root cause, what went well, what went wrong, and action items. Its goal is learning and prevention, not blame.

---

*TechPath Institute -- Spec-Kit Development Methodology*

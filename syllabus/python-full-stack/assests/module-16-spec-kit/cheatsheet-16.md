# Cheat Sheet: Spec-Kit Development Methodology

**Module 16 -- Quick Reference**

---

## Spec-Kit Components Checklist

| Document | Purpose | Key Question It Answers |
|----------|---------|------------------------|
| PRD | Product requirements | What are we building and why? |
| System Design | Architecture and tech stack | How is the system structured? |
| API Spec | Endpoint contracts | What data goes in and out? |
| DB Schema | Data organization | How is data stored and related? |
| Sprint Plan | Work scheduling | What gets built, when, by whom? |
| Deployment Plan | Shipping and monitoring | How do we safely go live? |

---

## PRD Template Outline

```
1. Problem Statement      --> Who has the problem? What is the impact?
2. Target Users           --> Table of user types, descriptions, pain points
3. User Stories            --> As a [user], I want to [action], so that [benefit]
4. Acceptance Criteria     --> Gherkin: Given / When / Then
5. Out of Scope            --> What is NOT included in this version
6. Success Metrics         --> Measurable outcomes with target values
7. Dependencies            --> External services, APIs, assumptions
8. Timeline                --> High-level milestones with dates
```

### Gherkin Syntax Quick Reference

```gherkin
Given [precondition]
  And [additional precondition]
When [action is performed]
Then [expected result]
  And [additional expected result]
```

---

## System Design Steps

1. Identify users and external systems (Context Diagram)
2. Define major containers: apps, databases, queues (Container Diagram)
3. Break each container into components (Component Diagram)
4. Map data flow for key use cases
5. Choose tech stack with justification
6. Document key design decisions

### C4 Model Levels

| Level | Shows | Audience |
|-------|-------|----------|
| 1 - Context | System + users + external services | Everyone |
| 2 - Container | Apps, databases, message queues | Developers, architects |
| 3 - Component | Modules inside a container | Developers on that container |
| 4 - Code | Classes and functions | Individual developers |

### Diagram Tools

| Tool | Type | Best For |
|------|------|----------|
| draw.io | Visual editor | All diagrams |
| Excalidraw | Sketch-style | Quick whiteboarding |
| Mermaid | Text-based (Markdown) | Docs in Git |

---

## OpenAPI Spec Structure

```yaml
openapi: 3.0.0
info:
  title: API Name
  version: 1.0.0
servers:
  - url: http://localhost:8000/api/v1
paths:
  /resource:
    get:
      summary: List resources
      parameters: [...]
      responses:
        '200': { description: Success, content: ... }
    post:
      summary: Create resource
      requestBody: { content: ... }
      responses:
        '201': { description: Created }
components:
  schemas:
    ResourceCreate: { type: object, properties: ... }
    Resource: { type: object, properties: ... }
  responses:
    NotFound: { description: Resource not found }
```

### Common HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing or invalid auth token |
| 403 | Forbidden | Authenticated but not allowed |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Duplicate resource (e.g., email taken) |
| 500 | Internal Server Error | Unhandled server error |

---

## Database Design Rules

### Relationship Patterns

| Type | Implementation | Example |
|------|---------------|---------|
| One-to-Many | Foreign key in the "many" table | `orders.user_id` references `users.id` |
| Many-to-Many | Junction table with two foreign keys | `product_categories(product_id, category_id)` |
| One-to-One | Foreign key with unique constraint | `user_profiles.user_id` (unique) |

### Normalization Quick Guide

| Form | Rule | Fix |
|------|------|-----|
| 1NF | No multi-valued columns | Split into separate table |
| 2NF | Every non-key column depends on the full key | Move partial dependencies out |
| 3NF | No non-key column depends on another non-key | Move transitive dependencies out |

### Alembic Commands

```bash
alembic revision --autogenerate -m "description"   # Create migration
alembic upgrade head                                 # Apply all migrations
alembic upgrade heads                                # Apply all (multiple branches)
alembic downgrade -1                                 # Roll back last migration
alembic current                                      # Show current version
alembic history                                      # Show migration history
```

---

## Sprint Planning Steps

1. Review previous sprint outcomes
2. Product owner presents prioritized backlog
3. Team estimates stories using story points (Fibonacci: 1, 2, 3, 5, 8, 13)
4. Select stories up to team velocity
5. Define sprint goal in one sentence
6. Assign tasks to team members
7. Identify dependencies between stories

### Story Point Reference

| Points | Complexity | Example |
|--------|-----------|---------|
| 1 | Trivial | Fix a typo |
| 2 | Simple | Add a field to a form |
| 3 | Moderate | CRUD API for new entity |
| 5 | Complex | File upload with validation |
| 8 | Very complex | WebSocket real-time feature |
| 13 | Huge | Payment gateway integration |

### GitHub Issue Template

```markdown
## Title: [Short descriptive title]

## Description
[What needs to be done and why]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Labels: [backend/frontend, sprint-N, priority]
## Story Points: [N]
```

---

## Code Review Checklist

### Readability
- [ ] Variable and function names are descriptive
- [ ] Functions do one thing (Single Responsibility)
- [ ] No magic numbers (use named constants)
- [ ] Comments explain WHY, not WHAT

### DRY and SOLID
- [ ] No duplicated code blocks
- [ ] Each class/module has one responsibility
- [ ] Dependencies are injected, not hardcoded

### Security
- [ ] No hardcoded secrets (API keys, passwords)
- [ ] No raw SQL string interpolation (use parameterized queries)
- [ ] No `dangerouslySetInnerHTML` with user input
- [ ] All endpoints have proper authentication
- [ ] Users can only access their own data (authorization)
- [ ] File uploads validated for type and size

### Tests
- [ ] Happy path tested
- [ ] Edge cases tested (empty input, max values)
- [ ] Error cases tested
- [ ] No test duplication

### Naming Conventions

| Context | Convention | Example |
|---------|-----------|---------|
| Python variable | snake_case | `user_count` |
| Python class | PascalCase | `UserProfile` |
| JS variable | camelCase | `userCount` |
| JS component | PascalCase | `UserProfile` |
| DB table | snake_case, plural | `order_items` |
| API endpoint | kebab-case | `/order-items` |

---

## Deployment Checklist

### Pre-Deploy
- [ ] All tests pass
- [ ] Linting and type checks pass
- [ ] PR reviewed and approved
- [ ] Environment variables verified on server
- [ ] Database backup taken
- [ ] Migrations tested on staging

### Deploy
- [ ] Pull latest code on server
- [ ] Install dependencies
- [ ] Run database migrations
- [ ] Build static assets (if applicable)
- [ ] Restart application service

### Post-Deploy
- [ ] Health endpoint returns 200
- [ ] Check error logs for 5 minutes
- [ ] Verify key user flows manually
- [ ] Monitor error rates in Sentry
- [ ] Confirm UptimeRobot shows green

### Rollback Plan
```bash
git log --oneline -5        # Find last good commit
git checkout <commit>        # Switch to it
alembic downgrade -1         # Roll back migration if needed
systemctl restart myapp      # Restart the service
curl localhost:8000/health   # Verify health
```

### Incident Severity

| Level | Impact | Response Time |
|-------|--------|---------------|
| SEV-1 | Complete outage | Within 15 minutes |
| SEV-2 | Major feature broken | Within 1 hour |
| SEV-3 | Minor feature broken | Within 4 hours |
| SEV-4 | Cosmetic issue | Next business day |

### Monitoring Tools (Free Tiers)

| Tool | Purpose |
|------|---------|
| UptimeRobot | Uptime monitoring (50 free monitors) |
| Sentry | Error tracking (5K events/month free) |
| journalctl | System logs on Linux servers |

---

*TechPath Institute -- Spec-Kit Development Methodology*

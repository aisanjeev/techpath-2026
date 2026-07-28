# Code Review Checklist

**Module 16 -- Spec-Kit Development Methodology | Topic 7**

---

## Why Code Reviews Matter

A code review is when one or more team members examine code written by another team member before it is merged into the main codebase. It is one of the most effective practices for catching bugs, improving code quality, and sharing knowledge across the team.

Think of it like proofreading an essay. The writer often misses their own mistakes because they know what they meant to write. A fresh pair of eyes catches spelling errors, unclear sentences, and logical gaps. Code reviews work the same way -- a reviewer sees things the author cannot.

### Benefits of Code Reviews

| Benefit | Explanation |
|---------|-------------|
| Catch bugs early | A reviewer might spot a null check you missed |
| Knowledge sharing | Everyone learns from reading each other's code |
| Consistent code style | Team maintains uniform coding standards |
| Better design | Reviewers suggest simpler or more efficient approaches |
| Reduced bus factor | More than one person understands each piece of code |
| Security | Reviewers catch hardcoded secrets or SQL injection |

---

## Pull Request Etiquette

Before diving into what to check, here are rules for creating and reviewing pull requests (PRs).

### For the Author (Person Creating the PR)

| Rule | Why |
|------|-----|
| Keep PRs small (under 400 lines) | Large PRs get rubber-stamped, not reviewed |
| Write a clear description | Help the reviewer understand what changed and why |
| Link to the issue | Connect the PR to the requirement it fulfills |
| Self-review first | Read your own diff before requesting review |
| Add screenshots for UI changes | Show the reviewer what the change looks like |
| Respond to feedback promptly | Do not let PRs go stale |

### For the Reviewer

| Rule | Why |
|------|-----|
| Review within 24 hours | Waiting blocks the author |
| Be kind and constructive | "Consider renaming this" not "This name is terrible" |
| Explain your reasoning | "This could cause an N+1 query because..." |
| Approve when ready | Do not block on trivial issues (use "nit:" prefix) |
| Distinguish suggestions from requirements | Use "nit:" for optional, "blocking:" for required |

### PR Description Template

```markdown
## What
[One sentence describing the change]

## Why
[Why this change is needed, link to issue]

## How
[Brief explanation of the approach taken]

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Edge cases considered

## Screenshots (if UI change)
[Before/After screenshots]
```

---

## The Checklist: What to Review

### 1. Readability

Code is read far more often than it is written. Prioritize readability.

| Check | Good | Bad |
|-------|------|-----|
| Variable names are descriptive | `student_count` | `sc`, `x`, `temp` |
| Functions do one thing | `calculate_total()` | `process_data_and_send_email()` |
| Comments explain WHY, not WHAT | `# Retry because the API is flaky` | `# increment i by 1` |
| No magic numbers | `MAX_RETRIES = 3` | `if retries > 3:` |
| Consistent formatting | Team uses Black/Prettier | Mixed tabs and spaces |

### 2. Naming Conventions

| Language | Convention | Example |
|----------|-----------|---------|
| Python variables/functions | snake_case | `get_student_by_id` |
| Python classes | PascalCase | `StudentProfile` |
| Python constants | UPPER_SNAKE_CASE | `MAX_FILE_SIZE` |
| JavaScript variables/functions | camelCase | `getStudentById` |
| JavaScript classes/components | PascalCase | `StudentProfile` |
| Database tables | snake_case, plural | `order_items` |
| API endpoints | kebab-case or snake_case | `/api/v1/order-items` |

### 3. DRY (Don't Repeat Yourself)

Look for duplicated code that should be extracted into a function or utility.

**Bad -- duplicated validation logic:**

```python
# In registration endpoint
if len(password) < 8:
    raise ValueError("Password must be at least 8 characters")
if not any(c.isupper() for c in password):
    raise ValueError("Password must contain an uppercase letter")

# In password reset endpoint (same code copied!)
if len(new_password) < 8:
    raise ValueError("Password must be at least 8 characters")
if not any(c.isupper() for c in new_password):
    raise ValueError("Password must contain an uppercase letter")
```

**Good -- extracted into a reusable function:**

```python
def validate_password(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain an uppercase letter")

# In registration endpoint
validate_password(password)

# In password reset endpoint
validate_password(new_password)
```

### 4. SOLID Principles (Simplified)

SOLID is a set of five design principles that make code easier to maintain. Here they are in simple terms:

| Principle | Simple Explanation | Example |
|-----------|-------------------|---------|
| **S** - Single Responsibility | Each class/function does one job | `UserService` handles user logic only, not email sending |
| **O** - Open/Closed | Add new behavior without modifying existing code | Use strategy pattern instead of endless if/elif chains |
| **L** - Liskov Substitution | Subclasses should work wherever the parent class works | If `Animal` has `speak()`, every subclass must implement it meaningfully |
| **I** - Interface Segregation | Don't force classes to implement methods they don't use | Split large interfaces into smaller, focused ones |
| **D** - Dependency Inversion | Depend on abstractions, not concrete implementations | Pass a `storage_service` parameter, not `AzureBlobStorage` directly |

For most student projects, focus on **S** (Single Responsibility) and **D** (Dependency Inversion). They solve 80% of design problems.

---

## Security Checks

Security issues in code reviews are critical. A single overlooked vulnerability can expose user data.

### SQL Injection

**Vulnerable:**

```python
# NEVER do this
query = f"SELECT * FROM users WHERE email = '{email}'"
result = db.execute(query)
```

**Safe:**

```python
# Use parameterized queries (SQLAlchemy does this automatically)
stmt = select(User).where(User.email == email)
result = await db.execute(stmt)
```

### Cross-Site Scripting (XSS)

**Vulnerable:**

```jsx
// NEVER do this -- renders raw HTML from user input
<div dangerouslySetInnerHTML={{__html: userComment}} />
```

**Safe:**

```jsx
// React automatically escapes text content
<div>{userComment}</div>
```

### Secrets in Code

**Never commit these:**

```python
# BAD -- hardcoded secrets
API_KEY = "sk-abc123def456"
DB_PASSWORD = "supersecret"
FIREBASE_KEY = "AIzaSyB..."
```

**Correct approach:**

```python
# GOOD -- read from environment variables
import os

API_KEY = os.environ["API_KEY"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
```

### Security Checklist

| Check | What to Look For |
|-------|-----------------|
| No hardcoded secrets | API keys, passwords, tokens in code |
| Input validation | All user inputs validated and sanitized |
| Authentication | Protected endpoints require auth tokens |
| Authorization | Users can only access their own data |
| SQL injection | Raw string interpolation in queries |
| XSS | Rendering raw HTML from user input |
| CORS | Only allowed origins can make requests |
| Rate limiting | Endpoints protected from abuse |
| File uploads | File type and size validation |
| Error messages | No sensitive info leaked in error responses |

---

## Test Coverage

### What to Check in Tests

| Check | Question to Ask |
|-------|----------------|
| Happy path tested | Does the test cover the normal, expected behavior? |
| Edge cases tested | What happens with empty input, zero, max values? |
| Error cases tested | Does the test verify proper error handling? |
| No test duplication | Are multiple tests checking the exact same thing? |
| Test independence | Does each test work without depending on other tests? |
| Meaningful assertions | Does the test check the right thing, not just "no error"? |

### Coverage Expectations

| Project Type | Minimum Coverage | Ideal Coverage |
|-------------|-----------------|----------------|
| MVP / Prototype | 40-50% | 60% |
| Production app | 70-80% | 85%+ |
| Critical systems (banking, health) | 90%+ | 95%+ |
| Utility libraries | 90%+ | 100% |

---

## Automated Linting

Automated tools catch style and quality issues before the review even starts.

| Tool | Language | What It Checks |
|------|----------|---------------|
| Black | Python | Code formatting (auto-fix) |
| Ruff | Python | Linting, import sorting, style |
| mypy | Python | Type checking |
| ESLint | JavaScript/TypeScript | Linting and style |
| Prettier | JavaScript/TypeScript | Code formatting (auto-fix) |

### Setting Up Pre-commit Hooks

Pre-commit hooks run checks automatically before every commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-added-large-files
      - id: detect-private-key
      - id: trailing-whitespace
```

---

## Key Takeaways

1. Code reviews catch bugs, share knowledge, and maintain code quality.
2. Keep PRs small (under 400 lines) and write clear descriptions.
3. Check for readability, naming, DRY violations, and SOLID principles.
4. Always check for security issues: SQL injection, XSS, hardcoded secrets.
5. Tests should cover happy paths, edge cases, and error cases.
6. Automated tools (Black, Ruff, ESLint, Prettier) catch style issues before the review.
7. Be kind in reviews: "Consider this approach" is better than "This is wrong."

---

*TechPath Institute -- Spec-Kit Development Methodology*

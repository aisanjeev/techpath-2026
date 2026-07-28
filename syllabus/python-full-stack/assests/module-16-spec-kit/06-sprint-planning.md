# Sprint Planning and Agile Workflow

**Module 16 -- Spec-Kit Development Methodology | Topic 6**

---

## What is Agile?

Agile is a way of building software in small, incremental steps rather than trying to build everything at once. Instead of spending six months planning and six months building (the "waterfall" approach), Agile teams deliver working software every one to two weeks.

Think of it like cooking a meal for a family. The waterfall approach is like preparing every dish in the kitchen, bringing everything out at once, and hoping everyone likes it. The Agile approach is like serving one dish at a time -- you bring out the appetizer, get feedback ("too much salt"), adjust, then bring the main course. You adapt based on real feedback.

---

## Scrum vs. Kanban

There are two popular Agile frameworks. Both help teams organize work, but they work differently.

### Scrum

| Aspect | Details |
|--------|---------|
| Work unit | Fixed-length sprints (usually 2 weeks) |
| Planning | Sprint planning meeting at the start |
| Daily check-in | Daily stand-up (15 minutes) |
| Review | Sprint review at the end to demo work |
| Retrospective | Team reflects on what went well and what to improve |
| Roles | Product Owner, Scrum Master, Development Team |
| Best for | Teams building a product with regular releases |

### Kanban

| Aspect | Details |
|--------|---------|
| Work unit | Continuous flow (no fixed sprints) |
| Planning | Pull new work when capacity is available |
| Daily check-in | Optional, often async |
| Review | No formal review ceremony |
| Retrospective | Periodic, not tied to sprints |
| Roles | No prescribed roles |
| Best for | Support teams, maintenance, ops work |

### Which One to Choose?

| Situation | Recommended | Why |
|-----------|-------------|-----|
| Building a new product | Scrum | Sprints give structure and regular delivery |
| Maintaining an existing product | Kanban | Bug fixes and support requests flow continuously |
| Small team (2-3 people) | Kanban | Less overhead, simpler process |
| Larger team (5-10 people) | Scrum | Clear roles and ceremonies prevent chaos |
| Learning Agile for the first time | Scrum | More structured, easier to follow |

For most student and startup projects, **Scrum with 2-week sprints** is the recommended approach.

---

## Key Agile Ceremonies

### 1. Sprint Planning (Start of Sprint)

The team decides what to build in the upcoming sprint.

**How it works:**
- Product Owner presents the prioritized backlog (list of features)
- Team discusses each item and asks clarifying questions
- Team estimates effort using story points
- Team commits to a set of items for the sprint

**Duration:** 1-2 hours for a 2-week sprint

### 2. Daily Stand-up (Every Day)

A quick check-in where each team member answers three questions:

```
1. What did I do yesterday?
2. What will I do today?
3. Is anything blocking me?
```

**Rules:**
- Maximum 15 minutes
- Standing up (to keep it short)
- No problem-solving during the stand-up (take it offline)

### 3. Sprint Review (End of Sprint)

The team demonstrates what they built to stakeholders.

**Example agenda:**
- Demo the login feature (Priya)
- Demo the product listing page (Arjun)
- Show the API documentation (Vikram)
- Gather feedback from the product owner

### 4. Sprint Retrospective (After Review)

The team reflects on the process itself.

| Column | Example Items |
|--------|--------------|
| What went well | "We finished all planned stories" |
| What did not go well | "Code reviews took too long" |
| Action items | "Set a 24-hour SLA for code reviews" |

---

## GitHub Projects: Your Digital Board

GitHub Projects is a free tool for managing sprints. It provides a Kanban-style board directly in your GitHub repository.

### Setting Up a Project Board

**Columns for a typical sprint board:**

| Column | Purpose | Example Items |
|--------|---------|---------------|
| Backlog | All planned work not yet started | "Add search functionality" |
| To Do | Items planned for the current sprint | "Build login API endpoint" |
| In Progress | Items currently being worked on | "Implement JWT authentication" |
| In Review | Items with open pull requests | "PR #42: Add user registration" |
| Done | Completed and merged items | "Setup project structure" |

### Creating Issues

GitHub Issues are the individual work items. Each issue should have:

```markdown
## Title
Build user registration API endpoint

## Description
Create a POST /api/v1/auth/register endpoint that accepts name, 
email, and password. Hash the password, save to database, and 
return a JWT token.

## Acceptance Criteria
- [ ] Endpoint accepts name, email, password
- [ ] Password is hashed using bcrypt
- [ ] Duplicate email returns 409 Conflict
- [ ] Successful registration returns JWT token
- [ ] Input validation for email format and password length (min 8)

## Labels
backend, auth, sprint-1

## Story Points
3
```

### Using Labels Effectively

| Label | Color | Purpose |
|-------|-------|---------|
| `bug` | Red | Something is broken |
| `feature` | Green | New functionality |
| `enhancement` | Blue | Improvement to existing feature |
| `frontend` | Purple | Frontend work |
| `backend` | Orange | Backend work |
| `sprint-1` | Yellow | Sprint assignment |
| `priority-high` | Dark red | Must be done this sprint |
| `good-first-issue` | Light green | Easy task for new contributors |

---

## Milestones

Milestones group issues into larger goals with deadlines.

**Example milestones for a student management app:**

| Milestone | Deadline | Issues |
|-----------|----------|--------|
| MVP - Authentication | Week 2 | Login, Register, Password Reset |
| MVP - Student Management | Week 4 | CRUD for students, batch assignment |
| MVP - Attendance | Week 6 | Mark attendance, view reports |
| Beta Release | Week 8 | Bug fixes, testing, deployment |

---

## Estimating with Story Points

Story points measure the effort and complexity of a task, not the time it takes. Teams use the Fibonacci sequence (1, 2, 3, 5, 8, 13) for estimates.

### Story Point Reference

| Points | Complexity | Example |
|--------|-----------|---------|
| 1 | Trivial | Fix a typo in the UI |
| 2 | Simple | Add a new field to an existing form |
| 3 | Moderate | Build a CRUD API for a new entity |
| 5 | Complex | Implement file upload with validation |
| 8 | Very complex | Build real-time notifications with WebSocket |
| 13 | Huge | Integrate payment gateway (Razorpay) |

**Why not hours?**

A senior developer might finish a task in 2 hours that takes a junior developer 8 hours. But the task's complexity is the same. Story points measure complexity, not duration. Over time, the team learns its **velocity** (how many points it completes per sprint) and can plan accordingly.

---

## Example: Planning a 2-Week Sprint

Let us walk through planning Sprint 1 for **EduTrack**, a student management app being built by a team of three in Bangalore.

### Team

| Member | Role | Capacity |
|--------|------|----------|
| Rahul | Backend developer | Full-time |
| Ananya | Frontend developer | Full-time |
| Amit | Full-stack developer | Full-time |

### Velocity Estimate

Since this is Sprint 1, the team estimates they can handle **20-25 story points** (a conservative starting velocity).

### Sprint 1 Backlog

| Issue | Title | Assignee | Points | Priority |
|-------|-------|----------|--------|----------|
| #1 | Setup project structure (frontend + backend) | Amit | 3 | High |
| #2 | Setup database and create User model | Rahul | 2 | High |
| #3 | Build registration API endpoint | Rahul | 3 | High |
| #4 | Build login API endpoint | Rahul | 3 | High |
| #5 | Create login page UI | Ananya | 3 | High |
| #6 | Create registration page UI | Ananya | 3 | High |
| #7 | Connect login page to API | Ananya | 2 | Medium |
| #8 | Setup CI/CD pipeline (GitHub Actions) | Amit | 3 | Medium |
| #9 | Write tests for auth endpoints | Rahul | 2 | Medium |
| | **Total** | | **24** | |

### Sprint Goal

"By the end of Sprint 1, users can register and log in to EduTrack through a working frontend connected to the backend API."

### What Gets Deferred to Sprint 2

- Password reset flow
- User profile page
- Student CRUD operations
- Admin dashboard

---

## Sprint Planning Meeting Agenda

Here is a template for running a sprint planning meeting:

```
Sprint Planning - Sprint [N]
Date: [Date]
Duration: 1 hour
Attendees: [Team members]

1. Review Sprint [N-1] outcomes (5 min)
   - What was completed?
   - What was not completed? Why?

2. Review and refine backlog (15 min)
   - Product owner presents top-priority items
   - Team asks clarifying questions
   - Update acceptance criteria if needed

3. Estimate stories (15 min)
   - Point poker or team discussion
   - Break down any story larger than 8 points

4. Commit to sprint scope (10 min)
   - Select stories up to team velocity
   - Define the sprint goal in one sentence

5. Assign tasks (10 min)
   - Each member picks or is assigned stories
   - Identify dependencies between stories

6. Wrap up (5 min)
   - Confirm next daily stand-up time
   - Any questions or concerns?
```

---

## Key Takeaways

1. Agile delivers software in small, iterative cycles with continuous feedback.
2. Scrum uses fixed sprints (usually 2 weeks) with defined ceremonies and roles.
3. Kanban uses continuous flow without fixed sprints -- best for maintenance and support.
4. GitHub Projects provides a free Kanban board integrated with your repository.
5. Story points measure complexity, not time -- use Fibonacci numbers (1, 2, 3, 5, 8, 13).
6. A sprint goal should be one sentence describing what the team will deliver.
7. Always define what is OUT of scope for each sprint to prevent overcommitment.

---

*TechPath Institute -- Spec-Kit Development Methodology*

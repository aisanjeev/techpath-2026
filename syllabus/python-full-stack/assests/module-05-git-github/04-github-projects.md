# GitHub Projects — Kanban Boards, Issues & Milestones

**Module 05 — Git, GitHub & Professional Workflow | Topic 4**

---

## What is Project Management in Software?

Building software is not just writing code. You need to plan features, track bugs, assign tasks, and meet deadlines. GitHub Projects gives you tools to manage all of this directly where your code lives.

**Real-world analogy:** Think of building a house. You need a plan (which rooms, what size), task lists (foundation first, then walls, then roof), assignments (plumber does pipes, electrician does wiring), and deadlines (move in by December). GitHub Projects does the same for software.

---

## GitHub Issues — Your Task List

An **Issue** is a single task, bug report, or feature request.

### Creating an Issue

On GitHub, go to your repository > **Issues** tab > **New Issue**.

**Bug Report Example:**

```markdown
## Bug: Student list shows wrong city after update

**Description**
When a student updates their city in the profile page, the student
list still shows the old city until the page is manually refreshed.

**Steps to Reproduce**
1. Go to /admin/students
2. Click "Edit" on Rahul Sharma
3. Change city from "Bhopal" to "Indore"
4. Click "Save"
5. Go back to the student list

**Expected Behavior**
Student list shows "Indore" for Rahul

**Actual Behavior**
Student list still shows "Bhopal"

**Screenshots**
(attach if applicable)

**Environment**
- Browser: Chrome 120
- OS: Windows 11
- API version: v1
```

**Feature Request Example:**

```markdown
## Feature: Export student data as CSV

**Description**
As an admin, I want to export the student list as a CSV file
so I can share it with the accounts team for fee tracking.

**Acceptance Criteria**
- [ ] "Export CSV" button on the student list page
- [ ] CSV includes: name, email, city, fee_paid, enrollment_date
- [ ] File is named `students_2026-07-25.csv` (with current date)
- [ ] Works for filtered lists too

**Priority:** Medium
**Estimated Effort:** 4 hours
```

### Issue Best Practices

| Do | Do Not |
|----|--------|
| One issue per task/bug | Mix multiple problems in one issue |
| Use clear titles | Write vague titles like "fix stuff" |
| Add steps to reproduce for bugs | Assume everyone knows the context |
| Use labels to categorize | Leave issues unlabeled |
| Close issues when done | Let stale issues pile up |

---

## Labels — Categorizing Issues

Labels help you filter and prioritize issues.

### Recommended Label System

| Label | Color | Use |
|-------|-------|-----|
| `bug` | Red | Something is broken |
| `feature` | Green | New functionality |
| `enhancement` | Blue | Improvement to existing feature |
| `documentation` | Purple | Docs, README, comments |
| `good first issue` | Teal | Easy tasks for newcomers |
| `priority: critical` | Dark Red | Must fix immediately |
| `priority: high` | Orange | Fix this sprint |
| `priority: medium` | Yellow | Fix soon |
| `priority: low` | Gray | Nice to have |
| `frontend` | Cyan | UI/React changes |
| `backend` | Brown | API/Python changes |
| `won't fix` | Gray | Not going to fix |

---

## Milestones — Grouping Issues by Deadline

A **Milestone** is a collection of issues with a target date. It represents a version release or a sprint.

### Creating a Milestone

Repository > Issues > Milestones > New Milestone

```
Title:       Sprint 3 - User Management
Due Date:    2026-08-15
Description: Complete all user-related features including registration,
             profile editing, and role-based access control.
```

### Assigning Issues to Milestones

When creating or editing an issue, select the milestone from the sidebar.

**Milestone Progress:**

GitHub shows a progress bar:
```
Sprint 3 - User Management
[===========           ] 55% complete (6 open, 5 closed)
Due by August 15, 2026
```

---

## GitHub Projects — Kanban Boards

A **Kanban board** is a visual way to manage tasks using columns.

### Default Columns

| Column | What Goes Here |
|--------|---------------|
| **Backlog** | Ideas and future tasks |
| **To Do** | Tasks planned for this sprint |
| **In Progress** | Tasks someone is actively working on |
| **In Review** | Tasks with open PRs waiting for review |
| **Done** | Completed tasks |

### Setting Up a Project Board

1. Go to your GitHub profile or organization
2. Click **Projects** > **New project**
3. Choose **Board** view
4. Add columns: Backlog, To Do, In Progress, In Review, Done
5. Add issues by clicking **+** in any column

### Automating the Board

GitHub can automatically move cards:

| When | Move To |
|------|---------|
| Issue is created | Backlog |
| Issue is assigned | To Do |
| PR is opened linking the issue | In Review |
| PR is merged / issue closed | Done |

### Views in GitHub Projects

| View | What It Shows |
|------|--------------|
| **Board** | Kanban columns — best for daily standups |
| **Table** | Spreadsheet-like view — best for planning |
| **Roadmap** | Timeline view — best for release planning |

---

## Sprint Workflow with GitHub

A **sprint** is a fixed time period (usually 1-2 weeks) where your team completes a set of tasks.

### Sprint Planning

```
Sprint 4 Planning - TechPath Team

Duration: July 25 - August 8, 2026

Goals:
1. Complete student registration feature
2. Fix critical bug in payment flow
3. Add CSV export for admin

Tasks (Issues):
- #23 [feature] Student registration form        → Assigned: Priya
- #24 [feature] Registration API endpoint         → Assigned: Amit
- #25 [feature] Email verification flow           → Assigned: Priya
- #31 [bug]     Payment fails on ₹0 courses       → Assigned: Rahul
- #28 [feature] CSV export for student list        → Assigned: Sneha
- #30 [docs]    Update API documentation           → Assigned: Ananya
```

### Daily Standup (Using the Board)

Every morning, the team looks at the Kanban board and answers:
1. What did I complete yesterday?
2. What am I working on today?
3. Am I blocked by anything?

### Sprint Retrospective

At the end of the sprint, review what went well and what to improve:

```markdown
## Sprint 4 Retrospective

### What went well
- Registration feature completed on time
- Good code review turnaround (< 24 hours)

### What to improve
- #31 took longer than estimated — need better debugging tools
- CSV export lacked tests — add testing to Definition of Done

### Action items
- [ ] Add "tests written" to the PR template checklist
- [ ] Set up error monitoring for payment flow
```

---

## Issue Templates

Create templates so team members file consistent issues.

Create a file `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug Report
about: Report a bug to help us fix it
labels: bug
---

## Description
(A clear description of the bug)

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
(What should happen)

## Actual Behavior
(What actually happens)

## Screenshots
(If applicable)

## Environment
- Browser:
- OS:
```

---

## Task Estimation

When planning sprints, estimate how long each task takes.

### T-Shirt Sizing

| Size | Time | Example |
|------|------|---------|
| **XS** | < 1 hour | Fix a typo, update a label |
| **S** | 1-4 hours | Add a simple form, fix a minor bug |
| **M** | 4-8 hours | Build a new page, write API endpoint |
| **L** | 1-3 days | Build a complete feature with tests |
| **XL** | 3-5 days | Major refactor, complex integration |

If a task is XL or larger, break it down into smaller issues.

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Issues | Individual tasks, bugs, or feature requests |
| Labels | Color-coded categories for filtering |
| Milestones | Group issues with a target date |
| Projects Board | Visual Kanban for task management |
| Sprint | Fixed time period for completing a set of tasks |
| Estimation | T-shirt sizing: XS, S, M, L, XL |
| Templates | Consistent format for bug reports and features |

---

*TechPath Institute — Python Full Stack Development*

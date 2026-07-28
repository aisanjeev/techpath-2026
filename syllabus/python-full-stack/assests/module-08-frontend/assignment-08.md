# Module 08 — Assignment: Build a Frontend for Your API

**Deadline:** End of module week
**Submission:** HTML/CSS/JS project folder + screenshots

---

## Build: TechPath Student Dashboard (Frontend)

Create a responsive frontend dashboard that consumes your Django DRF or FastAPI backend from Module 07.

### Task 1: Responsive Layout with CSS Grid & Flexbox — 25 marks

Build a dashboard page with this layout:

```
+--------------------------------------------------+
|  Navbar (TechPath Institute, Bhopal)              |
+----------+---------------------------------------+
|          |  Stats Cards (4 cards in a row)        |
| Sidebar  |  [Total] [Avg Marks] [Passed] [Failed] |
|  (nav    |---------------------------------------|
|   links) |  Charts (2 charts side by side)       |
|          |  [Bar Chart]    [Pie Chart]            |
|          |---------------------------------------|
|          |  Student Table (with search)           |
+----------+---------------------------------------+
|  Footer                                          |
+--------------------------------------------------+
```

**Requirements:**
- Use CSS Grid for the overall layout (sidebar + main content)
- Use Flexbox for the navbar and stat cards row
- Use CSS variables for colors (at least 5 variables)
- Mobile responsive: sidebar hides, cards stack vertically on small screens
- Use at least 3 `@media` breakpoints

### Task 2: Fetch API Integration — 30 marks

Connect your frontend to your backend API:

| Feature | API Endpoint | Method |
|---------|-------------|--------|
| Load all students | `/api/students/` | GET |
| Search students | `/api/students/?search=query` | GET |
| Load stats | `/api/students/stats/` | GET |
| Create student | `/api/students/` | POST |
| Delete student | `/api/students/{id}/` | DELETE |

**Requirements:**
- All API calls use `async/await` with `try/catch` error handling
- Show loading state while data is being fetched
- Display error messages if the API is down
- Include JWT token in POST/DELETE requests (store in localStorage)
- Form validation before submission (name min 2 chars, valid email, marks 0-100)

### Task 3: Data Visualization with Chart.js — 20 marks

Add two charts that use data from your API:

1. **Bar Chart** — Top 8 students by marks (color-coded: green for 80+, blue for 40-79, red for below 40)
2. **Doughnut/Pie Chart** — Students by city distribution

**Requirements:**
- Charts load data from your API (not hardcoded)
- Charts are responsive (resize with the page)
- Include chart titles and legends
- Use meaningful colors

### Task 4: Bootstrap Components & HTMX — 25 marks

Use at least 5 Bootstrap components:
- Navbar with responsive toggle
- Cards for stats
- Table with striped rows and hover effect
- Modal for delete confirmation
- Alert for success/error messages
- Badge for Pass/Fail status

Add HTMX for at least one dynamic feature:
- Live search (search as you type, no page reload)
- OR inline edit (click a cell to edit it)
- OR delete with swap (row disappears without page reload)

---

## Project Structure

```
student-dashboard/
├── index.html          (Main dashboard page)
├── css/
│   └── style.css       (Custom styles with CSS variables)
├── js/
│   └── app.js          (Fetch API calls, charts, DOM logic)
└── screenshots/
    ├── desktop.png
    ├── mobile.png
    └── api-calls.png
```

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Layout | Grid + Flexbox, fully responsive | Mostly responsive | Not responsive |
| API Integration | All CRUD + auth + error handling | GET + POST work | Only hardcoded data |
| Charts | Both charts from API data, responsive | One chart works | No charts |
| Bootstrap | 5+ components used correctly | 3 components | Minimal Bootstrap |
| HTMX | Working dynamic feature | Attempted but buggy | Not attempted |
| Code Quality | Clean, commented, well-organized | Mostly clean | Messy, no comments |

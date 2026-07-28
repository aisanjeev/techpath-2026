# Module 09 — Assignment: Interactive Web Application

**Deadline:** End of Week 12
**Submission:** Zipped project folder OR GitHub repo link

---

## Build: Student Expense Tracker

Create a single-page web app where students can track their monthly expenses using HTML, CSS (Bootstrap), and vanilla JavaScript.

### Task 1: UI Layout with Bootstrap — 25 marks
- Responsive navbar with app name and a dark/light toggle button
- Two-column layout on desktop (form on left, list on right), stacked on mobile
- Use Bootstrap grid (`row`, `col-md-6`)
- Card component for the form area
- Styled table for expense list using `table table-striped`
- Footer showing total expenses

### Task 2: Add Expense Functionality — 30 marks
- Form with: Description (text), Amount (number), Category (select: Food, Transport, Study, Entertainment, Other), Date (date input)
- All fields are required — show Bootstrap validation on submit
- On submit: add expense to the table dynamically (no page reload)
- Each row shows: Description, ₹Amount, Category (as a colored badge), Date, Delete button
- Running total updates automatically at the bottom

### Task 3: Delete & Filter — 25 marks
- Each expense row has a delete button (Bootstrap trash icon or text)
- Clicking delete removes that expense and updates the total
- Category filter dropdown above the table — selecting "Food" shows only food expenses
- "All" option to show everything again
- Use `Array.filter()` for filtering (don't hide/show DOM elements)

### Task 4: LocalStorage Persistence — 20 marks
- Save expenses to `localStorage` as JSON
- On page load, read from `localStorage` and display saved expenses
- Deleting an expense also removes it from `localStorage`
- Show a "No expenses yet" message when the list is empty

### Expected Folder Structure
```
expense-tracker/
├── index.html
├── css/
│   └── style.css     (custom styles beyond Bootstrap)
├── js/
│   └── app.js        (all JavaScript logic)
```

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Bootstrap usage | Grid, cards, table, badges, validation | Basic grid + table | No Bootstrap / broken layout |
| JS functionality | Add, delete, filter, total — all work | Add + delete work | Only partial functionality |
| DOM manipulation | Clean selectors, dynamic rendering | Works but messy | Direct HTML string injection |
| LocalStorage | Save, load, delete all work | Save + load work | No persistence |
| Code quality | Modular functions, clear naming | Readable | Spaghetti code, no functions |

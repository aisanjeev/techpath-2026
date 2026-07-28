# Excel Formulas — The Complete Job-Ready Guide

**Module 03 — MS Office | Excel Deep Dive**

---

## Why This Matters

> Every office job in India — from Rs 15,000/month data entry to Rs 80,000/month analyst — uses Excel daily. The difference between a Rs 15K salary and an Rs 40K salary is often just how well you know formulas.

---

## Level 1: Formulas Every Employee Must Know (Day 1 on the Job)

### SUM, AVERAGE, COUNT, MIN, MAX

**Scenario:** Your manager gives you a sales sheet with 500 rows and says "Give me the total sales, average order value, and how many orders we got this month."

```
| A          | B          | C       |
|------------|------------|---------|
| Order ID   | Customer   | Amount  |
| ORD-001    | Rahul      | 1500    |
| ORD-002    | Priya      | 2300    |
| ORD-003    | Amit       | 800     |
| ...        | ...        | ...     |
| ORD-500    | Sneha      | 3200    |
```

```
=SUM(C2:C501)        → Total sales: ₹12,45,000
=AVERAGE(C2:C501)    → Average order: ₹2,490
=COUNT(C2:C501)      → Total orders: 500
=MAX(C2:C501)        → Biggest order: ₹15,000
=MIN(C2:C501)        → Smallest order: ₹120
=COUNTA(B2:B501)     → Counts non-empty cells (text too)
```

**Common mistake:** `COUNT` only counts numbers. If your column has text, use `COUNTA`.

---

### IF — The Decision Maker

**Scenario:** HR asks you to mark employees as "Eligible" or "Not Eligible" for bonus based on their rating.

```
Rule: Rating >= 4 → Eligible, otherwise Not Eligible

=IF(C2>=4, "Eligible", "Not Eligible")
```

**Real uses in offices:**
```
=IF(B2>100000, "High Value", "Regular")           → Customer classification
=IF(D2="", "Missing", "OK")                       → Data quality check
=IF(E2>=40, "Pass", "Fail")                        → Exam results
=IF(F2-TODAY()<=7, "Due Soon!", "On Track")        → Deadline tracking
```

### Nested IF (Multiple Conditions)

**Scenario:** Grade students based on marks.

```
=IF(B2>=90, "A+", IF(B2>=80, "A", IF(B2>=70, "B", IF(B2>=60, "C", IF(B2>=40, "D", "Fail")))))
```

| Marks | Grade |
|-------|-------|
| 95 | A+ |
| 82 | A |
| 71 | B |
| 55 | C |
| 42 | D |
| 30 | Fail |

**Pro tip:** In modern Excel, use `IFS` instead — it's cleaner:
```
=IFS(B2>=90,"A+", B2>=80,"A", B2>=70,"B", B2>=60,"C", B2>=40,"D", TRUE,"Fail")
```

---

### CONCATENATE / TEXTJOIN — Combine Text

**Scenario:** You have First Name in column A and Last Name in column B. HR needs Full Name.

```
=A2 & " " & B2                          → "Rahul Sharma"
=CONCATENATE(A2, " ", B2)               → "Rahul Sharma"
=TEXTJOIN(" ", TRUE, A2, B2, C2)        → Joins with space, skips blanks
```

**Real use:** Creating email IDs from names:
```
=LOWER(LEFT(A2,1) & B2 & "@company.com")    → "rsharma@company.com"
```

---

## Level 2: Formulas That Get You Promoted (Month 1-3)

### VLOOKUP — The Most Asked Formula in Interviews

**What it does:** Looks up a value in one table and brings matching data from another column.

**Scenario:** You have an Employee ID and need to find their Department from a master list.

```
Employee Sheet (where you're working):
| A         | B        | C           |
|-----------|----------|-------------|
| Emp ID    | Name     | Department  |
| E001      | Rahul    | ???         |

Master List (reference data, maybe another sheet):
| F         | G        | H           |
|-----------|----------|-------------|
| Emp ID    | Name     | Department  |
| E001      | Rahul    | Sales       |
| E002      | Priya    | HR          |
| E003      | Amit     | IT          |
```

```
=VLOOKUP(A2, MasterList!A:C, 3, FALSE)
```

**Breaking it down:**
| Part | Meaning |
|------|---------|
| `A2` | What to search for (Emp ID "E001") |
| `MasterList!A:C` | Where to search (columns A to C of master sheet) |
| `3` | Return value from 3rd column (Department) |
| `FALSE` | Exact match (ALWAYS use FALSE) |

**Common VLOOKUP mistakes (interview question!):**
1. Search column must be the FIRST column in your range
2. Always use `FALSE` for exact match
3. `#N/A` error = value not found (check for extra spaces)
4. VLOOKUP only looks RIGHT, never left

### INDEX-MATCH — The Pro Alternative

**Why learn this:** VLOOKUP can't look left. INDEX-MATCH can look anywhere. Senior analysts use this.

```
=INDEX(C2:C100, MATCH(F2, A2:A100, 0))
```

**Breaking it down:**
| Part | Meaning |
|------|---------|
| `INDEX(C2:C100, ...)` | Return value from column C |
| `MATCH(F2, A2:A100, 0)` | Find which row F2 appears in column A |
| `0` | Exact match |

**When to use which:**
| Situation | Use |
|-----------|-----|
| Simple lookup, search column is first | VLOOKUP |
| Need to look left | INDEX-MATCH |
| Very large datasets (50K+ rows) | INDEX-MATCH (faster) |
| Interview answer | Say "I know both" |

---

### COUNTIF / SUMIF / AVERAGEIF — Conditional Calculations

**Scenario:** Sales data with 1000 rows. Manager asks: "How many orders came from Mumbai? What's the total sales from Delhi? What's the average order value for Premium customers?"

```
=COUNTIF(B2:B1000, "Mumbai")                        → Count orders from Mumbai
=SUMIF(B2:B1000, "Delhi", D2:D1000)                 → Total sales from Delhi
=AVERAGEIF(C2:C1000, "Premium", D2:D1000)           → Average order for Premium
```

**Multiple conditions (COUNTIFS, SUMIFS):**
```
=COUNTIFS(B2:B1000, "Mumbai", C2:C1000, "Premium")
→ Count Premium customers from Mumbai

=SUMIFS(D2:D1000, B2:B1000, "Delhi", E2:E1000, ">=2024-01-01")
→ Total sales from Delhi in 2024
```

**Wildcards in COUNTIF:**
```
=COUNTIF(A2:A100, "Rahul*")       → Starts with "Rahul"
=COUNTIF(A2:A100, "*sharma*")     → Contains "sharma" anywhere
=COUNTIF(A2:A100, "???")          → Exactly 3 characters
```

---

### TEXT Functions — Data Cleaning (You'll Do This Daily)

**Scenario:** Someone gives you messy data. Names are all caps, phone numbers have dashes, dates are text.

```
=PROPER("RAHUL SHARMA")        → "Rahul Sharma"
=UPPER("rahul")                → "RAHUL"
=LOWER("RAHUL")                → "rahul"
=TRIM("  Rahul  Sharma  ")    → "Rahul Sharma" (removes extra spaces)
=CLEAN(A2)                     → Removes invisible characters
=LEN(A2)                       → Character count (useful to check data)
```

**Extract parts of text:**
```
=LEFT("TechPath", 4)           → "Tech"
=RIGHT("TechPath", 4)          → "Path"
=MID("TechPath", 5, 4)         → "Path" (start at 5th char, take 4)
```

**Real workplace example — Extract domain from email:**
```
=MID(A2, FIND("@",A2)+1, LEN(A2))
"rahul@gmail.com" → "gmail.com"
```

**Find and Replace within formula:**
```
=SUBSTITUTE("099-123-4567", "-", "")   → "0991234567"
=SUBSTITUTE(A2, " ", "")              → Remove all spaces
```

---

## Level 3: Formulas That Make You the "Excel Person" (Month 3-6)

### Date Formulas

```
=TODAY()                         → Today's date
=NOW()                          → Current date + time
=DATEDIF(A2, TODAY(), "Y")      → Years between (age calculator)
=DATEDIF(A2, B2, "M")          → Months between two dates
=EOMONTH(TODAY(), 0)            → Last day of current month
=NETWORKDAYS(A2, B2)            → Working days between dates
=TEXT(A2, "DD-MMM-YYYY")        → Format: "15-Jan-2026"
=YEAR(A2)                       → Extract year
=MONTH(A2)                      → Extract month
```

**Real use — Employee tenure:**
```
=DATEDIF(D2, TODAY(), "Y") & " years, " & DATEDIF(D2, TODAY(), "YM") & " months"
→ "3 years, 7 months"
```

**Real use — Due date tracking:**
```
=IF(B2-TODAY()<0, "OVERDUE", IF(B2-TODAY()<=7, "Due This Week", "On Track"))
```

---

### Data Validation (Dropdowns)

**What:** Restrict what users can enter in a cell — prevents errors.

**How to create:**
1. Select the cells
2. Data → Data Validation
3. Allow: List
4. Source: type options separated by commas, or select a range

**Common dropdowns in office work:**
- Status: "Pending, In Progress, Completed, On Hold"
- Priority: "High, Medium, Low"
- Department: "Sales, HR, IT, Finance, Marketing"
- Yes/No: "Yes, No"

---

### Conditional Formatting — Visual Alerts

**What:** Automatically color cells based on rules.

**Common workplace uses:**

| Rule | Visual | Use Case |
|------|--------|----------|
| Values > 100000 | Green fill | High-value orders |
| Values < 0 | Red text | Negative balance |
| Duplicates | Yellow fill | Find duplicate entries |
| Dates < Today | Red fill | Overdue items |
| Top 10 values | Green gradient | Best performers |
| Data bars | In-cell bars | Quick visual comparison |
| Icon sets | Arrows/traffic lights | KPI dashboards |

**How:** Select range → Home → Conditional Formatting → New Rule

---

### XLOOKUP (Modern Excel / 365)

Replaces VLOOKUP — simpler, more powerful:

```
=XLOOKUP(F2, A2:A100, C2:C100, "Not Found")
```

| Part | Meaning |
|------|---------|
| `F2` | What to search |
| `A2:A100` | Where to search |
| `C2:C100` | What to return |
| `"Not Found"` | Default if no match |

**Advantages over VLOOKUP:**
- Can look left or right
- Simpler syntax
- Built-in error handling
- Can return multiple columns

---

## Practice Exercises (Do All 10)

### Exercise 1: Sales Report
Create a sheet with 20 rows of sales data (Date, Salesperson, City, Product, Quantity, Unit Price). Add formulas for:
- Total Revenue (Quantity × Unit Price) for each row
- Total sales, average, max, min at the bottom
- COUNTIF for each city
- SUMIF for each salesperson's total

### Exercise 2: Employee Attendance Tracker
Build a monthly attendance sheet. Columns: Employee Name, then dates 1-31. Mark P (Present), A (Absent), L (Leave), H (Holiday).
- COUNTIF to count total P, A, L for each employee
- Conditional formatting: A = Red, L = Yellow, P = Green
- Calculate attendance percentage

### Exercise 3: Student Marksheet
Create for 30 students with 5 subjects. Add:
- Total marks, percentage, grade (using nested IF)
- Pass/Fail (minimum 40 in each subject AND 50% overall)
- Rank using RANK function
- Class average for each subject
- Conditional formatting for fail marks (< 40)

### Exercise 4: Invoice Generator
Build a professional invoice template with:
- Customer details section
- Item table: Description, Qty, Rate, Amount (=Qty×Rate)
- Subtotal (SUM), GST (18%), Grand Total
- VLOOKUP to auto-fill item rates from a product master list

### Exercise 5: Loan EMI Calculator
Build a calculator using:
```
=PMT(rate/12, tenure*12, -principal)
```
Input cells: Loan Amount, Interest Rate, Tenure (years)
Output: Monthly EMI, Total Payment, Total Interest

---

## Keyboard Shortcuts That Make You Fast

| Shortcut | Action |
|----------|--------|
| Ctrl+D | Fill down (copy formula) |
| Ctrl+R | Fill right |
| Ctrl+Shift+L | Toggle filters |
| Ctrl+T | Convert to Table |
| Ctrl+; | Insert today's date |
| Ctrl+Shift+; | Insert current time |
| Alt+= | Auto SUM |
| F2 | Edit cell |
| F4 | Toggle absolute reference ($) |
| Ctrl+` | Show all formulas |
| Ctrl+Shift+~ | General format |
| Ctrl+1 | Format cells dialog |
| Ctrl+Space | Select entire column |
| Shift+Space | Select entire row |
| Ctrl+Home | Go to cell A1 |
| Ctrl+End | Go to last used cell |

---

## Formula Errors and How to Fix Them

| Error | Meaning | Fix |
|-------|---------|-----|
| `#N/A` | Value not found | Check spelling, extra spaces (use TRIM) |
| `#REF!` | Reference broken | You deleted a referenced cell — undo |
| `#VALUE!` | Wrong data type | Number formatted as text — check format |
| `#DIV/0!` | Dividing by zero | Use `=IF(B2=0, 0, A2/B2)` |
| `#NAME?` | Formula name wrong | Check spelling of function name |
| `#NUM!` | Invalid number | Check function arguments |
| `######` | Column too narrow | Widen the column |

---

## What Interviewers Ask About Excel

1. "What's the difference between VLOOKUP and INDEX-MATCH?"
2. "How would you remove duplicates from 10,000 rows?"
3. "Create a pivot table from this data" (they'll give you a dataset)
4. "Write a SUMIFS formula with 3 conditions"
5. "How do you handle #N/A errors in VLOOKUP?"
6. "What's the difference between relative and absolute cell references?"
7. "How would you create a dashboard with charts?"

**Tip:** They don't just ask theory — they sit you down and watch you work. Speed matters. Practice with keyboard shortcuts.

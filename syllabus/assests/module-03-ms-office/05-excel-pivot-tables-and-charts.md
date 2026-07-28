# Excel Pivot Tables & Charts — From Data to Decisions

**Module 03 — MS Office | Excel Advanced**

---

## Why Pivot Tables?

> Your manager won't ask "What's in row 847?" They'll ask "Which city gave us the most revenue last quarter?" Pivot tables answer business questions from raw data in seconds.

**Without Pivot Table:** Manually filter, sort, use SUMIF for every combination — takes 30 minutes.
**With Pivot Table:** Drag, drop, done — takes 30 seconds.

---

## Building Your First Pivot Table

### Sample Data (Imagine 5000 rows like this)

```
| Date       | Salesperson | City      | Product    | Category    | Quantity | Revenue  |
|------------|-------------|-----------|------------|-------------|----------|----------|
| 01-Jan-26  | Rahul       | Mumbai    | Laptop     | Electronics | 2        | 120000   |
| 01-Jan-26  | Priya       | Delhi     | Mouse      | Accessories | 10       | 5000     |
| 02-Jan-26  | Amit        | Bangalore | Keyboard   | Accessories | 5        | 7500     |
| 02-Jan-26  | Rahul       | Mumbai    | Monitor    | Electronics | 1        | 25000    |
| 03-Jan-26  | Sneha       | Pune      | Headphones | Accessories | 8        | 12000    |
```

### Steps

1. Click anywhere inside your data
2. Insert → Pivot Table
3. Choose "New Worksheet" → OK
4. You'll see 4 areas: **Filters, Columns, Rows, Values**

### Answering Business Questions

**Q1: "What's the total revenue by city?"**
- Drag `City` → Rows
- Drag `Revenue` → Values

Result:
```
| City      | Sum of Revenue |
|-----------|---------------|
| Bangalore | 45,00,000     |
| Delhi     | 38,00,000     |
| Mumbai    | 62,00,000     |
| Pune      | 28,00,000     |
```

**Q2: "Revenue by city AND category?"**
- Drag `City` → Rows
- Drag `Category` → Columns
- Drag `Revenue` → Values

Result:
```
|           | Accessories | Electronics | Grand Total |
|-----------|-------------|-------------|-------------|
| Bangalore | 12,00,000   | 33,00,000   | 45,00,000   |
| Delhi     | 8,00,000    | 30,00,000   | 38,00,000   |
| Mumbai    | 15,00,000   | 47,00,000   | 62,00,000   |
| Pune      | 10,00,000   | 18,00,000   | 28,00,000   |
```

**Q3: "Monthly revenue trend?"**
- Drag `Date` → Rows (Excel auto-groups into months)
- Drag `Revenue` → Values

**Q4: "Top salesperson by revenue?"**
- Drag `Salesperson` → Rows
- Drag `Revenue` → Values
- Click dropdown on "Salesperson" → Sort Largest to Smallest

**Q5: "Show me only Electronics from Mumbai?"**
- Drag `Category` → Filters
- Drag `City` → Filters
- Select "Electronics" and "Mumbai" from dropdowns

---

## Pivot Table Power Moves

### Change Calculation Type

Right-click on any value → "Value Field Settings":

| Option | Use |
|--------|-----|
| Sum | Total (default) |
| Count | How many entries |
| Average | Mean value |
| Max/Min | Highest/lowest |
| % of Grand Total | Each category as % of total |
| % of Column Total | Compare within a column |

### Grouping Dates

Right-click any date → Group:
- Days, Months, Quarters, Years
- "Show me quarterly revenue for 2025 vs 2026" — Group by Year + Quarter

### Calculated Field

Insert → Fields, Items & Sets → Calculated Field

```
Profit = Revenue - Cost
Margin% = Profit / Revenue
```

### Slicers — Visual Filters

Insert → Slicer → Choose fields (City, Category, etc.)
Clickable buttons appear — way better than dropdown filters.

### Refresh Data

When source data changes: Right-click Pivot Table → Refresh

---

## Charts — Making Data Visual

### Which Chart for Which Data?

| Data Type | Best Chart | Example |
|-----------|-----------|---------|
| Compare categories | Bar / Column | Revenue by city |
| Show trend over time | Line | Monthly sales |
| Show parts of whole | Pie / Donut | Market share % |
| Show relationship | Scatter | Price vs Sales |
| Compare two measures | Combo (bar + line) | Revenue + Profit margin |
| Show distribution | Histogram | Age distribution |
| Geographic data | Map chart | Sales by state |

### Creating a Chart

1. Select your data (including headers)
2. Insert → Choose chart type
3. Chart appears — now customize it

### Chart Design Rules (Professional Look)

| Do | Don't |
|----|-------|
| Add a clear title | Leave default "Chart Title" |
| Label axes | Let people guess |
| Use 2-3 colors max | Rainbow colors |
| Remove chart border | Keep the default box |
| Start Y-axis at 0 (bar charts) | Start at a misleading number |
| Use data labels on small charts | Clutter large charts |
| Keep it simple | Add 3D effects, shadows |
| Use consistent colors | Random colors each chart |

### Formatting Tips

- **Title:** Click → type your title (e.g., "Monthly Revenue — Q1 2026")
- **Colors:** Click any bar → Format → Fill → choose brand colors
- **Data Labels:** Click chart → + button → Data Labels
- **Legend:** Move to bottom or right, never overlapping
- **Gridlines:** Remove major gridlines for clean look (keep minor if needed)

---

## Building a Dashboard

A dashboard = multiple charts + KPI numbers on one sheet, showing business performance at a glance.

### Step-by-Step Dashboard

**Step 1: Prepare your data**
- Clean data in one sheet
- Create Pivot Tables in a separate sheet (hide this sheet later)

**Step 2: Create KPI section at top**
```
| Total Revenue    | Total Orders | Avg Order Value | Top City    |
| ₹1,73,00,000     | 5,000        | ₹3,460          | Mumbai      |
```

Use large font, bold, colored backgrounds for these numbers.

**Step 3: Add charts (3-4 max)**
- Chart 1: Monthly revenue trend (Line chart)
- Chart 2: Revenue by city (Bar chart)
- Chart 3: Category split (Donut chart)
- Chart 4: Top 5 salespersons (Horizontal bar)

**Step 4: Add Slicers**
- Connect all Pivot Tables to the same slicer
- Add City, Month, Category slicers

**Step 5: Format the dashboard**
- Remove gridlines (View → uncheck Gridlines)
- Set background color for the sheet
- Align all charts neatly
- Add company logo
- Freeze top row with KPIs

**Step 6: Protect the sheet**
- Review → Protect Sheet
- Users can click slicers but can't edit data

---

## Practice Exercises

### Exercise 1: Sales Dashboard
Download/create sales data with 500+ rows (Date, Product, City, Salesperson, Revenue, Cost). Build:
- Pivot table: Revenue by Month
- Pivot table: Revenue by City × Product Category
- 3 charts: Line (monthly trend), Bar (city comparison), Pie (category %)
- KPI row: Total Revenue, Profit, Orders, Avg Order Value
- Add 2 slicers (City, Month)

### Exercise 2: HR Dashboard
Employee data: Name, Department, Joining Date, Salary, Rating, City. Build:
- Headcount by department (bar chart)
- Average salary by department (bar chart)
- Joining trend by year (line chart)
- Rating distribution (pie chart)
- Slicer: Department, City

### Exercise 3: Expense Tracker
Monthly expenses: Date, Category (Food, Transport, Bills, Shopping, etc.), Amount, Payment Mode (Cash, UPI, Card). Build:
- Monthly spending trend
- Spending by category (donut)
- Category comparison across months (stacked bar)
- Average daily spending

---

## What Makes You Stand Out in Interviews

**Beginner says:** "I know Pivot Tables."
**You say:** "I built a sales dashboard with Pivot Tables, slicers, and combo charts that the team used for weekly reviews. It pulled from 5,000 rows of data and showed revenue trends, city performance, and category splits — all filterable by quarter and region."

That's the difference between getting a Rs 18K job and a Rs 35K job.

# Module 11 — Assignment: Data Analysis Project

**Deadline:** End of Week 18
**Submission:** Jupyter Notebook (.ipynb) OR Python file + output charts (PNG)

---

## Task 1: Sales Data Dashboard — 40 marks

Download or create a CSV file with 50+ rows of sales data:
```
date,product,category,quantity,price,city
2026-01-05,Laptop,Electronics,2,45000,Mumbai
```

**Analysis required:**
- Total revenue per category (bar chart)
- Top 5 products by revenue (horizontal bar chart)
- Monthly sales trend (line chart)
- City-wise sales distribution (pie chart)
- Revenue statistics: mean, median, max, min per category (printed table)

**Requirements:**
- Use Pandas for all data operations
- Use Matplotlib or Seaborn for all charts
- Add proper titles, labels, and colors to every chart
- Save charts as PNG files
- Print a summary table using `df.groupby().agg()`

---

## Task 2: Student Performance Analysis — 30 marks

Create a dataset with 30+ students:
```
name,roll,course,hindi,english,maths,science,computer,city
```

**Analysis required:**
- Calculate total, percentage, and grade for each student
- Subject-wise average marks (grouped bar chart)
- Pass/Fail ratio (pie chart)
- Top 10 students (sorted table)
- Box plot comparing marks distribution across subjects
- Correlation heatmap between subjects (Seaborn)

---

## Task 3: API Data Fetch and Analysis — 30 marks

Use any free public API to fetch data and analyze it.

**Suggested APIs (pick one):**
- Weather: OpenWeatherMap (temperature across Indian cities)
- Currency: ExchangeRate API (INR vs USD/EUR over time)
- GitHub: Fetch public repos of a user and analyze (stars, languages)

**Requirements:**
- Use `requests` library to fetch data
- Convert API response to Pandas DataFrame
- Create at least 2 charts from the data
- Handle API errors (try/except, check status_code)
- Print formatted summary

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Pandas usage | groupby, agg, apply, merge | Basic filtering | Only read_csv |
| Charts | Labeled, colored, professional | Charts exist but plain | Missing or broken |
| Code quality | Functions, clean notebook cells | Readable | One long script |
| Analysis depth | Insights + statistics | Basic counts | Just displayed raw data |
| API integration | Fetch + parse + chart | Fetch works | No API used |

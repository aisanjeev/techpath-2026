# Module 04 — Spreadsheet / MS Excel — Assignment

**CCC Exam Preparation | TechPath Institute**

---

## Assignment Overview

This assignment contains 4 practical tasks that cover the key concepts from Module 04. Complete all tasks in Microsoft Excel (or LibreOffice Calc / Google Sheets). Save each task as a separate file or as separate worksheets in one workbook.

---

## Task 1: Create a Student Marksheet

**Objective:** Practice data entry, basic formulas (SUM, AVERAGE, MAX, MIN), cell formatting, and conditional logic.

### Instructions

1. Open a new Excel workbook and name the first worksheet "Marksheet".

2. Create the following table structure starting from cell A1:

   | Column | Header |
   |--------|--------|
   | A | Roll No. |
   | B | Student Name |
   | C | Hindi |
   | D | English |
   | E | Mathematics |
   | F | Science |
   | G | Computer |
   | H | Total |
   | I | Average |
   | J | Result |

3. Enter data for **8 students** using Indian names. Use marks between 20 and 100 for each subject. Use these names: Rahul Sharma, Priya Verma, Amit Patel, Sneha Gupta, Ananya Singh, Vikram Joshi, Kavita Mishra, Deepak Tiwari. Roll numbers should be 2601 to 2608.

4. Write formulas:
   - **Total (Column H):** Use `=SUM()` to add marks of all 5 subjects for each student.
   - **Average (Column I):** Use `=AVERAGE()` to calculate the average marks for each student.
   - **Result (Column J):** Use `=IF(I2>=33,"Pass","Fail")` to determine if the student passed (average 33 or above).

5. Below the student data, add summary rows:
   - **Highest Marks:** Use `=MAX()` for each subject column.
   - **Lowest Marks:** Use `=MIN()` for each subject column.
   - **Class Average:** Use `=AVERAGE()` for each subject column.
   - **Total Students:** Use `=COUNT()` for any subject column.

6. Apply formatting:
   - Make the header row **bold** with a **blue background** and **white text**.
   - Center-align all headers.
   - Apply **number format** with 1 decimal place for the Average column.
   - Use **green fill color** for "Pass" cells and **red fill color** for "Fail" cells in the Result column.
   - Add **borders** to all cells containing data.
   - Set column widths so all data is visible.

### Submission
Save the file as `CCC_Marksheet_YourName.xlsx`.

---

## Task 2: Build a Monthly Budget Spreadsheet

**Objective:** Practice data organization, currency formatting, formulas, absolute references, and percentage calculations.

### Instructions

1. Create a new worksheet named "Budget".

2. In cell A1, type the title "Monthly Budget — July 2026" and merge cells A1:E1. Center the title and make it bold with font size 16.

3. In cell B3, enter the **Monthly Income: Rs. 35,000**.

4. Create the following expense table starting from row 5:

   | Column A | Column B | Column C | Column D | Column E |
   |----------|----------|----------|----------|----------|
   | **Category** | **Budgeted (Rs.)** | **Actual (Rs.)** | **Difference (Rs.)** | **% of Income** |
   | Rent | 8,000 | 8,000 | | |
   | Food & Groceries | 6,000 | 6,500 | | |
   | Transport | 3,000 | 2,800 | | |
   | Electricity & Water | 2,000 | 2,200 | | |
   | Phone & Internet | 1,500 | 1,500 | | |
   | Clothing | 2,000 | 1,800 | | |
   | Entertainment | 1,500 | 2,000 | | |
   | Education/Books | 3,000 | 3,500 | | |
   | Medical | 1,000 | 500 | | |
   | Savings | 5,000 | 4,200 | | |
   | Miscellaneous | 2,000 | 2,500 | | |

5. Write formulas:
   - **Difference (Column D):** `=B-C` for each row (Budgeted minus Actual). Positive means under budget, negative means over budget.
   - **% of Income (Column E):** Use an **absolute reference** to the Monthly Income cell. Formula: `=C6/$B$3*100` (actual amount as percentage of income).
   - Add a **Total row** at the bottom using `=SUM()` for columns B, C, and D.
   - Add a **Remaining Balance** row: `=Income - Total Actual Expenses`.

6. Apply formatting:
   - **Currency format** (Rs.) for columns B, C, and D.
   - **Percentage format** with 1 decimal place for column E.
   - Use **conditional formatting** or manual fill colors: green for positive differences (under budget), red for negative differences (over budget).
   - Add borders to the entire table.
   - Bold the Total and Remaining Balance rows.

### Submission
Save the file as `CCC_Budget_YourName.xlsx`.

---

## Task 3: Create Charts from Data

**Objective:** Practice creating different chart types, adding chart elements, and choosing the appropriate chart for different data.

### Instructions

1. Create a new worksheet named "Charts".

2. Enter the following quarterly sales data for a shop in Bhopal:

   | Quarter | Electronics (Rs.) | Clothing (Rs.) | Stationery (Rs.) |
   |---------|-------------------|-----------------|-------------------|
   | Q1 (Jan-Mar) | 1,50,000 | 80,000 | 45,000 |
   | Q2 (Apr-Jun) | 1,80,000 | 1,00,000 | 50,000 |
   | Q3 (Jul-Sep) | 1,60,000 | 1,20,000 | 60,000 |
   | Q4 (Oct-Dec) | 2,20,000 | 1,50,000 | 75,000 |

3. Create the following charts:

   **Chart 1 — Clustered Column Chart:**
   - Select all the data and create a Clustered Column chart.
   - Add a **chart title**: "Quarterly Sales Comparison — 2026".
   - Add **axis titles**: X-axis = "Quarter", Y-axis = "Sales (Rs.)".
   - Add a **legend** showing the three product categories.

   **Chart 2 — Pie Chart:**
   - Calculate the **total annual sales** for each category.
   - Create a Pie chart showing the proportion of total sales by category.
   - Add a chart title: "Sales Distribution by Category — 2026".
   - Add **data labels** showing percentages.

   **Chart 3 — Line Chart:**
   - Using the quarterly data, create a Line chart showing the trend for each category.
   - Add a chart title: "Sales Trends — 2026".
   - Add axis titles and a legend.

4. For each chart:
   - Position the chart so it does not overlap the data.
   - Ensure all labels are readable.
   - Choose appropriate colors.

5. On the same worksheet, write a brief note (2-3 sentences) below each chart explaining **why you chose that chart type** for that particular data.

### Submission
Save the file as `CCC_Charts_YourName.xlsx`.

---

## Task 4: Data Management — Sorting, Filtering, and Print Setup

**Objective:** Practice sorting, filtering, freeze panes, and print setup features.

### Instructions

1. Create a new worksheet named "Employee Data".

2. Enter the following employee data for a company in Delhi:

   | Emp ID | Name | Department | City | Salary (Rs.) | Joining Date |
   |--------|------|------------|------|-------------|-------------|
   | E001 | Rahul Verma | IT | Delhi | 45,000 | 15-Jan-2023 |
   | E002 | Priya Nair | HR | Mumbai | 38,000 | 20-Mar-2022 |
   | E003 | Amit Singh | IT | Pune | 52,000 | 10-Jun-2021 |
   | E004 | Sneha Reddy | Finance | Hyderabad | 41,000 | 05-Aug-2023 |
   | E005 | Vikram Das | HR | Delhi | 36,000 | 12-Nov-2022 |
   | E006 | Kavita Joshi | Finance | Mumbai | 43,000 | 28-Feb-2021 |
   | E007 | Deepak Rao | IT | Bangalore | 55,000 | 18-Jul-2022 |
   | E008 | Ananya Iyer | Marketing | Chennai | 39,000 | 03-Sep-2023 |
   | E009 | Suresh Kumar | Marketing | Delhi | 42,000 | 22-Apr-2022 |
   | E010 | Meera Sharma | IT | Pune | 48,000 | 14-Dec-2021 |
   | E011 | Arjun Patel | Finance | Ahmedabad | 40,000 | 07-May-2023 |
   | E012 | Neha Gupta | HR | Bhopal | 35,000 | 19-Jan-2022 |

3. Perform the following tasks:

   **Sorting:**
   - First, sort the data by **Department** (A to Z).
   - Then apply a two-level sort: sort by **Department** (A to Z), then by **Salary** (highest to lowest) within each department.
   - Take note of the order after each sort.

   **Filtering:**
   - Apply filters to the data.
   - Filter to show only employees in the **IT** department.
   - Clear the filter and then filter to show employees with **Salary above Rs. 40,000**.
   - Clear all filters when done.

   **Freeze Panes:**
   - Apply Freeze Panes to keep the **header row** visible while scrolling.
   - Verify by scrolling down (even though there are only 12 rows, practice the feature).

   **Print Setup:**
   - Set the Print Area to include all employee data.
   - Add a **header**: "Employee Directory — TechPath Institute" (centered).
   - Add a **footer**: "Page &[Page] of &[Pages]" (centered) and today's date (right-aligned).
   - Set the page orientation to **Landscape**.
   - Set Print Titles so the header row repeats on every page.
   - Open Print Preview (Ctrl + P) to verify the setup looks correct.

### Submission
Save the file as `CCC_EmployeeData_YourName.xlsx`.

---

## Submission Guidelines

1. Complete all 4 tasks.
2. Save each file with the naming convention specified above, replacing "YourName" with your actual name.
3. Verify that all formulas work correctly — click on formula cells to check.
4. Ensure all formatting is applied as instructed.
5. Submit all files to your trainer at TechPath Institute.

**Grading Criteria:**
- Correct use of formulas and functions (40%)
- Proper formatting and presentation (25%)
- Correct chart creation and labeling (20%)
- Sorting, filtering, and print setup (15%)

---

*TechPath Institute — CCC Exam Preparation*

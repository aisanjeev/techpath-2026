# Formulas and Functions in Excel

**Module 04 — CCC Exam Preparation | Topic 4**

---

## What is a Formula?

A **formula** is an expression that performs calculations on values in your worksheet. Every formula in Excel must start with an **equals sign (=)**.

For example:
- `=5+3` calculates the sum of 5 and 3 (result: 8)
- `=A1+B1` adds the values in cells A1 and B1
- `=C2*D2` multiplies the values in cells C2 and D2

### Arithmetic Operators in Excel

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Addition | `=5+3` | 8 |
| `-` | Subtraction | `=10-4` | 6 |
| `*` | Multiplication | `=6*7` | 42 |
| `/` | Division | `=20/4` | 5 |
| `^` | Exponent (power) | `=2^3` | 8 |
| `%` | Percentage | `=50%` | 0.5 |

### Order of Operations (BODMAS)

Excel follows the standard mathematical order of operations:

1. **B** — Brackets (parentheses)
2. **O** — Orders (exponents/powers)
3. **D** — Division
4. **M** — Multiplication
5. **A** — Addition
6. **S** — Subtraction

Example: `=2+3*4` gives **14** (not 20), because multiplication is done before addition. To change the order, use brackets: `=(2+3)*4` gives **20**.

**CCC Exam Tip:** The CCC exam frequently asks about the order of operations. Remember that **multiplication and division** are performed **before** addition and subtraction. Use **brackets** to override the default order.

---

## What is a Function?

A **function** is a predefined (built-in) formula that performs a specific calculation. Functions save time because you do not need to write complex formulas from scratch.

### Function Syntax

Every function follows this pattern:

```
=FUNCTION_NAME(argument1, argument2, ...)
```

- The **function name** tells Excel what calculation to perform.
- **Arguments** are the values or cell references the function uses. They are enclosed in **parentheses**.
- Multiple arguments are separated by **commas**.

### Cell Ranges

Many functions work with a **range** of cells. A range is written using a **colon (:)** between the first and last cell:

| Range | Meaning |
|-------|---------|
| `A1:A10` | All cells from A1 to A10 (a column of 10 cells) |
| `A1:D1` | All cells from A1 to D1 (a row of 4 cells) |
| `A1:D10` | A rectangular block of 40 cells (4 columns x 10 rows) |
| `B2:B100` | All cells from B2 to B100 |

**CCC Exam Tip:** "What is the correct formula to add cells A1 to A10?" — The answer is `=SUM(A1:A10)`. The colon `:` is used to define a range of cells.

---

## Essential Excel Functions

### 1. SUM Function

The **SUM** function adds up all the numbers in a range.

**Syntax:** `=SUM(range)`

**Examples:**
- `=SUM(A1:A10)` — Adds all values from A1 to A10
- `=SUM(A1,B1,C1)` — Adds values in A1, B1, and C1
- `=SUM(A1:A5,C1:C5)` — Adds values in two separate ranges

### 2. AVERAGE Function

The **AVERAGE** function calculates the average (mean) of numbers in a range.

**Syntax:** `=AVERAGE(range)`

**Examples:**
- `=AVERAGE(B2:B6)` — Average of values from B2 to B6
- `=AVERAGE(80,75,90,85)` — Average of these four numbers (result: 82.5)

### 3. MAX Function

The **MAX** function returns the largest (maximum) value in a range.

**Syntax:** `=MAX(range)`

**Examples:**
- `=MAX(C2:C10)` — Finds the highest value in C2 to C10
- `=MAX(45,78,23,91,56)` — Returns 91

### 4. MIN Function

The **MIN** function returns the smallest (minimum) value in a range.

**Syntax:** `=MIN(range)`

**Examples:**
- `=MIN(C2:C10)` — Finds the lowest value in C2 to C10
- `=MIN(45,78,23,91,56)` — Returns 23

### 5. COUNT Function

The **COUNT** function counts how many cells in a range contain numbers.

**Syntax:** `=COUNT(range)`

**Examples:**
- `=COUNT(A1:A20)` — Counts how many cells from A1 to A20 have numbers
- If A1=10, A2="Rahul", A3=20, A4=30, then `=COUNT(A1:A4)` returns **3** (skips the text)

**Note:** COUNT only counts cells with **numbers**. To count cells with any data (including text), use `=COUNTA(range)`.

**CCC Exam Tip:** Know the difference between COUNT and COUNTA. COUNT counts only numeric values. COUNTA counts all non-empty cells (numbers + text). This distinction is tested in the exam.

---

## Practical Example — Student Marksheet

Let us create a marksheet for students at TechPath Institute, Bhopal:

| | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| 1 | **Roll No.** | **Name** | **Hindi** | **English** | **Maths** | **Total** | **Average** |
| 2 | 101 | Rahul | 78 | 85 | 72 | | |
| 3 | 102 | Priya | 92 | 88 | 95 | | |
| 4 | 103 | Amit | 65 | 70 | 58 | | |
| 5 | 104 | Sneha | 88 | 91 | 83 | | |
| 6 | 105 | Ananya | 74 | 80 | 77 | | |
| 7 | | | | | | | |
| 8 | | | **Highest** | | | | |
| 9 | | | **Lowest** | | | | |
| 10 | | | **Class Avg** | | | | |
| 11 | | | **Count** | | | | |

### Formulas to Use

**Total Marks (Column F):**
- Cell F2: `=SUM(C2:E2)` — Adds Hindi + English + Maths for Rahul
- Copy this formula down to F3, F4, F5, F6 using AutoFill

**Average Marks (Column G):**
- Cell G2: `=AVERAGE(C2:E2)` — Average of three subjects for Rahul
- Copy down to G3, G4, G5, G6

**Highest Marks in Hindi (Cell C8):**
- `=MAX(C2:C6)` — Returns 92 (Priya's score)

**Lowest Marks in Hindi (Cell C9):**
- `=MIN(C2:C6)` — Returns 65 (Amit's score)

**Class Average in Hindi (Cell C10):**
- `=AVERAGE(C2:C6)` — Returns 79.4

**Number of Students (Cell C11):**
- `=COUNT(C2:C6)` — Returns 5

Copy the formulas in C8:C11 to D8:D11 and E8:E11 to calculate the same for English and Maths.

---

## Other Useful Functions (For Reference)

| Function | Purpose | Example |
|----------|---------|---------|
| `COUNTIF` | Count cells meeting a condition | `=COUNTIF(F2:F6,">200")` |
| `SUMIF` | Sum cells meeting a condition | `=SUMIF(C2:C6,">80")` |
| `IF` | Returns one value if condition is true, another if false | `=IF(G2>=33,"Pass","Fail")` |
| `ROUND` | Rounds a number to specified decimals | `=ROUND(G2,1)` |
| `LEN` | Returns the length of text | `=LEN(B2)` |
| `UPPER` | Converts text to uppercase | `=UPPER(B2)` |
| `LOWER` | Converts text to lowercase | `=LOWER(B2)` |
| `TODAY` | Returns today's date | `=TODAY()` |
| `NOW` | Returns current date and time | `=NOW()` |
| `CONCATENATE` | Joins text strings together | `=CONCATENATE(A2," ",B2)` |

**CCC Exam Tip:** While the exam focuses most on SUM, AVERAGE, MAX, MIN, and COUNT, questions about IF, COUNTIF, and TODAY also appear occasionally. The IF function syntax is: `=IF(condition, value_if_true, value_if_false)`.

---

## Common Formula Errors

| Error | Meaning | Common Cause |
|-------|---------|-------------|
| `#DIV/0!` | Division by zero | Formula divides by a cell that contains 0 or is empty |
| `#VALUE!` | Wrong value type | Using text where a number is expected |
| `#REF!` | Invalid reference | A cell referenced by the formula was deleted |
| `#NAME?` | Unrecognized name | Misspelled function name (e.g., SUMM instead of SUM) |
| `#NUM!` | Invalid number | Number is too large or formula produces an impossible result |
| `######` | Column too narrow | Widen the column — this is not actually an error |

**CCC Exam Tip:** "#DIV/0!" error (division by zero) and "#NAME?" error (misspelled function) are the most commonly asked errors in the exam.

---

## Summary Table

| Concept | Key Point |
|---------|-----------|
| Formula starts with | `=` (equals sign) |
| SUM | `=SUM(A1:A10)` — adds values |
| AVERAGE | `=AVERAGE(A1:A10)` — calculates mean |
| MAX | `=MAX(A1:A10)` — highest value |
| MIN | `=MIN(A1:A10)` — lowest value |
| COUNT | `=COUNT(A1:A10)` — counts numeric cells |
| COUNTA | Counts all non-empty cells |
| Cell range | A1:A10 (colon separates start and end) |
| BODMAS | Brackets first, then powers, then *, /, then +, - |
| #DIV/0! | Division by zero error |
| #NAME? | Misspelled function name |

---

*TechPath Institute — CCC Exam Preparation*

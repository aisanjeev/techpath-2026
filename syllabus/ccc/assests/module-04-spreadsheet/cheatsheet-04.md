# Module 04 — Spreadsheet / MS Excel — Cheatsheet

**CCC Exam Preparation | TechPath Institute**

---

## Formula Syntax Reference

| Function | Syntax | Example | Result |
|----------|--------|---------|--------|
| SUM | `=SUM(range)` | `=SUM(A1:A10)` | Total of values in A1 to A10 |
| AVERAGE | `=AVERAGE(range)` | `=AVERAGE(B2:B6)` | Mean of values in B2 to B6 |
| MAX | `=MAX(range)` | `=MAX(C1:C20)` | Largest value in C1 to C20 |
| MIN | `=MIN(range)` | `=MIN(C1:C20)` | Smallest value in C1 to C20 |
| COUNT | `=COUNT(range)` | `=COUNT(A1:A50)` | Count of numeric cells |
| COUNTA | `=COUNTA(range)` | `=COUNTA(A1:A50)` | Count of non-empty cells |
| IF | `=IF(test, true, false)` | `=IF(A1>33,"Pass","Fail")` | "Pass" if A1>33, else "Fail" |
| COUNTIF | `=COUNTIF(range, criteria)` | `=COUNTIF(A1:A10,">50")` | Count of cells >50 |
| SUMIF | `=SUMIF(range, criteria)` | `=SUMIF(B1:B10,">100")` | Sum of cells >100 |
| ROUND | `=ROUND(number, decimals)` | `=ROUND(3.567,1)` | 3.6 |
| UPPER | `=UPPER(text)` | `=UPPER("hello")` | HELLO |
| LOWER | `=LOWER(text)` | `=LOWER("HELLO")` | hello |
| LEN | `=LEN(text)` | `=LEN("Rahul")` | 5 |
| TODAY | `=TODAY()` | `=TODAY()` | Current date |
| NOW | `=NOW()` | `=NOW()` | Current date and time |
| CONCATENATE | `=CONCATENATE(text1, text2)` | `=CONCATENATE(A1," ",B1)` | Joins A1 and B1 with space |

---

## Arithmetic Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Addition | `=5+3` | 8 |
| `-` | Subtraction | `=10-4` | 6 |
| `*` | Multiplication | `=6*7` | 42 |
| `/` | Division | `=20/4` | 5 |
| `^` | Power/Exponent | `=2^3` | 8 |
| `%` | Percentage | `=50%` | 0.5 |

**Order of Operations (BODMAS):** Brackets > Powers > Multiply/Divide > Add/Subtract

---

## Cell Reference Types

| Type | Format | Column | Row | Behavior When Copied |
|------|--------|--------|-----|---------------------|
| Relative | `A1` | Changes | Changes | Both adjust to new position |
| Absolute | `$A$1` | Fixed | Fixed | Nothing changes |
| Mixed | `$A1` | Fixed | Changes | Column stays, row adjusts |
| Mixed | `A$1` | Changes | Fixed | Row stays, column adjusts |

**Toggle shortcut:** Press **F4** while editing a cell reference to cycle through all four types.

---

## Excel Keyboard Shortcuts

### File Operations

| Shortcut | Action |
|----------|--------|
| Ctrl + N | New workbook |
| Ctrl + O | Open file |
| Ctrl + S | Save |
| F12 | Save As |
| Ctrl + W | Close workbook |
| Ctrl + P | Print / Print Preview |

### Editing

| Shortcut | Action |
|----------|--------|
| Ctrl + Z | Undo |
| Ctrl + Y | Redo |
| Ctrl + C | Copy |
| Ctrl + X | Cut |
| Ctrl + V | Paste |
| Ctrl + Alt + V | Paste Special |
| Ctrl + F | Find |
| Ctrl + H | Find and Replace |
| F2 | Edit active cell |
| Delete | Clear cell content |
| Ctrl + D | Fill Down (copy from cell above) |
| Ctrl + R | Fill Right (copy from cell to left) |

### Formatting

| Shortcut | Action |
|----------|--------|
| Ctrl + B | Bold |
| Ctrl + I | Italic |
| Ctrl + U | Underline |
| Ctrl + 1 | Open Format Cells dialog |
| Ctrl + Shift + $ | Currency format |
| Ctrl + Shift + % | Percentage format |
| Ctrl + Shift + # | Date format |
| Ctrl + Shift + ! | Number format (with commas) |

### Navigation

| Shortcut | Action |
|----------|--------|
| Ctrl + Home | Go to cell A1 |
| Ctrl + End | Go to last used cell |
| Ctrl + Arrow | Jump to edge of data region |
| Ctrl + G | Go To dialog |
| Ctrl + Page Down | Next worksheet tab |
| Ctrl + Page Up | Previous worksheet tab |
| Home | Go to column A in current row |
| Tab | Move one cell right |
| Shift + Tab | Move one cell left |

### Selection

| Shortcut | Action |
|----------|--------|
| Ctrl + A | Select all cells |
| Ctrl + Space | Select entire column |
| Shift + Space | Select entire row |
| Ctrl + Shift + End | Select from current cell to last used cell |
| Shift + Arrow | Extend selection by one cell |
| Ctrl + Shift + Arrow | Extend selection to edge of data |

### Charts and Other

| Shortcut | Action |
|----------|--------|
| F11 | Create chart on new sheet |
| Alt + F1 | Create embedded chart on same sheet |
| Ctrl + Shift + L | Toggle Filter on/off |
| Ctrl + E | Flash Fill |
| F4 | Toggle cell reference type |
| Ctrl + ; | Insert current date |
| Ctrl + Shift + ; | Insert current time |
| Ctrl + Shift + + | Insert cells/rows/columns |

---

## Chart Type Comparison

| Chart Type | Shape | Best For | Avoid When | Example Use |
|-----------|-------|----------|------------|-------------|
| **Column** | Vertical bars | Comparing categories side by side | Too many categories (>10) | Student marks by subject |
| **Bar** | Horizontal bars | Long category names, rankings | Showing time trends | City population comparison |
| **Pie** | Circular slices | Parts of a whole (percentages) | Multiple data series, >7 slices | Monthly budget breakdown |
| **Line** | Connected points | Trends over time, continuous data | Unrelated categories | Website traffic over months |
| **Area** | Filled line chart | Volume/magnitude over time | Overlapping data series | Revenue growth over years |
| **Scatter** | Individual dots | Relationship between two variables | Category data | Height vs weight data |

### Chart Elements Quick Reference

| Element | What It Does |
|---------|-------------|
| Chart Title | Names the chart |
| X-Axis (Horizontal) | Shows categories or time |
| Y-Axis (Vertical) | Shows values |
| Axis Titles | Labels for axes |
| Legend | Identifies colors/patterns |
| Data Labels | Shows exact values |
| Gridlines | Background lines for reading values |
| Data Table | Shows source data below chart |

---

## Common Excel Errors

| Error | Meaning | How to Fix |
|-------|---------|-----------|
| `#DIV/0!` | Division by zero | Check if divisor cell is empty or contains 0 |
| `#VALUE!` | Wrong data type | Check for text in cells that should have numbers |
| `#REF!` | Invalid cell reference | A referenced cell was deleted; fix the formula |
| `#NAME?` | Unrecognized name | Check for misspelled function name |
| `#NUM!` | Invalid number | Check for impossible calculations |
| `#N/A` | Value not available | Usually from VLOOKUP — value not found |
| `######` | Column too narrow | Widen the column — this is NOT an error |
| `Circular Reference` | Formula refers to itself | Remove the self-reference in the formula |

---

## Number Format Codes

| Format | Display Example | Use For |
|--------|----------------|---------|
| General | 1234.5 | Default, auto-detected |
| Number | 1,234.50 | General numbers |
| Currency | Rs. 1,234.50 | Monetary values |
| Percentage | 85.00% | Rates, proportions |
| Date (Short) | 26/07/2026 | Dates |
| Date (Long) | 26 July 2026 | Formal dates |
| Time | 10:30 AM | Time values |
| Text | 001234 | IDs, phone numbers (preserves leading zeros) |
| Scientific | 1.23E+03 | Very large or small numbers |
| Fraction | 1/4 | Fractional values |

---

## Excel Interface — Key Tabs and Their Functions

| Tab | Contains |
|-----|----------|
| **Home** | Clipboard, Font, Alignment, Number format, Styles, Cells, Editing |
| **Insert** | Tables, Charts, Sparklines, Filters, Links, Text, Header & Footer |
| **Page Layout** | Themes, Page Setup, Scale to Fit, Print Area, Sheet Options |
| **Formulas** | Function Library, Defined Names, Formula Auditing, Calculation |
| **Data** | Get Data, Sort & Filter, Data Tools, Outline |
| **Review** | Proofing, Comments, Protect Sheet/Workbook |
| **View** | Workbook Views, Show, Zoom, Window, Freeze Panes |

---

## Quick Facts for CCC Exam

| Fact | Answer |
|------|--------|
| Maximum rows in Excel | 10,48,576 |
| Maximum columns in Excel | 16,384 (A to XFD) |
| Default worksheet count | 1 (Sheet1) |
| Default file extension | .xlsx |
| Older file extension | .xls |
| Default text alignment | Left |
| Default number alignment | Right |
| Formula always starts with | = (equals sign) |
| Fill Handle appearance | Small black cross (+) |
| Cell = intersection of | Row and Column |
| Freeze Panes location | View tab |
| Print Area location | Page Layout tab |
| Filter location | Data tab |
| Chart creation location | Insert tab |
| Format Cells shortcut | Ctrl + 1 |
| Page number in footer | &[Page] |

---

*TechPath Institute — CCC Exam Preparation*

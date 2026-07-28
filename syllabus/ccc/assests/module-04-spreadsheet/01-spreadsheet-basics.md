# Spreadsheet Basics — Introduction to MS Excel

**Module 04 — CCC Exam Preparation | Topic 1**

---

## What is a Spreadsheet?

A **spreadsheet** is a software application that organizes data in **rows** and **columns**, forming a grid of **cells**. It is used for calculations, data analysis, and creating charts. The most widely used spreadsheet program is **Microsoft Excel**, which is part of the Microsoft Office suite.

In simple words: A spreadsheet is like a digital notebook with rows and columns where you can type data and perform calculations automatically.

**CCC Exam Tip:** The CCC exam frequently asks: "Which application is used for spreadsheet calculations?" The answer is **MS Excel**. Other spreadsheet programs include LibreOffice Calc and Google Sheets, but the CCC exam focuses on MS Excel.

---

## Opening MS Excel

There are several ways to open Microsoft Excel on your computer:

1. **Start Menu:** Click on the Windows Start button, search for "Excel", and click on the Microsoft Excel icon.
2. **Desktop Shortcut:** If there is an Excel shortcut on your desktop, double-click on it.
3. **Run Command:** Press `Win + R`, type `excel`, and press Enter.
4. **From File Explorer:** Double-click on any `.xlsx` file to open it directly in Excel.

When Excel opens, you see a **Start Screen** where you can create a new blank workbook or open a recent file.

---

## Workbook vs Worksheet

Understanding the difference between a workbook and a worksheet is essential for the CCC exam.

| Feature | Workbook | Worksheet |
|---------|----------|-----------|
| **Definition** | The entire Excel file | A single sheet (tab) inside the workbook |
| **File Extension** | `.xlsx` (or `.xls` for older versions) | No separate file — part of the workbook |
| **Contains** | One or more worksheets | Rows and columns of data |
| **Analogy** | Like a physical notebook | Like one page of that notebook |
| **Default count** | 1 workbook when you open Excel | 1 worksheet (Sheet1) by default |

**CCC Exam Tip:** "A workbook can contain multiple worksheets" is a frequently tested statement. By default, a new workbook in modern Excel has **1 worksheet**, but you can add more by clicking the **+** button next to the sheet tabs at the bottom.

---

## Understanding Rows, Columns, and Cells

The Excel worksheet is organized into a grid structure:

### Rows
- Rows run **horizontally** (left to right) across the screen.
- They are identified by **numbers**: 1, 2, 3, 4, ... up to **10,48,576** (over 10 lakh rows).
- Row numbers appear on the **left side** of the worksheet.

### Columns
- Columns run **vertically** (top to bottom) down the screen.
- They are identified by **letters**: A, B, C, ... Z, then AA, AB, AC, ... up to **XFD** (16,384 columns).
- Column letters appear at the **top** of the worksheet.

### Cells
- A **cell** is the **intersection** (meeting point) of a row and a column.
- Each cell has a unique **cell address** (also called a cell reference).
- The cell address is formed by combining the **column letter** and the **row number**.

**CCC Exam Tip:** "The intersection of a row and column is called a **Cell**" is one of the most frequently asked questions in the CCC exam. Remember this definition.

---

## Cell Addressing

Every cell in Excel has a unique address that identifies its position. This is called **cell addressing** or **cell referencing**.

### How Cell Addresses Work

The cell address is written as: **Column Letter + Row Number**

| Cell Address | Meaning |
|-------------|---------|
| **A1** | Column A, Row 1 (top-left corner cell) |
| **B2** | Column B, Row 2 |
| **C5** | Column C, Row 5 |
| **D10** | Column D, Row 10 |
| **AA1** | Column AA, Row 1 |

### The Name Box

The **Name Box** is located to the left of the Formula Bar. It shows the address of the currently selected (active) cell. You can also type a cell address in the Name Box and press Enter to quickly jump to that cell.

### Active Cell

The cell that is currently selected is called the **active cell**. It is highlighted with a dark border. You can identify the active cell by:
- Looking at the **Name Box** (shows the cell address)
- Looking at the **highlighted column letter** and **row number**

---

## Navigating in a Spreadsheet

You can move around the spreadsheet using these methods:

| Action | Shortcut Key |
|--------|-------------|
| Move one cell right | `Tab` or Right Arrow |
| Move one cell left | `Shift + Tab` or Left Arrow |
| Move one cell up | Up Arrow |
| Move one cell down | `Enter` or Down Arrow |
| Go to cell A1 | `Ctrl + Home` |
| Go to last used cell | `Ctrl + End` |
| Move to next worksheet | `Ctrl + Page Down` |
| Move to previous worksheet | `Ctrl + Page Up` |
| Go to a specific cell | `Ctrl + G` (Go To dialog) |
| Move to beginning of row | `Home` |

**CCC Exam Tip:** The shortcut `Ctrl + Home` to go to cell A1 and `Ctrl + End` to go to the last used cell are commonly asked in exams.

---

## Saving Workbooks

Saving your work is one of the most important tasks in Excel.

### Save vs Save As

| Feature | Save (Ctrl + S) | Save As (F12) |
|---------|-----------------|---------------|
| **Purpose** | Save changes to an existing file | Save with a new name, location, or format |
| **First time saving** | Opens Save As dialog automatically | Opens Save As dialog |
| **Shortcut** | `Ctrl + S` | `F12` or `Ctrl + Shift + S` |

### Excel File Formats

| Extension | Format Name | Description |
|-----------|------------|-------------|
| `.xlsx` | Excel Workbook | Default format for modern Excel (2007+) |
| `.xls` | Excel 97-2003 Workbook | Older format, smaller size limit |
| `.xlsm` | Excel Macro-Enabled Workbook | Supports macros (VBA code) |
| `.csv` | Comma Separated Values | Plain text, data only, no formatting |
| `.pdf` | PDF Document | For sharing, cannot be edited in Excel |

**CCC Exam Tip:** The default file extension for Excel 2007 and later is **`.xlsx`**. The older format is **`.xls`**. This distinction is frequently tested.

---

## Print Area and Page Break

### Setting Print Area

Sometimes you do not want to print the entire worksheet. You can select only the data you want to print:

1. Select the range of cells you want to print.
2. Go to **Page Layout** tab.
3. Click **Print Area** > **Set Print Area**.

Now only the selected area will be printed. To remove the print area, click **Print Area** > **Clear Print Area**.

### Page Break Preview

Page Break Preview shows you how your data will be divided across printed pages:

1. Go to **View** tab.
2. Click **Page Break Preview**.
3. Blue dashed lines show automatic page breaks.
4. You can drag these lines to adjust where pages break.

To return to normal view, go to **View** > **Normal**.

**CCC Exam Tip:** Questions about Print Area and Page Break Preview often appear in the exam. Remember that Print Area is found under the **Page Layout** tab.

---

## Summary Table — Key Concepts

| Concept | Key Point |
|---------|-----------|
| Spreadsheet | Software for data in rows and columns |
| Workbook | The entire Excel file (.xlsx) |
| Worksheet | One sheet/tab inside a workbook |
| Cell | Intersection of a row and a column |
| Cell Address | Column letter + Row number (e.g., A1) |
| Rows | Horizontal, numbered 1 to 10,48,576 |
| Columns | Vertical, lettered A to XFD (16,384 total) |
| Active Cell | Currently selected cell |
| Name Box | Shows address of the active cell |
| Save shortcut | Ctrl + S |
| Default extension | .xlsx |
| Print Area | Page Layout > Print Area > Set Print Area |

---

*TechPath Institute — CCC Exam Preparation*

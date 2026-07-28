# Data Entry and Editing in Excel

**Module 04 — CCC Exam Preparation | Topic 3**

---

## Entering Data in Cells

In Excel, you can enter three main types of data into cells:

### 1. Text (Labels)

Text entries are used for headings, names, descriptions, and other non-numeric data.

- Text is **left-aligned** by default in a cell.
- Examples: "Name", "Rahul", "Delhi", "Product A"
- If text is longer than the column width, it overflows into the next cell (if that cell is empty) or gets cut off visually.

### 2. Numbers (Values)

Numbers are used for quantities, prices, scores, and any data you want to calculate.

- Numbers are **right-aligned** by default in a cell.
- Examples: 100, 45000, 3.14, -25
- Do not type Rs. or % directly with the number if you plan to use it in calculations. Instead, use number formatting (explained below).

### 3. Dates and Times

Excel stores dates and times as numbers internally, which allows you to perform calculations with them (for example, finding the difference between two dates).

- Dates are **right-aligned** by default.
- Common date formats: `26/07/2026`, `26-Jul-2026`, `July 26, 2026`
- Common time formats: `10:30 AM`, `14:30`, `10:30:00`

**CCC Exam Tip:** The exam may ask about default alignment. Remember: **Text = Left-aligned, Numbers = Right-aligned, Dates = Right-aligned**. This is a frequently tested concept.

---

## Entering Data — Step by Step

To enter data in a cell:

1. **Click** on the cell where you want to enter data (it becomes the active cell).
2. **Type** your data using the keyboard.
3. **Confirm** the entry by pressing:
   - `Enter` — confirms and moves to the cell below
   - `Tab` — confirms and moves to the cell to the right
   - Click on another cell — confirms and moves to that cell
4. **Cancel** an entry by pressing `Esc` before confirming.

### The Formula Bar

The **Formula Bar** is located above the worksheet grid, below the Ribbon. It shows the content of the currently selected cell. You can also type or edit data directly in the Formula Bar.

---

## Editing Cell Data

### Modifying Cell Content

There are several ways to edit data in a cell:

| Method | How To |
|--------|--------|
| **Double-click** | Double-click on the cell to enter edit mode directly in the cell |
| **Formula Bar** | Click on the cell, then click in the Formula Bar to edit |
| **F2 key** | Select the cell and press F2 to enter edit mode |
| **Retype** | Select the cell and start typing — the old content is replaced completely |

### Clearing Cell Content

To remove data from cells without deleting the cells themselves:

| Action | Method |
|--------|--------|
| Clear content only | Select cells, press `Delete` key |
| Clear everything | Select cells, go to **Home** > **Clear** > **Clear All** |
| Clear formatting only | **Home** > **Clear** > **Clear Formats** |
| Clear content only | **Home** > **Clear** > **Clear Contents** |

### Undo and Redo

- **Undo** (`Ctrl + Z`): Reverses the last action. You can undo up to 100 actions.
- **Redo** (`Ctrl + Y`): Restores an action that was undone.

**CCC Exam Tip:** The shortcut keys `Ctrl + Z` (Undo) and `Ctrl + Y` (Redo) are frequently asked in the exam.

---

## Inserting and Deleting Rows and Columns

### Inserting Rows

1. Right-click on the **row number** where you want to insert a new row above.
2. Select **Insert** from the context menu.
3. A new blank row appears, and existing rows shift down.

**Shortcut:** Select the row, then press `Ctrl + Shift + +` (plus key).

### Inserting Columns

1. Right-click on the **column letter** where you want to insert a new column to the left.
2. Select **Insert** from the context menu.
3. A new blank column appears, and existing columns shift to the right.

### Deleting Rows

1. Right-click on the **row number** you want to delete.
2. Select **Delete** from the context menu.
3. The row is removed and rows below shift up.

### Deleting Columns

1. Right-click on the **column letter** you want to delete.
2. Select **Delete** from the context menu.
3. The column is removed and columns to the right shift left.

**CCC Exam Tip:** Remember that inserting a row pushes existing rows **down**, and inserting a column pushes existing columns **to the right**. Deleting does the opposite.

---

## Changing Row Height and Column Width

### Changing Column Width

| Method | Steps |
|--------|-------|
| **Drag** | Place cursor on the border between two column headers, drag left or right |
| **Exact width** | Right-click column header > **Column Width** > type a number > OK |
| **Auto-fit** | Double-click the border between two column headers — Excel adjusts to fit the widest content |
| **Menu** | **Home** > **Format** > **Column Width** or **AutoFit Column Width** |

### Changing Row Height

| Method | Steps |
|--------|-------|
| **Drag** | Place cursor on the border between two row numbers, drag up or down |
| **Exact height** | Right-click row number > **Row Height** > type a number > OK |
| **Auto-fit** | Double-click the border between two row numbers |
| **Menu** | **Home** > **Format** > **Row Height** or **AutoFit Row Height** |

---

## Cell Formatting

Formatting changes how data **looks** in a cell without changing the actual data. All formatting options are available in the **Home** tab of the Ribbon.

### Text Formatting

| Format | Shortcut | Location |
|--------|----------|----------|
| **Bold** | `Ctrl + B` | Home > Font group |
| **Italic** | `Ctrl + I` | Home > Font group |
| **Underline** | `Ctrl + U` | Home > Font group |
| Font size | — | Home > Font group (dropdown) |
| Font color | — | Home > Font group (A with color) |
| Font name | — | Home > Font group (dropdown) |

### Alignment

| Alignment | Description | Location |
|-----------|-------------|----------|
| **Left** | Text aligns to the left edge | Home > Alignment group |
| **Center** | Text aligns in the middle | Home > Alignment group |
| **Right** | Text aligns to the right edge | Home > Alignment group |
| **Merge & Center** | Combines multiple cells and centers the text | Home > Alignment group |
| **Wrap Text** | Shows all text in a cell by displaying it on multiple lines | Home > Alignment group |

### Cell Background Color (Fill Color)

1. Select the cells you want to color.
2. In the **Home** tab, click the **Fill Color** button (paint bucket icon) in the Font group.
3. Choose a color from the palette.

This is useful for highlighting headings, important data, or creating visual distinction between sections.

### Number Formatting

Number formatting changes how numbers are displayed without changing their actual value.

| Format | Example | Use For |
|--------|---------|---------|
| **General** | 1234.5 | Default, no specific format |
| **Number** | 1,234.50 | General numbers with decimal places |
| **Currency** | Rs. 1,234.50 | Prices, monetary values |
| **Percentage** | 85.00% | Scores, rates, proportions |
| **Date** | 26/07/2026 | Dates |
| **Text** | 001234 | Phone numbers, codes (preserves leading zeros) |

To apply number formatting:
1. Select the cells.
2. In the **Home** tab, use the **Number Format** dropdown in the Number group.
3. Or press `Ctrl + 1` to open the **Format Cells** dialog for more options.

**CCC Exam Tip:** The shortcut `Ctrl + 1` opens the Format Cells dialog box. This is a frequently asked shortcut. Also remember that `Ctrl + B` is for Bold, `Ctrl + I` is for Italic, and `Ctrl + U` is for Underline.

---

## Borders

Borders add lines around cells to make data easier to read, especially when printing.

1. Select the cells where you want borders.
2. In the **Home** tab, click the **Borders** button (grid icon) in the Font group.
3. Choose a border style: All Borders, Outside Borders, Thick Box Border, etc.

---

## Copy, Cut, and Paste

| Action | Shortcut | Description |
|--------|----------|-------------|
| **Copy** | `Ctrl + C` | Copies the selected cells |
| **Cut** | `Ctrl + X` | Cuts (moves) the selected cells |
| **Paste** | `Ctrl + V` | Pastes the copied/cut cells |
| **Paste Special** | `Ctrl + Alt + V` | Paste with options (values only, formatting only, etc.) |

### Paste Special Options

Paste Special lets you choose what to paste:
- **Values** — pastes only the calculated values, not the formulas
- **Formulas** — pastes only the formulas
- **Formatting** — pastes only the formatting (colors, fonts, borders)
- **Transpose** — swaps rows and columns

**CCC Exam Tip:** "Paste Special" and its various options (especially "Values" and "Transpose") are commonly tested in the CCC exam.

---

## Summary Table

| Concept | Key Point |
|---------|-----------|
| Text alignment | Left-aligned by default |
| Number alignment | Right-aligned by default |
| Edit cell | Double-click, F2, or click Formula Bar |
| Delete content | Press Delete key |
| Undo | Ctrl + Z |
| Redo | Ctrl + Y |
| Bold | Ctrl + B |
| Italic | Ctrl + I |
| Format Cells dialog | Ctrl + 1 |
| Copy | Ctrl + C |
| Paste | Ctrl + V |
| Paste Special | Ctrl + Alt + V |
| Insert row/column | Right-click > Insert |

---

*TechPath Institute — CCC Exam Preparation*

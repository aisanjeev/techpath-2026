# Printing, Sorting, and Filtering in Excel

**Module 04 — CCC Exam Preparation | Topic 6**

---

## Print Area Selection

When you have a large worksheet but only want to print a specific portion, you can set a **Print Area**.

### Setting a Print Area

1. Select the range of cells you want to print.
2. Go to the **Page Layout** tab.
3. Click **Print Area** > **Set Print Area**.

A thin dashed border appears around the selected area, indicating it is now the print area. When you print, only this area will be printed.

### Clearing the Print Area

1. Go to **Page Layout** tab.
2. Click **Print Area** > **Clear Print Area**.

After clearing, the entire worksheet will be included when printing.

### Adding to an Existing Print Area

1. Select the additional cells you want to include.
2. Go to **Page Layout** > **Print Area** > **Add to Print Area**.

**CCC Exam Tip:** The Print Area option is located under the **Page Layout** tab, not the File tab or Home tab. This location is frequently asked in the exam.

---

## Page Break Preview

**Page Break Preview** shows you exactly how your data will be divided across printed pages. This is very useful for ensuring that important data is not split awkwardly between pages.

### Accessing Page Break Preview

1. Go to the **View** tab.
2. Click **Page Break Preview**.

In this view:
- **Blue solid lines** indicate manual page breaks (set by you).
- **Blue dashed lines** indicate automatic page breaks (set by Excel).
- **Grey areas** indicate areas that will not be printed.

### Adjusting Page Breaks

- **Drag** a blue dashed line to move the automatic page break to a new position. It becomes a manual page break (solid blue line).
- **Insert a manual page break:** Select the row or column where you want the break, go to **Page Layout** > **Breaks** > **Insert Page Break**.
- **Remove a page break:** Select the row/column below/right of the break, go to **Page Layout** > **Breaks** > **Remove Page Break**.
- **Reset all page breaks:** Go to **Page Layout** > **Breaks** > **Reset All Page Breaks**.

### Returning to Normal View

Go to **View** > **Normal** to return to the standard editing view.

---

## Fit to Page (Scaling)

When your data is slightly too wide or too tall for one page, you can scale it to fit:

### Using Page Layout Tab

1. Go to **Page Layout** tab.
2. In the **Scale to Fit** group:
   - **Width:** Set to "1 page" to fit all columns on one page
   - **Height:** Set to "1 page" to fit all rows on one page
   - **Scale:** Adjust the percentage (e.g., 80% to shrink the content)

### Using Print Preview

1. Press `Ctrl + P` to open Print Preview.
2. At the bottom of the settings, look for **Scaling** options:
   - No Scaling
   - Fit Sheet on One Page
   - Fit All Columns on One Page
   - Fit All Rows on One Page

**CCC Exam Tip:** "Fit Sheet on One Page" is a scaling option available in the print settings. It shrinks the content so that everything fits on a single printed page.

---

## Print Preview

**Print Preview** shows you exactly how your document will look when printed, without wasting paper.

### Accessing Print Preview

- Press `Ctrl + P` — this opens the Print dialog with a preview on the right side.
- Or go to **File** > **Print**.

### Print Preview Features

- **Page navigation** — If your data spans multiple pages, use the arrows at the bottom to navigate between pages.
- **Zoom** — Click on the preview to zoom in and see details.
- **Orientation** — Switch between **Portrait** (tall) and **Landscape** (wide).
- **Margins** — Click **Show Margins** to see and adjust margins directly on the preview.
- **Paper size** — Choose A4, Letter, Legal, or other paper sizes.

---

## Headers and Footers

**Headers** appear at the top of every printed page, and **footers** appear at the bottom. They are useful for adding page numbers, dates, file names, and titles.

### Adding Headers and Footers

**Method 1 — Page Layout View:**
1. Go to **View** > **Page Layout**.
2. Click on the "Click to add header" area at the top of the page.
3. Type your header text.
4. Click on the "Click to add footer" area at the bottom.

**Method 2 — Insert Tab:**
1. Go to **Insert** > **Header & Footer**.
2. This switches to Page Layout view with the header selected.

**Method 3 — Page Setup Dialog:**
1. Go to **Page Layout** > click the dialog launcher (small arrow) in the Page Setup group.
2. Click the **Header/Footer** tab.
3. Click **Custom Header** or **Custom Footer**.

### Header/Footer Sections

Both headers and footers have three sections:
- **Left section** — Text appears at the left edge
- **Center section** — Text appears in the center
- **Right section** — Text appears at the right edge

### Common Header/Footer Elements

| Element | Button/Code | Description |
|---------|-------------|-------------|
| Page Number | `&[Page]` | Current page number |
| Total Pages | `&[Pages]` | Total number of pages |
| Date | `&[Date]` | Current date |
| Time | `&[Time]` | Current time |
| File Name | `&[File]` | Name of the workbook |
| Sheet Name | `&[Tab]` | Name of the worksheet |

**Example:** A common footer format is: `Page &[Page] of &[Pages]` — which prints as "Page 1 of 3".

**CCC Exam Tip:** Questions about headers and footers are common in the exam. Remember that headers/footers can include page numbers, dates, and file names using special codes.

---

## Freezing Panes

When you have a large dataset, scrolling down makes the header row disappear, making it hard to understand the data. **Freeze Panes** keeps certain rows or columns visible while you scroll.

### Freeze Top Row

1. Go to **View** tab.
2. Click **Freeze Panes** > **Freeze Top Row**.
3. Now when you scroll down, the first row (usually your headers) stays visible.

### Freeze First Column

1. Go to **View** > **Freeze Panes** > **Freeze First Column**.
2. Now when you scroll right, the first column stays visible.

### Freeze Both Rows and Columns

1. Click on the cell **below** the rows and **to the right** of the columns you want to freeze.
   - For example, click on cell B2 to freeze Row 1 and Column A.
2. Go to **View** > **Freeze Panes** > **Freeze Panes** (the first option).

### Unfreezing Panes

Go to **View** > **Freeze Panes** > **Unfreeze Panes**.

**CCC Exam Tip:** "Freeze Panes is used to keep rows or columns visible while scrolling" is a commonly tested statement. Remember that this feature is found under the **View** tab.

---

## Sorting Data

**Sorting** arranges your data in a specific order — either ascending (A to Z, smallest to largest) or descending (Z to A, largest to smallest).

### Quick Sort

1. Click on any cell in the column you want to sort by.
2. Go to the **Data** tab.
3. Click one of the sort buttons:
   - **A to Z** (ascending) — for text: alphabetical; for numbers: smallest to largest
   - **Z to A** (descending) — for text: reverse alphabetical; for numbers: largest to smallest

### Custom Sort (Multiple Levels)

When you want to sort by more than one column (for example, sort by City first, then by Name within each city):

1. Click anywhere in your data.
2. Go to **Data** > **Sort**.
3. In the Sort dialog:
   - Choose the first column to sort by (e.g., City).
   - Click **Add Level** to add a second sorting criterion (e.g., Name).
   - Set ascending or descending for each level.
4. Click **OK**.

### Example

Student data at TechPath Institute, Bhopal:

| Name | City | Marks |
|------|------|-------|
| Rahul | Delhi | 78 |
| Priya | Pune | 92 |
| Amit | Delhi | 65 |
| Sneha | Bhopal | 88 |
| Ananya | Pune | 74 |

Sorting by **Marks (Descending)** gives: Priya (92), Sneha (88), Rahul (78), Ananya (74), Amit (65).

**CCC Exam Tip:** Sorting options are found under the **Data** tab. Ascending means A to Z (or smallest to largest), and Descending means Z to A (or largest to smallest).

---

## Basic Filtering

**Filtering** allows you to temporarily hide rows that do not match certain criteria, so you can focus on the data you need.

### Applying a Filter

1. Click anywhere in your data.
2. Go to **Data** tab.
3. Click **Filter** (or press `Ctrl + Shift + L`).
4. Small **dropdown arrows** appear in the header row of each column.

### Using the Filter

1. Click the dropdown arrow in the column you want to filter.
2. Uncheck **Select All** to clear all selections.
3. Check only the values you want to see.
4. Click **OK**.

Only rows matching your selection will be visible. The other rows are hidden (not deleted).

### Clearing a Filter

- To clear a filter on one column: Click the dropdown arrow > **Clear Filter From [Column Name]**.
- To remove all filters: Go to **Data** > click **Filter** again to toggle it off.

### Number Filters

For numeric columns, click the dropdown arrow and choose **Number Filters** to access options like:
- Greater Than
- Less Than
- Between
- Top 10
- Above Average

### Example

Using the student data above, if you filter by City = "Pune", only Priya and Ananya's rows will be visible. All other rows are hidden but not deleted.

**CCC Exam Tip:** "Filtering hides data temporarily; it does not delete data" is an important concept. Also remember that the Filter option is in the **Data** tab, and the shortcut is `Ctrl + Shift + L`.

---

## Page Setup Options

The **Page Setup** dialog (Page Layout tab > click the dialog launcher) has several important settings:

| Tab | Options |
|-----|---------|
| **Page** | Orientation (Portrait/Landscape), Scaling, Paper size |
| **Margins** | Top, Bottom, Left, Right margins; Center on page |
| **Header/Footer** | Custom headers and footers |
| **Sheet** | Print area, Print titles (repeat rows/columns), Gridlines, Row & column headings |

### Print Titles (Repeating Headers on Every Page)

When printing a long list, you want the header row to appear on every page:

1. Go to **Page Layout** > **Print Titles**.
2. In the **Rows to repeat at top** field, click on the row(s) you want to repeat (e.g., $1:$1).
3. Click **OK**.

---

## Summary Table

| Concept | Key Point |
|---------|-----------|
| Print Area | Page Layout > Print Area > Set Print Area |
| Page Break Preview | View tab > Page Break Preview |
| Print Preview | Ctrl + P |
| Fit to Page | Page Layout > Scale to Fit |
| Headers/Footers | Insert > Header & Footer |
| Page number code | &[Page] |
| Freeze Panes | View > Freeze Panes |
| Freeze Top Row | View > Freeze Panes > Freeze Top Row |
| Unfreeze | View > Freeze Panes > Unfreeze Panes |
| Sort Ascending | Data tab > A to Z |
| Sort Descending | Data tab > Z to A |
| Filter | Data tab > Filter (Ctrl + Shift + L) |
| Filter hides data | Temporarily hidden, NOT deleted |
| Print Titles | Page Layout > Print Titles |
| Orientation | Portrait (tall) or Landscape (wide) |

---

*TechPath Institute — CCC Exam Preparation*

# Module 03 — MS Office — Quick Revision Notes

---

## Excel — Key Formulas
| Formula | What It Does | Example |
|---------|-------------|---------|
| `=SUM(A1:A10)` | Add values | Total sales |
| `=AVERAGE(A1:A10)` | Average | Average marks |
| `=COUNT(A1:A10)` | Count numbers | How many entries |
| `=COUNTA(A1:A10)` | Count non-empty | Filled cells |
| `=IF(A1>40,"Pass","Fail")` | Condition | Grade check |
| `=VLOOKUP(value,range,col,FALSE)` | Vertical lookup | Find employee details by ID |
| `=INDEX(range,MATCH(value,col,0))` | Better lookup | Flexible search (replaces VLOOKUP) |
| `=COUNTIF(range,criteria)` | Count matches | Count "Pass" results |
| `=SUMIF(range,criteria,sum_range)` | Sum matches | Total sales for specific region |
| `=CONCATENATE(A1," ",B1)` | Join text | Full name from first + last |
| `=TEXT(A1,"DD-MMM-YYYY")` | Format date | Display date as "23-Jul-2026" |
| `=LEFT(A1,3)` | First N chars | Area code from phone |
| `=TRIM(A1)` | Remove extra spaces | Clean data |

## Excel — Pivot Tables
1. Select data range → Insert → PivotTable
2. Drag fields: **Rows** (categories), **Values** (numbers to summarize), **Columns** (sub-groups), **Filters** (narrow down)
3. Change calculation: right-click value → Summarize by → Count/Average/Max etc.
4. Group dates: right-click date → Group → Months/Quarters

## Excel — Charts
| Data Type | Best Chart |
|-----------|-----------|
| Trends over time | Line chart |
| Compare categories | Bar/Column chart |
| Parts of whole | Pie chart (max 6 slices) |
| Two related values | Scatter plot |
| Multiple series | Combo chart |

## Word — Professional Documents
- **Heading styles**: Use Heading 1, 2, 3 → enables auto Table of Contents
- **Page setup**: Margins (Normal/Narrow), Orientation, Size
- **Headers/Footers**: Insert → Header → add page numbers
- **Section breaks**: Different headers/footers per section
- **Mail Merge**: Create template → connect data source → generate personalized letters
- **Track Changes**: Review → Track Changes → for collaborative editing

## PowerPoint — Presentation Rules
- **6x6 rule**: Max 6 bullets, max 6 words per bullet
- **One idea per slide**
- **Large fonts**: Title 36pt+, Body 24pt+
- **High contrast**: Dark text on light bg or vice versa
- **Minimal animation**: Fade/Appear only, no spinning/bouncing
- **Presenter View**: Shows notes + next slide (audience sees only current)

## Key Shortcuts
| App | Shortcut | Action |
|-----|----------|--------|
| Excel | Ctrl+; | Insert today's date |
| Excel | Alt+= | AutoSum |
| Excel | F4 | Toggle $ in formula |
| Excel | Ctrl+~ | Show formulas |
| Word | Ctrl+Enter | Page break |
| Word | Ctrl+Shift+L | Bullet list |
| All | Ctrl+S | Save |
| All | Ctrl+Z | Undo |
| All | Ctrl+B/I/U | Bold/Italic/Underline |

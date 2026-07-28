# Word — Professional Document Creation

**Module 03 — MS Office | Word Deep Dive**

---

## Why This Matters

> On your first day at work, nobody will ask you to type a paragraph. They'll say "Format this 40-page report by 3 PM" or "Create a letter with our company letterhead." This guide teaches you what offices actually need.

---

## Document Types You'll Create at Work

| Document | Who Asks | How Often |
|----------|----------|-----------|
| Business letters | Manager/HR | Weekly |
| Reports (with TOC) | Any department | Monthly |
| Meeting minutes | Admin/Secretary | After every meeting |
| Invoices/Quotations | Sales team | Daily |
| Offer letters/Contracts | HR | As needed |
| SOPs (Standard Operating Procedures) | Quality team | Quarterly |
| Certificates | Training/HR | After events |
| Memos/Circulars | Management | As needed |

---

## Professional Formatting — The Non-Negotiables

### Page Setup (First thing before typing)

Layout → Margins → Custom Margins:
- **Reports/Letters:** Top: 2.54cm, Bottom: 2.54cm, Left: 3.17cm, Right: 2.54cm
- **Printing both sides:** Mirror margins — Left (inner): 3.5cm for binding
- **Paper size:** A4 (always, unless told otherwise)

### Font Rules in Indian Offices

| Use | Font | Size |
|-----|------|------|
| Body text | Calibri, Arial, or Times New Roman | 11-12pt |
| Headings | Calibri, Arial | 14-16pt, Bold |
| Company name | As per brand guidelines | Varies |
| Tables | Same as body | 10-11pt |

**Never use:** Comic Sans, Papyrus, or decorative fonts in professional documents.

### Paragraph Spacing

- **Line spacing:** 1.15 or 1.5 (never single for reports)
- **After paragraph:** 6pt or 8pt (not a blank line)
- **Before heading:** 12pt
- **How:** Home → Paragraph → Spacing → Set Before/After

---

## Heading Styles — The Foundation of Professional Documents

### Why Use Styles (Not Manual Formatting)

| Manual formatting | Styles |
|-------------------|--------|
| Change every heading one by one | Change style → all headings update |
| No automatic Table of Contents | TOC generates from styles |
| No navigation pane | Click headings to jump |
| Inconsistent look | Always uniform |

### Setting Up Styles

1. Home → Styles panel
2. Right-click "Heading 1" → Modify
3. Set: Font, Size, Color, Spacing, Bold
4. Apply to all main headings

**Recommended hierarchy:**
```
Heading 1: 16pt, Bold, Dark Blue — Main sections
Heading 2: 14pt, Bold, Dark Gray — Sub-sections
Heading 3: 12pt, Bold, Black — Points within sub-sections
Normal: 11pt, Regular — Body text
```

### Navigation Pane

View → Check "Navigation Pane" — click any heading to jump there. This is how people navigate 50+ page documents.

---

## Table of Contents (TOC)

### Creating a TOC

1. Apply Heading 1, 2, 3 styles to your headings
2. Click where you want the TOC (usually page 2, after cover page)
3. References → Table of Contents → Automatic Table 1
4. TOC appears with page numbers!

### Updating TOC

When you add/remove content:
- Right-click TOC → Update Field
- Choose "Update page numbers only" or "Update entire table"

**Pro tip:** Always update TOC as the last step before printing/sharing.

---

## Headers, Footers & Page Numbers

### Adding Header/Footer

Insert → Header → Edit Header

**Common professional header:**
```
Left: Company Logo    |    Center: Document Title    |    Right: Date
```

**Common footer:**
```
Left: "Confidential"  |  Center: Page X of Y  |  Right: Version 1.0
```

### Page Numbers

- Insert → Page Number → Bottom of Page
- "Page X of Y": Insert → Page Number → Current Position → "Page X of Y"
- **Different first page:** Check "Different First Page" in Header & Footer tab (so cover page has no number)
- **Start numbering from page 2:** Page Number → Format → Start at: 0

### Section Breaks (Different Headers for Different Sections)

**Scenario:** Your report has a cover page (no header), table of contents (roman numerals), and main content (regular page numbers).

1. After cover page: Layout → Breaks → Next Page
2. After TOC: Layout → Breaks → Next Page
3. Click in Section 2 header → Unlink from Previous
4. Set roman numerals (i, ii, iii) for TOC section
5. Set regular numbers (1, 2, 3) for main section

---

## Mail Merge — Bulk Letters/Certificates

### What It Does

Write one letter → merge with a data list → generate 100 personalized letters automatically.

### When You'll Use It

- Sending offer letters to 50 new hires
- Creating certificates for 200 workshop attendees
- Sending payment reminders to 500 customers
- Creating ID cards with names from a list

### Step-by-Step

**Step 1:** Write the letter template with placeholders:

```
Dear <<Name>>,

We are pleased to inform you that you have been selected for the
position of <<Position>> in our <<Department>> department.

Your joining date is <<JoiningDate>> and your CTC will be
₹<<Salary>> per annum.

Please report to our <<Office>> office at 10:00 AM.

Regards,
HR Department
```

**Step 2:** Prepare data in Excel:

```
| Name    | Position     | Department | JoiningDate | Salary  | Office   |
|---------|-------------|------------|-------------|---------|----------|
| Rahul   | Developer   | IT         | 01-Feb-2026 | 5,00,000| Pune     |
| Priya   | Designer    | Marketing  | 15-Feb-2026 | 4,50,000| Mumbai   |
| Amit    | Analyst     | Finance    | 01-Mar-2026 | 4,00,000| Delhi    |
```

**Step 3:** Connect data
- Mailings → Start Mail Merge → Letters
- Mailings → Select Recipients → Use Existing List → Choose your Excel file
- Click in the letter → Mailings → Insert Merge Field → Select field

**Step 4:** Preview & Finish
- Mailings → Preview Results (see each letter)
- Mailings → Finish & Merge → Print or Edit Individual Documents

---

## Track Changes & Comments (Collaboration)

### Track Changes

Review → Track Changes → toggle ON

- Every edit shows in color with the editor's name
- Insertions = underlined color text
- Deletions = strikethrough color text

### Accepting/Rejecting Changes

- Right-click change → Accept or Reject
- Or: Review → Accept All / Reject All

### Comments

- Select text → Review → New Comment
- Reply to comments in the panel
- Resolve comments when addressed

**Workplace rule:** Never send a document to your manager with Track Changes still visible. Accept all → save → send.

---

## Practice Exercises

### Exercise 1: Business Report
Create a 10+ page report with:
- Cover page (use built-in cover page design)
- Table of Contents (auto-generated)
- 3 sections with Heading 1, 2, 3 styles
- At least one table formatted professionally
- Header: Company name + date, Footer: page numbers (Page X of Y)
- Different first page (cover page has no header/footer)

### Exercise 2: Official Letter
Create a formal business letter with:
- Company letterhead (logo, address, phone, email at top)
- Date, Reference number
- Recipient address
- Subject line (bold, underlined)
- Body with proper paragraphs
- Closing with signature block
- "CC:" and "Encl:" at bottom

### Exercise 3: Mail Merge Certificates
Create a certificate of completion template. Use mail merge with an Excel list of 10 names to generate 10 personalized certificates. Include:
- Certificate border/design
- Name placeholder (large, centered)
- Course name, date, and organization name
- Signature line

### Exercise 4: Meeting Minutes
Create a meeting minutes template with:
- Meeting title, date, time, venue
- Attendees list (present/absent)
- Agenda items (numbered)
- Discussion summary for each item
- Action items table (Task, Owner, Deadline, Status)
- Next meeting date

---

## Keyboard Shortcuts — Speed Matters at Work

| Shortcut | Action |
|----------|--------|
| Ctrl+B / I / U | Bold / Italic / Underline |
| Ctrl+E / L / R / J | Center / Left / Right / Justify |
| Ctrl+1 / 2 / 5 | Single / Double / 1.5 line spacing |
| Ctrl+Shift+> / < | Increase / Decrease font size |
| Ctrl+D | Font dialog |
| Ctrl+Enter | Page break |
| Ctrl+Shift+Enter | Column break |
| F7 | Spelling & Grammar check |
| Ctrl+Shift+C | Copy formatting |
| Ctrl+Shift+V | Paste formatting |
| Ctrl+K | Insert hyperlink |
| Alt+Shift+D | Insert date field |

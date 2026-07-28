# Advanced Word Features

**Module 03 — CCC Exam Preparation | Topic 6**

---

## Spelling and Grammar Check

MS Word can automatically check your spelling and grammar as you type, and you can also run a manual check.

### Automatic Checking (As You Type)

| Indicator | Meaning |
|-----------|---------|
| **Red wavy underline** | Spelling mistake (the word is not in Word's dictionary) |
| **Blue wavy underline** | Grammar mistake or contextual spelling error |

Right-click on the underlined word to see suggestions and choose the correct one.

### Manual Spelling and Grammar Check

- Press **F7** or go to **Review** tab → **Spelling & Grammar**
- Word checks the entire document from the cursor position to the end
- For each error, it shows suggestions — you can:
  - **Change** — accept the suggestion
  - **Ignore** — skip this occurrence
  - **Ignore All** — skip all occurrences of this word
  - **Add to Dictionary** — add the word to the custom dictionary so it is not flagged again

**CCC Exam Tip:** **F7** opens the Spelling and Grammar checker. Red underline = spelling error, Blue/Green underline = grammar error. The spelling check is found in the **Review** tab. These facts are frequently asked.

---

## AutoCorrect

**AutoCorrect** automatically fixes common typing mistakes as you type. For example:
- Typing "teh" is automatically corrected to "the"
- Typing "adn" is automatically corrected to "and"
- Typing "(c)" is automatically converted to the copyright symbol (c)

### Customizing AutoCorrect

1. Go to **File** → **Options** → **Proofing** → **AutoCorrect Options**
2. You can:
   - Add new entries (e.g., always replace "tp" with "TechPath Institute")
   - Delete entries you do not want
   - Enable/disable specific features

### AutoCorrect Features

| Feature | What It Does |
|---------|-------------|
| Correct TWo INitial CApitals | Fixes accidental double capitals |
| Capitalize first letter of sentences | Auto-capitalizes after a period |
| Capitalize names of days | Monday, Tuesday, etc. |
| Replace text as you type | Fixes common typos from the AutoCorrect list |

**CCC Exam Tip:** AutoCorrect is found under **File → Options → Proofing**. It automatically fixes common spelling mistakes while you type.

---

## Word Count

Word Count tells you how many words, characters, paragraphs, and lines are in your document.

### How to Check Word Count

**Method 1:** Look at the **Status Bar** at the bottom of the screen — it shows the word count by default.

**Method 2:** Go to **Review** tab → **Word Count** button.

**Method 3:** Press **Ctrl + Shift + G** (in some versions).

### Word Count Details

The Word Count dialog box shows:
- **Pages** — total number of pages
- **Words** — total word count
- **Characters (no spaces)** — count of letters/numbers without spaces
- **Characters (with spaces)** — count including spaces
- **Paragraphs** — number of paragraphs
- **Lines** — number of lines

To count words in a specific section, select the text first, then check Word Count.

**CCC Exam Tip:** Word count can be seen on the **Status Bar** or through **Review** tab → **Word Count**. This is a commonly asked feature.

---

## Mail Merge

**Mail Merge** is a powerful feature that lets you create multiple personalized copies of a document (like letters, labels, or envelopes) by combining a main document with a data source.

### When to Use Mail Merge

**Example:** Amit at TechPath Institute needs to send the same letter to 500 students, but each letter should have the student's own name, address, and course name. Instead of typing 500 separate letters, he uses Mail Merge.

### Components of Mail Merge

| Component | Description |
|-----------|-------------|
| **Main Document** | The letter template with placeholders (merge fields) |
| **Data Source** | A file containing the actual data (names, addresses, etc.) — can be an Excel file, Word table, or database |
| **Merge Fields** | Placeholders in the main document like <<First_Name>>, <<Address>>, <<Course>> |
| **Merged Document** | The final output — individual letters for each person |

### Steps for Mail Merge

1. **Start Mail Merge:** Go to **Mailings** tab → **Start Mail Merge** → choose the document type (Letters, E-mail Messages, Envelopes, Labels)
2. **Select Recipients:** Click **Select Recipients** → choose your data source:
   - **Type a New List** — create a new data list in Word
   - **Use an Existing List** — import from Excel, Access, or other file
   - **Choose from Outlook Contacts** — use your email contacts
3. **Insert Merge Fields:** Place the cursor where you want data to appear → click **Insert Merge Field** → choose the field (First_Name, Last_Name, Address, etc.)
4. **Preview Results:** Click **Preview Results** to see how the merged letters will look
5. **Finish & Merge:** Click **Finish & Merge** → choose:
   - **Edit Individual Documents** — creates a new document with all merged letters
   - **Print Documents** — sends directly to the printer
   - **Send E-mail Messages** — sends as emails

### Example Main Document

```
Dear <<First_Name>> <<Last_Name>>,

We are pleased to inform you that your admission to the <<Course>> 
program at TechPath Institute, <<City>> has been confirmed.

Your batch starts on <<Start_Date>>.

Regards,
TechPath Institute
```

### Example Data Source (Excel)

| First_Name | Last_Name | Course | City | Start_Date |
|------------|-----------|--------|------|------------|
| Rahul | Sharma | CCC | Bhopal | 01-Aug-2026 |
| Priya | Verma | ADCA | Delhi | 15-Aug-2026 |
| Amit | Patel | Tally | Pune | 01-Sep-2026 |

**CCC Exam Tip:** Mail Merge is found in the **Mailings** tab. The three components are: Main Document, Data Source, and Merge Fields. The data source is often an Excel file. This topic is important for the exam.

---

## Page Borders

Page borders add a decorative border around the entire page (not just a paragraph).

### How to Add Page Borders

1. Go to **Design** tab → **Page Background** group → click **Page Borders**
2. In the Borders and Shading dialog box, click the **Page Border** tab
3. Choose:
   - **Setting:** Box, Shadow, 3-D, or Custom
   - **Style:** Solid line, dashed, dotted, etc.
   - **Colour:** Choose a colour
   - **Width:** Thickness of the border
   - **Art:** Decorative borders (stars, hearts, trees, etc.)
4. Click OK

**CCC Exam Tip:** Page Borders are found in the **Design** tab (not the Home tab and not the Insert tab). The "Art" option in Page Borders gives decorative picture borders.

---

## Inserting Images and Clip Art

### Inserting a Picture from Your Computer

1. Place the cursor where you want the image
2. Go to **Insert** tab → **Pictures** → **This Device**
3. Browse to the image file and click **Insert**

### Inserting Online Pictures

1. Go to **Insert** tab → **Pictures** → **Online Pictures**
2. Search for an image using Bing search
3. Select the image and click **Insert**

### Inserting Shapes

1. Go to **Insert** tab → **Shapes**
2. Choose from lines, rectangles, circles, arrows, flowchart shapes, etc.
3. Draw the shape on the document

### Text Wrapping Options

After inserting an image, you need to set how text flows around it:

| Wrapping Style | Description |
|---------------|-------------|
| **In Line with Text** | Image sits on the same line as text (default) |
| **Square** | Text wraps around the image in a square shape |
| **Tight** | Text wraps closely following the image shape |
| **Through** | Text flows through transparent areas of the image |
| **Top and Bottom** | Text appears above and below the image only |
| **Behind Text** | Image goes behind the text |
| **In Front of Text** | Image covers the text |

To change wrapping: Click the image → click the **Layout Options** icon (small icon next to the image) → choose a wrapping style. Or go to **Format** tab → **Wrap Text**.

**CCC Exam Tip:** Images and shapes are inserted from the **Insert** tab. Know the different text wrapping options, especially **Square**, **Behind Text**, and **In Front of Text**. The default wrapping is **In Line with Text**.

---

## Watermarks

A **watermark** is a faint text or image that appears behind the document text on every page. Common uses include "CONFIDENTIAL", "DRAFT", or a company logo.

### How to Add a Watermark

1. Go to **Design** tab → **Page Background** group → click **Watermark**
2. Choose a preset watermark (CONFIDENTIAL, DO NOT COPY, DRAFT, etc.)
3. Or click **Custom Watermark** to create your own:
   - **Text watermark** — type your own text, choose font, size, colour, and layout
   - **Picture watermark** — use an image as the watermark

### Removing a Watermark

Go to **Design** tab → **Watermark** → **Remove Watermark**.

**CCC Exam Tip:** Watermarks are found in the **Design** tab under **Page Background**. They appear on every page behind the text. This is occasionally asked.

---

## Columns

The **Columns** feature lets you split your text into multiple columns, like a newspaper or magazine.

### How to Create Columns

1. Select the text you want to put in columns (or select nothing for the entire document)
2. Go to **Layout** tab → **Page Setup** group → click **Columns**
3. Choose: One, Two, Three, Left, Right, or **More Columns** for custom settings

### Column Options

In the "More Columns" dialog:
- **Number of columns** — choose how many
- **Width and spacing** — set each column's width and the gap between columns
- **Line between** — adds a vertical line between columns
- **Equal column width** — makes all columns the same width

To switch back to a single column, go to **Layout** → **Columns** → **One**.

**CCC Exam Tip:** Columns are found in the **Layout** tab (not Insert). The maximum number of columns depends on the page width, but commonly asked options are Two and Three columns.

---

## Saving in Different Formats

MS Word allows you to save documents in various formats:

| Format | Extension | Use |
|--------|-----------|-----|
| **Word Document** | .docx | Default format for Word 2007+ |
| **Word 97-2003** | .doc | For compatibility with older Word versions |
| **PDF** | .pdf | Universal format that preserves layout on all devices |
| **Rich Text Format** | .rtf | Compatible with most word processors |
| **Plain Text** | .txt | Only text, no formatting |
| **Web Page** | .html | For viewing in web browsers |
| **Template** | .dotx | Reusable document template |

### How to Save as PDF

1. Go to **File** → **Save As** (or press F12)
2. In the "Save as type" dropdown, select **PDF**
3. Choose a location and click **Save**

Alternatively: **File** → **Export** → **Create PDF/XPS Document**.

**CCC Exam Tip:** The default format is **.docx**. To save as PDF, use Save As and change the file type. The shortcut for Save As is **F12**. Knowing the difference between .doc and .docx is important — .docx is the newer XML-based format introduced in Word 2007.

---

## Summary — Key Points for CCC Exam

| Topic | Key Point |
|-------|-----------|
| Spell check | F7 or Review tab |
| Red underline | Spelling error |
| Blue underline | Grammar error |
| AutoCorrect | File → Options → Proofing |
| Word Count | Status Bar or Review tab |
| Mail Merge | Mailings tab — Main Document + Data Source + Merge Fields |
| Page Borders | Design tab → Page Borders |
| Insert Picture | Insert tab → Pictures |
| Default text wrapping | In Line with Text |
| Watermark | Design tab → Watermark |
| Columns | Layout tab → Columns |
| Default file format | .docx (Word 2007+) |
| Save As shortcut | F12 |
| Save as PDF | File → Save As → choose PDF, or File → Export |

---

*TechPath Institute — CCC Exam Preparation*

# File and Directory Management

**Module 02 — CCC Exam Preparation | Topic 3**

---

## What are Files and Folders?

### File
A **file** is a collection of related data stored on a computer with a unique name. Every document, photo, song, video, or program on your computer is a file.

**Examples:**
- `resume.docx` — a Word document file
- `photo.jpg` — an image file
- `song.mp3` — a music file
- `budget.xlsx` — an Excel spreadsheet file

Every file has two parts in its name:
- **File Name:** The name you give it (e.g., `resume`)
- **File Extension:** The part after the dot that tells the computer what type of file it is (e.g., `.docx`)

### Folder (Directory)
A **folder** (also called a **directory**) is a container that holds files and other folders. Folders help you organize your files, just like physical folders in an office filing cabinet.

**Example:** Amit creates a folder called "CCC Study" and keeps all his study notes, practice papers, and screenshots inside it.

A **subfolder** is a folder inside another folder. You can create multiple levels of subfolders to organize files neatly.

```
C:\Users\Amit\Documents\
├── CCC Study\
│   ├── Notes\
│   │   ├── module-01-notes.docx
│   │   └── module-02-notes.docx
│   ├── Practice Papers\
│   │   ├── paper-1.pdf
│   │   └── paper-2.pdf
│   └── Screenshots\
│       └── system-properties.png
├── Personal\
│   └── resume.docx
└── Office\
    └── salary-slip.pdf
```

**CCC Exam Tip:** A folder is also called a **directory**. A subfolder is a folder inside another folder.

---

## File Explorer (Windows Explorer)

**File Explorer** is the built-in Windows tool for browsing, managing, and organizing files and folders. In older Windows versions (XP, 7), it was called **Windows Explorer**.

### How to Open File Explorer:
- Press **Windows + E** (keyboard shortcut)
- Click the **File Explorer icon** on the taskbar (yellow folder icon)
- Right-click Start > File Explorer

### Parts of File Explorer:

| Part | Purpose |
|------|---------|
| **Navigation Pane (Left)** | Shows Quick Access, This PC, Desktop, Documents, Downloads, drives |
| **Address Bar (Top)** | Shows the current folder path (e.g., C:\Users\Amit\Documents) |
| **Search Box (Top Right)** | Search for files within the current folder |
| **Ribbon/Toolbar** | Buttons for common actions (Copy, Paste, Delete, New Folder) |
| **Content Area (Centre)** | Shows the files and folders in the current location |
| **Status Bar (Bottom)** | Shows number of items and selected items |
| **View Options** | Change how files appear (Large Icons, Details, List, etc.) |

**CCC Exam Tip:** The shortcut to open File Explorer is **Windows + E**. This is commonly asked.

---

## File and Folder Operations

### Creating a New Folder

**Method 1 — Using Right-Click:**
1. Open File Explorer and go to the location where you want the folder
2. Right-click on an empty area
3. Click **New > Folder**
4. Type the folder name and press **Enter**

**Method 2 — Using Keyboard:**
1. Go to the desired location in File Explorer
2. Press **Ctrl + Shift + N**
3. Type the folder name and press Enter

**Method 3 — Using Ribbon:**
1. In File Explorer, click **Home** tab
2. Click **New Folder** button

### Creating a New File

1. Right-click in an empty area
2. Click **New**
3. Choose the file type (Text Document, Word Document, Excel Spreadsheet, etc.)
4. Type the file name and press Enter

---

### Selecting Files and Folders

| Action | How to Do It |
|--------|-------------|
| Select one item | Click on it |
| Select multiple adjacent items | Click the first item, hold **Shift**, click the last item |
| Select multiple non-adjacent items | Hold **Ctrl** and click each item |
| Select all items | Press **Ctrl + A** |

---

### Copying Files and Folders

Copying creates a **duplicate** — the original stays in its place.

**Method 1 — Right-Click:**
1. Right-click the file/folder
2. Click **Copy**
3. Go to the destination folder
4. Right-click on empty area > **Paste**

**Method 2 — Keyboard Shortcuts:**
1. Select the file
2. Press **Ctrl + C** (Copy)
3. Go to destination
4. Press **Ctrl + V** (Paste)

**Method 3 — Drag and Drop:**
- Hold **Ctrl** and drag the file to the destination folder

---

### Moving Files and Folders

Moving **transfers** the file — it is removed from the original location.

**Method 1 — Right-Click:**
1. Right-click the file > **Cut**
2. Go to destination > Right-click > **Paste**

**Method 2 — Keyboard Shortcuts:**
1. Select the file
2. Press **Ctrl + X** (Cut)
3. Go to destination
4. Press **Ctrl + V** (Paste)

**Method 3 — Drag and Drop:**
- Simply drag the file to the destination (within the same drive, this moves; across drives, this copies)

**CCC Exam Tip:** 
- Ctrl + C = Copy, Ctrl + X = Cut, Ctrl + V = Paste
- Copy = original stays. Cut (Move) = original is removed.

---

### Renaming Files and Folders

1. Right-click the file/folder > **Rename**
2. Or select the file and press **F2**
3. Type the new name and press Enter

**Rules for file/folder names:**
- Cannot use these characters: `\ / : * ? " < > |`
- Cannot be longer than 255 characters
- Cannot use reserved names like CON, PRN, NUL

---

### Deleting Files and Folders

| Action | What Happens |
|--------|-------------|
| Press **Delete** key | Moves to Recycle Bin (can be recovered) |
| Press **Shift + Delete** | Permanently deletes (CANNOT be recovered) |
| Right-click > Delete | Moves to Recycle Bin |

**CCC Exam Tip:** **Shift + Delete** permanently deletes a file — it does NOT go to the Recycle Bin. This is a very commonly asked question.

---

## The Recycle Bin

The **Recycle Bin** is a special folder where deleted files are temporarily stored. It gives you a chance to recover accidentally deleted files.

### Key Facts:
- When you delete a file (using Delete key or right-click > Delete), it goes to the Recycle Bin
- Files in the Recycle Bin still take up disk space
- You can **Restore** a file from Recycle Bin — it goes back to its original location
- You can **Empty Recycle Bin** to permanently delete all files in it
- **Shift + Delete** bypasses the Recycle Bin entirely

### Recycle Bin Operations:

| Action | How |
|--------|-----|
| Open Recycle Bin | Double-click the Recycle Bin icon on Desktop |
| Restore a file | Right-click the file in Recycle Bin > **Restore** |
| Restore all files | Click **Restore all items** in the toolbar |
| Permanently delete one file | Right-click > Delete (from within Recycle Bin) |
| Empty Recycle Bin | Right-click Recycle Bin icon > **Empty Recycle Bin** |

**CCC Exam Tip:** The Recycle Bin stores deleted files temporarily. Shift + Delete skips the Recycle Bin and permanently deletes. Both concepts are frequently asked.

---

## File Paths

A **file path** is the complete address of a file on the computer. It tells the OS exactly where the file is stored.

### Types of Paths:

**Absolute Path (Full Path):**
The complete path from the drive letter to the file.
```
C:\Users\Priya\Documents\CCC Study\notes.docx
```

**Relative Path:**
The path relative to the current folder.
```
CCC Study\notes.docx    (relative to Documents folder)
```

### Understanding the Path:
```
C:\Users\Priya\Documents\CCC Study\notes.docx
│   │      │       │          │         │
│   │      │       │          │         └── File name
│   │      │       │          └── Subfolder
│   │      │       └── Folder
│   │      └── User folder
│   └── Users directory
└── Drive letter
```

The **backslash (\\)** separates folder names in Windows paths.

---

## Searching for Files

### Using Search Box in File Explorer:
1. Open File Explorer (Windows + E)
2. Navigate to the folder you want to search in
3. Click the **Search Box** (top right)
4. Type the file name or part of it
5. Results appear as you type

### Using Start Menu Search:
1. Press the **Windows key**
2. Start typing the file name
3. Results show files, folders, apps, and settings

### Search Tips:
- Use `*.docx` to find all Word documents
- Use `*.jpg` to find all images
- Use `*.pdf` to find all PDF files
- The `*` is a **wildcard** — it matches any characters

**CCC Exam Tip:** The wildcard character `*` matches any characters in a file search. `?` matches exactly one character.

---

## Summary

| Operation | Shortcut/Method |
|-----------|----------------|
| Open File Explorer | Windows + E |
| New Folder | Ctrl + Shift + N |
| Select All | Ctrl + A |
| Copy | Ctrl + C |
| Cut (Move) | Ctrl + X |
| Paste | Ctrl + V |
| Rename | F2 |
| Delete (to Recycle Bin) | Delete key |
| Permanent Delete | Shift + Delete |
| Undo | Ctrl + Z |
| Search | Type in Search Box |
| Wildcard | * (any characters), ? (one character) |

---

*TechPath Institute — CCC Exam Preparation*

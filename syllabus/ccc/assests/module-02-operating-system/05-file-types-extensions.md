# File Types and Extensions

**Module 02 — CCC Exam Preparation | Topic 5**

---

## What is a File Extension?

A **file extension** is the part of a file name that comes after the last dot (`.`). It tells the computer (and you) what type of file it is and which program should open it.

**Example:** `resume.docx`
- `resume` = file name
- `.docx` = file extension (tells us it is a Microsoft Word document)

When you double-click a file, Windows looks at the extension to decide which program to use. For example:
- `.docx` files open in Microsoft Word
- `.jpg` files open in the Photos app
- `.mp3` files open in a music player

**CCC Exam Tip:** File extensions tell the computer what type the file is and which program should open it. This concept is frequently tested.

---

## Common File Extensions

### Document Files

| Extension | Full Form / Type | Opens With |
|-----------|-----------------|-----------|
| **.txt** | Plain Text File | Notepad |
| **.doc** | Word Document (old format) | Microsoft Word |
| **.docx** | Word Document (new format) | Microsoft Word |
| **.pdf** | Portable Document Format | Adobe Reader, Chrome |
| **.rtf** | Rich Text Format | WordPad, MS Word |
| **.odt** | Open Document Text | LibreOffice Writer |
| **.xls** | Excel Spreadsheet (old) | Microsoft Excel |
| **.xlsx** | Excel Spreadsheet (new) | Microsoft Excel |
| **.ppt** | PowerPoint (old) | Microsoft PowerPoint |
| **.pptx** | PowerPoint (new) | Microsoft PowerPoint |
| **.csv** | Comma Separated Values | Excel, Notepad |

**CCC Exam Tip:** 
- `.docx` = Word, `.xlsx` = Excel, `.pptx` = PowerPoint
- The "x" at the end indicates the newer XML-based format
- `.pdf` = Portable Document Format (can be viewed on any device without the original software)

---

### Image Files

| Extension | Full Form / Type | Details |
|-----------|-----------------|---------|
| **.jpg / .jpeg** | Joint Photographic Experts Group | Most common photo format, compressed |
| **.png** | Portable Network Graphics | Supports transparency, used for logos |
| **.gif** | Graphics Interchange Format | Supports animation (moving images) |
| **.bmp** | Bitmap Image | Uncompressed, large file size |
| **.svg** | Scalable Vector Graphics | Vector image, does not blur when resized |
| **.ico** | Icon File | Used for desktop icons |
| **.tiff / .tif** | Tagged Image File Format | High quality, used in printing |

**CCC Exam Tip:** JPEG is the most common image format. PNG supports transparency. GIF supports animation.

---

### Audio Files

| Extension | Full Form / Type | Details |
|-----------|-----------------|---------|
| **.mp3** | MPEG Audio Layer 3 | Most popular music format, compressed |
| **.wav** | Waveform Audio | Uncompressed, high quality, large size |
| **.aac** | Advanced Audio Coding | Better quality than MP3 at same size |
| **.wma** | Windows Media Audio | Microsoft's audio format |
| **.flac** | Free Lossless Audio Codec | High quality, compressed without loss |
| **.ogg** | Ogg Vorbis | Open source audio format |

**CCC Exam Tip:** MP3 is the most widely used audio format. It uses compression to reduce file size.

---

### Video Files

| Extension | Full Form / Type | Details |
|-----------|-----------------|---------|
| **.mp4** | MPEG-4 Video | Most common video format |
| **.avi** | Audio Video Interleave | Older format by Microsoft |
| **.mkv** | Matroska Video | Supports multiple audio/subtitle tracks |
| **.mov** | QuickTime Movie | Apple's video format |
| **.wmv** | Windows Media Video | Microsoft's video format |
| **.flv** | Flash Video | Used for online streaming (older) |
| **.3gp** | 3GPP Multimedia | Used on older mobile phones |

**CCC Exam Tip:** MP4 is the most common video format used today.

---

### Program and System Files

| Extension | Type | Details |
|-----------|------|---------|
| **.exe** | Executable File | A program that runs when double-clicked |
| **.msi** | Microsoft Installer | Installer package for Windows programs |
| **.bat** | Batch File | Script with DOS/command prompt commands |
| **.dll** | Dynamic Link Library | Shared code used by multiple programs |
| **.sys** | System File | Critical Windows system file |
| **.ini** | Initialization File | Configuration/settings file |
| **.tmp** | Temporary File | Temporary data, can be safely deleted |
| **.log** | Log File | Records events and errors |

**CCC Exam Tip:** `.exe` = Executable file (a program you can run). This is one of the most commonly asked extensions.

---

### Compressed (Archived) Files

| Extension | Type | Details |
|-----------|------|---------|
| **.zip** | ZIP Archive | Most common compressed format |
| **.rar** | RAR Archive | Better compression than ZIP |
| **.7z** | 7-Zip Archive | Open source, excellent compression |
| **.tar** | Tape Archive | Used in Linux systems |
| **.gz** | Gzip | Compressed file used in Linux |

**How compression works:** Compression reduces the file size so it takes less storage space and can be sent faster over email or the internet. You need to **extract** (unzip) the files before using them.

**Example:** Sneha has 50 photos (200 MB total). She compresses them into one ZIP file (80 MB) and emails it to her friend in Pune. The friend extracts the ZIP to see all 50 photos.

---

### Web Files

| Extension | Type | Details |
|-----------|------|---------|
| **.html / .htm** | HyperText Markup Language | Web page file |
| **.css** | Cascading Style Sheet | Styles for web pages |
| **.js** | JavaScript | Programming for web pages |
| **.php** | PHP Script | Server-side web programming |
| **.xml** | Extensible Markup Language | Data storage and transfer |
| **.json** | JavaScript Object Notation | Data format used in web apps |

---

### Database Files

| Extension | Type | Details |
|-----------|------|---------|
| **.mdb** | Microsoft Access Database (old) | Access 2003 and earlier |
| **.accdb** | Access Database (new) | Access 2007 and later |
| **.sql** | SQL Query File | Database queries |
| **.db** | Database File | Generic database file |

---

## File Associations

A **file association** links a file extension to a specific program. This determines which program opens when you double-click a file.

### How to Change File Associations:

**Method 1 — Open With:**
1. Right-click the file
2. Click **Open with**
3. Choose a program from the list
4. Check "Always use this app to open this file type" if you want to change the default permanently

**Method 2 — Settings:**
1. Open Settings > Apps > Default Apps
2. Scroll down and click **Choose default apps by file type**
3. Find the extension and select the program you want

**Example:** By default, `.pdf` files might open in Microsoft Edge. You can change the association so they always open in Adobe Acrobat Reader instead.

---

## Showing and Hiding File Extensions

By default, Windows hides file extensions. This can be confusing — you might not know if a file is `photo.jpg` or `photo.png`.

### How to Show File Extensions:
1. Open File Explorer (Windows + E)
2. Click the **View** tab (or View menu)
3. Check **File name extensions**

Or:
1. Open File Explorer > View > Options > Change folder and search options
2. Go to the **View** tab
3. Uncheck "Hide extensions for known file types"
4. Click OK

**Why it matters:** Some viruses disguise themselves. A file named `photo.jpg.exe` appears as `photo.jpg` when extensions are hidden — but it is actually a dangerous executable program!

---

## Hidden Files and Folders

Windows hides certain system files and folders to protect them from accidental deletion.

### How to Show Hidden Files:
1. Open File Explorer
2. Click the **View** tab
3. Check **Hidden items**

Hidden files and folders appear slightly transparent/faded compared to normal files.

---

## File Properties

Every file has properties that give information about it.

### How to View Properties:
- Right-click the file > **Properties**
- Or select the file and press **Alt + Enter**

### Properties Information:

| Tab | Shows |
|-----|-------|
| **General** | File name, type, location, size, created/modified/accessed dates |
| **Security** | Who has permission to read, write, or modify the file |
| **Details** | Detailed metadata (for photos: camera, resolution, date taken) |
| **Previous Versions** | Earlier saved versions of the file (if System Restore is enabled) |

### File Attributes:

| Attribute | Meaning |
|-----------|---------|
| **Read-only** | File can be read but not modified |
| **Hidden** | File is hidden from normal view |
| **Archive** | File is marked for backup |
| **System** | Critical system file — should not be modified |

---

## Summary

| Category | Key Extensions |
|----------|---------------|
| Documents | .txt, .docx, .xlsx, .pptx, .pdf |
| Images | .jpg, .png, .gif, .bmp |
| Audio | .mp3, .wav, .aac |
| Video | .mp4, .avi, .mkv |
| Programs | .exe, .msi, .bat, .dll |
| Compressed | .zip, .rar, .7z |
| Web | .html, .css, .js |

**Key Exam Points:**
- `.exe` = executable (program) file
- `.pdf` = Portable Document Format
- `.docx` = Word document
- `.xlsx` = Excel spreadsheet
- `.pptx` = PowerPoint presentation
- `.jpg` = most common image format
- `.mp3` = most common audio format
- `.mp4` = most common video format
- `.zip` = compressed archive

---

*TechPath Institute — CCC Exam Preparation*

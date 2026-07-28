# Hardware and Software

**Module 01 — CCC Exam Preparation | Topic 3**

---

## What is Hardware?

**Hardware** refers to all the physical parts of a computer that you can **see and touch**. If you can hold it in your hand, it is hardware.

**Examples of Hardware:**
- Monitor, Keyboard, Mouse, Printer, Speaker
- CPU, Motherboard, RAM stick, Hard Disk
- Pen Drive, CD/DVD, Scanner, Webcam

Think of hardware as the body of a computer — without hardware, there is nothing to run programs on.

---

## What is Software?

**Software** is a set of programs, instructions, and data that tells the hardware **what to do**. You cannot see or touch software — it exists as code stored in memory.

**Examples of Software:**
- Windows, Android, Linux (operating systems)
- MS Word, Excel, Tally, Chrome (applications)
- Games, media players, calculators

Think of software as the mind or soul of a computer — without software, the hardware is just a useless collection of parts.

**CCC Exam Tip:** Hardware = physical parts (touchable). Software = programs and instructions (not touchable). This basic difference is frequently asked.

---

## Hardware vs Software

| Feature | Hardware | Software |
|---------|----------|----------|
| Nature | Physical (tangible) | Logical (intangible) |
| Can you touch it? | Yes | No |
| Wear and tear | Gets damaged over time | Does not wear out (can become outdated) |
| Example | Keyboard, Monitor, CPU | Windows, MS Word, Chrome |
| Development | Manufactured in factories | Written by programmers |
| Transfer | Physically moved | Copied, downloaded, installed |
| Dependency | Needs software to function | Needs hardware to run |
| Cost | One-time purchase | May need licence renewal |

---

## Types of Software

Software is divided into two main categories:

### 1. System Software

System software controls and manages the computer hardware. It acts as a bridge between the user and the hardware. The user does not directly interact with most system software.

#### (a) Operating System (OS)
The most important system software. It manages all hardware and software resources.
- **Examples:** Windows 10, Windows 11, Linux, macOS, Android, iOS
- **Functions:** Memory management, file management, process management, device management, security
- Covered in detail in Module 2

#### (b) Language Translators
These convert programs written by humans into machine language (binary) that the computer can understand.

| Translator | Input | How It Works |
|-----------|-------|-------------|
| **Assembler** | Assembly language | Converts assembly code to machine code |
| **Compiler** | High-level language | Translates the entire program at once, then runs it |
| **Interpreter** | High-level language | Translates and runs the program line by line |

**CCC Exam Tip:** Compiler translates the whole program at once. Interpreter translates line by line. This difference is frequently asked.

#### (c) Utility Programs
Small programs that perform specific maintenance tasks.
- **Antivirus:** Protects against viruses and malware (e.g., Quick Heal, Norton)
- **Disk Defragmenter:** Reorganizes files on disk for faster access
- **File Compression:** Reduces file size (e.g., WinZip, WinRAR, 7-Zip)
- **Backup Utility:** Creates copies of data for safety
- **Disk Cleanup:** Removes temporary and unnecessary files

### 2. Application Software

Application software is designed for specific tasks that users want to perform. Users directly interact with application software.

#### (a) General Purpose Application Software
Used by many people for everyday tasks.

| Software | Purpose | Examples |
|----------|---------|---------|
| Word Processor | Create and edit documents | MS Word, LibreOffice Writer, Google Docs |
| Spreadsheet | Work with numbers, tables, charts | MS Excel, LibreOffice Calc, Google Sheets |
| Presentation | Create slide shows | MS PowerPoint, LibreOffice Impress |
| Web Browser | Access websites on the internet | Google Chrome, Firefox, Edge |
| Email Client | Send and receive emails | Gmail, Outlook, Thunderbird |
| Media Player | Play audio and video | VLC, Windows Media Player |

#### (b) Special Purpose Application Software
Designed for specific professional tasks.

| Software | Purpose | Used By |
|----------|---------|---------|
| **Tally** | Accounting and GST | Accountants, businesses across India |
| **AutoCAD** | Engineering design | Engineers, architects |
| **Photoshop** | Image editing | Designers, photographers |
| **Hospital Management System** | Patient records, billing | Hospitals like AIIMS, Apollo |
| **Railway Reservation System** | Train ticket booking | IRCTC |

#### (c) Customized (Tailor-made) Software
Software built specifically for one organization.
- **Example:** The software used by Indian Railways for IRCTC reservation is custom-built for their specific needs.

---

## System Software vs Application Software

| Feature | System Software | Application Software |
|---------|----------------|---------------------|
| Purpose | Manages hardware and system | Performs user tasks |
| User interaction | Mostly runs in background | User interacts directly |
| Installation | Installed first (before apps) | Installed after OS |
| Examples | Windows, Linux, Antivirus | MS Word, Chrome, Tally |
| Dependency | Can run without app software | Cannot run without system software |
| Developed by | System programmers | Application developers |

**CCC Exam Tip:** The CCC exam often asks you to classify software. Remember: OS and translators are system software. Word, Excel, PowerPoint, and Tally are application software.

---

## Programming Languages

A **programming language** is a set of rules and instructions used to write programs that tell the computer what to do.

### Types of Programming Languages

#### 1. Machine Language (First Generation)
- The only language the computer directly understands
- Written entirely in **binary** (0s and 1s)
- Extremely difficult for humans to write and understand
- Very fast execution — no translation needed
- Machine-specific — a program for one type of CPU may not work on another
- **Example:** `10110000 01100001`

#### 2. Assembly Language (Second Generation)
- Uses **mnemonics** (short codes) instead of binary
- Easier than machine language but still complex
- Needs an **assembler** to convert to machine language
- **Example:** `MOV A, 61` (means: move the value 61 to register A)
- Also called **low-level language**

#### 3. High-Level Language (Third Generation and above)
- Written in **English-like words** — easy to learn and use
- Needs a **compiler** or **interpreter** to convert to machine language
- Portable — can run on different types of computers
- **Examples:** C, C++, Java, Python, BASIC, COBOL, FORTRAN

| Language | Year | Used For |
|----------|------|----------|
| FORTRAN | 1957 | Scientific calculations |
| COBOL | 1959 | Business and banking |
| BASIC | 1964 | Teaching programming to beginners |
| C | 1972 | System programming, OS development |
| C++ | 1983 | Game development, system software |
| Java | 1995 | Web applications, Android apps |
| Python | 1991 | AI, data science, web development, automation |

**CCC Exam Tip:** Know the full forms:
- BASIC = Beginner's All-purpose Symbolic Instruction Code
- COBOL = Common Business Oriented Language
- FORTRAN = Formula Translation

---

## Firmware

**Firmware** is software that is permanently stored on hardware (usually in ROM). It provides low-level control for the hardware.

- **Example:** The BIOS in your computer is firmware — it runs when you turn on the PC and tells it how to start up.
- Firmware sits between hardware and software — it is software stored on hardware.

---

## Open Source vs Proprietary Software

| Feature | Open Source | Proprietary |
|---------|-----------|-------------|
| Source code | Available to everyone | Hidden, not shared |
| Cost | Usually free | Usually paid (licence fee) |
| Modification | Anyone can modify | Only the company can modify |
| Examples | Linux, LibreOffice, Firefox, VLC | Windows, MS Office, Adobe Photoshop |
| Support | Community support | Official company support |

**CCC Exam Tip:** Linux and LibreOffice are open source. Windows and MS Office are proprietary. This is frequently asked.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Hardware | Physical parts — touchable |
| Software | Programs and instructions — not touchable |
| System Software | Manages hardware (OS, translators, utilities) |
| Application Software | User tasks (Word, Excel, Tally) |
| Machine Language | Binary (0s and 1s) — computer understands directly |
| Assembly Language | Mnemonics — needs assembler |
| High-Level Language | English-like — needs compiler or interpreter |
| Compiler | Translates entire program at once |
| Interpreter | Translates line by line |
| Open Source | Free, source code available (Linux, LibreOffice) |
| Proprietary | Paid, source code hidden (Windows, MS Office) |

---

*TechPath Institute — CCC Exam Preparation*

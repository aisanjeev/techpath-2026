# Module 02: Introduction to GUI Based Operating System — Comprehensive Notes

**CCC Exam Preparation | TechPath Institute**

---

## 1. What is an Operating System?

An **Operating System (OS)** is system software that manages all hardware and software resources of a computer. It acts as an interface between the user and the hardware.

**Key Functions:**
- **Process Management** — runs and manages multiple programs
- **Memory Management** — allocates and frees RAM
- **File Management** — organizes files and folders on storage
- **Device Management** — controls input/output devices via drivers
- **Security** — user accounts, passwords, firewall
- **User Interface** — GUI (visual) or CLI (text commands)

---

## 2. Types of Operating Systems

| Type | Description | Example |
|------|-------------|---------|
| Batch OS | Processes jobs in batches, no user interaction | Early mainframes |
| Time-Sharing / Multitasking | Multiple programs share CPU time | Windows 10/11 |
| Real-Time OS (RTOS) | Immediate response, no delays | ATM, missile systems |
| Distributed OS | Multiple networked computers as one system | Google's servers |
| Network OS | Server manages shared resources for clients | Windows Server |
| Mobile OS | Designed for phones/tablets | Android, iOS |

---

## 3. Popular Operating Systems

| OS | Developer | Type | Cost |
|----|-----------|------|------|
| Windows 10/11 | Microsoft | Desktop | Paid (proprietary) |
| Linux (Ubuntu) | Community | Desktop/Server | Free (open source) |
| macOS | Apple | Desktop | Paid (Apple only) |
| Android | Google | Mobile | Free (open source) |
| iOS | Apple | Mobile | Paid (iPhone only) |
| BOSS | C-DAC (India) | Desktop | Free (Indian Linux) |

**Exam Key Points:**
- Windows = proprietary (paid), most used desktop OS
- Linux = open source (free), most secure, used for servers
- BOSS = Bharat Operating System Solutions, Indian Linux by C-DAC
- Android = most used mobile OS, open source, by Google

---

## 4. GUI (Graphical User Interface)

**GUI** = Graphical User Interface — users interact using visual elements.

**WIMP** = Windows, Icons, Menus, Pointer — the four elements of a GUI.

Before GUI, users used **CLI (Command Line Interface)** — typing text commands in DOS or Terminal.

### GUI vs CLI

| Feature | GUI | CLI |
|---------|-----|-----|
| Interaction | Visual (mouse clicks) | Text (type commands) |
| Easy to use? | Yes, beginner-friendly | No, needs command knowledge |
| Speed | Slower (more processing) | Faster (direct commands) |
| Example | Windows Desktop | Command Prompt, Linux Terminal |

---

## 5. Windows Desktop Components

| Component | Description |
|-----------|------------|
| **Desktop** | Main screen with wallpaper and icons |
| **Taskbar** | Bottom bar with Start, running apps, system tray |
| **Start Menu** | Access all apps, settings, power options (press Windows key) |
| **System Tray** | Right side of taskbar — clock, volume, network, battery |
| **Icons** | Small pictures representing files, folders, programs |
| **Recycle Bin** | Stores deleted files temporarily |

### Taskbar Parts:
Start Button > Search > Task View > Pinned Apps > Running Apps > System Tray > Show Desktop

### Window Controls:
- **Minimize (—)** = hides window, program continues running
- **Maximize (□)** = full screen
- **Restore (⧉)** = returns from full screen to previous size
- **Close (X)** = exits the program

---

## 6. File and Folder Management

### Key Operations:

| Operation | Shortcut | Notes |
|-----------|----------|-------|
| Open File Explorer | **Windows + E** | Main file management tool |
| New Folder | **Ctrl + Shift + N** | Creates new folder in current location |
| Copy | **Ctrl + C** | Copies — original stays |
| Cut (Move) | **Ctrl + X** | Moves — original is removed |
| Paste | **Ctrl + V** | Places copied/cut item |
| Select All | **Ctrl + A** | Selects everything |
| Rename | **F2** | Rename selected file/folder |
| Delete | **Delete** | Moves to Recycle Bin |
| Permanent Delete | **Shift + Delete** | Permanently deletes (NO Recycle Bin) |
| Undo | **Ctrl + Z** | Undoes last action |
| Properties | **Alt + Enter** | Shows file/folder details |

### Recycle Bin:
- Deleted files go to Recycle Bin first (temporary storage)
- **Restore** = put the file back to its original location
- **Empty Recycle Bin** = permanently delete all files in it
- **Shift + Delete** bypasses Recycle Bin — CANNOT be recovered
- Files in Recycle Bin still occupy disk space

### File Paths:
- **Absolute path:** `C:\Users\Priya\Documents\notes.docx` (complete path from drive)
- **Relative path:** `Documents\notes.docx` (relative to current location)
- Backslash `\` separates folders in Windows

### Wildcards in Search:
- `*` = matches any number of characters (e.g., `*.pdf` finds all PDFs)
- `?` = matches exactly one character (e.g., `file?.txt` finds file1.txt, file2.txt)

---

## 7. Control Panel and Settings

### Control Panel Categories:
| Category | Controls |
|----------|---------|
| System and Security | Firewall, Updates, Power Options |
| User Accounts | Passwords, account types |
| Network and Internet | Wi-Fi, sharing |
| Hardware and Sound | Printers, sound, devices |
| Programs | Install/uninstall software |
| Appearance | Wallpaper, screen resolution, fonts |
| Clock and Region | Date/time, language |
| Ease of Access | Accessibility features |

### Date/Time:
- Right-click clock > Adjust date/time
- India's time zone: **IST = UTC + 5:30**

### Display:
- Right-click Desktop > Display settings
- Screen resolution: 1920x1080 (Full HD) is most common
- Wallpaper: Right-click Desktop > Personalize

### Task Manager:
- **Ctrl + Shift + Esc** = open Task Manager directly (fastest)
- **Ctrl + Alt + Delete** = security screen with Task Manager option
- Use to: end frozen programs, check CPU/RAM usage, disable startup programs

### Power Options:
| Option | What Happens |
|--------|-------------|
| Shut Down | Computer turns off completely |
| Restart | Turns off and on again |
| Sleep | Low power, RAM stays active, quick wake |
| Hibernate | Saves to disk, no power used, slower wake |
| Lock (Win+L) | Locks screen, requires password |

---

## 8. File Types and Extensions

### Document Extensions:
| Extension | Application |
|-----------|------------|
| .txt | Notepad (plain text) |
| .docx | Microsoft Word |
| .xlsx | Microsoft Excel |
| .pptx | Microsoft PowerPoint |
| .pdf | Adobe Reader / any PDF viewer |
| .csv | Excel / Notepad (data) |

### Media Extensions:
| Extension | Type | Most Common? |
|-----------|------|-------------|
| .jpg/.jpeg | Image | Yes (photos) |
| .png | Image | Yes (logos, web) |
| .gif | Image | Yes (animations) |
| .mp3 | Audio | Yes (music) |
| .wav | Audio | High quality |
| .mp4 | Video | Yes (videos) |
| .avi | Video | Older format |

### System Extensions:
| Extension | Type |
|-----------|------|
| .exe | Executable program |
| .dll | Shared code library |
| .sys | System file |
| .bat | Batch script |
| .msi | Installer package |
| .tmp | Temporary file |

### Compressed:
| Extension | Type |
|-----------|------|
| .zip | Most common archive |
| .rar | Better compression |
| .7z | Open source archive |

### File Associations:
- Links a file extension to a program
- Change via: Right-click > Open with > Choose default app
- Or: Settings > Apps > Default Apps

---

## 9. Windows Keyboard Shortcuts — Complete Reference

### General Shortcuts:
| Shortcut | Action |
|----------|--------|
| Ctrl + C | Copy |
| Ctrl + X | Cut |
| Ctrl + V | Paste |
| Ctrl + Z | Undo |
| Ctrl + Y | Redo |
| Ctrl + A | Select All |
| Ctrl + S | Save |
| Ctrl + P | Print |
| Ctrl + F | Find |
| Ctrl + N | New |
| F2 | Rename |
| F5 | Refresh |
| Alt + F4 | Close window |
| Alt + Tab | Switch windows |

### Windows Key Shortcuts:
| Shortcut | Action |
|----------|--------|
| Windows | Open Start Menu |
| Windows + E | Open File Explorer |
| Windows + D | Show Desktop (minimize all) |
| Windows + L | Lock screen |
| Windows + R | Open Run dialog |
| Windows + I | Open Settings |
| Windows + S | Open Search |
| Windows + Tab | Task View |
| Windows + Left/Right | Snap window left/right |
| Windows + Up | Maximize window |
| Windows + Down | Minimize window |

### System Shortcuts:
| Shortcut | Action |
|----------|--------|
| Ctrl + Shift + Esc | Open Task Manager |
| Ctrl + Alt + Delete | Security screen |
| Print Screen | Screenshot (full screen) |
| Alt + Print Screen | Screenshot (active window only) |
| Windows + Shift + S | Snipping Tool screenshot |

---

## 10. CCC Exam — Most Frequently Asked Questions from Module 02

1. What is the full form of GUI? — **Graphical User Interface**
2. What does WIMP stand for? — **Windows, Icons, Menus, Pointer**
3. What is the function of Recycle Bin? — **Temporarily stores deleted files**
4. What does Shift + Delete do? — **Permanently deletes (bypasses Recycle Bin)**
5. What is the shortcut to open Task Manager? — **Ctrl + Shift + Esc**
6. What is the file extension for an executable file? — **.exe**
7. What is the shortcut to open File Explorer? — **Windows + E**
8. What is a .pdf file? — **Portable Document Format**
9. What is the shortcut to lock the computer? — **Windows + L**
10. Linux is open source or proprietary? — **Open source (free)**
11. BOSS Linux was developed by? — **C-DAC (India)**
12. What is the difference between Sleep and Hibernate? — **Sleep = RAM stays powered; Hibernate = saves to disk**
13. Alt + F4 does what? — **Closes the current window**
14. Control Panel is used for? — **Changing system settings**
15. What does F2 do? — **Rename a selected file or folder**

---

*TechPath Institute — CCC Exam Preparation*

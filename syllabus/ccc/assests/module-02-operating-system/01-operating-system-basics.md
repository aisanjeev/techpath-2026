# Operating System Basics

**Module 02 — CCC Exam Preparation | Topic 1**

---

## What is an Operating System?

An **Operating System (OS)** is system software that manages all the hardware and software resources of a computer. It acts as a bridge (interface) between the user and the computer hardware.

Without an operating system, a computer is just a collection of useless electronic parts. The OS makes it possible for you to use the computer — open programs, save files, print documents, and connect to the internet.

**In simple words:** The OS is the manager of the computer. Just like a school principal manages teachers, students, and classrooms, the OS manages the CPU, memory, storage, and programs.

**CCC Exam Tip:** "An Operating System is system software that manages hardware and software resources" — this definition is frequently asked.

---

## Functions of an Operating System

The OS performs many important functions. Here are the key ones:

### 1. Process Management
- The OS manages all running programs (called **processes**)
- It decides which program gets CPU time and for how long
- It can run multiple programs at the same time (multitasking)
- **Example:** You can listen to music on Gaana while typing in Word — the OS manages both simultaneously

### 2. Memory Management
- The OS manages RAM (primary memory)
- It allocates memory to programs when they start
- It frees memory when programs are closed
- It ensures one program does not access another program's memory

### 3. File Management
- The OS organizes files and folders on your storage devices
- It handles creating, reading, writing, deleting, and searching files
- It manages the file system (like NTFS on Windows, ext4 on Linux)
- **Example:** When you save a document in the Documents folder, the OS decides where to physically store it on the hard disk

### 4. Device Management
- The OS manages all input/output devices (keyboard, mouse, printer, etc.)
- It uses **device drivers** — small programs that tell the OS how to communicate with each device
- **Example:** When you plug in a new printer, Windows installs its driver so the OS knows how to send print commands to it

### 5. Security and Access Control
- The OS protects your data with user accounts and passwords
- It controls who can access which files and programs
- It provides firewalls and Windows Defender for protection against viruses
- **Example:** On a shared computer at a cyber cafe in Bhopal, each user has a separate login — the OS keeps their files separate

### 6. User Interface
- The OS provides a way for users to interact with the computer
- **GUI (Graphical User Interface):** Visual interface with windows, icons, menus (Windows, macOS)
- **CLI (Command Line Interface):** Text-based interface where you type commands (Command Prompt, Linux Terminal)

**CCC Exam Tip:** GUI stands for **Graphical User Interface**. This full form is asked very frequently.

---

## Types of Operating Systems

### 1. Batch Operating System
- Jobs are collected in a batch and processed one after another
- No user interaction during processing
- Used in early computers (1950s–1960s)
- **Example:** Processing a batch of electricity bills at once

### 2. Time-Sharing (Multitasking) Operating System
- Multiple users or programs share the CPU time
- The OS switches between tasks so fast that it feels like all programs are running simultaneously
- **Example:** Windows 10/11 — you can run Chrome, Word, and Tally at the same time

### 3. Real-Time Operating System (RTOS)
- Responds to input immediately with guaranteed response time
- No delays allowed — used in critical applications
- **Examples:** Missile guidance systems, medical equipment, ATM machines, traffic signal controllers
- Two types:
  - **Hard RTOS:** Strict time limits — even 1 ms delay is not acceptable (missile systems)
  - **Soft RTOS:** Small delays are acceptable (video streaming, online gaming)

### 4. Distributed Operating System
- Manages multiple computers connected through a network as a single system
- Workload is distributed across machines
- **Example:** Google's search engine runs on thousands of computers worldwide working together

### 5. Network Operating System
- Manages a network of computers (server-client model)
- The server provides shared resources (files, printers) to client computers
- **Examples:** Windows Server, Linux Server
- **Used in:** Office LANs, school computer labs

### 6. Mobile Operating System
- Designed for smartphones and tablets
- Optimized for touch screens and battery life
- **Examples:** Android (by Google), iOS (by Apple)

**CCC Exam Tip:** Know the types — Batch, Time-sharing, Real-time, Distributed, Network, and Mobile. The exam may ask you to match types with their descriptions.

---

## Popular Operating Systems

### Windows (by Microsoft)

| Version | Year | Key Feature |
|---------|------|-------------|
| Windows 95 | 1995 | Start Menu introduced |
| Windows 98 | 1998 | Internet Explorer integrated |
| Windows XP | 2001 | Most popular, stable, user-friendly |
| Windows 7 | 2009 | Improved UI, very popular in India |
| Windows 8 | 2012 | Tile-based Start Screen |
| Windows 10 | 2015 | Cortana, Edge browser, widely used |
| Windows 11 | 2021 | Centered taskbar, rounded corners |

- **Most used desktop OS in the world**
- **GUI-based** — uses windows, icons, menus, and pointer (WIMP)
- **Proprietary software** — requires a paid licence
- Used by most offices, schools, and homes in India

### Linux

- **Open source** — free to download, use, and modify
- Created by **Linus Torvalds** in 1991
- More secure than Windows — rarely gets viruses
- Popular distributions: Ubuntu, Fedora, CentOS, Linux Mint
- Used for web servers, supercomputers, and by programmers
- **BOSS (Bharat Operating System Solutions)** — Indian Linux distribution by C-DAC

### macOS (by Apple)

- OS for Apple Mac computers
- Known for security, smooth design, and reliability
- **Proprietary** — only runs on Apple hardware
- Popular among designers, video editors, and creative professionals

### Android (by Google)

- Most popular **mobile OS** in the world
- **Open source** — based on Linux kernel
- Used in smartphones by Samsung, Xiaomi, OnePlus, Vivo, Oppo, etc.
- App store: Google Play Store

### iOS (by Apple)

- Mobile OS for iPhones and iPads
- **Proprietary** — only runs on Apple devices
- App store: Apple App Store

---

## Windows vs Linux Comparison

| Feature | Windows | Linux |
|---------|---------|-------|
| Developer | Microsoft | Community (Linus Torvalds) |
| Cost | Paid (licence required) | Free (open source) |
| Source Code | Closed (proprietary) | Open (anyone can view/modify) |
| GUI | Yes (default) | Yes (optional, can use CLI) |
| Security | Vulnerable to viruses | Very secure |
| User-Friendly | Very easy for beginners | Steeper learning curve |
| Used For | Offices, homes, schools | Servers, programming, hacking |
| File System | NTFS, FAT32 | ext4, ext3 |
| Popular In | Most PCs and offices in India | Web servers, supercomputers |
| Software | MS Office, Tally, most commercial software | LibreOffice, GIMP, open source software |

**CCC Exam Tip:** Windows is proprietary (paid), Linux is open source (free). BOSS is India's Linux distribution. These comparisons are commonly asked.

---

## Key Terms

| Term | Meaning |
|------|---------|
| **Booting** | The process of starting a computer and loading the OS |
| **Cold Boot** | Starting a computer that is completely off (pressing power button) |
| **Warm Boot** | Restarting a computer that is already on (Ctrl+Alt+Delete or Restart) |
| **Kernel** | The core part of the OS that directly communicates with hardware |
| **Shell** | The interface between the user and the kernel (GUI or CLI) |
| **Driver** | Software that helps the OS communicate with hardware devices |
| **BIOS** | Basic Input Output System — firmware that starts the boot process |
| **Multitasking** | Running multiple programs at the same time |
| **Multiprocessing** | Using multiple CPUs to process tasks |
| **Multi-user** | Multiple users can use the computer simultaneously |

---

## Summary

| Concept | Key Point |
|---------|-----------|
| OS Definition | System software that manages hardware and software |
| Main Functions | Process, Memory, File, Device management + Security + UI |
| GUI | Graphical User Interface (windows, icons, menus) |
| CLI | Command Line Interface (text commands) |
| Windows | Proprietary, paid, most popular desktop OS |
| Linux | Open source, free, secure, used for servers |
| BOSS | Bharat Operating System Solutions (Indian Linux by C-DAC) |
| Android | Most popular mobile OS, open source, by Google |
| Booting | Process of starting computer and loading OS |
| Kernel | Core part of OS that talks to hardware |

---

*TechPath Institute — CCC Exam Preparation*

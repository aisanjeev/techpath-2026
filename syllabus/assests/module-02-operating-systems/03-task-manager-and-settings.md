# Troubleshooting, Software & Environment — The IT Professional's Toolkit

**Module 02 — Operating Systems | Topic 3 — What IT Support Actually Does**

---

## Why This Matters

> Day one at your job. A colleague says "My computer is slow, can you check?" Another says "I installed something and now nothing works." The IT manager asks "Can you set up the dev environment on the new machine?" THIS is the chapter that prepares you for those moments.

---

## Part 1: Task Manager — Your Diagnostic Tool

### How to Open

- `Ctrl + Shift + Esc` (direct — memorize this!)
- Or: Right-click Taskbar → Task Manager

### Understanding Each Tab

> 🖼️ **IMAGE:** Windows 11 Task Manager showing the Processes tab — columns visible: Name, Status, CPU %, Memory, Disk, Network — with Chrome highlighted showing high memory usage (1.2 GB across multiple processes), and the Performance tab graphs shown in the background
> `task-manager-processes-tab.png`

#### Processes Tab (Most Important)

| Column | What It Tells You | Healthy Range |
|--------|------------------|---------------|
| **CPU** | How much processor power is being used | 0-30% idle, 50-90% under load |
| **Memory** | RAM usage | Should not stay at 90%+ |
| **Disk** | Read/write activity | 0% when idle, spikes during file operations |
| **Network** | Data being sent/received | Low unless downloading/streaming |
| **GPU** | Graphics card usage | Low unless gaming/video editing |

**Color coding:** Higher usage = more intense color. If a row is bright red → that app is using too many resources.

#### Performance Tab

Shows real-time graphs for CPU, RAM, Disk, Network, and GPU.

| What to Look For | What It Means |
|-----------------|---------------|
| CPU stuck at 100% | A program is hogging the processor (or malware) |
| Memory near 100% | Too many apps open, or a memory leak |
| Disk at 100% for minutes | Windows Update running, antivirus scanning, or failing hard drive |
| Network with constant activity you didn't start | Could be background updates — or malware phoning home |

**Useful info at the bottom of Performance tab:**
- **Up time:** How long since last restart (restart if 7+ days)
- **Speed, Cores, Logical processors:** CPU specs
- **Slots used / Available:** RAM stick info

#### Startup Tab

Shows apps that run automatically when you turn on your PC.

| Column | Meaning |
|--------|---------|
| **Status** | Enabled (runs at startup) or Disabled |
| **Startup Impact** | High / Medium / Low / Not measured |
| **Publisher** | Who made the app |

**Startup Impact guide:**

| Impact | Action |
|--------|--------|
| **High** | Disable unless critical (antivirus, cloud sync) |
| **Medium** | Disable if you don't use it daily |
| **Low** | Keep or disable — won't make much difference |

> 🖼️ **IMAGE:** Task Manager Startup tab showing 8 apps — Spotify (High impact, Disabled with green status), Microsoft Teams (High impact, Enabled), Discord (Medium impact, Disabled), OneDrive (Low impact, Enabled), Realtek Audio (Low impact, Enabled) — with annotations showing which ones to disable
> `task-manager-startup-guide.png`

---

## Part 2: The Top 10 Problems (And How to Fix Them)

### Problem 1: "My Computer is Slow"

```
Step 1: Open Task Manager (Ctrl+Shift+Esc)
        → Check which app uses most CPU/RAM
        → Close or End Task if not needed

Step 2: Check Startup apps
        → Disable unnecessary ones
        → Restart to apply

Step 3: Check Storage
        → Win+I → System → Storage
        → Run "Temporary files" cleanup
        → If drive is 90%+ full → delete/move files

Step 4: Check for malware
        → Win+I → Privacy & Security → Windows Security
        → Run Quick scan

Step 5: Restart the computer
        → Yes, seriously. "Have you tried restarting?"
           is the #1 fix because it clears RAM, stops
           stuck processes, and applies pending updates.
```

### Problem 2: "An App is Frozen / Not Responding"

```
Step 1: Wait 30 seconds (it might recover)

Step 2: If still frozen:
        → Ctrl+Shift+Esc → find the app
        → Status will show "Not Responding"
        → Right-click → End Task

Step 3: If the entire screen is frozen:
        → Ctrl+Alt+Delete → Task Manager
        → End the problematic app

Step 4: If NOTHING works:
        → Hold power button for 10 seconds (force shutdown)
        → This is a last resort — you may lose unsaved work
```

### Problem 3: "No Sound"

```
Step 1: Check the obvious
        → Is volume muted? Click speaker icon in taskbar
        → Are headphones plugged in? (might route sound there)

Step 2: Right-click speaker icon → Sound settings
        → Check Output device — is the correct one selected?
        → Play test sound

Step 3: Device Manager → Sound devices
        → Yellow triangle? → Right-click → Update driver

Step 4: Services
        → Win+R → type services.msc → Enter
        → Find "Windows Audio" → should be Running
        → If stopped → Right-click → Start
```

### Problem 4: "Can't Connect to WiFi"

```
Step 1: Toggle WiFi off/on (click WiFi icon in taskbar)

Step 2: Forget the network and reconnect
        → Settings → Network → WiFi → Manage known networks
        → Click network → Forget → Reconnect with password

Step 3: Network troubleshooter
        → Settings → Network → Network troubleshooter

Step 4: DNS flush
        → Open CMD as admin
        → ipconfig /flushdns
        → ipconfig /release
        → ipconfig /renew

Step 5: Reset network adapter
        → Settings → Network → Advanced → Network reset
        → This reinstalls all network adapters (restart required)
```

### Problem 5: "Printer Not Working"

```
Step 1: Is it turned on and connected? (USB or WiFi)
Step 2: Settings → Bluetooth & Devices → Printers
        → Is your printer listed? Set as default?
Step 3: Try: Remove printer → Add printer again
Step 4: Download latest driver from manufacturer's website
```

### Problem 6: "Low Disk Space Warning"

```
Quick fixes:
→ Settings → System → Storage → Temporary files → Clean up
→ Empty Recycle Bin (right-click → Empty)
→ Clean Downloads folder (move old files to external drive)
→ Uninstall unused apps (Settings → Apps → Installed apps)

Find what's using space:
→ Settings → System → Storage → Show more categories
→ Or use free tool: WinDirStat (shows visual map of disk usage)
```

### Problem 7: "Windows Update Stuck"

```
Step 1: Wait. Some updates take 30-60 minutes.
Step 2: Restart and try again
Step 3: Run troubleshooter:
        Settings → System → Troubleshoot → Windows Update
Step 4: Manually reset update components:
        CMD (admin) →
        net stop wuauserv
        net stop bits
        net start wuauserv
        net start bits
```

### Problem 8: "I Deleted Something Important"

```
Step 1: Check Recycle Bin (it's probably there)
        → Double-click Recycle Bin on desktop
        → Right-click file → Restore

Step 2: If you emptied Recycle Bin
        → STOP using the drive immediately
        → Downloaded files might be recoverable with
           free tools like Recuva
        → But no guarantee — this is why backups matter

Step 3: Check if the file is in cloud sync
        → OneDrive, Google Drive have version history
```

### Problem 9: "Blue Screen of Death (BSOD)"

```
What happened: Windows crashed so badly it had to restart.

Step 1: Note the error code (e.g., IRQL_NOT_LESS_OR_EQUAL)
Step 2: Restart — if it boots normally, it might be a one-time issue
Step 3: If it happens repeatedly:
        → Check RAM: Windows Memory Diagnostic (search it)
        → Check drivers: Did you install something new?
        → Check disk: chkdsk C: /f (CMD admin)
        → Check system files: sfc /scannow (CMD admin)
Step 4: Google the error code — Microsoft has specific fixes
```

### Problem 10: "I Think I Have a Virus"

```
Signs of malware:
→ Random popups/ads even when browser is closed
→ Computer very slow for no reason
→ Programs you didn't install appearing
→ Browser homepage changed
→ Antivirus turned off and can't turn back on

What to do:
Step 1: Disconnect from internet (pull WiFi)
Step 2: Run Windows Security full scan:
        Win+I → Privacy & Security → Windows Security → Full scan
Step 3: Boot into Safe Mode for deeper scan:
        Settings → System → Recovery → Advanced startup → Restart now
        → Troubleshoot → Startup Settings → Safe Mode with Networking
Step 4: If Windows Security doesn't catch it:
        → Download Malwarebytes (free) from another PC on a USB
        → Run it in Safe Mode
```

---

## Part 3: Software Management

### Installing Software — The Right Way

| Method | How | Best For | Risk Level |
|--------|-----|---------|------------|
| **Microsoft Store** | Search in Store app | Common apps (Spotify, Netflix, WhatsApp) | Lowest (curated) |
| **Official website** | Download from developer's website | VS Code, Chrome, Python, Git | Low (if correct URL) |
| **winget** (command line) | `winget install AppName` | Developers who want speed | Low |
| **Chocolatey** | `choco install AppName` | Developers (advanced) | Low |
| **Random website** | Download from any site | Nothing | **HIGH — malware risk!** |

**NEVER install software from:**
- Random download sites (softonic, download.com, etc.)
- Email attachments
- Pop-ups saying "Your PC is infected, download this"
- Torrent/pirated software

**Developer's Setup — Install These Using winget:**

```cmd
# Open CMD or PowerShell

# Code editor
winget install Microsoft.VisualStudioCode

# Web browsers
winget install Google.Chrome

# Version control
winget install Git.Git

# Python
winget install Python.Python.3.12

# Node.js
winget install OpenJS.NodeJS.LTS

# Database tool
winget install DBBrowserForSQLite.DBBrowserForSQLite

# Terminal
winget install Microsoft.WindowsTerminal
```

**Search for available apps:**
```cmd
winget search "python"
```

### Uninstalling Software — Properly

```
Method 1 (Recommended):
Settings → Apps → Installed apps → Find app → ⋮ → Uninstall

Method 2 (Command line):
winget uninstall "App Name"

Method 3 (Old way):
Control Panel → Programs → Uninstall a program

WRONG WAY:
❌ Never just delete the app's folder — leaves behind
   registry entries, config files, and startup entries
```

### Portable Apps — No Installation Needed

Some apps work without installing — just download, extract, and run.

| Portable App | What It Does | Why Use Portable? |
|-------------|-------------|-------------------|
| **7-Zip Portable** | Extract/create archives | Use on any PC without admin rights |
| **Notepad++ Portable** | Code editor | Run from USB at work/college |
| **FileZilla Portable** | FTP client | Transfer files to server |
| **GIMP Portable** | Image editor | Edit images without installation |

**Where:** portableapps.com — all free, all safe

---

## Part 4: Environment Variables — What Developers Must Know

### What Are Environment Variables?

They're **system-wide settings** stored as name-value pairs that programs can read.

```
PATH = C:\Python312;C:\Windows\System32;C:\Program Files\Git\cmd
```

When you type `python` in CMD, Windows checks each folder in `PATH` to find python.exe. If it's not in any PATH folder → "command not found."

### The PATH Variable (Most Important)

**Problem:** You install Python, but typing `python` in CMD says "not recognized."

**Fix:** Python's folder isn't in PATH. Add it:

```
1. Win + S → search "Environment Variables"
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "System variables" → find "Path" → click Edit
5. Click "New" → paste the path to Python:
   C:\Users\YourName\AppData\Local\Programs\Python\Python312
6. Also add the Scripts folder:
   C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts
7. Click OK → OK → OK
8. RESTART CMD (old windows don't see the change)
9. Type: python --version → should work now!
```

> 🖼️ **IMAGE:** Windows Environment Variables dialog showing the Path variable editor — a list of folder paths with New/Edit/Delete/Move Up/Move Down buttons — Python paths highlighted with arrows showing where to add them
> `environment-variables-path.png`

### Common Environment Variables

| Variable | Purpose | Example Value |
|----------|---------|--------------|
| `PATH` | Folders to search for commands | `C:\Python312;C:\Git\cmd;...` |
| `USERPROFILE` | Your home folder | `C:\Users\Rahul` |
| `TEMP` / `TMP` | Temporary file storage | `C:\Users\Rahul\AppData\Local\Temp` |
| `JAVA_HOME` | Where Java is installed | `C:\Program Files\Java\jdk-21` |
| `PYTHONPATH` | Extra folders Python should look in | `C:\projects\mylib` |

### Checking Variables from CMD

```cmd
# See all environment variables
set

# See a specific one
echo %PATH%
echo %USERPROFILE%

# Temporarily set one (only for this CMD session)
set MY_VAR=hello
echo %MY_VAR%

# Set permanently from command line (admin)
setx PATH "%PATH%;C:\new\folder"
```

### In Linux

```bash
# See all
env

# See one
echo $PATH
echo $HOME

# Set temporarily
export MY_VAR="hello"

# Set permanently — add to ~/.bashrc
echo 'export MY_VAR="hello"' >> ~/.bashrc
source ~/.bashrc
```

---

## Part 5: Windows Services

### What Are Services?

Services are programs that run in the background without a window. They start automatically and handle system functions.

**How to see them:** Win + R → `services.msc` → Enter

### Important Services

| Service | What It Does | Should Be Running? |
|---------|-------------|-------------------|
| **Windows Update** | Downloads and installs updates | Yes (usually) |
| **Windows Audio** | Makes sound work | Yes |
| **DHCP Client** | Gets IP address from router | Yes |
| **DNS Client** | Resolves domain names to IPs | Yes |
| **Print Spooler** | Manages print jobs | Yes (if you print) |
| **Windows Defender** | Antivirus protection | Yes |
| **Windows Search** | Indexes files for fast search | Yes (uses disk when indexing) |

**When services matter:** If sound stops working → check Windows Audio service. If search is slow → check Windows Search service. If printing fails → restart Print Spooler.

---

## Part 6: Registry Basics (Know But Don't Touch)

### What Is the Registry?

The Windows Registry is a **database** that stores all system and app settings. Everything from your wallpaper choice to driver configurations lives here.

**How to open:** Win + R → `regedit` → Enter

```
HKEY_LOCAL_MACHINE (HKLM)  → System-wide settings
├── HARDWARE               → Detected hardware
├── SOFTWARE               → Installed software settings
└── SYSTEM                 → Boot and system config

HKEY_CURRENT_USER (HKCU)   → Your personal settings
├── SOFTWARE               → Your app preferences
├── Control Panel          → Your personalization settings
└── Environment            → Your environment variables
```

**Rules:**
1. NEVER edit the registry unless you know exactly what you're changing
2. ALWAYS create a backup before editing: File → Export → Save
3. Most things you'd change in the registry have a GUI equivalent in Settings
4. If a tutorial says "edit registry to fix X" — search for a Settings-based fix first

---

## Practice Exercises

### Exercise 1: Diagnose Your PC
1. Open Task Manager → how many processes are running?
2. Which app uses the most RAM right now?
3. How many startup apps are enabled? Disable the unnecessary ones
4. Check Performance tab → what's your CPU usage idle?
5. How long has your PC been running without restart? (Up time in Performance → CPU)

### Exercise 2: Software Setup
1. Open CMD and try running: `python --version`
2. If it says "not recognized" → find where Python is installed → add it to PATH
3. Install Git using winget: `winget install Git.Git`
4. Verify: close CMD, open new CMD, type `git --version`
5. Install VS Code using winget: `winget install Microsoft.VisualStudioCode`

### Exercise 3: Troubleshooting Practice
On your PC or a friend's PC, investigate:
1. What's using the most disk space? (Settings → Storage)
2. How much temporary file space can you reclaim?
3. Is Windows Defender running? (Windows Security → check status)
4. Are all drivers working? (Device Manager → look for yellow triangles)
5. What's your current IP address? (CMD → ipconfig)

### Exercise 4: Environment Variables
1. Open CMD → type `echo %PATH%` → copy the output somewhere
2. Add a new folder to PATH (Settings → Environment Variables)
3. Create a custom variable: `MY_NAME=YourName`
4. Open a NEW CMD → type `echo %MY_NAME%`
5. If using WSL: `echo $PATH` → notice how it includes Windows paths too!

---

## Interview Questions

| Question | Key Answer |
|----------|-----------|
| "How would you troubleshoot a slow PC?" | Check Task Manager for CPU/RAM hogs, disable startup apps, clear temp files, check for malware, restart. Follow a systematic approach, not random fixes. |
| "What is a process vs a service?" | Process = program running with a window (Chrome, Word). Service = background program with no window (Windows Update, Audio). Services run automatically. |
| "What are environment variables?" | System-wide key-value settings programs can read. PATH tells the OS where to find executable files. Essential for development tools like Python, Git, Node.js. |
| "What's the difference between killing and ending a task?" | End Task = asks the app to close gracefully (save data first). End Process = force kills immediately (may lose unsaved data). Always try End Task first. |
| "How do you install software on Windows vs Linux?" | Windows: .exe installer, Microsoft Store, or winget command. Linux: apt/snap package manager from terminal (e.g., `sudo apt install git`). |
| "What is the Windows Registry?" | A hierarchical database storing all system and application settings. HKLM for system-wide, HKCU for current user. Edit with extreme caution. |

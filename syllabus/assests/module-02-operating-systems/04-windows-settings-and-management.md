# Windows Settings & System Management

**Module 02 — Operating Systems | Practical Windows Administration**

---

## Why This Matters

> Every IT job — even web development — requires managing your Windows installation. HR won't fix your display settings. The network admin won't connect your Bluetooth. You need to handle these yourself, fast.

---

## Windows Settings — Complete Guide

### How to Open Settings

- **Win + I** (keyboard shortcut — learn this!)
- Or: Start menu → Settings gear icon

> 🖼️ **IMAGE:** Windows 11 Settings home screen with all category icons visible (System, Bluetooth, Network, Personalization, Apps, Accounts, etc.), with arrows pointing to the 6 most important categories
> `windows-settings-home.png`

---

### System Settings

| Setting | Where | When You Need It |
|---------|-------|-----------------|
| **Display resolution** | System → Display | External monitor, text too small/big |
| **Multiple displays** | System → Display → Multiple displays | Connecting projector/second monitor |
| **Scale** | System → Display → Scale | Text too small on high-res screen |
| **Night light** | System → Display → Night light | Reduce eye strain at night |
| **Sound output** | System → Sound → Output | Switch between speaker/headphones |
| **Notifications** | System → Notifications | Turn off annoying popups |
| **Power & battery** | System → Power & battery | Laptop battery saving |
| **Storage** | System → Storage | Free up disk space |

#### Connecting a Second Monitor/Projector

1. Connect HDMI/VGA cable
2. **Win + P** → Choose mode:

| Mode | What It Does | When to Use |
|------|-------------|-------------|
| **PC screen only** | Only your laptop screen | Default |
| **Duplicate** | Same on both screens | Presentations |
| **Extend** | Two separate screens | Coding, multitasking |
| **Second screen only** | Only external display | When docked at desk |

> 🖼️ **IMAGE:** The Win+P projection mode popup in Windows 11 showing all 4 options with icons — PC screen only, Duplicate, Extend, Second screen only
> `windows-projection-modes.png`

---

### Network & Internet

#### Connecting to WiFi

Settings → Network & Internet → WiFi → Show available networks

#### Checking Your IP Address

```
Method 1: Settings → Network → WiFi → Properties → IPv4 address
Method 2: Open CMD → type: ipconfig
```

> 🖼️ **IMAGE:** Command Prompt showing output of `ipconfig` command with arrows highlighting IPv4 Address, Subnet Mask, and Default Gateway
> `cmd-ipconfig-output.png`

#### Network Troubleshooting Steps

```
1. Check WiFi icon in taskbar → Connected?
2. Open browser → Can you load google.com?
3. Run: Settings → Network → Network troubleshooter
4. Try: Turn WiFi off → wait 10 sec → turn on
5. Try: Restart your router (unplug → wait 30 sec → plug back)
6. Open CMD → ping 8.8.8.8 (if this works, it's DNS)
7. Open CMD → ipconfig /flushdns
8. Still broken → ipconfig /release → ipconfig /renew
```

---

### Apps & Features

**Uninstalling apps:**
Settings → Apps → Installed apps → Find app → Click ⋮ → Uninstall

**Default apps:**
Settings → Apps → Default apps
- Set default browser (Chrome instead of Edge)
- Set default PDF reader
- Set default email app

**Startup apps:**
Settings → Apps → Startup
- **Disable** apps you don't need at boot (Spotify, Discord, OneDrive if not used)
- This is the #1 fix for slow startup!

> 🖼️ **IMAGE:** Windows Startup apps settings page showing a list of apps with toggle switches — some turned ON (highlighted green), some OFF — with a callout saying "Turn off apps you don't use → faster boot"
> `windows-startup-apps.png`

---

### Accounts & Security

#### Creating a Local Account

Settings → Accounts → Other users → Add account

**When to use:**
- Setting up a computer for someone else
- Creating a guest account
- IT admin setting up shared machines

#### Windows Hello (Biometric Login)

Settings → Accounts → Sign-in options
- **PIN** (faster than password)
- **Fingerprint** (if laptop has scanner)
- **Face recognition** (if laptop has IR camera)

---

## File Management — Organize Like a Professional

### Folder Structure Every IT Professional Uses

```
C:\Users\YourName\
├── Desktop\          ← Keep CLEAN (max 5-10 items)
├── Documents\
│   ├── Work\
│   │   ├── Company Name\
│   │   │   ├── Reports\
│   │   │   ├── Presentations\
│   │   │   └── Data\
│   │   └── Projects\
│   ├── Personal\
│   └── Certifications\
├── Downloads\        ← Clean this weekly!
├── Pictures\
│   ├── Screenshots\
│   └── Projects\
└── Videos\
```

> 🖼️ **IMAGE:** File Explorer showing a clean, well-organized folder structure matching the above — left pane showing folder tree, right pane showing contents of "Work" folder with subfolders
> `organized-folder-structure.png`

### File Explorer Shortcuts

| Shortcut | Action |
|----------|--------|
| Win + E | Open File Explorer |
| Alt + D | Go to address bar |
| Ctrl + N | New window |
| Ctrl + W | Close window |
| Ctrl + Shift + N | New folder |
| F2 | Rename selected file |
| Alt + ← | Go back |
| Alt + → | Go forward |
| Ctrl + F | Search in current folder |

### File Extensions You Must Know

| Extension | Type | Opens With |
|-----------|------|-----------|
| .docx | Word document | MS Word |
| .xlsx | Excel spreadsheet | MS Excel |
| .pptx | PowerPoint | MS PowerPoint |
| .pdf | Portable document | Any PDF reader |
| .txt | Plain text | Notepad |
| .jpg/.png | Image | Photos app |
| .mp4/.mkv | Video | Media player |
| .zip/.rar | Compressed archive | 7-Zip, WinRAR |
| .exe | Program installer | Windows |
| .py | Python script | Python |
| .html | Web page | Browser |
| .csv | Comma-separated data | Excel, Notepad |
| .json | Data format | Notepad, VS Code |

**Show file extensions (IMPORTANT for IT work):**
File Explorer → View → Show → File name extensions ✅

> 🖼️ **IMAGE:** File Explorer View menu with "File name extensions" checkbox highlighted — showing the difference between files with extensions hidden (just "report") vs shown ("report.docx")
> `show-file-extensions.png`

---

## Control Panel vs Settings

| Feature | Settings (New) | Control Panel (Old) |
|---------|---------------|-------------------|
| Interface | Modern, touch-friendly | Classic, detailed |
| How to open | Win + I | Search "Control Panel" |
| Use when | Most tasks | Advanced tasks |
| Future | Microsoft is moving here | Being phased out |

**Still need Control Panel for:**
- Advanced network settings
- Programs and Features (detailed uninstall)
- Device Manager (detailed)
- System Properties (advanced)
- User Account Control (UAC) settings

---

## Device Manager — Hardware Control Center

**Open:** Right-click Start button → Device Manager (or Win + X → M)

> 🖼️ **IMAGE:** Device Manager window showing expanded categories — Display adapters (showing GPU), Network adapters (showing WiFi and Ethernet), and one device with a yellow warning triangle icon
> `device-manager-annotated.png`

| Category | What's Inside |
|----------|--------------|
| Display adapters | Graphics card (Intel/NVIDIA/AMD) |
| Network adapters | WiFi card, Ethernet, Bluetooth |
| Disk drives | HDD, SSD |
| Sound, video, game | Audio devices |
| USB controllers | All USB ports |
| Keyboards/Mice | Input devices |

**Yellow triangle ⚠️** = Driver problem
- Right-click → Update driver
- Or: Right-click → Uninstall device → Restart (Windows reinstalls)

---

## Command Prompt (CMD) — Essential Commands

Open: Search "cmd" or **Win + R → type cmd → Enter**

### Must-Know Commands

| Command | What It Does | Example |
|---------|-------------|---------|
| `ipconfig` | Show IP address | `ipconfig` |
| `ping` | Test if a server is reachable | `ping google.com` |
| `tracert` | Show route to a server | `tracert google.com` |
| `nslookup` | Find IP of a domain | `nslookup techpath.biz` |
| `netstat` | Show active connections | `netstat -an` |
| `systeminfo` | Full system details | `systeminfo` |
| `tasklist` | List running processes | `tasklist` |
| `taskkill` | Kill a process | `taskkill /f /im chrome.exe` |
| `sfc /scannow` | Scan & fix system files | `sfc /scannow` (admin) |
| `chkdsk` | Check disk for errors | `chkdsk C: /f` (admin) |
| `shutdown /s /t 0` | Shutdown immediately | `shutdown /s /t 0` |
| `shutdown /r /t 0` | Restart immediately | `shutdown /r /t 0` |

### Useful Combos

```cmd
# Find your PC name
hostname

# See all WiFi passwords saved on your PC
netsh wlan show profiles
netsh wlan show profile name="WiFi-Name" key=clear

# Flush DNS cache (when website won't load)
ipconfig /flushdns

# Release and renew IP (fix network issues)
ipconfig /release
ipconfig /renew

# Check if a website's server is responding
ping -n 10 google.com

# See which app is using a specific port
netstat -ano | findstr :8000
```

---

## Practice Exercises

### Exercise 1: System Exploration
On your own computer, find and write down:
1. Your Windows version (Settings → System → About)
2. RAM installed
3. Processor name and speed
4. Storage total and free space
5. Your IP address (use ipconfig)
6. Your computer name
7. Number of startup apps enabled

### Exercise 2: Display Setup
If you have access to a second monitor or TV:
1. Connect via HDMI
2. Use Win+P to try all 4 modes
3. In Extend mode, drag a window to the second screen
4. Change the resolution of the external display

### Exercise 3: Network Diagnosis
1. Open CMD and run `ping google.com` — note response time
2. Run `tracert google.com` — how many hops to reach Google?
3. Run `ipconfig` — find your IPv4 address and default gateway
4. Run `nslookup techpath.biz` — what IP does it resolve to?

### Exercise 4: Cleanup Challenge
1. Open Settings → Storage → Temporary files → See how much space you can reclaim
2. Open Task Manager → Startup tab → Disable unnecessary apps
3. Check Downloads folder — move/delete files older than 30 days
4. Uninstall one app you no longer use

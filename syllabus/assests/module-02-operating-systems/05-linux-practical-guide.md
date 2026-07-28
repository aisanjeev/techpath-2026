# Linux Practical Guide — From Zero to Comfortable

**Module 02 — Operating Systems | Topic 5 — Hands-On Linux for Your IT Career**

---

## Why This Matters

> Every web developer deploys to a Linux server. Every DevOps engineer lives in the terminal. Every cloud platform (AWS, Azure, GCP) defaults to Linux. You WILL use Linux in your career — the question is whether you'll struggle with it or be comfortable.

---

## Setting Up — Get Linux on Your Windows PC

### Option 1: WSL (Recommended — Takes 5 Minutes)

```powershell
# Open PowerShell as Administrator
wsl --install

# Restart your computer
# Open "Ubuntu" from Start menu
# Create username and password when prompted
# Done! You have Linux inside Windows.
```

After setup, open Ubuntu from Start menu anytime. Your Linux home folder is at:
```
\\wsl$\Ubuntu\home\yourname\
```

And you can access your Windows files from Linux at:
```
/mnt/c/Users/YourName/
```

> 🖼️ **IMAGE:** Windows 11 Start menu showing "Ubuntu" app icon, and below it the Ubuntu terminal window open with a green prompt showing `rahul@DESKTOP:~$` — annotated with "This is Linux running inside Windows"
> `wsl-ubuntu-terminal.png`

### Option 2: VirtualBox (For Full Desktop Experience)

1. Download VirtualBox from virtualbox.org
2. Download Ubuntu Desktop ISO from ubuntu.com
3. Create new VM → select the ISO → follow installer
4. You get a full Ubuntu desktop inside a window

**Use this when:** You want to practice Ubuntu's graphical interface, not just the terminal.

---

## Part 1: The Terminal — Your New Best Friend

### The Prompt

```
rahul@laptop:~/projects$
│      │     │          │
│      │     │          └── $ means normal user (# means root/admin)
│      │     └── current folder (~ = home)
│      └── computer name
└── your username
```

### Your First 15 Commands (In Order)

Open your terminal and follow along — type each command:

```bash
# 1. Where am I?
pwd
# Output: /home/rahul

# 2. What's in this folder?
ls
# Output: Desktop  Documents  Downloads  ...

# 3. Create a practice folder
mkdir practice

# 4. Go into it
cd practice

# 5. Confirm you're inside
pwd
# Output: /home/rahul/practice

# 6. Create some files
touch file1.txt
touch file2.txt
touch notes.md

# 7. See your files
ls
# Output: file1.txt  file2.txt  notes.md

# 8. Write something into a file
echo "Hello, this is my first Linux file!" > file1.txt

# 9. Read the file
cat file1.txt
# Output: Hello, this is my first Linux file!

# 10. Copy a file
cp file1.txt file1-backup.txt

# 11. Rename (move) a file
mv file2.txt renamed.txt

# 12. Delete a file
rm notes.md

# 13. See detailed list (permissions, size, date)
ls -la

# 14. Go back to home
cd ~

# 15. See your practice folder is still there
ls practice/
# Output: file1.txt  file1-backup.txt  renamed.txt
```

---

## Part 2: Working with Files and Folders

### Creating Project Structures

Real projects have organized folders. Build one:

```bash
# Create a web project structure in one command
mkdir -p mywebsite/{css,js,images,pages}

# See the result
ls mywebsite/
# Output: css  images  js  pages

# Create files in subfolders
touch mywebsite/index.html
touch mywebsite/css/style.css
touch mywebsite/js/app.js

# See the full tree structure
# Install tree first (if not installed):
sudo apt install tree -y

tree mywebsite/
# Output:
# mywebsite/
# ├── css
# │   └── style.css
# ├── images
# ├── index.html
# ├── js
# │   └── app.js
# └── pages
```

> 🖼️ **IMAGE:** Terminal showing the output of `tree mywebsite/` command — folder tree displayed with ASCII art lines connecting folders and files — matching the output above
> `linux-tree-command.png`

### Writing and Reading Files

```bash
# Write one line to a file (creates or OVERWRITES)
echo "First line" > file.txt

# APPEND to a file (adds at the end, doesn't overwrite)
echo "Second line" >> file.txt
echo "Third line" >> file.txt

# Read entire file
cat file.txt

# Read first 5 lines of a large file
head -5 file.txt

# Read last 5 lines
tail -5 file.txt

# Read with line numbers
cat -n file.txt

# Live-watch a file (useful for log files — new lines appear automatically)
tail -f /var/log/syslog
# Press Ctrl+C to stop watching
```

### Editing Files in Terminal

**nano** — the simplest editor (recommended for beginners):

```bash
nano file.txt
```

| Action | Key |
|--------|-----|
| Save | Ctrl + O → Enter |
| Exit | Ctrl + X |
| Cut line | Ctrl + K |
| Paste | Ctrl + U |
| Search | Ctrl + W |
| Go to line | Ctrl + _ |

**vim** — the powerful editor (harder but faster once learned):

```bash
vim file.txt
```

| Mode | How to Enter | What It Does |
|------|-------------|-------------|
| **Normal** | Press `Esc` | Navigate, delete, copy |
| **Insert** | Press `i` | Type text |
| **Command** | Press `:` | Save, quit, search |

| Action | Keys |
|--------|------|
| Start typing | `i` (enter Insert mode) |
| Stop typing | `Esc` (back to Normal) |
| Save and quit | `:wq` then Enter |
| Quit without saving | `:q!` then Enter |
| Delete a line | `dd` (in Normal mode) |
| Undo | `u` (in Normal mode) |

**Learning tip:** Use `nano` for now. Learn `vim` later when you're comfortable — many servers only have `vim` installed.

---

## Part 3: File Permissions — Understanding rwx

### Reading Permissions

```bash
ls -la
# Output:
# drwxr-xr-x  2 rahul rahul 4096 Jul 23 10:30 projects
# -rw-r--r--  1 rahul rahul  156 Jul 23 10:30 notes.txt
# -rwxr-xr-x  1 rahul rahul  512 Jul 23 10:30 script.sh
```

Breaking down `-rw-r--r--`:

```
-   rw-   r--   r--
│   │     │     │
│   │     │     └── Others (everyone else): read only
│   │     └── Group (your group): read only
│   └── Owner (you): read + write
└── Type: - = file, d = directory
```

| Letter | Permission | Number |
|--------|-----------|--------|
| `r` | Read (view contents) | 4 |
| `w` | Write (edit, delete) | 2 |
| `x` | Execute (run as program) | 1 |
| `-` | No permission | 0 |

### Setting Permissions

```bash
# Make a script executable (so you can run it)
chmod +x script.sh

# Using numbers (add them up):
# Owner: rwx = 4+2+1 = 7
# Group: r-x = 4+0+1 = 5
# Others: r-x = 4+0+1 = 5
chmod 755 script.sh

# Common permission sets:
chmod 644 file.txt      # Owner: rw, Others: read-only (normal files)
chmod 755 script.sh     # Owner: rwx, Others: rx (executable scripts)
chmod 600 secrets.env   # Owner only: rw, NO ONE else can read
chmod 777 file.txt      # Everyone: everything (NEVER do this in production!)
```

**Why this matters at work:**
- Deploying a web app? Server files need correct permissions
- Writing a script? Must be executable (`chmod +x`)
- Storing API keys? Must be owner-only readable (`chmod 600`)

---

## Part 4: Pipes and Redirection — Combining Commands

### The Pipe `|`

Pipes send output from one command as input to another.

```bash
# List all files, then search for .py files
ls -la | grep ".py"

# Count number of files in a folder
ls | wc -l

# Show running processes, find Python ones
ps aux | grep python

# Sort a file's contents and show unique lines
cat names.txt | sort | uniq

# Show top 10 largest files in current folder
du -sh * | sort -rh | head -10
```

### Redirection `>` and `>>`

```bash
# Save command output to a file (creates/overwrites)
ls -la > file-list.txt

# Append output to a file
echo "new line" >> file-list.txt

# Save error messages to a file
python script.py 2> errors.txt

# Save both output AND errors
python script.py > output.txt 2>&1

# Throw away output (silence a command)
ping google.com > /dev/null
```

### Real-World Example: Log Analysis

```bash
# Your server has a log file. Find errors from today:
grep "ERROR" /var/log/app.log | grep "2026-07-23" | tail -20

# Count how many errors today:
grep "ERROR" /var/log/app.log | grep "2026-07-23" | wc -l

# Save today's errors to a report:
grep "ERROR" /var/log/app.log | grep "2026-07-23" > today-errors.txt
```

---

## Part 5: Package Management (Installing Software)

### APT — Ubuntu's Package Manager

```bash
# Update package list (always do this first)
sudo apt update

# Install a package
sudo apt install git -y

# Install multiple packages at once
sudo apt install git curl wget python3 python3-pip -y

# Remove a package
sudo apt remove firefox

# Remove a package AND its config files
sudo apt purge firefox

# Update all installed packages
sudo apt upgrade -y

# Remove unnecessary packages
sudo apt autoremove -y

# Search for a package
apt search "text editor"

# Show info about a package
apt show git
```

### Essential Packages for IT Students

```bash
# Install everything you'll need for the course:
sudo apt update
sudo apt install -y \
  git \
  curl \
  wget \
  python3 \
  python3-pip \
  python3-venv \
  nodejs \
  npm \
  tree \
  htop \
  net-tools \
  openssh-client
```

| Package | What It Does |
|---------|-------------|
| `git` | Version control (GitHub) |
| `curl` / `wget` | Download files from internet |
| `python3` | Python language |
| `python3-pip` | Python package manager |
| `python3-venv` | Python virtual environments |
| `nodejs` / `npm` | JavaScript runtime + package manager |
| `tree` | Visual folder structure |
| `htop` | Better Task Manager (color-coded) |
| `net-tools` | Network tools (ifconfig, netstat) |
| `openssh-client` | SSH to connect to remote servers |

---

## Part 6: Networking Commands

```bash
# Show IP address
ip addr
# Or older command:
ifconfig

# Test internet connectivity
ping google.com -c 5
# -c 5 means send only 5 pings (Linux pings forever by default)

# Trace route to a server
traceroute google.com

# Check DNS resolution
nslookup techpath.biz

# Download a file
wget https://example.com/file.zip
curl -O https://example.com/file.zip

# Check which ports are open
ss -tuln
# Or older:
netstat -tuln

# SSH into a remote server (you'll use this for deployment!)
ssh username@server-ip-address
# Example: ssh rahul@192.168.1.100
```

---

## Part 7: Process Management

```bash
# See all running processes
ps aux

# Interactive process viewer (like Task Manager)
htop
# Press q to exit

# Find a specific process
ps aux | grep python

# Run something in the background
python3 server.py &

# See background jobs
jobs

# Kill a process by name
pkill python3

# Kill a process by ID
kill 1234

# Force kill (when normal kill doesn't work)
kill -9 1234
```

---

## Part 8: Shell Scripts — Automate Repetitive Tasks

### What Is a Shell Script?

A text file with commands that run in sequence — like recording your actions for playback.

### Your First Script

```bash
# Create the script
nano my-setup.sh
```

Write this inside:
```bash
#!/bin/bash

echo "Setting up your project..."

# Create project structure
mkdir -p myproject/{src,tests,docs,config}

# Create initial files
touch myproject/src/main.py
touch myproject/tests/test_main.py
touch myproject/README.md
touch myproject/.gitignore

# Write .gitignore
echo "__pycache__/" > myproject/.gitignore
echo ".env" >> myproject/.gitignore
echo "*.pyc" >> myproject/.gitignore

# Write README
echo "# My Project" > myproject/README.md
echo "Created on $(date)" >> myproject/README.md

echo "Project setup complete!"
echo "Files created:"
tree myproject/
```

Save (Ctrl+O) and exit (Ctrl+X).

```bash
# Make it executable
chmod +x my-setup.sh

# Run it
./my-setup.sh
```

> 🖼️ **IMAGE:** Terminal showing the script being run — the output messages "Setting up your project..." followed by "Project setup complete!" and the tree output showing the created folder structure with all files
> `shell-script-output.png`

### Useful Script: Backup Script

```bash
#!/bin/bash

# Backup script — run daily
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_DIR="/home/rahul/backups"
SOURCE="/home/rahul/projects"

mkdir -p $BACKUP_DIR

tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" $SOURCE

echo "Backup created: backup_$TIMESTAMP.tar.gz"
echo "Size: $(du -h $BACKUP_DIR/backup_$TIMESTAMP.tar.gz | cut -f1)"
```

### Useful Script: Quick Git Push

```bash
#!/bin/bash

# Quick git commit and push
# Usage: ./push.sh "commit message"

if [ -z "$1" ]; then
    echo "Usage: ./push.sh 'your commit message'"
    exit 1
fi

git add .
git commit -m "$1"
git push

echo "Pushed with message: $1"
```

Usage:
```bash
./push.sh "Add login feature"
```

---

## Part 9: SSH — Connecting to Remote Servers

### What Is SSH?

SSH (Secure Shell) lets you control a remote computer from your terminal. This is how you manage web servers.

```bash
# Connect to a remote server
ssh username@ip-address
# Example:
ssh rahul@143.198.45.67

# First time? It asks to trust the server — type "yes"
# Enter password when prompted
# You're now ON the server — every command runs there, not on your PC
# Type "exit" to disconnect
```

### SSH Keys (Password-Free Login)

```bash
# Generate a key pair (on YOUR computer)
ssh-keygen -t ed25519 -C "rahul@techpath"
# Press Enter for default location
# Enter passphrase (optional)

# Copy your public key to the server
ssh-copy-id username@server-ip

# Now you can login without password!
ssh username@server-ip
```

### Copy Files to/from Server

```bash
# Copy file from your PC to server
scp myfile.txt rahul@server:/home/rahul/

# Copy file from server to your PC
scp rahul@server:/home/rahul/report.txt ./

# Copy entire folder
scp -r myproject/ rahul@server:/home/rahul/
```

---

## Command Cheat Sheet by Situation

### "I need to find something"

| What | Command |
|------|---------|
| Find a file by name | `find / -name "config.py" 2>/dev/null` |
| Find files modified today | `find . -mtime 0` |
| Search inside files for text | `grep -r "database" .` |
| Find large files (>100MB) | `find / -size +100M 2>/dev/null` |

### "I need to monitor something"

| What | Command |
|------|---------|
| Live process monitor | `htop` |
| Watch disk space | `df -h` |
| Watch RAM usage | `free -h` |
| Watch a log file live | `tail -f /var/log/syslog` |
| Watch a command repeatedly | `watch -n 2 "ls -la"` (every 2 seconds) |

### "I need to manage files"

| What | Command |
|------|---------|
| Compress a folder | `tar -czf archive.tar.gz folder/` |
| Extract an archive | `tar -xzf archive.tar.gz` |
| Download a file | `wget URL` or `curl -O URL` |
| Compare two files | `diff file1.txt file2.txt` |
| Count lines/words | `wc -l file.txt` (lines) / `wc -w` (words) |

---

## Practice Projects

### Project 1: System Info Script
Write a script (`sysinfo.sh`) that displays:
- Hostname
- Current user
- OS version (`cat /etc/os-release`)
- Uptime
- CPU info (first line of `/proc/cpuinfo`)
- Total and free RAM
- Disk usage
- Current IP address

### Project 2: File Organizer
Write a script that organizes your Downloads folder:
- Move `.jpg` and `.png` to a `Images/` folder
- Move `.pdf` to a `Documents/` folder
- Move `.py` and `.js` to a `Code/` folder
- Report how many files were moved

### Project 3: Log Analyzer
Given a log file with lines like:
```
2026-07-23 10:30:15 ERROR Database connection failed
2026-07-23 10:30:16 INFO User login successful
2026-07-23 10:31:00 WARNING Disk usage at 85%
```
Write a script that:
- Counts total lines
- Counts ERROR, WARNING, and INFO lines separately
- Extracts all ERROR messages to a separate file
- Shows the most recent 5 errors

---

## Interview Questions

| Question | Key Answer |
|----------|-----------|
| "What Linux commands do you know?" | Navigation (cd, ls, pwd), file operations (cp, mv, rm, mkdir), text (cat, grep, head, tail), permissions (chmod, chown), packages (apt), processes (ps, kill, htop), networking (ping, ssh, scp). |
| "How do you find a file in Linux?" | `find / -name "filename"` for exact match, `find . -name "*.py"` for pattern, `grep -r "text" .` for searching inside files. |
| "What does chmod 755 mean?" | Owner gets rwx (7=4+2+1), Group gets r-x (5=4+0+1), Others get r-x (5). Common for executable scripts and web server directories. |
| "How do you connect to a remote server?" | SSH: `ssh user@ip`. For password-free: set up SSH keys with `ssh-keygen` and `ssh-copy-id`. Transfer files with `scp`. |
| "What is a pipe in Linux?" | The `\|` operator sends output from one command as input to another. Example: `ps aux \| grep python` finds Python processes. Pipes let you chain simple commands into powerful combinations. |
| "Difference between > and >>?" | `>` creates/overwrites a file. `>>` appends to a file without overwriting. Example: `echo "line" > file.txt` overwrites, `echo "line" >> file.txt` adds at the end. |

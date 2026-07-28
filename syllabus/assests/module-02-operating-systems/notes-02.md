# Module 02 — Operating Systems — Quick Revision Notes

---

## What is an OS?
- System software that manages hardware + provides platform for apps
- **5 Jobs:** Process management, Memory management, File management, Device management, Security

## Process Management
- A **process** = running program
- CPU uses **time-slicing** — gives each process ~10ms turns
- Process states: New → Ready → Running → Waiting → Terminated
- Chrome creates separate process per tab (crash isolation)

## Memory Management
- **RAM** = fast, temporary (lost on shutdown)
- **Virtual Memory** = OS uses disk as overflow when RAM is full
- **Thrashing** = constant swapping between RAM and disk = very slow
- 4 GB = basic | 8 GB = coding | 16 GB = heavy work | 32 GB = Docker/VMs

## File Systems
| File System | Used By | Max File | Notes |
|-------------|---------|----------|-------|
| NTFS | Windows | 16 TB | Default, supports permissions |
| FAT32 | USB drives | 4 GB | Universal but limited |
| exFAT | USB/SD | 128 PB | Modern replacement for FAT32 |
| ext4 | Linux | 16 TB | Linux default |

## Boot Process
Power → BIOS/UEFI (POST) → Find boot drive → Boot loader → OS kernel → Drivers → Services → Login

## 32-bit vs 64-bit
- 32-bit: max 4 GB RAM | 64-bit: 128+ GB RAM
- Always install 64-bit software on modern PCs

## Windows Key Parts
- **Taskbar** — running apps, system tray, clock
- **Start Menu** — Win key
- **File Explorer** — Win + E
- **Settings** — Win + I
- **Task Manager** — Ctrl + Shift + Esc
- **Virtual Desktops** — Win + Ctrl + D (create), Win + Ctrl + Arrow (switch)

## Linux Essentials
- **96.3%** of top web servers run Linux
- Distros: Ubuntu (beginners), Fedora (devs), Kali (security), Debian (servers)
- Install via WSL: `wsl --install` in PowerShell (admin)

## Must-Know Linux Commands
| Purpose | Commands |
|---------|----------|
| Navigate | `pwd`, `ls`, `cd`, `cd ..`, `cd ~` |
| Files | `touch`, `mkdir`, `cp`, `mv`, `rm`, `cat` |
| Search | `find`, `grep` |
| Permissions | `chmod 755`, `chmod +x` |
| Packages | `sudo apt update`, `sudo apt install` |
| System | `whoami`, `df -h`, `free -h`, `htop` |
| Network | `ping`, `ifconfig`, `ssh`, `scp` |

## Permissions (rwx)
- r=4 (read), w=2 (write), x=1 (execute)
- `chmod 755` = Owner rwx, Group r-x, Others r-x
- `chmod 600` = Owner rw only (for secret files)

## Key Shortcuts
| Action | Shortcut |
|--------|----------|
| Copy/Paste | Ctrl+C / Ctrl+V |
| Save | Ctrl+S |
| Undo | Ctrl+Z |
| Find | Ctrl+F |
| Lock PC | Win+L |
| Screenshot | Win+Shift+S |
| Task Manager | Ctrl+Shift+Esc |
| Switch app | Alt+Tab |
| Snap window | Win+Arrow |

## Environment Variables
- **PATH** — folders where OS searches for commands
- If `python` not recognized → Python folder not in PATH
- Set via: Settings → search "Environment Variables" → Edit Path

## Troubleshooting Steps
1. Restart the computer
2. Check Task Manager for resource hogs
3. Check Device Manager for driver issues (yellow ⚠️)
4. Run `sfc /scannow` for system file corruption
5. Check for malware with Windows Security

# Ports, Connectors & Basic Troubleshooting

**Module 01 — Computer Fundamentals | Practical Knowledge**

---

## Why This Matters

> On your first day in any IT job, someone will hand you a tangled cable and ask "Can you connect this?" or say "My computer is slow, fix it." This chapter makes sure you're never stuck.

---

## Ports & Connectors — Know What Plugs Where

### Common Ports on a Computer

> 🖼️ **IMAGE:** Back panel of a desktop computer with arrows pointing to each port — USB-A, USB-C, HDMI, VGA, Ethernet, Audio jack, Power — each labeled with name and what it connects to
> `ports-back-panel-labeled.png`

| Port | What It Connects | Shape | Speed |
|------|-----------------|-------|-------|
| **USB-A** | Mouse, keyboard, pen drive | Rectangular | USB 2.0: 480 Mbps, 3.0: 5 Gbps |
| **USB-C** | Phone charger, new laptops, data | Small oval | Up to 40 Gbps (Thunderbolt) |
| **HDMI** | Monitor, TV, projector | Trapezoid | Video + Audio |
| **VGA** | Old monitors, projectors | D-shape, 15 pins | Video only (analog) |
| **DisplayPort** | High-end monitors | Similar to HDMI | Video + Audio (higher res) |
| **Ethernet (RJ45)** | Internet cable (LAN) | Wide, clip-on | 1 Gbps (Cat 6) |
| **3.5mm Audio** | Headphones, speakers | Small round | Analog audio |
| **Power (DC-in)** | Laptop charger | Round or USB-C | Power only |

> 🖼️ **IMAGE:** A comparison chart showing USB-A, USB-B, USB-C, Micro-USB, and Mini-USB connectors side by side with actual connector shapes drawn clearly, each labeled with common devices that use them
> `usb-connector-types.png`

### USB Versions — Why Your Pen Drive is Slow

| Version | Speed | Color (usually) | Year |
|---------|-------|-----------------|------|
| USB 2.0 | 480 Mbps | Black/White | 2000 |
| USB 3.0 | 5 Gbps (10× faster) | Blue | 2008 |
| USB 3.1 | 10 Gbps | Teal | 2013 |
| USB 3.2 | 20 Gbps | Red | 2017 |
| USB 4 | 40 Gbps | — | 2019 |

**Practical tip:** If your pen drive transfer is slow, check if you're using a USB 2.0 port (black). Switch to the blue USB 3.0 port — same pen drive, much faster.

---

## Types of Cables

| Cable | Use | Max Length |
|-------|-----|-----------|
| **HDMI** | Monitor/TV (video + audio) | 15 meters |
| **VGA** | Old monitors (video only) | 10 meters |
| **Ethernet (Cat 5e/6)** | Wired internet | 100 meters |
| **USB** | Data + charging | 3-5 meters |
| **Power cable** | Computer/monitor power | — |
| **SATA** | Internal hard drive connection | 1 meter (inside PC) |
| **DisplayPort** | High-res monitors (4K/8K) | 3 meters |

> 🖼️ **IMAGE:** Six common cables laid out side by side — HDMI, VGA, Ethernet (Cat6), USB-A to USB-C, 3.5mm audio, and power cable — each labeled with name
> `common-cables.png`

---

## Peripheral Devices

### Input Devices

| Device | Use | Connection |
|--------|-----|------------|
| Keyboard | Typing | USB / Bluetooth / Wireless |
| Mouse | Pointing/clicking | USB / Bluetooth / Wireless |
| Scanner | Paper → digital image | USB |
| Webcam | Video calls | USB / Built-in |
| Microphone | Audio input | 3.5mm / USB |
| Graphics Tablet | Drawing/design | USB |
| Barcode Scanner | Retail/inventory | USB |

### Output Devices

| Device | Use | Connection |
|--------|-----|------------|
| Monitor | Display | HDMI / VGA / DisplayPort |
| Printer | Paper output | USB / WiFi / Ethernet |
| Speaker | Audio | 3.5mm / Bluetooth / USB |
| Projector | Big screen display | HDMI / VGA |
| Headphones | Personal audio | 3.5mm / Bluetooth / USB |

### Storage Devices

| Device | Capacity | Speed | Best For |
|--------|----------|-------|----------|
| Pen Drive | 8GB - 256GB | Medium | Carrying files |
| External HDD | 500GB - 5TB | Medium | Backup |
| External SSD | 256GB - 4TB | Fast | Fast backup, editing |
| SD Card | 16GB - 1TB | Medium | Camera, phone |
| DVD | 4.7GB | Slow | Old software, movies |
| Cloud (Google Drive) | 15GB free | Depends on internet | Anywhere access |

---

## Basic Troubleshooting — The "IT Guy" Skill

### The Universal Fix Order

Every IT professional follows this order:

```
Step 1: Restart it
Step 2: Check cables
Step 3: Check settings
Step 4: Google the error message
Step 5: Update drivers/software
Step 6: Run diagnostic tools
Step 7: Call senior / escalate
```

> 🖼️ **IMAGE:** A flowchart showing the 7 troubleshooting steps as a vertical flow — each step in a box with an arrow pointing down, with "Fixed?" decision diamond after each step leading to "Done!" on yes, or continuing down on no
> `troubleshooting-flowchart.png`

### Top 10 Computer Problems and Fixes

| # | Problem | Check This First | Fix |
|---|---------|-----------------|-----|
| 1 | Computer won't turn on | Power cable plugged in? | Check power cable, try different outlet, check power button |
| 2 | Computer is slow | Too many programs running? | Close unused apps, check Task Manager (Ctrl+Shift+Esc) |
| 3 | No internet | WiFi connected? Cable plugged? | Restart router, forget and reconnect WiFi |
| 4 | Printer not working | Turned on? Connected? | Check connection, set as default printer, restart print spooler |
| 5 | Blue screen (BSOD) | Note the error code | Google the error code, check RAM, update drivers |
| 6 | No sound | Volume muted? Right output? | Check volume, click speaker icon → output device |
| 7 | Screen blank (monitor on) | HDMI/VGA cable firm? | Reseat cable, try different port, check brightness |
| 8 | Mouse/keyboard not working | USB plugged in fully? | Try different USB port, replace batteries (wireless) |
| 9 | Storage full | What's using space? | Settings → Storage → Delete temp files, old downloads |
| 10 | App crashing | Outdated? | Update the app, restart PC, reinstall if needed |

### Task Manager — Your Best Friend

Open with: **Ctrl + Shift + Esc**

> 🖼️ **IMAGE:** Windows Task Manager screenshot showing the Processes tab with columns: Name, CPU%, Memory%, Disk%, Network% — highlight a process using 90% CPU in red to show how to identify the problem app
> `task-manager-annotated.png`

| Tab | What It Shows | When to Use |
|-----|---------------|-------------|
| **Processes** | Running apps + resource usage | Find what's making PC slow |
| **Performance** | CPU, RAM, Disk, Network graphs | Check if hardware is maxed |
| **Startup** | Apps that run at boot | Disable unnecessary startup apps |
| **Details** | Technical process info | Advanced troubleshooting |

**How to fix a slow PC using Task Manager:**
1. Open Task Manager (Ctrl+Shift+Esc)
2. Click "CPU" column header to sort by usage
3. Find the app using 80-100% CPU
4. Right-click → End Task (if it's not critical)
5. If Chrome is the culprit — close tabs!

### Disk Cleanup

```
Settings → System → Storage → Temporary files → Clean up
```

What you can safely delete:
- Temporary files
- Recycle Bin contents
- Thumbnails
- Delivery Optimization Files
- Previous Windows installations (after major update)

---

## BIOS/UEFI — The First Thing That Runs

When you press the power button, before Windows loads, **BIOS/UEFI** runs first.

| | BIOS | UEFI |
|-|------|------|
| **Full form** | Basic Input/Output System | Unified Extensible Firmware Interface |
| **Era** | Old computers | Modern computers (2012+) |
| **Interface** | Text only, keyboard | Graphical, mouse support |
| **Boot speed** | Slower | Faster |
| **Drive support** | Up to 2TB | Beyond 2TB |

**How to enter BIOS/UEFI:**
- Press **F2, F10, F12, Del, or Esc** during startup (varies by brand)
- HP: F10 | Dell: F2 | Lenovo: F2/Fn+F2 | Asus: F2/Del

**What you can do in BIOS:**
- Change boot order (boot from USB for OS installation)
- Check hardware info (RAM, CPU, storage)
- Enable/disable features (virtualization, secure boot)
- Set a BIOS password

> 🖼️ **IMAGE:** A UEFI/BIOS screen showing the boot order menu — USB drive first, then SSD, then network — with labels explaining what each option means
> `bios-boot-order.png`

---

## How to Install an Operating System (Overview)

1. Download ISO file (Windows/Ubuntu)
2. Create bootable USB using Rufus or Balena Etcher
3. Restart → Enter BIOS → Set USB as first boot device
4. Restart → Follow installation wizard
5. Set language, region, keyboard
6. Create partitions (or use entire disk)
7. Create user account
8. Install drivers (network, display, audio)
9. Install essential software

> 🖼️ **IMAGE:** A 6-step visual flow showing OS installation — download ISO → create USB → boot from USB → partition disk → install → setup complete — each step as an icon with a short label
> `os-installation-steps.png`

---

## Practice Exercises

### Exercise 1: Port Identification
Look at your computer/laptop right now. Identify every port. Write down:
- Port name
- What you can connect to it
- USB version (check color)

### Exercise 2: Troubleshooting Scenarios
For each scenario, write the steps you'd take to fix it:
1. "My laptop turns on but the screen is black"
2. "The internet was working yesterday, now it's not"
3. "My computer takes 5 minutes to start up"
4. "I can't hear any sound from my speakers"
5. "My pen drive doesn't show up when I plug it in"

### Exercise 3: Task Manager Analysis
Open Task Manager on your computer. Write down:
- Top 3 CPU-consuming processes
- Total RAM usage percentage
- Number of startup programs enabled
- Disable any unnecessary startup programs

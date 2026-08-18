# Month 1 Resources — Networks & Internet

## Tools to Download & Install

### 1. Wireshark
**Purpose:** Industry-standard packet capture and protocol analyser  
**Download:** https://www.wireshark.org/download.html  
**Platforms:** Windows, macOS, Linux  
**Notes:** Install on your host OS. The bundled **tshark** CLI is useful for scripted captures. On Linux: `sudo apt install wireshark`. During install, allow non-root packet capture when prompted.

---

### 2. Cisco Packet Tracer
**Purpose:** Network simulation — build, configure, and test full topologies without physical hardware  
**Download:** https://www.netacad.com/cisco-packet-tracer (free Cisco NetAcad account required)  
**Platforms:** Windows, macOS, Ubuntu  
**Notes:** Use Packet Tracer to build the OSI lab exercises. Start with the included "Getting Started" templates. This tool is required for the Month 1 portfolio piece.

---

### 3. VirtualBox
**Purpose:** Free Type-2 hypervisor — runs VMs for the homelab you build in Month 2  
**Download:** https://www.virtualbox.org/wiki/Downloads  
**Platforms:** Windows, macOS, Linux  
**Notes:** Install now and allocate at least 50 GB of disk space. Download the Extension Pack for USB 3.0 and RDP support. Required in Month 2 for the 3-VM homelab.

---

### 4. nmap (+ Zenmap GUI)
**Purpose:** Port scanning, host discovery, service version detection, OS fingerprinting  
**Download:** https://nmap.org/download.html  
**Platforms:** Windows, macOS, Linux  
**Notes:** ONLY scan networks you own or have written permission to scan. Useful commands:
```bash
nmap -sV -p 1-1000 192.168.1.1   # Version scan, top 1000 ports
nmap -sn 192.168.1.0/24          # Ping sweep — discover live hosts
```

---

### 5. ipcalc
**Purpose:** Subnet calculator — instantly validates subnetting work  
**Download (web):** http://jodies.de/ipcalc  
**Install (Linux):** `sudo apt install ipcalc`  
**Example:**
```bash
ipcalc 192.168.10.0/26
# Output: Network, broadcast, first/last host, mask
```

---

## Online Learning Resources

### 1. Professor Messer — Free Network+ & Security+ Courses
**URL:** https://www.professormesser.com/free-a-plus-training/220-1101/220-1101-video/  
**What it covers:** Every OSI layer, TCP/IP, DNS, protocols, ports, subnetting, TLS.  
**Recommended:** Watch the "Network Concepts" playlist. His notes PDFs are free too.

---

### 2. TryHackMe — Pre-Security Path
**URL:** https://tryhackme.com/path/outline/presecurity  
**What it covers:** "How The Web Works", "Network Fundamentals", "Linux Fundamentals" — all browser-based, no VM required.  
**Recommended rooms:** DNS in Detail, HTTP in Detail, Intro to LAN, OSI Model, Packets & Frames

---

### 3. Cloudflare Learning Centre
**URL:** https://www.cloudflare.com/learning/  
**What it covers:** Deep-dive articles on DNS, TLS, DDoS, CDN, network security. Written by practitioners. Excellent reference quality.  
**Start with:** "What is DNS?" and "How does TLS work?"

---

### 4. Subnet Practice Tool
**URL:** https://subnettingpractice.com/  
**What it covers:** Randomised subnetting drills with instant feedback. Tracks your accuracy and time.  
**Goal:** Aim for under 90 seconds per question by end of Month 1.

---

### 5. Wireshark Official Sample Captures
**URL:** https://wiki.wireshark.org/SampleCaptures  
**What it covers:** Pre-recorded .pcap files covering HTTP, TLS, DNS, Telnet (cleartext), FTP, and more — great for analysis without generating traffic yourself.  
**Recommended:** Download the HTTP capture and the SSL/TLS capture to see both plaintext and encrypted traffic side-by-side.

---

## Reference Documents (Read Introductions Only)

| Document | URL | Why |
|---------|-----|-----|
| RFC 793 (TCP) | https://www.rfc-editor.org/rfc/rfc793 | Original TCP specification |
| RFC 1035 (DNS) | https://www.rfc-editor.org/rfc/rfc1035 | DNS message format |
| RFC 8446 (TLS 1.3) | https://www.rfc-editor.org/rfc/rfc8446 | Current TLS standard |
| OWASP TLS Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html | Practical TLS hardening |

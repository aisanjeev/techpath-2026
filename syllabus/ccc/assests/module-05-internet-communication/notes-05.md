# Comprehensive Notes: Computer Communication and Internet

**Module 05 — CCC Exam Preparation**

---

## Section 1: Computer Networks

### What is a Computer Network?
A computer network is a collection of two or more computers connected together to share data, resources, and information. Networks allow computers to communicate with each other and share resources like printers, scanners, and internet connections.

### Types of Networks by Area

**PAN (Personal Area Network)**
- Smallest type of network
- Covers area around one person (up to 10 meters)
- Examples: Bluetooth connection between phone and earphones, connecting phone to smartwatch
- Typically used for personal devices

**LAN (Local Area Network)**
- Covers a small area: one room, building, or campus
- Range: up to a few kilometers
- Speed: Very fast (100 Mbps to 10 Gbps)
- Ownership: Private (owned by the organization)
- Cost: Low setup and maintenance cost
- Examples: School computer lab, office network, home WiFi network
- Most common type of network you will encounter daily

**MAN (Metropolitan Area Network)**
- Covers a city or metropolitan area
- Range: up to 50-100 kilometers
- Connects multiple LANs within a city
- Can be privately or publicly owned
- Examples: Cable TV network across a city, bank branches connected across Pune, government offices across Bhopal

**WAN (Wide Area Network)**
- Covers very large areas: countries, continents, or the entire world
- Usually operated by telecom companies
- Speed: Variable, generally slower than LAN
- Cost: Very high
- The Internet is the largest WAN in the world
- Examples: Indian Railways network connecting all stations, multinational company offices worldwide

### Network Topologies

A topology describes the physical or logical arrangement of computers in a network.

**Star Topology**
- All computers connect to a central hub or switch
- Most commonly used topology today
- Advantages: Easy to install, easy to add/remove devices, one device failure does not affect others
- Disadvantages: If the central hub fails, entire network goes down; requires more cable
- Used in: Most modern offices, homes, schools

**Bus Topology**
- All computers connect to a single main cable (backbone/bus)
- Data travels in both directions along the cable
- Advantages: Cheap, simple, easy to set up for small networks
- Disadvantages: If main cable fails, entire network fails; performance degrades with more devices; difficult to troubleshoot
- Status: Rarely used today

**Ring Topology**
- Computers connected in a circular fashion, each connected to exactly two neighbors
- Data travels in one direction around the ring
- Advantages: Equal access for all devices; performs better than bus under heavy load
- Disadvantages: If one device fails, the ring breaks (unless dual ring); difficult to add/remove devices
- Status: Mostly replaced by star topology

**Mesh Topology**
- Every computer connects to every other computer
- Most fault-tolerant — if one connection fails, data takes another path
- Very expensive (requires many cables)
- Used in critical networks like military or core internet infrastructure

**Hybrid Topology**
- Combination of two or more topologies
- Example: Star-bus hybrid (common in large offices)

### Important Network Devices

| Device | Function |
|--------|----------|
| **Hub** | Central connecting point — sends data to all connected devices (broadcasts). Not smart. |
| **Switch** | Like a smart hub — sends data only to the intended device. More efficient. |
| **Router** | Connects different networks together. Connects your LAN to the internet. Decides the best path for data. |
| **Modem** | Modulator-Demodulator. Converts digital signals to analog and vice versa. Needed for internet connection. |
| **Bridge** | Connects two LANs that use the same protocol. |
| **Gateway** | Connects networks that use different protocols. |
| **Repeater** | Boosts/amplifies weak signals to extend network range. |
| **Access Point** | Extends wireless network coverage. |

---

## Section 2: Internet Fundamentals

### What is the Internet?
The Internet is a global network of interconnected computer networks. The word "Internet" comes from "Interconnected Network." It is the world's largest WAN, connecting billions of devices worldwide.

### History of the Internet
- **1969:** ARPANET created by US Department of Defense — first 4 nodes
- **1971:** First email sent by Ray Tomlinson (introduced @ symbol)
- **1974:** TCP/IP protocol designed by Vint Cerf and Bob Kahn
- **1983:** TCP/IP adopted as standard protocol — "birthday" of the modern internet
- **1989:** World Wide Web (WWW) invented by Tim Berners-Lee at CERN
- **1991:** WWW made public
- **1993:** First graphical web browser (Mosaic) released
- **1995:** Internet becomes commercial — Amazon, eBay, Yahoo launch
- **1998:** Google founded
- **2004:** Facebook launched — social media era
- **2007:** iPhone launched — mobile internet revolution
- **2016:** Jio launches in India — affordable internet for millions
- **2022:** 5G services launched in India

### Internet vs. WWW
| Feature | Internet | WWW |
|---------|----------|-----|
| What it is | Physical network infrastructure | A service running on the internet |
| Includes | Cables, routers, servers, protocols | Web pages, websites, hyperlinks |
| Invented | 1969 (ARPANET) | 1989 (Tim Berners-Lee) |
| Without the other | Internet can exist without WWW | WWW cannot exist without Internet |

### Client-Server Model
- **Client:** The device that requests information (your computer, phone)
- **Server:** The powerful computer that stores data and responds to requests
- Process: Client sends request -> Server processes it -> Server sends response -> Client displays it
- Example: Your browser (client) requests irctc.co.in -> IRCTC's server sends the web page -> Your browser displays it

### IP Address (Internet Protocol Address)
- Unique numerical address assigned to every device connected to the internet
- Works like a postal address for computers
- **IPv4:** Four numbers (0-255) separated by dots — Example: 192.168.1.100 (about 4.3 billion addresses)
- **IPv6:** Eight groups of hexadecimal numbers — Example: 2001:0db8:85a3::8a2e:0370:7334 (virtually unlimited)
- **Private IP:** Used within your local network (e.g., 192.168.x.x) — not visible on the internet
- **Public IP:** Assigned by your ISP — visible on the internet
- **Static IP:** Does not change (used for servers)
- **Dynamic IP:** Changes each time you connect (used for home users, assigned by DHCP)

### DNS (Domain Name System)
- Translates human-readable domain names (google.com) into IP addresses (142.250.77.110)
- Often called the "phone book of the internet"
- Without DNS, you would have to remember IP addresses for every website
- DNS servers are maintained by ISPs and organizations like Google (8.8.8.8)

### Internet Protocols

| Protocol | Full Form | Port | Purpose |
|----------|-----------|------|---------|
| HTTP | HyperText Transfer Protocol | 80 | Web page transfer (not secure) |
| HTTPS | HyperText Transfer Protocol Secure | 443 | Secure web page transfer (encrypted) |
| FTP | File Transfer Protocol | 21 | File upload/download |
| SMTP | Simple Mail Transfer Protocol | 25 | Sending email |
| POP3 | Post Office Protocol v3 | 110 | Receiving email (downloads to device) |
| IMAP | Internet Message Access Protocol | 143 | Receiving email (keeps on server) |
| Telnet | Terminal Network | 23 | Remote access (not secure) |
| SSH | Secure Shell | 22 | Secure remote access |
| DNS | Domain Name System | 53 | Domain name to IP resolution |
| DHCP | Dynamic Host Configuration Protocol | 67/68 | Automatic IP address assignment |

---

## Section 3: Internet Services

### World Wide Web (WWW)
- System of interlinked web pages accessed via browsers using HTTP/HTTPS
- Invented by Tim Berners-Lee in 1989 at CERN
- Components: Web pages (HTML), Websites, Web servers, Web browsers, URLs
- Uses hyperlinks to connect pages together

### Email (Electronic Mail)
- Sending and receiving messages electronically
- Protocols: SMTP (send), POP3 (receive + delete from server), IMAP (receive + keep on server)
- Email address format: username@domain.com
- Parts of email: To, CC (Carbon Copy), BCC (Blind Carbon Copy), Subject, Body, Attachments
- Popular services: Gmail, Outlook, Yahoo Mail, Rediffmail

### FTP (File Transfer Protocol)
- Used to transfer files between computers
- Upload: send file from your computer to server
- Download: get file from server to your computer
- Uses FTP client software like FileZilla

### Chat and Instant Messaging
- Real-time text, voice, and video communication
- Popular in India: WhatsApp (most used), Telegram, Signal
- Business use: Slack, Microsoft Teams, Google Chat

### Video Conferencing
- Face-to-face meetings over the internet
- Popular tools: Zoom, Google Meet, Microsoft Teams, Cisco Webex
- Features: Screen sharing, recording, chat, virtual backgrounds
- Became essential during COVID-19

### VoIP (Voice over Internet Protocol)
- Phone calls over the internet
- Much cheaper than traditional calls, especially international
- Examples: WhatsApp calls, Skype, Google Voice

---

## Section 4: Internet Connectivity

### ISP (Internet Service Provider)
- Company that provides internet access
- Popular in India: Jio, Airtel, BSNL, ACT, Vi
- ISP assigns you an IP address and connects you to the internet backbone

### Types of Internet Connections

| Type | Speed | Medium | Notes |
|------|-------|--------|-------|
| Dial-up | Up to 56 Kbps | Phone line | Slowest; cannot use phone simultaneously; obsolete |
| DSL | 1-100 Mbps | Phone line (copper) | Can use phone + internet together |
| Cable | 10-500 Mbps | TV cable (coaxial) | Good speeds; shared bandwidth |
| WiFi | 50-1000 Mbps | Radio waves | Wireless; most convenient |
| 4G/5G | 10-10000 Mbps | Cellular towers | Mobile internet |
| Fiber Optic | 100-10000 Mbps | Glass fiber (light) | Fastest; most reliable |
| Satellite | 1-25 Mbps | Satellite signals | Available anywhere; high latency |

### Modem vs. Router
- **Modem:** Converts digital to analog signals (and vice versa). Connects to ISP.
- **Router:** Connects multiple devices. Creates WiFi network. Routes data to correct device. Provides basic firewall.
- Modern devices often combine both functions into one unit.

---

## Section 5: Internet Security

### Types of Threats
- **Virus:** Self-replicating malware that needs a host file
- **Worm:** Self-replicating malware that spreads on its own
- **Trojan Horse:** Malware disguised as legitimate software
- **Spyware:** Secretly monitors and collects user data
- **Ransomware:** Encrypts files and demands payment
- **Phishing:** Fake emails/websites to steal personal information
- **Spam:** Bulk unwanted messages
- **Keylogger:** Records keystrokes to steal passwords

### Protection Measures
- **Antivirus software:** Detects and removes malware (Windows Defender, Quick Heal, Kaspersky)
- **Firewall:** Monitors and filters network traffic (Windows Firewall)
- **Strong passwords:** 8+ characters, mix of types, unique per account
- **HTTPS:** Look for padlock icon for secure websites
- **Two-Factor Authentication (2FA):** Extra security layer with OTP
- **Regular updates:** Keep OS, browser, and software updated
- **Safe browsing:** Do not click unknown links, avoid public WiFi for banking

### Digital India Initiatives
- **Launched:** 1 July 2015
- **DigiLocker:** Cloud storage for government documents (Aadhaar, PAN, DL)
- **UMANG:** Unified Mobile Application for New-age Governance — single app for government services
- **UPI:** Unified Payments Interface — instant mobile payments
- **Aadhaar:** 12-digit unique identity number
- **Common Service Centers (CSC):** Internet access in rural areas
- **PM-WANI:** Public WiFi hotspots across India
- **BharatNet:** Optical fiber network connecting villages

### Cyber Law
- **IT Act, 2000:** India's primary cyber law
- **IT Amendment Act, 2008:** Updated to cover more cyber crimes
- Report cyber crimes at: cybercrime.gov.in or helpline 1930

---

## CCC Exam Tips Summary

1. Internet = Interconnected Network = World's largest WAN
2. ARPANET = Ancestor of internet (1969, US Department of Defense)
3. WWW = Invented by Tim Berners-Lee (1989)
4. DNS = Domain Name System = Converts domain names to IP addresses
5. SMTP = Sends email; POP3/IMAP = Receives email
6. FTP = File Transfer Protocol
7. Modem = Modulator-Demodulator = Converts digital to analog
8. ISP = Internet Service Provider
9. LAN = Building; MAN = City; WAN = Country/World
10. Star topology = Most common; central hub
11. Firewall = Barrier between computer and internet
12. Virus needs host file; Worm spreads on its own; Trojan disguises as useful software
13. HTTPS = Secure (padlock icon); HTTP = Not secure
14. UMANG = Unified Mobile Application for New-age Governance
15. DigiLocker = Digital document storage
16. Digital India launched = 1 July 2015
17. Phishing = Tricking users to reveal personal information
18. Strong password = 8+ characters, mix of uppercase, lowercase, numbers, special characters
19. IPv4 = 4 groups of numbers (192.168.1.1); IPv6 = 8 groups of hex
20. Dial-up = Slowest connection; Fiber optic = Fastest connection

---

## Quick Reference Table

| Abbreviation | Full Form |
|-------------|-----------|
| LAN | Local Area Network |
| MAN | Metropolitan Area Network |
| WAN | Wide Area Network |
| PAN | Personal Area Network |
| ISP | Internet Service Provider |
| IP | Internet Protocol |
| DNS | Domain Name System |
| HTTP | HyperText Transfer Protocol |
| HTTPS | HyperText Transfer Protocol Secure |
| FTP | File Transfer Protocol |
| SMTP | Simple Mail Transfer Protocol |
| POP3 | Post Office Protocol version 3 |
| IMAP | Internet Message Access Protocol |
| TCP | Transmission Control Protocol |
| UDP | User Datagram Protocol |
| URL | Uniform Resource Locator |
| WWW | World Wide Web |
| HTML | HyperText Markup Language |
| VoIP | Voice over Internet Protocol |
| DHCP | Dynamic Host Configuration Protocol |
| SSH | Secure Shell |
| UMANG | Unified Mobile Application for New-age Governance |
| UPI | Unified Payments Interface |
| ARPANET | Advanced Research Projects Agency Network |

---

*TechPath Institute — CCC Exam Preparation*

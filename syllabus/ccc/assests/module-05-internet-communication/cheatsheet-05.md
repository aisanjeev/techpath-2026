# Cheatsheet: Computer Communication and Internet

**Module 05 — CCC Exam Quick Reference**

---

## Network Types Comparison

| Type | Full Form | Area | Speed | Example |
|------|-----------|------|-------|---------|
| PAN | Personal Area Network | Around a person (~10m) | Variable | Bluetooth |
| LAN | Local Area Network | Building/campus | Very fast | Office network |
| MAN | Metropolitan Area Network | City/town | Moderate | City cable TV |
| WAN | Wide Area Network | Country/world | Variable | Internet |

---

## Network Topology Quick Reference

| Topology | Shape | Central Device | Failure Impact | Used Today? |
|----------|-------|---------------|----------------|-------------|
| Star | Star/spoke | Hub/Switch (center) | Hub fails = all down; one PC fails = rest OK | Yes (most common) |
| Bus | Straight line | None (shared cable) | Cable breaks = all down | Rarely |
| Ring | Circle | None | One PC fails = ring breaks | Rarely |
| Mesh | Web/grid | None | Most fault-tolerant | Critical networks |

---

## Network Devices

| Device | What It Does | One-Line Memory Aid |
|--------|-------------|-------------------|
| Hub | Broadcasts data to ALL devices | "Shouting in a room" |
| Switch | Sends data to SPECIFIC device | "Whispering to one person" |
| Router | Connects networks, directs traffic | "Traffic police for data" |
| Modem | Digital <-> Analog conversion | "Translator between languages" |
| Repeater | Boosts weak signals | "Amplifier for network" |
| Gateway | Connects different protocol networks | "International translator" |

---

## Internet Protocol Table

| Protocol | Full Form | Purpose | Port |
|----------|-----------|---------|------|
| HTTP | HyperText Transfer Protocol | Web pages (not secure) | 80 |
| HTTPS | HyperText Transfer Protocol Secure | Web pages (secure) | 443 |
| FTP | File Transfer Protocol | File transfer | 21 |
| SMTP | Simple Mail Transfer Protocol | Sending email | 25 |
| POP3 | Post Office Protocol 3 | Receiving email (download) | 110 |
| IMAP | Internet Message Access Protocol | Receiving email (server) | 143 |
| DNS | Domain Name System | Name to IP conversion | 53 |
| Telnet | Terminal Network | Remote access (not secure) | 23 |
| SSH | Secure Shell | Remote access (secure) | 22 |
| TCP | Transmission Control Protocol | Reliable data delivery | - |
| UDP | User Datagram Protocol | Fast data delivery | - |
| IP | Internet Protocol | Addressing/routing | - |
| DHCP | Dynamic Host Config Protocol | Auto IP assignment | 67/68 |

---

## Abbreviation Master List

| Abbreviation | Full Form |
|-------------|-----------|
| ARPANET | Advanced Research Projects Agency Network |
| DNS | Domain Name System |
| DHCP | Dynamic Host Configuration Protocol |
| DSL | Digital Subscriber Line |
| FTP | File Transfer Protocol |
| HTML | HyperText Markup Language |
| HTTP | HyperText Transfer Protocol |
| HTTPS | HyperText Transfer Protocol Secure |
| IMAP | Internet Message Access Protocol |
| IP | Internet Protocol |
| ISP | Internet Service Provider |
| LAN | Local Area Network |
| MAC | Media Access Control |
| MAN | Metropolitan Area Network |
| PAN | Personal Area Network |
| POP3 | Post Office Protocol version 3 |
| SMTP | Simple Mail Transfer Protocol |
| SSH | Secure Shell |
| TCP | Transmission Control Protocol |
| TCP/IP | Transmission Control Protocol/Internet Protocol |
| UDP | User Datagram Protocol |
| UMANG | Unified Mobile Application for New-age Governance |
| UPI | Unified Payments Interface |
| URL | Uniform Resource Locator |
| VoIP | Voice over Internet Protocol |
| VPN | Virtual Private Network |
| WAN | Wide Area Network |
| WiFi | Wireless Fidelity |
| WWW | World Wide Web |

---

## Internet Connection Types (Speed Order)

```
Slowest ←————————————————————————————→ Fastest

Dial-up → DSL → Cable → WiFi → 4G → 5G → Fiber Optic
56 Kbps   100M  500M   1 Gbps  1G   10G   10 Gbps
```

---

## Email Protocol Memory Trick

```
SMTP  = Sending Mail To People     (SEND)
POP3  = Pull Out from Post-office  (DOWNLOAD to device)
IMAP  = I Manage All from Phone    (KEEP on server, sync)
```

---

## Security Threats Quick Reference

| Threat | Key Characteristic | Memory Aid |
|--------|-------------------|-----------|
| Virus | Needs host file to spread | "Hitchhiker — rides along with files" |
| Worm | Spreads on its own | "Independent traveler" |
| Trojan | Disguised as useful software | "Wolf in sheep's clothing" |
| Spyware | Secretly watches you | "Hidden camera" |
| Ransomware | Locks files, demands money | "Digital kidnapper" |
| Phishing | Fake website/email | "Fishing for your password" |
| Spam | Bulk junk messages | "Junk mail in inbox" |
| Keylogger | Records keystrokes | "Invisible note-taker" |

---

## Digital India Quick Facts

| Service | What It Does | Key Fact for Exam |
|---------|-------------|------------------|
| DigiLocker | Store documents digitally | Aadhaar, PAN, DL, marksheets |
| UMANG | One app for govt services | 1300+ services |
| UPI | Instant mobile payments | Google Pay, PhonePe, Paytm |
| Aadhaar | 12-digit unique ID | Issued by UIDAI |
| Digital India | Govt programme | Launched 1 July 2015 |
| CSC | Internet for rural areas | Common Service Centers |
| IT Act | Cyber law of India | Information Technology Act, 2000 |
| Cyber Crime | Report online | cybercrime.gov.in / 1930 |

---

## URL Anatomy

```
https://www.irctc.co.in/nget/train-search?date=today
|_____|   |_| |____|  |___| |________________| |________|
  |        |    |       |          |                |
Protocol  Sub  Domain  TLD      Path            Query
(HTTPS)  domain        (.co.in)               (parameters)
```

---

## IP Address Quick Facts

| Version | Format | Example | Total Addresses |
|---------|--------|---------|----------------|
| IPv4 | 4 groups (0-255) separated by dots | 192.168.1.1 | ~4.3 billion |
| IPv6 | 8 groups of hex separated by colons | 2001:0db8::7334 | Virtually unlimited |

**Private IP ranges:** 192.168.x.x, 10.x.x.x, 172.16-31.x.x
**Public IP:** Assigned by ISP, visible on internet

---

## Key People to Remember

| Person | Contribution |
|--------|-------------|
| Tim Berners-Lee | Invented the World Wide Web (1989) |
| Ray Tomlinson | Sent first email, introduced @ symbol (1971) |
| Vint Cerf | Co-creator of TCP/IP ("Father of Internet") |
| Bob Kahn | Co-creator of TCP/IP |

---

## Most Frequently Asked CCC Questions (Module 05)

1. Full form of DNS? **Domain Name System**
2. LAN covers which area? **Building or office**
3. Modem converts ___? **Digital to analog signals**
4. Which protocol sends email? **SMTP**
5. Full form of ISP? **Internet Service Provider**
6. Largest network? **Internet (WAN)**
7. UMANG stands for? **Unified Mobile Application for New-age Governance**
8. Star topology fails when? **Central hub fails**
9. ARPANET started in? **1969**
10. WWW invented by? **Tim Berners-Lee**
11. Dial-up speed? **Up to 56 Kbps**
12. Fiber optic uses? **Light through glass fibers**
13. Firewall does what? **Blocks unauthorized network access**
14. Virus vs Worm? **Virus needs host; worm spreads alone**
15. DigiLocker is used for? **Storing government documents digitally**

---

*TechPath Institute — CCC Exam Preparation*

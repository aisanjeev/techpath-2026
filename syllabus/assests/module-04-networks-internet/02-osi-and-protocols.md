# OSI Model & Network Protocols

**Module 04 — Networks & Internet | Topic 2**

---

## OSI Model — 7 Layers of Networking

The **OSI Model** (Open Systems Interconnection) explains how data travels from your computer to another computer. It has 7 layers.

> **Think of it like sending a letter:** You write it (Application), put it in envelope (Presentation), address it (Session), send via postal service (Transport), it goes through sorting offices (Network), onto roads (Data Link), onto physical trucks (Physical).

### The 7 Layers

| # | Layer | What It Does | Example | Easy Memory |
|---|-------|-------------|---------|-------------|
| 7 | **Application** | What the user sees and uses | Chrome, WhatsApp, Gmail | **A**ll |
| 6 | **Presentation** | Formats data (encryption, compression) | JPEG, SSL, UTF-8 | **P**eople |
| 5 | **Session** | Opens and closes connections | Login sessions | **S**eem |
| 4 | **Transport** | Ensures data reaches correctly | TCP, UDP | **T**o |
| 3 | **Network** | Finds the best path (routing) | IP, Router | **N**eed |
| 2 | **Data Link** | Direct device-to-device transfer | MAC address, Switch | **D**ata |
| 1 | **Physical** | Actual cables and signals | Ethernet cable, WiFi radio | **P**rocessing |

> **Memory trick (top to bottom):** "**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing"
>
> **Bottom to top:** "**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way"

---

## TCP/IP Model — Simplified Version

The internet actually uses the **TCP/IP model** (4 layers), which is a simplified version of OSI.

| TCP/IP Layer | Matches OSI Layers | Protocols |
|-------------|-------------------|-----------|
| **Application** | 7 + 6 + 5 | HTTP, HTTPS, FTP, SMTP, DNS |
| **Transport** | 4 | TCP, UDP |
| **Internet** | 3 | IP, ICMP |
| **Network Access** | 2 + 1 | Ethernet, WiFi, MAC |

---

## Important Protocols

### What is a Protocol?

A **protocol** is a set of rules for how data is sent and received. Like how postal service has rules for addressing letters.

### Protocol Quick Reference

| Protocol | Full Name | What It Does | Port |
|----------|-----------|-------------|------|
| **HTTP** | HyperText Transfer Protocol | Web pages (not secure) | 80 |
| **HTTPS** | HTTP Secure | Web pages (secure, encrypted) | 443 |
| **FTP** | File Transfer Protocol | Upload/download files to/from server | 21 |
| **SMTP** | Simple Mail Transfer Protocol | Send emails | 25 |
| **POP3** | Post Office Protocol | Receive emails (downloads) | 110 |
| **IMAP** | Internet Message Access Protocol | Receive emails (keeps on server) | 143 |
| **SSH** | Secure Shell | Remote access to server (secure) | 22 |
| **DNS** | Domain Name System | Convert domain names to IP | 53 |
| **DHCP** | Dynamic Host Configuration Protocol | Auto-assign IP addresses to devices | 67/68 |
| **TCP** | Transmission Control Protocol | Reliable data transfer (confirms delivery) | — |
| **UDP** | User Datagram Protocol | Fast data transfer (no confirmation) | — |

### TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| **Reliable?** | Yes (confirms every packet received) | No (just sends, no confirmation) |
| **Speed** | Slower (extra checking) | Faster (no checking) |
| **Order** | Data arrives in order | May arrive out of order |
| **Use case** | Web pages, email, file download | Video calls, gaming, live streaming |

> **Simple way to remember:**
> - TCP = like registered post (guaranteed delivery, signed for)
> - UDP = like throwing a paper airplane (fast, but might not reach)

---

## HTTP vs HTTPS

| Feature | HTTP | HTTPS |
|---------|------|-------|
| **Secure?** | No (data visible to hackers) | Yes (data encrypted) |
| **URL starts with** | http:// | https:// |
| **Lock icon?** | No | Yes (green lock in browser) |
| **Use** | Old websites (avoid) | All modern websites |

> **Always check for HTTPS** before entering passwords or card numbers on any website!

---

## Subnetting — Very Basic Concept

**Subnet** = dividing a big network into smaller parts.

Like how a big office building has different floors for different departments.

| Term | What It Means |
|------|-------------|
| **IP Address** | Your device address (e.g., 192.168.1.5) |
| **Subnet Mask** | Tells which part is network, which is device (e.g., 255.255.255.0) |
| **Gateway** | The door to the internet (usually your router: 192.168.1.1) |

In subnet mask `255.255.255.0`:
- First 3 parts (192.168.1) = Network address (same for all devices in network)
- Last part (.5) = Device address (unique for each device)

---

## How a Web Request Works (Step by Step)

```
1. You type www.google.com in Chrome
2. Browser checks its cache (did I visit before?)
3. If not cached → asks DNS: "What IP is google.com?"
4. DNS replies: "142.250.183.206"
5. Browser creates TCP connection to that IP (port 443 for HTTPS)
6. Browser sends HTTP GET request: "Give me the homepage"
7. Google's server processes the request
8. Server sends back HTML, CSS, JS, images
9. Browser renders (draws) the page
10. You see Google homepage!
```

---

## CDN — Content Delivery Network

A **CDN** stores copies of websites in servers around the world.

| Without CDN | With CDN |
|------------|---------|
| Every request goes to one server (maybe in USA) | Your request goes to nearest server (maybe in Mumbai) |
| Slow for users far from server | Fast for everyone |
| Server gets overloaded | Load is distributed |

> **Example:** Netflix, YouTube, and Instagram all use CDNs. That's why videos load fast from anywhere in the world.

---

## Summary

- **OSI Model** = 7 layers that explain how data travels in networks
- **TCP/IP** = Simplified 4-layer model used by the internet
- **HTTP/HTTPS** = Web protocol (always use HTTPS for security)
- **TCP** = Reliable but slow, **UDP** = Fast but unreliable
- **DNS** = Converts website names to IP addresses
- **CDN** = Copies of websites stored near you for faster loading
- A web request goes through: DNS → TCP → HTTP → Server → Response → Render

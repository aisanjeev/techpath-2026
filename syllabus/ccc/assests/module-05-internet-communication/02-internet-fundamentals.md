# Internet Fundamentals

**Module 05 — CCC Exam Preparation | Topic 2**

---

## What is the Internet?

The **Internet** is a global network of millions of computers connected together across the world. It allows people to share information, communicate, and access services from anywhere.

**Simple Definition:** The Internet is a worldwide network of networks — it connects LANs, MANs, and WANs all over the world into one giant network.

Think of it like this: Each city has its own road network. But highways connect all cities together. The Internet is like the highway system that connects all computer networks around the world.

**CCC Exam Tip:** "Internet" stands for **Inter**connected **Net**work. The Internet is the world's largest WAN.

---

## Brief History of the Internet

| Year | Event |
|------|-------|
| 1969 | **ARPANET** — The first version of the internet, created by the US Department of Defense. Connected 4 universities. |
| 1971 | First **email** sent by Ray Tomlinson. He introduced the @ symbol in email addresses. |
| 1983 | **TCP/IP protocol** adopted — this is the language all computers use to communicate on the internet. |
| 1989 | **World Wide Web (WWW)** invented by **Tim Berners-Lee** at CERN (Switzerland). |
| 1990 | First web browser and web page created. |
| 1991 | WWW made available to the public. |
| 1995 | Internet became commercially available. Amazon, Yahoo, and eBay launched. |
| 1998 | Google founded. |
| 2004 | Facebook launched. Social media era begins. |
| 2007 | iPhone launched — mobile internet revolution. |
| 2016 | Digital India initiative accelerates internet adoption in India. |

**CCC Exam Tip:** ARPANET is the ancestor of the Internet. Tim Berners-Lee invented the World Wide Web (WWW). These are frequently asked.

---

## Important Internet Terms

### Internet vs. Intranet vs. Extranet

| Feature | Internet | Intranet | Extranet |
|---------|----------|----------|----------|
| **Access** | Open to everyone worldwide | Only for employees of an organization | Selected external partners + employees |
| **Example** | google.com, irctc.co.in | Company's internal portal | Supplier portal for a company |
| **Security** | Public | High (behind firewall) | Moderate (password-protected) |

**CCC Exam Tip:** Intranet = Internal network of an organization. Extranet = Intranet extended to selected outsiders.

---

## Client-Server Model

The internet works on a **Client-Server model**.

- **Client:** Your computer, phone, or tablet — the device that requests information
- **Server:** A powerful computer that stores websites, files, and data — it responds to client requests

**How it works:**
1. You open your browser and type `www.irctc.co.in`
2. Your browser (client) sends a request to IRCTC's server
3. The server finds the requested web page
4. The server sends the web page back to your browser
5. Your browser displays the web page on your screen

```
[Your Computer] ----request----> [IRCTC Server]
   (Client)     <----response----  (Server)
```

**Real-life analogy:** Think of a restaurant. You (client) place an order. The kitchen (server) prepares the food and sends it to your table.

**CCC Exam Tip:** In the client-server model, the client requests and the server responds.

---

## IP Address

An **IP Address** (Internet Protocol Address) is a unique number assigned to every device connected to the internet. It works like a postal address — it tells other computers where to find your device.

### Types of IP Addresses

**IPv4 (Internet Protocol version 4)**
- Format: Four groups of numbers separated by dots
- Example: `192.168.1.105`
- Each group ranges from 0 to 255
- Total possible addresses: About 4.3 billion (which is not enough for all devices today)

**IPv6 (Internet Protocol version 6)**
- Format: Eight groups of hexadecimal numbers separated by colons
- Example: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- Provides a virtually unlimited number of addresses
- Created because IPv4 addresses were running out

### Private vs. Public IP

| Type | Description | Example |
|------|-------------|---------|
| **Private IP** | Used within your local network (home/office) | 192.168.1.105 |
| **Public IP** | Used on the internet, visible to the world | 103.25.178.42 |

Your router has a public IP (given by your ISP). All devices at home share this public IP but have different private IPs.

**CCC Exam Tip:** Every device on the internet has a unique IP address. IPv4 uses 4 groups of numbers (e.g., 192.168.1.1).

---

## DNS (Domain Name System)

Imagine if you had to remember `142.250.77.110` every time you wanted to visit Google. That would be very difficult! This is where **DNS** comes in.

**DNS (Domain Name System)** is like a phone book for the internet. It converts human-friendly website names (like `google.com`) into computer-friendly IP addresses (like `142.250.77.110`).

### How DNS Works:

1. You type `www.google.com` in your browser
2. Your computer asks a DNS server: "What is the IP address of google.com?"
3. The DNS server looks up its records and replies: "It is 142.250.77.110"
4. Your browser connects to that IP address and loads the website

```
You type: www.google.com
    ↓
DNS Server: "google.com = 142.250.77.110"
    ↓
Browser connects to 142.250.77.110
    ↓
Google's homepage loads on your screen
```

**CCC Exam Tip:** "Full form of DNS?" = Domain Name System. "What does DNS do?" = Converts domain names to IP addresses.

---

## How Data Travels on the Internet

When you send a message or open a website, your data does not travel as one big piece. It is broken into small pieces called **packets**.

### Data Transmission Steps:

1. **Breaking into packets:** Your message/file is divided into small packets. Each packet is numbered so it can be reassembled later.

2. **Routing:** Each packet may take a different route through the internet. Routers along the way decide the best path for each packet.

3. **Reassembly:** When all packets reach the destination, they are put back together in the correct order.

4. **Delivery:** The complete message/file is delivered to the recipient.

**Analogy:** Imagine sending a 10-page letter. Instead of sending all 10 pages in one envelope, you put each page in a separate envelope. Each envelope might take a different postal route. When all 10 envelopes arrive, the recipient arranges the pages in order and reads the complete letter.

---

## Internet Protocols

**Protocols** are rules that computers follow to communicate with each other on the internet. Just like how people follow traffic rules on the road, computers follow protocols on the internet.

| Protocol | Full Form | Purpose |
|----------|-----------|---------|
| **HTTP** | HyperText Transfer Protocol | Loading web pages |
| **HTTPS** | HyperText Transfer Protocol Secure | Loading web pages securely (encrypted) |
| **FTP** | File Transfer Protocol | Transferring files between computers |
| **SMTP** | Simple Mail Transfer Protocol | Sending emails |
| **POP3** | Post Office Protocol 3 | Receiving emails (downloads to device) |
| **IMAP** | Internet Message Access Protocol | Receiving emails (keeps on server) |
| **TCP** | Transmission Control Protocol | Reliable data delivery |
| **IP** | Internet Protocol | Addressing and routing |
| **TCP/IP** | Transmission Control Protocol/Internet Protocol | Foundation protocol of the internet |

**CCC Exam Tip:** "Which protocol sends email?" = SMTP. "Which protocol is used for secure web browsing?" = HTTPS. These are very frequently asked.

---

## Internet Architecture Basics

The internet follows a layered architecture. The most important model to know is the **TCP/IP model**.

### TCP/IP Model (4 Layers)

| Layer | Name | What It Does | Example |
|-------|------|-------------|---------|
| 4 | Application | What the user interacts with | HTTP, FTP, SMTP, DNS |
| 3 | Transport | Ensures reliable delivery of data | TCP, UDP |
| 2 | Internet | Addressing and routing of packets | IP |
| 1 | Network Access | Physical transmission of data | Ethernet, WiFi |

**How they work together:**
- You write an email (Application layer)
- TCP breaks it into packets and ensures reliable delivery (Transport layer)
- IP adds addresses and routes the packets (Internet layer)
- The data is physically transmitted through cables or WiFi (Network Access layer)

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Internet | World's largest network — interconnected networks |
| ARPANET | Ancestor of the internet (1969) |
| WWW Inventor | Tim Berners-Lee |
| Client-Server | Client requests, server responds |
| IP Address | Unique number for every device on the internet |
| IPv4 Example | 192.168.1.1 (four groups of numbers) |
| DNS | Converts domain names to IP addresses (phone book of internet) |
| Packets | Data is broken into small pieces for transmission |
| SMTP | Protocol for sending email |
| HTTPS | Secure web browsing protocol |
| TCP/IP | Foundation protocol of the internet |

---

*TechPath Institute — CCC Exam Preparation*

# Computer Networks — Basics

**Module 04 — Networks & Internet | Topic 1**

---

## What is a Computer Network?

A **network** is two or more computers connected together so they can share data, files, and resources (like a printer).

> **Simple example:** Your home WiFi connects your phone, laptop, and TV — that's a network!

---

## Why Do We Need Networks?

| Benefit | Example |
|---------|---------|
| **Share files** | Send photos from phone to laptop |
| **Share devices** | One printer used by all office computers |
| **Communication** | Email, WhatsApp, video calls |
| **Internet access** | All devices connect through one router |
| **Centralized data** | Company stores all files on one server |

---

## Types of Networks (by Size)

| Type | Full Name | Area | Example |
|------|-----------|------|---------|
| **PAN** | Personal Area Network | Around one person (1-10m) | Bluetooth headphone + phone |
| **LAN** | Local Area Network | One building (10-1000m) | Office, school lab, home WiFi |
| **MAN** | Metropolitan Area Network | One city (10-100 km) | Cable TV network in a city |
| **WAN** | Wide Area Network | Countries / worldwide | The Internet itself |

> **Remember order:** PAN (smallest) → LAN → MAN → WAN (largest)

---

## Network Topologies (How Computers are Connected)

| Topology | Shape | How It Works | Pros | Cons |
|----------|-------|-------------|------|------|
| **Bus** | One straight line | All computers share one cable | Simple, cheap | If cable breaks, all stop |
| **Star** | Star shape | All connect to a central hub/switch | Easy to add/remove devices | Hub fails = all stop |
| **Ring** | Circle | Each connects to next in a circle | Equal access to all | One break = whole ring fails |
| **Mesh** | Web/net | Every computer connects to every other | Very reliable | Expensive, complex wiring |

> **Most used today:** Star topology (with a router/switch at center)

---

## Wired vs Wireless

| Feature | Wired | Wireless |
|---------|-------|----------|
| **Connection** | Cable (Ethernet) | Radio waves (WiFi, Bluetooth) |
| **Speed** | Faster (up to 10 Gbps) | Slower (up to 1-2 Gbps WiFi 6) |
| **Reliability** | Very stable | Can have interference |
| **Mobility** | Stuck to one place | Move anywhere in range |
| **Security** | Hard to hack (physical access needed) | Can be hacked if weak password |
| **Use** | Office desktops, servers | Phones, laptops, tablets |

---

## Network Devices

| Device | What It Does | Real Life Example |
|--------|-------------|-------------------|
| **Router** | Connects your network to the internet, directs traffic | Your WiFi box at home |
| **Switch** | Connects devices within a LAN, sends data only to destination | In office server rooms |
| **Hub** | Like a switch but sends data to ALL devices (old, rarely used) | Replaced by switches |
| **Modem** | Converts internet signal from ISP to digital signal | Cable/DSL modem from ISP |
| **Access Point** | Extends WiFi range | WiFi extender |
| **Firewall** | Blocks unauthorized access (security guard) | Hardware or software (Windows Firewall) |

### Home Network Diagram

```
[Internet] → [Modem] → [Router/WiFi] → [Your Phone]
                                      → [Your Laptop]
                                      → [Smart TV]
                                      → [Printer]
```

---

## IP Addresses

Every device on a network gets a unique address called an **IP address** (Internet Protocol address).

### IPv4 vs IPv6

| Feature | IPv4 | IPv6 |
|---------|------|------|
| **Format** | 4 numbers separated by dots | 8 groups of hex numbers |
| **Example** | `192.168.1.1` | `2001:0db8:85a3::8a2e:0370:7334` |
| **Total addresses** | ~4.3 billion | 340 trillion trillion trillion |
| **Status** | Running out! | Future-proof |

### Private vs Public IP

| Type | What It Is | Example | Who Can See |
|------|-----------|---------|-------------|
| **Private IP** | Your device's address inside your network | 192.168.1.5 | Only your network |
| **Public IP** | Your router's address on the internet | 103.45.67.89 | Everyone on internet |

---

## DNS — The Phone Book of Internet

**DNS** = Domain Name System

Computers use IP addresses (numbers), but humans remember names. DNS converts names to numbers.

```
You type: www.google.com
DNS converts to: 142.250.183.206
Browser connects to: 142.250.183.206
You see: Google homepage
```

> **Think of DNS like a phone contact list.** You search "Mom" — phone dials 9876543210 for you.

---

## How the Internet Works (Simple Version)

1. You type `www.techpath.biz` in browser
2. Browser asks **DNS server**: "What's the IP of techpath.biz?"
3. DNS replies: "It's 103.x.x.x"
4. Browser sends request to that IP address
5. **Web server** at that IP sends back the webpage
6. Your browser **renders** (displays) the webpage

This entire process takes less than 1 second!

---

## Summary

- **Network** = computers connected to share data
- **PAN → LAN → MAN → WAN** (smallest to largest)
- **Star topology** is most common today
- **Router** connects you to internet, **Switch** connects devices in LAN
- **IP address** = unique device address (IPv4: 192.168.1.1)
- **DNS** converts website names to IP addresses
- Internet works by: DNS lookup → connect to server → get webpage

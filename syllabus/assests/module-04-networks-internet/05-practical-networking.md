# Practical Networking — Hands-On Skills

**Module 04 — Networks & Internet | Workplace Skills**

---

## Why This Matters

> "My internet is slow" — this is the #1 complaint in every office. If you can troubleshoot network issues, you're instantly the most valuable person in the room. This isn't theory — this is what you'll actually do at work.

---

## Understanding Your Home/Office Network

### What's Inside Your Router

```
Internet (ISP) → Modem → Router → Your devices
                              ├── Laptop (WiFi)
                              ├── Phone (WiFi)
                              ├── Desktop (Ethernet cable)
                              └── Smart TV (WiFi)
```

> 🖼️ **IMAGE:** A simple home network diagram showing ISP connection → modem → WiFi router in the center → lines going to laptop, phone, desktop (wired), and smart TV — each device labeled with connection type (WiFi/Ethernet)
> `home-network-diagram.png`

### Router vs Modem vs Switch

| Device | Job | Analogy |
|--------|-----|---------|
| **Modem** | Connects to ISP, converts signal | The front gate |
| **Router** | Directs traffic between devices | The traffic police |
| **Switch** | Connects multiple wired devices | A power strip for network |
| **Access Point** | Extends WiFi range | A WiFi booster |

---

## WiFi — What Every IT Person Must Know

### WiFi Standards

| Standard | Name | Max Speed | Range | Year |
|----------|------|-----------|-------|------|
| 802.11n | WiFi 4 | 600 Mbps | 70m | 2009 |
| 802.11ac | WiFi 5 | 3.5 Gbps | 35m | 2013 |
| 802.11ax | WiFi 6 | 9.6 Gbps | 30m | 2019 |
| 802.11be | WiFi 7 | 46 Gbps | 30m | 2024 |

### 2.4 GHz vs 5 GHz

| | 2.4 GHz | 5 GHz |
|-|---------|-------|
| **Speed** | Slower | Faster |
| **Range** | Longer (goes through walls) | Shorter |
| **Interference** | More (microwave, Bluetooth) | Less |
| **Best for** | Far rooms, IoT devices | Streaming, gaming, near router |

**Pro tip:** Most routers broadcast both. Connect to 5GHz when near the router, 2.4GHz when far away.

### Why Your WiFi is Slow — Checklist

| # | Check | Fix |
|---|-------|-----|
| 1 | Too far from router? | Move closer or get a WiFi extender |
| 2 | Too many devices connected? | Disconnect unused devices |
| 3 | Using 2.4GHz near the router? | Switch to 5GHz |
| 4 | Router placed on floor/behind furniture? | Place it high, in center of room |
| 5 | Neighbors on same WiFi channel? | Change channel in router settings |
| 6 | Router hasn't been restarted in months? | Restart it (unplug 30 sec) |
| 7 | ISP giving slow speed? | Run speedtest.net, call ISP if below plan |

---

## Network Tools You'll Use Daily

### 1. Ping — Is It Alive?

```cmd
ping google.com
```

```
Reply from 142.250.77.110: bytes=32 time=12ms TTL=117
Reply from 142.250.77.110: bytes=32 time=11ms TTL=117
Reply from 142.250.77.110: bytes=32 time=13ms TTL=117
Reply from 142.250.77.110: bytes=32 time=12ms TTL=117
```

| Result | Meaning |
|--------|---------|
| `time=12ms` | Response time — lower is better |
| `time=200ms+` | Slow connection |
| `Request timed out` | Server not reachable or firewall blocking |
| `TTL=117` | Time To Live — how many hops left |

**Troubleshooting with ping:**
```cmd
ping localhost          # Test your own network stack
ping 192.168.1.1        # Test router connectivity
ping 8.8.8.8            # Test internet (Google DNS)
ping google.com         # Test DNS + internet
```

If `8.8.8.8` works but `google.com` doesn't → DNS problem.

### 2. Traceroute — Where's the Problem?

```cmd
tracert google.com
```

Shows every "hop" (router) between you and the destination.

```
 1     1ms    1ms    1ms   192.168.1.1        ← Your router
 2    12ms   11ms   12ms   103.87.125.1       ← ISP router
 3    15ms   14ms   15ms   72.14.209.137      ← Google's network
 4    16ms   15ms   16ms   142.250.77.110     ← Google server
```

If a hop shows `* * * Request timed out`, that's where the problem is.

### 3. Speedtest

- Open browser → go to **speedtest.net** → Click "Go"
- Or use: **fast.com** (simpler, by Netflix)

| Measurement | Good For |
|-------------|----------|
| **Download** | Watching videos, loading websites |
| **Upload** | Video calls, uploading files |
| **Ping/Latency** | Gaming, real-time apps |

**What's good speed?**

| Speed | Can Do |
|-------|--------|
| 10 Mbps | Basic browsing, email |
| 25 Mbps | HD video streaming |
| 50 Mbps | Video calls + streaming simultaneously |
| 100+ Mbps | Multiple users, 4K, gaming |

### 4. Netstat — What's Connected?

```cmd
netstat -an
```

Shows all active connections on your machine.

```cmd
# Find what's using port 8000 (your FastAPI server)
netstat -ano | findstr :8000
```

### 5. NSLookup — Find IP of Any Website

```cmd
nslookup techpath.biz
```

Shows the IP address behind a domain name. Useful for DNS troubleshooting.

---

## IP Addresses — Practical Understanding

### Private vs Public IP

| | Private IP | Public IP |
|-|-----------|-----------|
| **Who assigns** | Your router | Your ISP |
| **Unique to** | Your local network | The entire internet |
| **Example** | 192.168.1.5 | 103.87.125.45 |
| **How to find** | `ipconfig` in CMD | Google "what is my IP" |
| **Changes?** | Can be fixed or dynamic | Usually changes (dynamic) |

> 🖼️ **IMAGE:** A diagram showing a house with 4 devices — each has a private IP (192.168.1.x) — all connecting through a router that has both a private IP (192.168.1.1) on the inside and a public IP (103.87.x.x) on the outside, connecting to the internet
> `private-vs-public-ip.png`

### Common Private IP Ranges

```
192.168.0.x  to  192.168.255.x  → Home/small office
10.0.0.x     to  10.255.255.x   → Large organizations
172.16.0.x   to  172.31.255.x   → Medium organizations
```

### Static vs Dynamic IP

| | Static IP | Dynamic IP (DHCP) |
|-|-----------|-------------------|
| **Changes?** | No — always same | Yes — changes periodically |
| **Set by** | Admin manually | Router automatically |
| **Used for** | Servers, printers | Regular devices |
| **Cost** | More expensive (ISP) | Included with plan |

---

## How Email Actually Works (Behind the Scenes)

```
You (Gmail) → SMTP → Gmail Server → Internet → 
→ Recipient's Server (Yahoo) → POP3/IMAP → Recipient (Yahoo Mail)
```

| Protocol | Job | Port |
|----------|-----|------|
| **SMTP** | Sends email | 587 (TLS) or 465 (SSL) |
| **POP3** | Downloads email (removes from server) | 995 |
| **IMAP** | Syncs email (keeps on server) | 993 |

**POP3 vs IMAP:**
- POP3 = Downloads to one device → deleted from server (old method)
- IMAP = Syncs across all devices → stays on server (modern, use this)

---

## How Websites Load — Step by Step

What happens when you type `www.techpath.biz` in your browser:

```
1. Browser checks cache — "Do I already know this?"
2. If not, asks OS DNS cache
3. If not, asks Router DNS cache
4. If not, asks ISP's DNS server
5. If not, asks Root DNS → .biz DNS → techpath.biz DNS
6. DNS returns IP address: 103.87.125.45
7. Browser connects to server at that IP (TCP handshake)
8. Browser sends HTTP request: GET /
9. Server processes request
10. Server sends back HTML, CSS, JS files
11. Browser renders the page
12. Browser loads images, fonts, scripts (more requests)
```

> 🖼️ **IMAGE:** Visual journey of a web request — browser icon → DNS resolver → server icon → response arrows back — each step numbered with a short label, showing the path data takes
> `how-websites-load.png`

This entire process takes about 0.5-3 seconds!

---

## Practice Exercises

### Exercise 1: Network Diagnosis Report
On your own network, run these and write a report:
1. `ipconfig` → Note your IP, subnet mask, gateway
2. `ping google.com` → Note average response time
3. `tracert google.com` → How many hops? Any slow ones?
4. speedtest.net → Download, Upload, Ping
5. Google "what is my IP" → Note your public IP

### Exercise 2: WiFi Optimization
1. Check which WiFi band you're connected to (2.4 vs 5 GHz)
2. Walk to different rooms and run speedtest in each
3. Note how speed changes with distance
4. If possible, try Ethernet vs WiFi speed comparison

### Exercise 3: Troubleshooting Simulation
For each scenario, write the commands and steps:
1. "I can ping 8.8.8.8 but can't open google.com" → What's wrong?
2. "My internet was fast yesterday, today it's 2 Mbps" → Troubleshoot steps?
3. "One computer can access internet, another can't" → What to check?
4. "Website loads on phone but not on laptop" → Diagnosis?

# Module 04 — Assignment: Network Investigation

**Deadline:** End of Week 5
**Submission:** Report document with screenshots and command outputs

---

## Task 1: Map Your Home Network (30 marks)

1. Draw a diagram of your home/college network:
   - Internet → Modem → Router → Devices (list all connected devices)
   - Label each device with its type (laptop, phone, smart TV, etc.)
2. Find your router's IP address (usually 192.168.1.1 or 192.168.0.1)
3. Find your device's private IP and public IP
4. How many devices are connected to your WiFi? (check router admin page or use Advanced IP Scanner)
5. What is your WiFi standard (WiFi 4/5/6)? What band (2.4 GHz / 5 GHz)?
6. Run a speed test (speedtest.net) — note Download, Upload, and Ping

---

## Task 2: Network Diagnostics (30 marks)

Run these commands in CMD and document each output:

1. `ipconfig /all` — Find: IPv4 address, Subnet Mask, Default Gateway, DNS Server, DHCP status
2. `ping google.com` — Note average response time
3. `ping 8.8.8.8` — If this works but `ping google.com` doesn't, what's the problem? (Answer: DNS)
4. `tracert google.com` — How many hops? Which hop has the highest latency?
5. `nslookup techpath.biz` — What IP does it resolve to?
6. `nslookup google.com 8.8.8.8` — This uses Google's DNS instead of your ISP's. Any difference?
7. `netstat -an | findstr ESTABLISHED` — How many active connections does your PC have right now?

---

## Task 3: OSI Model Application (20 marks)

For each scenario, identify which OSI layer is primarily involved:

1. You type `https://techpath.biz` in Chrome
2. Your WiFi router assigns your laptop an IP address
3. A web page's images are compressed as JPEG
4. Your email app maintains a session with Gmail
5. Data packets are routed through 12 routers to reach a server in Mumbai
6. Your Ethernet cable carries electrical signals
7. Chrome encrypts your login page with TLS
8. A switch forwards a frame based on MAC address

---

## Task 4: Cybersecurity Awareness (20 marks)

1. Check your email — find one actual spam/phishing email. Screenshot it and explain 3 red flags that identify it as phishing
2. Go to `haveibeenpwned.com` — check if your email has been in any data breaches. Screenshot the result
3. List 5 security practices you follow (or will start following) with explanations
4. Explain the difference between HTTP and HTTPS — why does it matter for an online banking site?

---

## Rubric

| Criteria | Excellent | Good | Needs Work |
|----------|----------|------|------------|
| Network diagram | Complete, accurate, labeled | Most devices, minor gaps | Incomplete or wrong |
| Command outputs | All 7 commands with analysis | 5-6 commands | Under 5 |
| OSI mapping | 7-8 correct | 5-6 correct | Under 5 |
| Security | Real phishing analysis, good practices | Generic answers | Copied from internet |

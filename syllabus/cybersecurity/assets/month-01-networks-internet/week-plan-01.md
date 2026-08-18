# Month 1 — Week-by-Week Study Plan
## Networks & The Internet: TCP/IP, OSI, TLS, DNS, Protocols

**Total study time: ~80 hours over 4 weeks**
Each day assumes ~3-4 hours of focused study (mornings) + 1-2 hours of hands-on practice (evenings).

---

## Week 1 — Foundations: How the Internet Actually Works

**Goal:** Understand the OSI model, TCP/IP stack, and the lifecycle of a single network packet.

### Day 1 — The Big Picture
- **Read:** `01-tcp-ip-osi-model.md` — first half (OSI model layers 1-4)
- **Watch:** "How the Internet Works" — Computer Science Crash Course (YouTube, free)
- **Hands-on:** Draw the OSI model from memory. Write one protocol at each layer.
- **Task:** Open a terminal. Run `ping 8.8.8.8 -c 4` and explain what each line of output means in terms of OSI layers
- **Vocabulary drill:** Define these 10 terms without looking: frame, packet, segment, socket, encapsulation, MAC address, IP address, port, TTL, subnet mask

### Day 2 — TCP/IP Deep Dive
- **Read:** `01-tcp-ip-osi-model.md` — second half (TCP three-way handshake, IP routing)
- **Hands-on:** Install Wireshark (free). Open it, select your network interface, browse to a website
- **Exercise:** In Wireshark, filter for `tcp.flags.syn == 1` — find a TCP handshake and identify the SYN, SYN-ACK, ACK packets
- **Draw:** The TCP three-way handshake from memory. Label: sequence numbers, flags, what each party does
- **Question to answer:** Why does TCP need a three-way handshake? Why not two steps? Why not four?

### Day 3 — Application Layer Protocols
- **Read:** `02-tls-dns-protocols.md` — DNS section
- **Hands-on DNS:**
  ```bash
  nslookup google.com
  dig google.com A          # A record (IPv4)
  dig google.com AAAA       # AAAA record (IPv6)
  dig google.com MX         # Mail exchange records
  dig -x 8.8.8.8            # Reverse DNS lookup
  ```
- **Wireshark task:** Filter `dns` in Wireshark while browsing. Find a DNS query and response. What is the transaction ID? What record type was requested?
- **Experiment:** Run `dig google.com @1.1.1.1` (query Cloudflare DNS directly). Then `dig google.com @8.8.8.8` (Google DNS). Do you get the same IPs?

### Day 4 — TLS and HTTPS
- **Read:** `02-tls-dns-protocols.md` — TLS/HTTPS section
- **Hands-on TLS investigation:**
  ```bash
  # Inspect a TLS certificate
  openssl s_client -connect google.com:443 -showcerts
  # Check TLS version and cipher suite
  nmap --script ssl-enum-ciphers -p 443 google.com
  ```
- **Browser task:** Click the padlock icon on any HTTPS website → Certificate → Details. Record: issuer, subject, valid dates, signature algorithm, public key size
- **Question:** What is the difference between TLS 1.2 and TLS 1.3? Why does TLS 1.3 require only 1 round-trip for handshake vs TLS 1.2's 2?
- **Security task:** Visit `badssl.com` — try clicking "expired" and "self-signed" links. What does your browser warn you about?

### Day 5 — Network Tools Mastery
- **Read:** `notes-01.md` and `cheatsheet-01.md` — full review
- **Tool deep-dive: Nmap**
  ```bash
  # Basic host discovery
  nmap -sn 192.168.1.0/24         # Ping scan (no port scan)
  nmap -sV 192.168.1.1            # Service version detection
  nmap -sS -p 1-1000 192.168.1.1  # TCP SYN scan, ports 1-1000
  nmap -A -p 80,443 scanme.nmap.org  # Aggressive scan on web ports
  ```
- **Wireshark task:** Capture an nmap scan in Wireshark. Can you see the SYN packets being sent to multiple ports? What does an open port response look like vs a closed port?
- **Weekly review:** Complete quiz questions 1-7 (first half of quiz). Check your answers. Re-read any topic you got wrong.

---

## Week 2 — Protocols, Packets, and Practical Tools

**Goal:** Develop fluency with Wireshark, learn protocol analysis, and understand common network attacks.

### Day 6 — Wireshark Professional Usage
- **Lab:** Complete `lab-01-a.json` fully — all 5 steps
- **Advanced Wireshark filters:**
  ```
  ip.src == 192.168.1.1              # Traffic from specific IP
  tcp.port == 443                    # HTTPS traffic only
  http.request.method == "POST"      # HTTP POST requests
  dns.qry.name contains "google"     # DNS queries for Google
  tcp.analysis.retransmission        # TCP retransmissions (slow connection indicator)
  http.response.code == 404          # 404 Not Found responses
  ```
- **Challenge:** Download a sample pcap from Wireshark's wiki (wireshark.org/docs/dfref/). Open it and answer: What protocols are in use? What IP addresses are communicating? Is there anything suspicious?

### Day 7 — Subnetting Mastery
- **Deep dive into IP addressing:**
  - Binary conversion: convert 192.168.10.50 to binary
  - CIDR notation: what does /24 mean? /16? /28?
  - Calculate: for 192.168.1.0/26, what is the network address, broadcast address, and how many usable host addresses?
- **Subnetting practice (do all of these):**
  1. A company needs 6 subnets, each supporting 30 hosts. What CIDR block do they need?
  2. You have 10.0.0.0/8. Divide it into 4 equal subnets. What are they?
  3. Is 172.16.100.200 in the same subnet as 172.16.100.150/25?
- **Tool:** Use `ipcalc` or online subnet calculator to verify your answers

### Day 8 — Routing and Switching Deep Dive
- **Study topics:** Static routes, dynamic routing (OSPF, BGP basics), ARP, VLAN
- **Hands-on ARP:**
  ```bash
  arp -a                              # Show ARP cache
  arp -n                              # Numeric format
  # In Wireshark: filter "arp"
  # See who is broadcasting "Who has 192.168.1.1? Tell 192.168.1.100"
  ```
- **ARP spoofing awareness:** Research how ARP spoofing works (without doing it). Draw a diagram showing: legitimate ARP flow, then how an attacker could poison the ARP table
- **VLAN exercise:** Why do enterprises use VLANs? Draw a network with 3 VLANs (Finance, HR, Engineering) and explain what traffic can and cannot cross VLAN boundaries without a router

### Day 9 — HTTP/HTTPS Protocol Analysis
- **HTTP deep dive:**
  ```bash
  # Use curl to inspect HTTP headers
  curl -I https://example.com                    # Headers only
  curl -v https://example.com 2>&1 | head -50   # Verbose including TLS
  curl -L http://example.com                     # Follow redirects
  ```
- **Wireshark HTTP filter task:** Browse to a non-HTTPS site (filter `http`). Find a GET request. Identify: request method, Host header, User-Agent, Accept headers, status code in response
- **Security headers analysis:** Use securityheaders.com to scan any website. What headers are missing? What do Content-Security-Policy and X-Frame-Options do?

### Day 10 — Lab Day + Mid-Month Assessment
- **Complete:** `lab-01-b.json` fully — all 5 steps
- **Assessment:** Complete the full `quiz-01.json` (all 15 questions) without notes. Score yourself
- **Review:** For every question you got wrong, go back to the relevant section and re-read it
- **Self-test:** Without looking at your notes, draw a diagram showing what happens when you type "https://example.com" in a browser and press Enter. Include: DNS resolution, TCP connection, TLS handshake, HTTP GET, server response. Aim for 20+ specific steps

---

## Week 3 — Applied Network Security

**Goal:** Understand how attackers use network protocols, practice packet analysis, build a network diagram.

### Day 11 — Network Attack Techniques (Theory)
- **Study topics:**
  - Port scanning (how Nmap works under the hood)
  - SYN flood attacks (why SYN without ACK overwhelms servers)
  - DNS poisoning (how Kaminsky attack worked)
  - Man-in-the-middle via ARP spoofing
  - Packet sniffing in promiscuous mode
- **Research task:** Look up CVE-2008-1447 (the Kaminsky DNS bug). What was the vulnerability? How was it discovered? What was the fix?
- **Defence mapping:** For each attack above, write the specific defence (e.g., SYN flood → SYN cookies, rate limiting, firewall rules)

### Day 12 — Network Forensics
- **Download and analyse:** Wireshark sample capture "http.cap" from Wireshark's sample captures page
- **Answer these questions from the pcap:**
  1. What is the source IP and destination IP of the HTTP session?
  2. What HTTP method was used?
  3. What was the URL requested?
  4. What was the server's response code?
  5. Can you extract any data from the HTTP response (hint: File → Export Objects → HTTP)?
- **Challenge capture analysis:** Download "telnet-raw.pcap" from the Wireshark samples. Find the username and password transmitted in cleartext. This demonstrates why Telnet was replaced by SSH.

### Day 13 — Firewall Rules and Network Segmentation
- **Study:** Stateful vs stateless firewalls, ACLs, DMZ architecture
- **Design task:** A company has: web servers (must be public), database servers (must only talk to app servers), internal users, and a payment processing system
  - Draw a network diagram with firewalls
  - Write 8 firewall rules (allow/deny with source, destination, port, protocol) that enforce the policy
  - Explain where you would place IDS/IPS sensors
- **Linux firewall hands-on:**
  ```bash
  # View current rules (Linux)
  sudo iptables -L -v -n
  sudo iptables -L -v -n --line-numbers
  # See what's listening
  ss -tlnp     # or netstat -tlnp
  ```

### Day 14 — VPN, Encryption in Transit, Zero Trust
- **Study:** VPN types (IPSec vs SSL/TLS VPN), split tunnelling risks, Zero Trust Network Access (ZTNA)
- **SSH deep dive:**
  ```bash
  # Generate SSH key pair
  ssh-keygen -t ed25519 -C "your_email@example.com"
  # Test SSH with verbose output to see the handshake
  ssh -v user@hostname
  # Secure SSH configuration (/etc/ssh/sshd_config)
  # Study: PermitRootLogin no, PasswordAuthentication no, AllowUsers, Protocol 2
  ```
- **Research:** What is Zero Trust? How is it different from perimeter-based security ("castle and moat")? Write a 200-word explanation a non-technical manager could understand.

### Day 15 — Network Interactive Lab + Practice
- **Complete:** `network-explorer-interactive.html` — work through all 3 panels
- **Complete:** `exercises-01.md` — questions 1-15
- **Portfolio work:** Write a 500-word "Network Security Analysis" entry for your GitHub portfolio. Include: a diagram of a simple network you've set up/studied, key protocols, one vulnerability and its defence

---

## Week 4 — Mastery, Assessment, and Portfolio

**Goal:** Consolidate knowledge, complete the assignment, and produce a portfolio artefact.

### Day 16 — Assignment Task 1
- **Complete:** `assignment-01.md` Task 1 — Wireshark Packet Analysis
- **Submit** your pcap analysis with annotated screenshots

### Day 17 — Assignment Task 2
- **Complete:** `assignment-01.md` Task 2 — Network Scanning Lab
- **Document** your nmap results with explanations

### Day 18 — Assignment Task 3
- **Complete:** `assignment-01.md` Task 3 — Protocol Investigation
- **Write** your HTTP/DNS analysis report

### Day 19 — Assignment Task 4 + Portfolio
- **Complete:** `assignment-01.md` Task 4 — Firewall Rule Design
- **GitHub:** Push all your lab outputs, pcap screenshots, diagrams to your portfolio repo under `/month-01-networks/`

### Day 20 — Final Assessment and Review
- **Complete:** `exercises-01.md` — questions 16-25
- **Final quiz attempt:** Redo `quiz-01.json` with notes allowed. You should score 14-15/15
- **Review session:** Read `resources-01.md` — visit at least 3 of the resources listed
- **Reflection:** Write 5 bullet points: what were the 5 most important things you learned this month? What surprised you most?
- **Next month prep:** Read the first 2 pages of `notes-02.md` to get a preview of Month 2 topics

---

## Monthly Competency Checklist

Before moving to Month 2, confirm you can do these WITHOUT looking at your notes:

- [ ] Draw the OSI 7-layer model with 2 example protocols at each layer
- [ ] Explain what happens (15+ steps) when you open a web browser and visit a site
- [ ] Calculate the subnet, broadcast address, and usable range for any /24, /25, /26 or /28 network
- [ ] Open Wireshark, capture traffic, and filter to show only DNS or only HTTPS traffic
- [ ] Explain what a TCP three-way handshake is and why it's needed
- [ ] Describe how TLS protects data in transit and what a certificate does
- [ ] Explain ARP and why ARP spoofing is a risk
- [ ] Run `nmap -sV` against a target and interpret the output
- [ ] Explain the difference between TCP and UDP and give 3 use cases for each
- [ ] Describe the difference between a stateful and stateless firewall

**Minimum score to progress:** 8/10 checklist items completed confidently

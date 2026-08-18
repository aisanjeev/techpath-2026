# Month 1 Assignment — Networks & Internet
**Total marks: 100 | Deadline: End of Week 4**
Submit a single PDF with all tasks included. Label each task clearly.

---

## Task 1: Wireshark Traffic Analysis (35 marks)

**Objective:** Capture and annotate live network traffic to identify key protocols in action.

### Setup
Install Wireshark (wireshark.org). Start a capture on your active network adapter.

### Steps
1. Navigate to `http://neverssl.com` (unencrypted HTTP) in a browser.
2. Navigate to `https://example.com` (HTTPS/TLS).
3. Run `nslookup google.com` in a terminal to generate DNS traffic.
4. Stop the capture. Apply the filters listed below and take a labelled screenshot of each.

### Required Screenshots + Analysis
| # | Filter to Apply | What to Find & Document |
|---|----------------|------------------------|
| A | `dns` | The DNS query for your nslookup; identify: query type, queried name, TTL, returned IP |
| B | `tcp.flags.syn==1` | A 3-way handshake; label: SYN, SYN-ACK, ACK packets and source/dest ports |
| C | `tls` | The TLS Client Hello; list 3 cipher suites visible in the packet details |
| D | `http` | Any cleartext HTTP packet; explain what data was visible and why HTTPS prevents this |

### Written Questions (included in your PDF)
- Why does DNS use UDP by default but fall back to TCP?
- What does the "Certificate Verify" message in a TLS handshake accomplish?

### Rubric
| Criteria | Marks |
|---------|-------|
| DNS capture with correct record type identified | 8 |
| TCP 3-way handshake correctly labelled | 8 |
| TLS Client Hello — 3 cipher suites listed | 9 |
| HTTP vs HTTPS comparison with explanation | 5 |
| Written questions answered accurately | 5 |

---

## Task 2: Subnetting Exercise (25 marks)

**Objective:** Partition a network and calculate all address ranges without a calculator.

### Problem
You are a network engineer assigned the address block **`10.20.0.0/20`**.
Divide it into **4 equal subnets** and complete the table below.

| Subnet | New Prefix | Network Address | First Usable | Last Usable | Broadcast | Usable Hosts |
|--------|-----------|----------------|-------------|------------|-----------|-------------|
| A | | | | | | |
| B | | | | | | |
| C | | | | | | |
| D | | | | | | |

Show all working (identify new prefix length first, then calculate each block).

### Bonus (5 marks)
Install `ipcalc` on Linux (`sudo apt install ipcalc`) and verify one subnet with:
```bash
ipcalc 10.20.0.0/22
```
Include a screenshot of the output.

### Rubric
| Criteria | Marks |
|---------|-------|
| Correct new prefix length identified | 5 |
| All 4 network addresses correct | 8 |
| All 4 broadcast addresses correct | 6 |
| Usable host counts correct | 6 |
| Bonus: ipcalc verification | 5 |

---

## Task 3: TLS Certificate Chain Analysis (25 marks)

**Objective:** Inspect a real certificate hierarchy in your browser.

### Steps
1. Visit `https://wikipedia.org` (or any HTTPS site you choose).
2. Click the padlock icon → Certificate (or "Connection is secure" → Certificate details).
3. Navigate to the full certificate chain.

### Deliverable
For the **end-entity certificate** (the site's own cert) document:
- Common Name (CN) and Subject Alternative Names (SANs)
- Valid From and Valid Until dates
- Public key algorithm and key length (e.g., RSA 2048-bit)
- Signature algorithm
- Issuer (Intermediate CA name)

For the **complete chain**, list: End-Entity → Intermediate CA → Root CA names.

Include screenshots showing each level of the chain.

### Written Answer
In 3–5 sentences: Why do browsers not directly trust end-entity certificates issued by Root CAs without an intermediate? What operational problem does the intermediate CA solve?

### Rubric
| Criteria | Marks |
|---------|-------|
| All end-entity certificate fields documented | 10 |
| Full certificate chain listed correctly | 8 |
| Written answer explains intermediate CA purpose | 7 |

---

## Task 4: Port & Service Threat Assessment (15 marks)

**Objective:** Interpret a port scan and make security recommendations.

### Scenario
Your company hired a penetration tester who ran nmap on an externally-facing server and sent you this output:

```
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.2p1
80/tcp   open  http     nginx 1.18.0
443/tcp  open  ssl/http nginx 1.18.0
3306/tcp open  mysql    MySQL 8.0.27
6379/tcp open  redis    Redis 6.2.6
8080/tcp open  http     Apache Tomcat 9.0.50
```

### Questions (write your answers in the PDF)
1. Which two ports represent the most critical immediate risk? Explain why for each.
2. What does an externally accessible Redis instance (6379) enable an attacker to do?
3. Write 4 concrete hardening actions to address this scan. Be specific (include config or command examples where possible).
4. Which service version information in this output would most concern you, and why?

### Rubric
| Criteria | Marks |
|---------|-------|
| Two highest-risk ports identified with reasoning | 5 |
| Redis exposure risk explained correctly | 4 |
| 4 concrete hardening actions (specific, actionable) | 6 |

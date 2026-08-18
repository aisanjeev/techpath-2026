# Month 03 — Assignment: Security Fundamentals & Scripting

**Deadline:** End of Month 3 (Week 13)
**Submission:** GitHub repo link + PDF report
**Total:** 100 marks

---

## Task 1: Cryptography in Practice (25 marks)

Use CyberChef (https://gchq.github.io/CyberChef/) or Python to complete the following:

| # | Task | Tool |
|---|------|------|
| 1 | Compute the MD5, SHA-1, and SHA-256 hash of your full name (as plain text) | CyberChef or Python hashlib |
| 2 | Encode the text "cybersecurity2026" in Base64 | CyberChef or Python base64 |
| 3 | Encrypt the text "my secret message" using AES-256 (ECB mode) with key "0123456789abcdef0123456789abcdef" | CyberChef |
| 4 | Generate an RSA key pair (2048-bit) using OpenSSL and show the public key | `openssl genrsa 2048` + `openssl rsa -pubout` |

**Deliverable:** Screenshots of each operation showing inputs and outputs. Document in a PDF.

**Marking:**
- All 4 operations completed correctly: 25 marks
- 3 operations: 18 marks
- 2 operations: 12 marks

---

## Task 2: Python Security Script (35 marks)

Write a Python script called `log_analyser.py` that:

1. **Reads** a log file (you will create a sample `auth.log` with at least 50 lines)
2. **Counts** total failed SSH login attempts using regex
3. **Lists** the top 5 attacking IP addresses with their attempt counts
4. **Flags** any IP with more than 5 failed attempts as HIGH RISK
5. **Writes** a summary report to `report.txt`

**Sample log format (create this file):**
```
Aug 04 10:23:45 server sshd[1234]: Failed password for root from 192.168.1.100 port 54321 ssh2
Aug 04 10:23:47 server sshd[1235]: Failed password for admin from 10.0.0.50 port 54322 ssh2
Aug 04 10:23:49 server sshd[1236]: Accepted password for user1 from 172.16.0.5 port 54323 ssh2
```

**Marking:**
- Script runs without errors: 10 marks
- Correctly counts failed logins: 8 marks
- Top 5 IPs correctly identified: 8 marks
- HIGH RISK flagging works: 5 marks
- Output written to file: 4 marks

**Submit:** `log_analyser.py` + `auth.log` + `report.txt` on GitHub

---

## Task 3: Threat Classification (20 marks)

Read the following 5 scenarios. For each, identify: (a) attack type, (b) which CIA Triad property is violated, (c) one defence.

**Scenario 1:** An employee receives an email from "IT Support" asking them to click a link and enter their password to "verify their account."

**Scenario 2:** Malware on a server silently copies all customer database records and sends them to an external IP.

**Scenario 3:** An attacker floods a web server with millions of requests, making it unavailable to real users.

**Scenario 4:** A USB drive labelled "Salary Information" is left in the company car park. An employee plugs it in and malware installs itself.

**Scenario 5:** An attacker intercepts network traffic between a bank's website and a customer, reading and modifying the data in transit.

**Marking:** 4 marks per scenario (attack type 1 + CIA 1 + defence 2)

---

## Task 4: CompTIA Security+ Progress (20 marks)

1. Complete at least **2 full practice tests** from a Security+ prep resource (Professor Messer, Jason Dion, or Examtopics)
2. **Screenshot your score** for each test attempt
3. For every **wrong answer**, write a one-sentence explanation of the correct answer in a notes document
4. List **5 topics you found hardest** and the resources you used to understand them

**Marking:**
- 2 practice tests with screenshots: 10 marks
- Wrong-answer notes completed: 6 marks
- 5 hard topics documented with resources: 4 marks

---

## Rubric

| Criteria | Excellent | Good (75%) | Needs Work (50%) |
|----------|-----------|------------|-----------------|
| Crypto tasks | All 4 correct with screenshots | 3 of 4 correct | 2 or fewer correct |
| Python script | Runs perfectly, all features | Minor bugs, main logic works | Script errors or incomplete |
| Threat analysis | All 5 scenarios correct | 3-4 correct | 1-2 correct |
| Security+ prep | 2 tests + notes + 5 topics | 1 test + partial notes | No tests done |

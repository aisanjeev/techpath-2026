# Month 8 — Web Application Security: Assignment

**Total Marks: 100**
**Submission:** PDF report with screenshots. Due end of Month 8 Week 4.

---

## Setup

Install both practice targets before starting:

```bash
# DVWA (via Docker)
docker run -d -p 80:80 vulnerables/web-dvwa

# OWASP Juice Shop (via Docker)
docker run -d -p 3000:3000 bkimminich/juice-shop

# Configure Burp Suite proxy at 127.0.0.1:8080
```

---

## Task 1 — SQL Injection (25 marks)

Using DVWA (set security level to **Low**, then **Medium**):

1. Identify the SQL injection vulnerable parameter in the "SQL Injection" module
2. Determine the number of columns using `ORDER BY` or `NULL` technique
3. Perform a UNION-based injection to extract the database name and user
4. Extract usernames and password hashes from the `users` table
5. Attempt to crack one password hash offline (MD5)

**Then repeat on Medium security level** and document how the application partially defends against SQLi and how you bypassed the defence.

**Deliverables:**
- Screenshots of each injection step with the payload used
- Extracted credentials table (username + hash + cracked password)
- Explanation of the bypass technique used for Medium difficulty

---

## Task 2 — Cross-Site Scripting (25 marks)

Using DVWA (all three XSS types) and **Juice Shop**:

1. Exploit **Reflected XSS** in DVWA: craft a URL that steals `document.cookie` when clicked
2. Exploit **Stored XSS** in DVWA: inject a payload into the guestbook that persists for all visitors
3. Find and exploit one **DOM-based XSS** in Juice Shop (hint: look at Angular template injection)
4. Demonstrate cookie theft by redirecting the cookie value to `http://127.0.0.1:9090/` (use a simple Python HTTP listener)

```bash
# Simple cookie catcher
python3 -m http.server 9090
```

**Deliverables:**
- Crafted XSS URL for reflected attack (full URL shown)
- Screenshot of stored XSS persisting after page refresh
- Cookie value captured in Python server output (screenshot)

---

## Task 3 — API Security Testing (35 marks)

Using **Juice Shop's REST API** (intercept with Burp Suite):

1. **BOLA/IDOR**: Register two accounts. Find an endpoint that returns user-specific data and access Account A's data using Account B's token. Document the vulnerable endpoint and response.

2. **JWT Analysis**: Capture your JWT after login. Decode it (use jwt.io or Burp Decoder). Document all claims. Attempt the `alg:none` attack to access a protected endpoint without a valid signature.

3. **Mass Assignment**: Find a registration or profile-update endpoint. Add undocumented fields to the JSON body (`role`, `isAdmin`, `credit`). Document which (if any) are accepted.

4. **Rate Limiting Test**: Use Burp Intruder to send 200 login attempts in rapid succession. Does the application block after N attempts? Screenshot the Intruder results grid showing responses.

**Deliverables:**
- Screenshots of each API test with request + response visible in Burp
- BOLA proof: two different responses for same endpoint with different tokens
- JWT decoded payload screenshot
- Intruder results showing rate limiting (or absence of it)

---

## Task 4 — Findings Report (15 marks)

Write a concise application security report covering your findings from Tasks 1-3.

**Structure:**
- Findings table (3 columns minimum: Vulnerability | OWASP Category | Severity | Remediation)
- For each finding: 2-3 sentences explaining the business risk
- Overall risk rating for the application (Critical/High/Medium/Low)

---

## Marking Rubric

| Task | Criteria | Marks |
|---|---|---|
| Task 1 | UNION injection with DB/table extraction | 10 |
| Task 1 | Credential dump + hash cracking | 10 |
| Task 1 | Medium security bypass explained | 5 |
| Task 2 | Reflected XSS with cookie theft URL | 8 |
| Task 2 | Stored XSS persisting after refresh | 8 |
| Task 2 | Cookie value captured in listener | 9 |
| Task 3 | BOLA/IDOR with two accounts demonstrated | 12 |
| Task 3 | JWT decoded + alg:none attempted | 10 |
| Task 3 | Rate limiting test results documented | 8 |
| Task 3 | Mass assignment result documented | 5 |
| Task 4 | Findings table with OWASP mapping | 5 |
| Task 4 | Business risk context per finding | 5 |
| Task 4 | Remediation quality | 5 |
| **Total** | | **100** |

---

> **Note:** All testing must be performed on local Docker containers. Do not test against live websites without explicit written authorisation.

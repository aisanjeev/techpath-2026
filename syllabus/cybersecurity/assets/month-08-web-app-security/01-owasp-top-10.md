# OWASP Top 10 — Web Application Vulnerabilities In Depth

## What is OWASP?

The Open Web Application Security Project (OWASP) is a non-profit foundation that publishes free resources on web application security. The OWASP Top 10 is the definitive reference for the most critical web application security risks, updated every few years based on real-world data from thousands of organisations.

The 2021 edition reflects a significant shift: three new categories were added (Insecure Design, Software Integrity Failures, SSRF), and Injection dropped from #1 to #3 — not because injection is less dangerous, but because Broken Access Control has become the most pervasive single category.

---

## A01 — Broken Access Control

**Root cause**: The application does not enforce what authenticated users are permitted to do.

Access control enforces policy so that users cannot act outside their intended permissions. Failures commonly result in unauthorised information disclosure, modification, or destruction of data, or performance of business functions outside the user's limits.

**Common manifestations:**
- IDOR (Insecure Direct Object Reference): `GET /api/invoices/1042` works for invoice 1041 too
- Forced browsing: accessing `/admin/users` without being an admin
- Privilege escalation: a customer accessing seller-only functionality
- CORS misconfiguration: allowing `Origin: null` or `Origin: *` on authenticated endpoints

**Exploitation example:**
```http
# Account A's order details
GET /api/orders/500 HTTP/1.1
Authorization: Bearer <account_a_token>

# Change order ID — does it return account B's order?
GET /api/orders/499 HTTP/1.1
Authorization: Bearer <account_a_token>
```

**Defence:** Deny by default. Enforce authorisation server-side on every request. Log access control failures. Test all API endpoints with another user's token before deploying.

---

## A02 — Cryptographic Failures

**Root cause**: Sensitive data exposed due to weak, missing, or incorrectly implemented cryptography.

**Common manifestations:**
- Passwords stored as MD5 or SHA1 (fast to crack, no salt)
- Sensitive data transmitted over HTTP (not HTTPS)
- Weak TLS configuration (SSLv3, TLS 1.0, RC4 cipher suites)
- Hardcoded encryption keys or secrets in source code
- Certificates not validated (hostname verification disabled)

**Why MD5/SHA1 are broken for passwords:**

MD5 computes in ~200 million operations per second on modern GPU hardware. With the rockyou wordlist (14 million entries), every password is cracked in seconds. bcrypt deliberately slows computation to ~100 hashes/second, making the same attack take years.

**Safe password storage:**
```python
import bcrypt

# Hash
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Verify
bcrypt.checkpw(password.encode(), hashed)
```

---

## A03 — Injection

**Root cause**: Untrusted data sent to an interpreter as part of a command or query.

SQL injection, command injection, LDAP injection, and XSS (a form of HTML injection) all share the same root cause: insufficient separation between data and code.

**SQL Injection attack chain:**
1. Identify injection point (error messages, boolean behaviour, time delays)
2. Determine query context (SELECT, INSERT, UPDATE, WHERE clause)
3. Enumerate columns, database names, table names
4. Exfiltrate data or achieve command execution (xp_cmdshell, UDF)

**Command Injection:**
```bash
# Vulnerable code (Python)
output = os.system("ping " + user_input)

# Attack: user_input = "8.8.8.8; cat /etc/passwd"
# Results in: ping 8.8.8.8; cat /etc/passwd

# Defence: avoid shell=True; use subprocess with list args
subprocess.run(["ping", "-c", "4", user_input], capture_output=True)
```

**Prevention:**
- Parameterised queries for all database interaction
- Input validation with strict allowlisting
- Use ORMs that parameterise by default
- Run processes with least-privilege database accounts

---

## A04 — Insecure Design

**Root cause**: Missing or ineffective security controls in the application design — not an implementation bug, but a design gap.

This category was added in 2021 to distinguish design-time failures from implementation-time failures. A correctly implemented insecure design cannot be patched — it must be redesigned.

**Examples:**
- Password reset via "secret questions" (guessable answers)
- No account lockout on login (enables brute force)
- Allowing users to upload arbitrary files without type validation
- Financial systems with no transaction approval for large amounts
- Retail systems with no rate limit on discount code usage

**Secure design practices:**
- Threat modelling: identify abuse cases alongside use cases
- Security requirements engineering: define non-functional security requirements
- Secure design patterns: fail securely, least privilege, defence-in-depth

---

## A05 — Security Misconfiguration

**Root cause**: Insecure default configurations, unnecessary features, or improperly configured permissions.

**Common manifestations:**
- Default admin credentials not changed (admin/admin, admin/password)
- Debug mode enabled in production (stack traces, verbose errors)
- Unnecessary HTTP methods enabled (TRACE, PUT on a read-only API)
- Cloud storage buckets publicly accessible
- Missing security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)

**Security headers quick reference:**

```http
Content-Security-Policy: default-src 'self'; script-src 'self'
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

---

## A10 — Server-Side Request Forgery (SSRF)

SSRF warrants special attention because it directly targets cloud infrastructure. When a web application fetches a remote resource on behalf of the user, an attacker can redirect that request to:

1. **Cloud IMDS**: `http://169.254.169.254/latest/meta-data/iam/security-credentials/` — returns AWS IAM keys
2. **Internal services**: databases, admin panels, message queues on 10.x.x.x or 172.16.x.x
3. **Localhost services**: Jenkins, Redis, Elasticsearch running on 127.0.0.1

**Filter bypass techniques:**

| Technique | Representation |
|---|---|
| Decimal IP | `http://2130706433/` (= 127.0.0.1) |
| Hex IP | `http://0x7f000001/` |
| IPv6 loopback | `http://[::1]/` |
| DNS rebinding | Point domain to public IP, then switch to 127.0.0.1 |
| URL redirect | `http://your-server.com/redirect?to=http://169.254.169.254/` |

**Defence:** Strict URL allowlisting; resolve DNS to IP and check against private ranges; use IMDSv2 on AWS (requires PUT token); deploy network-level egress filtering.

---

## Putting It Together — Secure Code Review

Reading code for security is a skill that pays dividends at every seniority level. Patterns to look for:

```python
# Dangerous patterns in Python
query = f"SELECT * FROM users WHERE id = {id}"        # SQLi
os.system(f"ping {host}")                              # CMDi
open(f"/uploads/{filename}")                           # Path traversal
pickle.loads(user_data)                                # Insecure deserialization
requests.get(user_supplied_url, allow_redirects=True)  # SSRF

# Safe equivalents
cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
subprocess.run(["ping", "-c", "1", host])
safe_path = os.path.join("/uploads", os.path.basename(filename))
json.loads(user_data)   # Prefer safe serialization formats
```

Regular code review using SAST tools (Semgrep, Bandit for Python, SonarQube) catches these patterns at commit time before they reach production.

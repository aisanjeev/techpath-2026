# API Security — Testing Modern Interfaces

## Why APIs Are a Unique Attack Surface

Modern applications communicate via APIs — REST, GraphQL, gRPC. APIs present distinct security challenges compared to traditional web applications:

- **Wider attack surface**: Mobile apps, partner integrations, internal microservices — all expose API endpoints that may not be visible in a browser
- **Less UI protection**: APIs skip many client-side controls (input masks, hidden fields) — testers interact with them directly via Burp or Postman
- **Version sprawl**: Old API versions (`/v1/`, `/v2/`) often stay live after newer ones are deployed, with weaker security

OWASP publishes a dedicated **API Security Top 10** that complements the web application Top 10.

---

## OWASP API Security Top 10 (2023)

| ID | Category | Core Issue |
|---|---|---|
| API1 | BOLA | Access other users' resources by changing object ID |
| API2 | Broken Auth | Weak tokens, no expiry, missing MFA |
| API3 | Broken Object Property Level Auth | Access/modify fields you shouldn't see |
| API4 | Unrestricted Resource Consumption | No rate limits, large payload attacks |
| API5 | Broken Function Level Auth | Access admin endpoints as regular user |
| API6 | Unrestricted Access to Sensitive Business Flows | Abuse business logic without rate limits |
| API7 | SSRF | API fetches attacker-controlled URLs |
| API8 | Security Misconfiguration | CORS, verbose errors, exposed debug endpoints |
| API9 | Improper Inventory Management | Undocumented or retired versions still active |
| API10 | Unsafe Consumption of APIs | Trusting third-party API responses |

---

## JWT (JSON Web Tokens) Deep Dive

### Structure

A JWT is three Base64URL-encoded sections separated by dots:

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9   <- Header
.eyJzdWIiOiIxMjM0NTY3ODkwIiwicm9sZSI6InVzZXIifQ  <- Payload
.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c  <- Signature
```

**Header**: `{"alg": "RS256", "typ": "JWT"}`
**Payload**: `{"sub": "user123", "role": "user", "iat": 1700000000, "exp": 1700003600}`
**Signature**: HMAC-SHA256 or RSA-SHA256 of `header.payload`

### Common JWT Attacks

**1. Algorithm None:**
```python
# Forged token — server might accept if alg validation is missing
header = base64url({"alg": "none", "typ": "JWT"})
payload = base64url({"sub": "user123", "role": "admin"})
token = header + "." + payload + "."   # No signature
```

**2. Secret Brute-force (HS256):**
```bash
# If HMAC is used, try cracking the secret
hashcat -a 0 -m 16500 jwt.txt wordlist.txt

# Or: john with jwt2john
python jwt2john.py token.txt > hash.txt
john hash.txt --wordlist=rockyou.txt
```

**3. RS256 → HS256 Key Confusion:**
If the server uses RS256 but accepts HS256, use the RS256 public key as the HMAC secret. The public key is often retrievable from `/.well-known/jwks.json`.

**4. jwks Injection:**
Some servers accept a `jku` or `kid` claim pointing to a JWKS endpoint. Host your own JWKS and forge a token signed with your private key.

---

## BOLA/IDOR in REST APIs

BOLA (Broken Object Level Authorization) is the #1 API risk. The pattern:

```
# Your resource
GET /api/v1/users/1001/documents/55

# Another user's resource — server should return 403
GET /api/v1/users/1001/documents/54
```

### Discovery Checklist

- All GET/PUT/DELETE endpoints with an ID in the path or query string
- Endpoints that accept `user_id`, `account_id`, `order_id` in the body
- File download endpoints with a filename or file ID parameter
- Referential endpoints: `/api/users/me/baskets` → try changing `me` to a number

### Automating IDOR Tests

In Burp Intruder, mark the object ID as the payload position and use a numeric sequence:

```
Payload type: Numbers
From: 1
To: 2000
Step: 1
```

Filter results by response length or status code — 200s with different lengths indicate IDOR.

---

## GraphQL Security Testing

GraphQL exposes a single endpoint (`/graphql`) but with a powerful query language. Key tests:

**1. Introspection (should be disabled in production):**
```graphql
{
  __schema {
    types {
      name
      fields {
        name
        type {
          name
        }
      }
    }
  }
}
```

**2. Batching attack (rate limit bypass):**
```json
[
  {"query": "mutation { login(email: \"admin@test.com\", password: \"pass1\") { token } }"},
  {"query": "mutation { login(email: \"admin@test.com\", password: \"pass2\") { token } }"},
  {"query": "mutation { login(email: \"admin@test.com\", password: \"pass3\") { token } }"}
]
```

One HTTP request sends 100 login attempts, bypassing per-request rate limiting.

**3. IDOR in GraphQL — object IDs in query variables:**
```graphql
query {
  user(id: "1041") {
    email
    phone
    creditCard
  }
}
```

---

## Postman for API Security Testing

Postman is invaluable for API security testing beyond simple request replay:

### Environment Variables

```json
{
  "baseUrl": "http://localhost:3000",
  "token_a": "eyJ...",
  "token_b": "eyJ..."
}
```

### Pre-request Script (auto-refresh token)

```javascript
pm.request.headers.add({
  key: 'Authorization',
  value: 'Bearer ' + pm.environment.get('token_a')
});
```

### Test Script (assert security properties)

```javascript
// Fail if response contains a password field
const body = pm.response.json();
pm.test("No password field exposed", () => {
  pm.expect(body).to.not.have.property('password');
});

// Check for proper 403 on cross-user access
pm.test("Returns 403 for unauthorized object", () => {
  pm.response.to.have.status(403);
});
```

Run a **Postman Collection Runner** with both tokens to systematically test all endpoints for BOLA.

---

## Secure API Design Patterns

| Pattern | Implementation |
|---|---|
| Object ownership check | `if order.user_id != current_user.id: raise 403` |
| Field-level auth | Strip sensitive fields based on role before serialising |
| Pagination limits | `MAX_PAGE_SIZE = 100`; reject larger requests |
| Rate limiting | Per IP + per user; 429 with `Retry-After` header |
| JWT best practices | Short expiry (15m); rotate refresh tokens; validate `aud` and `iss` |
| API versioning | Retire old versions; audit traffic to `/v1/` monthly |
| GraphQL depth limiting | Reject queries deeper than 5 levels |

The shift from perimeter-based security to object-level authorisation checks is the single most impactful change an API development team can make.

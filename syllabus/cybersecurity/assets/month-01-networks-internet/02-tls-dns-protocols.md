# TLS, DNS, and Critical Protocols: What Travels in the Clear

## DNS: The Internet's Phone Book

The Domain Name System converts human-readable names into IP addresses. Despite being essential to every internet action, DNS was designed in 1983 with no authentication and no encryption — most DNS traffic today still travels in plaintext.

### DNS Hierarchy

```
Root (.)
├── .com (TLD)
│   ├── google.com (Second-Level Domain)
│   │   └── mail.google.com (Subdomain)
├── .org
├── .uk
└── .io
```

### Full DNS Resolution Walk-Through

```
Your PC → Local DNS Cache? → No
Your PC → Recursive Resolver (8.8.8.8)
  Resolver → Root NS: "Who handles .com?"
  Root NS  → Resolver: "Verisign TLD servers: a.gtld-servers.net"
  Resolver → TLD NS: "Who handles google.com?"
  TLD NS   → Resolver: "ns1.google.com, ns2.google.com"
  Resolver → Authoritative NS (ns1.google.com): "What is mail.google.com?"
  Auth NS  → Resolver: "142.250.x.x, TTL=300"
  Resolver → Your PC: "142.250.x.x"
```

The resolver caches each response for the TTL duration. Subsequent queries are answered instantly from cache.

### DNS Record Reference

| Type | Full Name | Maps | Example |
|------|-----------|------|---------|
| A | Address | Name → IPv4 | `example.com A 93.184.216.34` |
| AAAA | IPv6 Address | Name → IPv6 | `example.com AAAA 2606:2800::1` |
| CNAME | Canonical Name | Alias → name | `www CNAME example.com` |
| MX | Mail Exchanger | Domain → mail server | `example.com MX 10 mail.example.com` |
| TXT | Text | Domain → text string | SPF, DKIM, domain verification |
| NS | Name Server | Zone → authoritative NS | `ns1.provider.com` |
| PTR | Pointer | IPv4 → name (reverse DNS) | `34.216.184.93.in-addr.arpa PTR example.com` |
| SOA | Start of Authority | Zone metadata | Serial, refresh, retry, expire |
| SRV | Service | Service location | `_https._tcp.example.com SRV 443` |

### DNS Security Threats

| Attack | Description | Defence |
|--------|-------------|---------|
| DNS Cache Poisoning | Inject false records into resolver cache | DNSSEC, DNS-over-HTTPS |
| DNS Hijacking | Attacker controls DNS server | Monitor DNS changes, DNSSEC |
| DNS Tunnelling | Encode data in DNS queries to bypass firewalls | DNS query length anomaly detection |
| DNS Amplification DDoS | Spoof victim IP in DNS queries; large responses flood victim | BCP38 ingress filtering |
| Typosquatting | Register `googIe.com` (capital i) to trap users | Browser safe-browsing, training |

### Investigating DNS with Command-Line Tools

```bash
# Basic lookup
nslookup example.com
nslookup example.com 8.8.8.8       # Query specific resolver

# Detailed lookup with dig (Linux/Mac)
dig example.com A                   # A record
dig example.com MX                  # Mail records
dig example.com TXT                 # Text records (SPF/DKIM)
dig +trace example.com              # Full recursive trace
dig @1.1.1.1 example.com            # Query Cloudflare resolver

# Reverse DNS lookup
dig -x 93.184.216.34
nslookup 93.184.216.34
```

---

## HTTP: The Application Layer Workhorse

HTTP (HyperText Transfer Protocol) is the protocol browsers use to request and receive web pages. HTTP/1.1 is text-based and stateless.

### Request Structure

```
GET /login.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Cookie: session=abc123xyz
Accept: text/html
Connection: keep-alive
```

### Response Structure

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 4521
Set-Cookie: session=def456; Secure; HttpOnly; SameSite=Strict
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains

<!DOCTYPE html>...
```

### Common HTTP Status Codes (Security Relevance)

| Code | Meaning | Security Note |
|------|---------|--------------|
| 200 | OK | Normal success |
| 301/302 | Redirect | Check for open redirect vulnerabilities |
| 400 | Bad Request | Malformed input — probe for injection |
| 401 | Unauthorised | Auth required |
| 403 | Forbidden | Auth OK but no permission |
| 404 | Not Found | Enumeration — reveals what exists |
| 500 | Internal Server Error | May reveal stack traces |
| 503 | Service Unavailable | DDoS indicator |

---

## HTTPS and TLS/SSL: Encrypting the Web

TLS (Transport Layer Security) wraps HTTP to create HTTPS. It provides:
- **Confidentiality**: AES-256 symmetric encryption of the payload
- **Integrity**: HMAC ensures data wasn't tampered with
- **Authentication**: Server certificate proves identity

### TLS 1.3 Handshake (Modern, Fast, Secure)

```
Client                                    Server
  |------ ClientHello ------------------>|
  |   (TLS 1.3, cipher suites, key share,|
  |    server_name extension = SNI)       |
  |                                       |
  |<----- ServerHello --------------------|
  |<----- {Certificate} -----------------|  (encrypted)
  |<----- {CertificateVerify} -----------|  (encrypted)
  |<----- {Finished} --------------------|  (encrypted)
  |                                       |
  |------ {Finished} ------------------->|
  |====== Application Data (encrypted) ===|
```

TLS 1.3 completes in **1 round-trip** (vs 2 for TLS 1.2) and supports only forward-secret key exchange.

### TLS Versions and Cipher Suites

| TLS Version | Status | Notes |
|-------------|--------|-------|
| SSL 2.0/3.0 | BROKEN — disable | POODLE, DROWN attacks |
| TLS 1.0 | Deprecated (RFC 8996) | BEAST attack |
| TLS 1.1 | Deprecated (RFC 8996) | |
| TLS 1.2 | Acceptable | Disable weak ciphers (RC4, 3DES, NULL) |
| TLS 1.3 | Recommended | Only strong AEAD ciphers; forward secrecy mandatory |

### PKI Certificate Validation

When a browser receives a server certificate, it performs:
1. **Chain validation**: builds a path from server cert → Intermediate CA → Root CA
2. **Signature verification**: each cert is signed by the one above it
3. **Revocation check**: queries OCSP (Online Certificate Status Protocol) or checks CRL
4. **Name matching**: CN or SANs must match the domain in the URL
5. **Validity period**: not before / not after must encompass today's date

**Certificate Transparency (CT)**: All publicly-trusted certificates must be logged in public CT logs. This allows monitoring for rogue certificates issued for your domain.
```bash
# Check CT logs for your domain
curl "https://crt.sh/?q=example.com&output=json" | python3 -m json.tool
```

---

## Other Critical Protocols

### SSH (Secure Shell) — Port 22

SSH provides an encrypted channel for remote terminal access, file transfer (SCP/SFTP), and tunnelling.

```bash
ssh user@192.168.1.10                    # Password auth
ssh -i ~/.ssh/id_ed25519 user@host       # Key-based auth (preferred)
ssh -L 8080:internal-server:80 user@host # Local port forwarding (tunnel)
```

**Security best practice:** Disable password auth (`PasswordAuthentication no` in `/etc/ssh/sshd_config`), use Ed25519 keys, change from port 22 if exposed publicly, allow only specific users.

### SMTP/IMAP/POP3 — Email Protocols

| Protocol | Port | Purpose | Encrypted Port |
|----------|------|---------|---------------|
| SMTP | 25 | Server-to-server relay | 465 (SMTPS) / 587 (STARTTLS) |
| IMAP | 143 | Email access (folder sync) | 993 (IMAPS) |
| POP3 | 110 | Email download | 995 (POP3S) |

**Email authentication (anti-spoofing):**
- **SPF**: TXT record listing authorised sending IPs
- **DKIM**: Cryptographic signature on each email
- **DMARC**: Policy specifying what to do when SPF/DKIM fail (reject, quarantine, none)

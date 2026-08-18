# Cheat Sheet — Security Fundamentals + Scripting

**Month 03 | Quick Reference Card**

---

## Cryptography Quick Reference

| Type | Algorithm | Key | Speed | Use Case |
|------|-----------|-----|-------|----------|
| Hash | SHA-256 | N/A | Fast | File integrity, passwords |
| Hash | MD5 | N/A | Fast | Legacy only (broken) |
| Symmetric | AES-256 | 256-bit | Fast | Bulk data encryption |
| Asymmetric | RSA-2048 | 2048-bit | Slow | Key exchange, signing |
| Asymmetric | ECC-256 | 256-bit | Fast | TLS, mobile |

---

## Hash Values Reference
```
MD5    = 32 hex chars  (128 bits)
SHA-1  = 40 hex chars  (160 bits)
SHA-256 = 64 hex chars (256 bits)
SHA-512 = 128 hex chars (512 bits)
```

---

## MFA Factor Types

| Factor | Examples |
|--------|---------|
| Knowledge | Password, PIN, security question |
| Possession | TOTP app, SMS OTP, hardware token (YubiKey) |
| Inherence | Fingerprint, face scan, iris |
| Location | GPS geofencing, IP range |

**Strongest MFA:** Phishing-resistant hardware key (FIDO2/WebAuthn)

---

## Common Attack Acronyms

| Attack | What it means |
|--------|---------------|
| MITM | Man-in-the-Middle — intercepts traffic |
| ARP | Address Resolution Protocol spoofing |
| DNS | Domain Name System poisoning |
| DoS | Denial of Service |
| DDoS | Distributed DoS |
| SQLi | SQL Injection |
| XSS | Cross-Site Scripting |
| CSRF | Cross-Site Request Forgery |
| RCE | Remote Code Execution |
| LFI/RFI | Local/Remote File Inclusion |

---

## Malware Quick Reference

| Name | Self-replicates? | User action needed? | Hides? |
|------|-----------------|---------------------|--------|
| Virus | Yes (files) | Yes | Sometimes |
| Worm | Yes (network) | No | Sometimes |
| Trojan | No | Yes (install) | Yes |
| RAT | No | Yes | Yes |
| Rootkit | No | No | Yes (deeply) |
| Ransomware | Sometimes | Initial only | No |

---

## Python Security Snippets

```python
# SHA-256 hash
import hashlib
hashlib.sha256(b"data").hexdigest()

# Base64 encode/decode
import base64
base64.b64encode(b"secret")
base64.b64decode("c2VjcmV0")

# Regex — extract IPs from log
import re
re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', log_text)

# HTTP request
import requests
r = requests.get("https://target.com")
print(r.status_code, r.headers)

# Read JSON log
import json
with open('events.json') as f:
    events = json.load(f)
```

---

## Security+ Domain Weights (SY0-701)

```
General Security Concepts          12%
Threats, Vulnerabilities, Mitigations  22%
Security Architecture              18%
Security Operations                28%   ← heaviest
Security Program Management        20%
```

---

## Common Ports (Security Focus)

| Port | Protocol | Risk if open |
|------|----------|-------------|
| 21 | FTP | Cleartext credentials |
| 22 | SSH | Brute force |
| 23 | Telnet | Cleartext everything |
| 25 | SMTP | Spam relay |
| 53 | DNS | DNS poisoning |
| 80 | HTTP | Cleartext traffic |
| 443 | HTTPS | Usually safe |
| 445 | SMB | EternalBlue, ransomware |
| 3389 | RDP | Brute force, ransomware |
| 3306 | MySQL | DB exposure |

---

## Social Engineering — Defence

| Attack | Defence |
|--------|---------|
| Phishing | Email filtering, user training, MFA |
| Vishing | Call-back verification, do not give info to callers |
| Tailgating | Mantraps, badge access, challenge unknown people |
| Pretexting | Verification procedures, need-to-know policy |
| Baiting | USB restrictions, endpoint protection |

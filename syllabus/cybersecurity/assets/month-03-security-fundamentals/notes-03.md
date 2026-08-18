# Month 03 — Security Fundamentals + Scripting + Security+ — Quick Revision Notes

---

## Cryptography Essentials

### Hashing
- One-way function — cannot reverse the hash to get original data
- **MD5** — 128-bit, fast, broken (never use for security)
- **SHA-1** — 160-bit, deprecated, vulnerable to collisions
- **SHA-256** — 256-bit, current standard (used in TLS, Bitcoin)
- **SHA-3 / bcrypt / Argon2** — for password storage (bcrypt/Argon2 are slow by design)
- Use: file integrity checks, password storage, digital signatures

### Symmetric Encryption (same key for encrypt + decrypt)
| Algorithm | Key Size | Use |
|-----------|----------|-----|
| **AES-128** | 128-bit | Standard encryption |
| **AES-256** | 256-bit | High-security standard |
| **DES/3DES** | 56/168-bit | Legacy — do not use |
- Fast — suitable for bulk data encryption
- Problem: how do you share the key securely?

### Asymmetric Encryption (public + private key pair)
| Algorithm | Use |
|-----------|-----|
| **RSA** | Key exchange, digital signatures (2048-bit minimum) |
| **ECC** | Same security as RSA at smaller key size (ECDSA, ECDH) |
| **Diffie-Hellman** | Key exchange only — no encryption |
- Public key: share freely → anyone can encrypt TO you
- Private key: keep secret → only you can decrypt
- Slower than symmetric — used to exchange symmetric keys

### Digital Signatures
1. Sender hashes the message → signs hash with private key
2. Receiver decrypts signature with sender's public key → verifies hash matches
- Proves: **integrity** (not tampered) + **non-repudiation** (sender can't deny)

---

## Authentication & Identity

| Term | Meaning |
|------|---------|
| **Authentication** | Proving who you are (login) |
| **Authorisation** | What you're allowed to do (permissions) |
| **Accounting** | Recording what you did (audit logs) |

### MFA Factors
- **Something you know** — password, PIN
- **Something you have** — TOTP app (Google Authenticator), hardware key (YubiKey)
- **Something you are** — fingerprint, face, retina (biometrics)
- **Somewhere you are** — geolocation-based

### IAM Concepts
- **Principle of Least Privilege** — minimum access needed to do the job
- **Separation of Duties** — no single person has complete control
- **Privileged Access Management (PAM)** — controls admin accounts
- **Zero Trust** — "never trust, always verify" — no implicit trust even inside network

---

## Attack Types

### Malware Families
| Type | Behaviour |
|------|-----------|
| **Virus** | Attaches to files, spreads on execution |
| **Worm** | Self-replicates across network without user action |
| **Trojan** | Disguised as legitimate software |
| **RAT** | Remote Access Trojan — gives attacker control |
| **Ransomware** | Encrypts files, demands payment |
| **Rootkit** | Hides malware from OS/AV — deeply embedded |
| **Spyware** | Secretly collects data |
| **Keylogger** | Records keystrokes |
| **Adware** | Unwanted ads, often bundled |
| **Botnet** | Network of infected machines controlled remotely |

### Ransomware Kill Chain
1. Initial access (phishing / RDP brute force)
2. Establish persistence (scheduled task, registry)
3. Lateral movement (spread through network)
4. Data exfiltration (steal before encrypting — double extortion)
5. Deploy encryption payload
6. Ransom note

### Network Attacks
- **MITM (Man-in-the-Middle)** — intercept and relay traffic between two parties
- **ARP Spoofing** — sends fake ARP replies to associate attacker's MAC with victim's IP
- **DNS Poisoning** — corrupt DNS cache to redirect to malicious site
- **Replay Attack** — capture and resend valid authentication packets

### Social Engineering
| Technique | Description |
|-----------|-------------|
| **Phishing** | Mass email impersonating trusted entity |
| **Spear Phishing** | Targeted phishing (researched victim) |
| **Whaling** | Phishing targeting executives (CFO, CEO) |
| **Vishing** | Voice phishing (phone calls) |
| **Smishing** | SMS phishing |
| **Pretexting** | Fabricated scenario to extract information |
| **Baiting** | Lure victim (USB drop, fake download) |
| **Tailgating** | Physical — following someone through secure door |

---

## Python for Security

```python
# Hash a file
import hashlib
with open('file.txt', 'rb') as f:
    print(hashlib.sha256(f.read()).hexdigest())

# Simple port scanner
import socket
for port in range(1, 1025):
    s = socket.socket()
    s.settimeout(0.1)
    if s.connect_ex(('target', port)) == 0:
        print(f"Port {port} open")
    s.close()

# Parse log file for failed logins
import re
with open('/var/log/auth.log') as f:
    for line in f:
        if 'Failed password' in line:
            ip = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
            if ip: print(ip.group(1))
```

---

## Security+ Exam Domains (SY0-701)
1. General Security Concepts (12%)
2. Threats, Vulnerabilities, Mitigations (22%)
3. Security Architecture (18%)
4. Security Operations (28%)
5. Security Program Management & Oversight (20%)

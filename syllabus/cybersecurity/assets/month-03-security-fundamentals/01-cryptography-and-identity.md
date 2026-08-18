# Cryptography & Identity Management

## Why Cryptography Matters in Security

Every time you visit a website over HTTPS, your bank verifies your identity, or you download software and check its hash — cryptography is working. Without it:
- Passwords are stored as plaintext (one breach = all accounts compromised)
- Network traffic is visible to anyone on the same WiFi
- Files can be tampered with undetected
- Anyone can impersonate anyone

Cryptography solves: **confidentiality, integrity, and authenticity**.

---

## Hashing — The Digital Fingerprint

A hash function takes any input and produces a fixed-size output. Properties:
- **Deterministic** — same input always produces same output
- **One-way** — cannot reverse the hash to get the input
- **Avalanche effect** — tiny input change → completely different hash
- **Collision resistant** — hard to find two inputs with the same hash

### Common Hash Algorithms

| Algorithm | Output Size | Status | Use Today? |
|-----------|-------------|--------|------------|
| MD5 | 128-bit (32 hex) | Broken (collisions) | File checksums only — NOT security |
| SHA-1 | 160-bit (40 hex) | Deprecated (2017) | Legacy only |
| SHA-256 | 256-bit (64 hex) | Secure | TLS, code signing, certificates |
| SHA-3 | 256-512-bit | Secure | Alternative to SHA-2 |
| bcrypt | Variable | Secure + slow | Password storage |
| Argon2 | Variable | Secure + slow | Password storage (winner of PHC) |

**Why bcrypt/Argon2 for passwords?** Regular hashes are fast — a GPU can compute billions of SHA-256 hashes per second. bcrypt/Argon2 are intentionally slow and memory-hard, making brute-force attacks infeasible.

### Hashing in Practice

```bash
# Linux — hash a file
sha256sum /etc/passwd
md5sum suspicious_file.exe

# Python
import hashlib
hash = hashlib.sha256(b"password123").hexdigest()
# Output: ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
```

**Password Storage (correct way):**
```
User types: "password123"
bcrypt hash: $2b$12$LqhYOzR9g6HNXIFxHcEqfOBIJPjHJ6...
Stored in DB: only the hash, never the plaintext
```

---

## Symmetric Encryption — One Key, Two Roles

The same key encrypts and decrypts. Fast — used for bulk data.

```
Plaintext → [AES Encrypt + Key] → Ciphertext
Ciphertext → [AES Decrypt + Key] → Plaintext
```

### AES (Advanced Encryption Standard)
- Block cipher operating on 128-bit blocks
- Key sizes: 128-bit, 192-bit, 256-bit (AES-256 is the gold standard)
- **Modes of operation:**
  - **ECB** — each block encrypted independently (DO NOT USE — patterns leak)
  - **CBC** — each block XORed with previous (good, requires IV)
  - **GCM** — authenticated encryption (best — provides integrity too)
  - **CTR** — turns block cipher into stream cipher

**AES-256-GCM** is what modern TLS, disk encryption (BitLocker), and VPNs use.

### The Key Distribution Problem
If you and I want to communicate securely with AES, we need to agree on a key. How do we share it without an attacker intercepting it? This is where asymmetric encryption comes in.

---

## Asymmetric Encryption — Public/Private Key Pairs

Two mathematically linked keys:
- **Public key** — share freely with everyone
- **Private key** — never share, keep secret

```
Sender: encrypt with recipient's PUBLIC key
Recipient: decrypt with their own PRIVATE key
→ Only recipient can read the message
```

**Digital Signatures (reversed):**
```
Signer: sign/hash with their PRIVATE key
Verifier: verify with signer's PUBLIC key
→ Only signer could have created that signature
```

### RSA (Rivest-Shamir-Adleman)
- Security based on difficulty of factoring large prime products
- Key sizes: 2048-bit minimum (4096 for high security)
- Slow — used to establish keys, not encrypt large data
- **Hybrid encryption:** RSA encrypts a random AES key, AES encrypts the data

### ECC (Elliptic Curve Cryptography)
- Based on elliptic curve discrete logarithm problem
- 256-bit ECC ≈ security of 3072-bit RSA
- Faster and smaller keys — used in TLS 1.3, mobile apps, Bitcoin
- Variants: ECDSA (signing), ECDH (key exchange)

---

## How HTTPS Works (Putting It Together)

1. Browser connects to bank.com
2. Server sends its **TLS certificate** (contains public key + identity, signed by a CA)
3. Browser verifies the certificate against trusted Certificate Authorities
4. **ECDH key exchange** — both sides derive a shared session key (never transmitted)
5. All traffic encrypted with **AES-256-GCM** using that session key
6. A MAC (message authentication code) detects any tampering

---

## Authentication, Authorisation & MFA

### The AAA Framework
| Term | Question | Example |
|------|----------|---------|
| **Authentication** | Who are you? | Login with username + password |
| **Authorisation** | What can you do? | Admin vs regular user permissions |
| **Accounting** | What did you do? | Audit logs, SIEM events |

### Multi-Factor Authentication (MFA)

Combining two or more factor types:
- **Something you know** — password, PIN, security question
- **Something you have** — TOTP (Google Authenticator), SMS OTP, hardware key (YubiKey)
- **Something you are** — fingerprint, face scan, iris
- **Somewhere you are** — GPS geofencing

**TOTP (Time-based One-Time Password):**
```
Shared secret seed + current time → 6-digit code (valid 30 seconds)
Attacker needs both your password AND your phone → much harder to compromise
```

**Why SMS OTP is weak:** SIM swapping attacks, SS7 vulnerabilities. Prefer authenticator apps or hardware keys.

**FIDO2/WebAuthn (strongest):** Hardware key (YubiKey) or device biometric. Phishing-resistant — domain-bound, so fake sites can't harvest it.

### Identity & Access Management (IAM)

**Principle of Least Privilege:** Give users only the minimum permissions to do their job. A marketing employee shouldn't have database admin rights.

**Separation of Duties:** No single person should be able to perform a critical operation alone (e.g., initiating AND approving a bank transfer).

**Privileged Access Management (PAM):** Special controls for admin/root accounts:
- Just-in-time access (request elevation only when needed)
- Session recording of all admin activity
- Rotation of privileged credentials

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| Hashing | One-way fingerprint — SHA-256 for integrity, bcrypt for passwords |
| AES-256-GCM | Fast symmetric encryption — bulk data |
| RSA/ECC | Slow asymmetric — key exchange and signing |
| Digital signatures | Private key signs, public key verifies — proves integrity + authenticity |
| MFA | Always enable — hardware keys > TOTP > SMS |
| Least privilege | Users get minimum required access — limits blast radius |

# Month 3 — Practice Exercises: Security Fundamentals

**25 exercises with worked answers.**

---

## Section A: Cryptography (Questions 1-10)

**Q1.** You need to store user passwords in a database. A colleague suggests using MD5. Another suggests SHA-256. A third suggests bcrypt. Evaluate each option and recommend the best choice with justification.

**Answer:** MD5 is completely unsuitable — it's fast (attackers can compute billions of MD5 hashes per second on a GPU) and lacks salting by default. SHA-256 is better than MD5 but still too fast for password storage for the same reason. **bcrypt is correct.** It's specifically designed for password hashing: it's intentionally slow (configurable work factor), automatically generates and stores a unique salt per password, and its speed is adjustable — as hardware improves, you increase the work factor. Argon2 (winner of the Password Hashing Competition) is the modern alternative if bcrypt is unavailable. Rule: use a purpose-built password hashing function, never a general-purpose hash.

---

**Q2.** Explain the "avalanche effect" in hashing and demonstrate it with a Python calculation.

**Answer:** The avalanche effect means a tiny change in input produces a dramatically different output — roughly 50% of the bits change. This property ensures hashes can't be predicted or reversed.

```python
import hashlib

def bit_diff(h1, h2):
    # Convert hex to binary and count different bits
    b1 = bin(int(h1, 16))[2:].zfill(256)
    b2 = bin(int(h2, 16))[2:].zfill(256)
    return sum(a != b for a, b in zip(b1, b2))

h1 = hashlib.sha256(b"hello").hexdigest()
h2 = hashlib.sha256(b"hellp").hexdigest()  # One char different

print(f"hash1: {h1}")
print(f"hash2: {h2}")
diff = bit_diff(h1, h2)
print(f"Bits different: {diff}/256 ({diff/256*100:.1f}%)")
# Typical result: ~128 bits (50%) differ — even for 1-character change
```

---

**Q3.** What is a "salt" in the context of password hashing? Write a Python function that creates a salted hash and another that verifies it.

**Answer:** A salt is a random value unique to each password, prepended/appended before hashing. It ensures two users with the same password have different hashes, and defeats rainbow table attacks (pre-computed hash→plaintext tables).

```python
import hashlib, os, binascii

def hash_password(password: str) -> str:
    # Generate random 32-byte salt
    salt = os.urandom(32)
    # Hash: SHA-256(salt + password)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    # Store: hex(salt) + ":" + hex(hash)
    return binascii.hexlify(salt).decode() + ':' + binascii.hexlify(pwd_hash).decode()

def verify_password(password: str, stored: str) -> bool:
    salt_hex, hash_hex = stored.split(':')
    salt = binascii.unhexlify(salt_hex)
    # Recompute hash with same salt
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return binascii.hexlify(pwd_hash).decode() == hash_hex

# Test
stored = hash_password("MySecurePassword!")
print(f"Stored: {stored}")
print(f"Correct: {verify_password('MySecurePassword!', stored)}")
print(f"Wrong: {verify_password('WrongPassword', stored)}")
```

---

**Q4.** Explain what "Perfect Forward Secrecy" (PFS) means and how ECDHE achieves it in TLS. Why does it matter if a server's private key is compromised?

**Answer:** PFS ensures that if an attacker captures encrypted traffic today and later obtains the server's private key, they CANNOT retroactively decrypt the captured traffic. Without PFS (RSA key exchange): the server's private key IS the session key encryption key. Capture traffic now, steal key later → decrypt everything ever sent. With PFS (ECDHE): the server generates a fresh ephemeral Diffie-Hellman key pair for each session. The session key is derived from this ephemeral key exchange, not from the server's long-term private key. After the session ends, the ephemeral key is discarded. Even with the server's private key, the ephemeral keys are gone, so past sessions cannot be decrypted. TLS 1.3 mandates PFS — only ECDHE and DHE cipher suites are permitted.

---

**Q5.** A developer stores API keys in their code like this:
```python
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
db_password = "SuperSecret123!"
```
List 4 better approaches and explain the tradeoffs of each.

**Answer:**
1. **Environment variables** (`os.environ['AWS_ACCESS_KEY']`) — simple, works in most environments, but still visible in process list (`/proc/PID/environ`) and CI logs if printed. Good for basic secrets.
2. **`.env` files with `python-dotenv`** — keeps secrets out of code, but the file itself must not be committed to Git (use `.gitignore`). Good for development.
3. **Cloud secrets managers** (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) — secrets never touch code or filesystem, auto-rotation supported, audit log of every access, access controlled by IAM. Best practice for production.
4. **CI/CD platform secrets** (GitHub Actions Secrets, GitLab CI Variables) — injected as environment variables at runtime, not visible in code or logs. Good for CI pipelines.

**Never:** check credentials into Git. Even a private repo — commits are permanent, repos can leak, team members leave.

---

**Q6.** Compare RSA-2048 and ECC P-256 for asymmetric encryption. Which would you choose for a TLS certificate and why?

**Answer:**
| Property | RSA-2048 | ECC P-256 |
|---------|---------|---------|
| Key size | 2048 bits | 256 bits |
| Equivalent security | ~112 bits | ~128 bits |
| Performance | Slow (modular exponentiation) | Fast (elliptic curve operations) |
| Certificate size | Large | Smaller |
| Browser support | Universal | Modern browsers (IE11+) |

**Recommendation: ECC P-256** for TLS certificates.
- Equivalent or better security with much smaller key size
- Faster TLS handshakes (important for mobile clients and IoT)
- ECDSA signatures are faster than RSA for signing operations
- TLS 1.3 explicitly favours ECDHE key exchange

---

**Q7.** You find a file on a server: `hashes.txt` containing:
```
5f4dcc3b5aa765d61d8327deb882cf99
e10adc3949ba59abbe56e057f20f883e
827ccb0eea8a706c4c34a16891f84e7b
```
What hash algorithm is this? What are these passwords? What does this demonstrate about MD5?

**Answer:** These are MD5 hashes (32 hex characters = 128 bits). Crack them using any online MD5 lookup table (e.g., crackstation.net):
- `5f4dcc3b5aa765d61d8327deb882cf99` → `password`
- `e10adc3949ba59abbe56e057f20f883e` → `123456`
- `827ccb0eea8a706c4c34a16891f84e7b` → `12345678`

This demonstrates that MD5 is completely unsuitable for password storage. These are among the most common passwords in the world — they've been pre-computed into massive lookup tables (rainbow tables). An attacker with a breached MD5 password database can crack 90%+ of hashes in seconds using these tables.

---

**Q8.** Write a Python script that checks if a given password has been seen in known data breaches using the Have I Been Pwned (HIBP) k-Anonymity API — without sending the actual password.

**Answer:**
```python
import hashlib, requests

def check_pwned_password(password: str) -> int:
    """Returns number of times password has appeared in breaches. 0 = not found."""
    # Hash the password with SHA-1
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    
    # Send only the first 5 characters (k-anonymity — HIBP never sees full hash)
    prefix = sha1[:5]
    suffix = sha1[5:]
    
    # Query HIBP API
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    # Parse response: "SUFFIX:COUNT" lines
    for line in response.text.splitlines():
        hash_suffix, count = line.split(':')
        if hash_suffix == suffix:
            return int(count)
    
    return 0  # Not found in breaches

# Test (safe — password never sent to HIBP)
passwords = ["password", "MyStr0ngP@ssw0rd!", "P@ssw0rd123"]
for pwd in passwords:
    count = check_pwned_password(pwd)
    if count > 0:
        print(f"'{pwd}': PWNED! Seen {count:,} times in breaches")
    else:
        print(f"'{pwd}': Not found in known breaches")
```

---

**Q9.** Explain the CIA Triad. For each of these incidents, identify which element of the CIA Triad was violated:
a) Ransomware encrypts all files on a server  
b) A hacker reads customer records without modifying them  
c) A DDoS attack takes a website offline for 4 hours  
d) An attacker modifies a bank transaction amount from £100 to £10,000

**Answer:** CIA Triad: Confidentiality (only authorised parties access data), Integrity (data is accurate and unmodified), Availability (systems are accessible when needed).
a) Ransomware: **Availability** — files are inaccessible. Also potentially Integrity (encrypted = corrupted from the owner's perspective).
b) Reading records: **Confidentiality** — unauthorised person viewed private data. Integrity and Availability may be intact.
c) DDoS: **Availability** — website unreachable for 4 hours. C and I may be intact (data wasn't stolen or modified).
d) Transaction modification: **Integrity** — the data (amount) was altered without authorisation. Potentially Confidentiality (they accessed the transaction) but the primary violation is Integrity.

---

**Q10.** What is a digital certificate and what problem does it solve? Explain the difference between DV, OV, and EV certificates.

**Answer:** A digital certificate binds a public key to an identity (domain name, organisation). Without certificates, you could be talking to the correct `bank.com` server's public key — or an attacker's public key. Certificates solve this: a trusted Certificate Authority (CA) has verified that this public key belongs to this entity and has signed the certificate. Your browser trusts the CA, so it trusts the certificate.

**Certificate types:**
- **DV (Domain Validated):** CA only checks you control the domain (automated via DNS/HTTP challenge). No organisation verification. Fast (minutes), cheap/free (Let's Encrypt). Shows padlock but no organisation name. Good for personal sites, APIs.
- **OV (Organisation Validated):** CA checks the domain AND verifies the organisation's legal existence. Shows organisation name in certificate details. Takes 1-3 days. Better for business sites.
- **EV (Extended Validation):** Rigorous verification — business registration, legal status, phone verification. Previously showed green bar/organisation name in browser address bar (browsers removed this visual indicator post-2019). Most thorough but most expensive. Used by banks, e-commerce. Provides highest assurance.

---

## Section B: Attack Types (Questions 11-17)

**Q11.** Explain the difference between phishing, spear phishing, whaling, and vishing. Give a real-world example scenario for each.

**Answer:**
- **Phishing:** Mass, generic attack sent to thousands. "Dear Customer, your account will be suspended. Click here." Low success rate per target but high volume.
- **Spear phishing:** Targeted at a specific individual or organisation using personal information. "Hi Sarah, I noticed your project on LinkedIn — I've attached relevant research. Can you review?" Higher success rate due to personalisation.
- **Whaling:** Spear phishing targeting senior executives (the "big fish"). "CEO, I need you to urgently authorise a wire transfer to complete the acquisition." Also called Business Email Compromise (BEC).
- **Vishing (voice phishing):** Phone call impersonation. "Hi, this is Microsoft Support. We've detected a virus on your computer. Please give us remote access to fix it." Exploits urgency and authority.

---

**Q12.** What is a SQL injection attack? Write an example of vulnerable code, the attack payload, and the fixed code.

**Answer:**
```python
# VULNERABLE CODE
def get_user(username):
    query = f"SELECT * FROM users WHERE name = '{username}'"
    # If username = "admin' OR '1'='1", query becomes:
    # SELECT * FROM users WHERE name = 'admin' OR '1'='1'
    # This returns ALL users!
    return db.execute(query)

# ATTACK PAYLOAD: username = "admin'; DROP TABLE users; --"
# Query becomes: SELECT * FROM users WHERE name = 'admin'; DROP TABLE users; --'
# Deletes the entire users table!

# FIXED CODE — parameterised query
def get_user_safe(username):
    query = "SELECT * FROM users WHERE name = ?"
    return db.execute(query, (username,))  # DB driver handles escaping
    # username is treated as DATA, never as SQL syntax
```

The fix: never concatenate user input into SQL strings. Always use parameterised queries or prepared statements. The database driver then sends the query structure and the data separately — user input can never be interpreted as SQL.

---

**Q13.** A user receives an email from `hr@acme-c0rp.com` (note the zero, not letter O) with an "urgent salary update form." Describe all the red flags in this email and the techniques being used.

**Answer:**
**Technical red flags:**
1. **Homograph/typosquatting domain:** `acme-c0rp.com` uses a zero (0) instead of the letter O in "corp" — designed to look like the real `acme-corp.com` at a glance
2. **SPF/DKIM likely different:** Check email headers — `Received-From` domain won't match the display domain
3. **Domain age:** `acme-c0rp.com` likely newly registered (check WHOIS) — legitimate companies have old domains

**Social engineering techniques:**
4. **Authority + urgency:** "HR" triggers deference to hierarchy; "urgent" triggers anxiety and suppresses careful thinking
5. **Topic relevance:** Salary affects everyone — high motivation to engage
6. **Pre-texting:** Creates a plausible scenario (salary update) to justify the action

**What to do:** Don't click. Don't reply. Forward to your security team. Check the real HR department's email address from the internal directory. Call HR directly using a known number.

---

**Q14.** What is a man-in-the-browser (MitB) attack? How does it differ from a man-in-the-middle (MitM) attack, and why is HTTPS insufficient to prevent MitB?

**Answer:**
**MITM:** Attacker intercepts communication at the network level, between the user's browser and the server. HTTPS prevents this by encrypting data in transit.

**MitB:** Attacker's malware is installed inside the browser itself (via malicious browser extension or trojan). The malware modifies web page content or form submissions AFTER decryption and BEFORE the user sees it — or intercepts credentials BEFORE encryption. 

**Why HTTPS can't help:** HTTPS encrypts the connection, but MitB operates at the point where data is already in plaintext (the browser has decrypted it). The malware can: change the destination bank account number in a transfer form before submission, capture credentials from login forms, inject fake content into the page.

**Real-world:** Zeus Trojan used MitB to steal banking credentials. The user saw the correct website with valid HTTPS. The trojan modified the form submission to redirect funds.

---

**Q15.** Explain what a "credential stuffing" attack is. How does it differ from brute force? What is an example of how attackers obtain the credential lists used?

**Answer:**
**Brute force:** Systematically trying all possible password combinations (aaaa, aaab, aaac...). Detected easily — massive volume of failed logins. Effective only against weak passwords.

**Credential stuffing:** Using actual username+password pairs from previous data breaches. These are real credentials that real users use. Attackers purchase breach datasets (LinkedIn 2012, RockYou 2009, Collection #1 2019 — billions of real credentials). They test these at scale against other sites, exploiting password reuse. Attack is "quiet" — each credential is only tried once, from different IPs.

**Why effective:** 65% of people reuse passwords. One breach of a low-value site (a forum) exposes credentials for high-value sites (bank, email).

**Defences:** MFA (credential stuffing bypassed — they have real passwords, but MFA requires a second factor), Have I Been Pwned integration to check if a user's password is in known breaches, bot detection (verify new device logins), rate limiting per IP and per account.

---

**Q16.** You receive a suspicious email with an attached file called `Invoice_Q4.pdf.exe`. What is the filename technique being used? What would you do to safely analyse this file without running it?

**Answer:**
**Technique:** Double extension with social engineering. `Invoice_Q4.pdf.exe` — Windows by default hides known file extensions. If the user has hidden extensions enabled, they see `Invoice_Q4.pdf` with a PDF icon (if the attacker added one). They double-click thinking it's a PDF — actually running an .exe.

**Safe analysis:**
1. **VirusTotal:** Upload the file hash (NOT the file itself if sensitive) to virustotal.com — check if any AV engine detects it
2. **Online sandboxing:** Submit to any.run or hybrid-analysis.com — watch it run in an isolated VM, observe: what processes it spawns, what registry keys it creates, what network connections it makes, what files it writes
3. **Static analysis:** Use `strings` command on Linux or Strings.exe (Sysinternals) to see readable text inside the binary — URLs, IP addresses, function names
4. **PEiD / Detect-It-Easy:** Check if the binary is packed/obfuscated
5. **Never** open on your work machine without these checks first

---

**Q17.** What is the difference between a virus, a worm, and a trojan? For each, describe how it spreads and give a famous real-world example.

**Answer:**
| | Virus | Worm | Trojan |
|-|-------|------|-------|
| **Spreads by** | Infecting legitimate files — requires user to run infected file | Self-replicates over networks automatically — no user action | Disguised as legitimate software — requires user to install it |
| **Requires user?** | Yes — must execute infected file | No — exploits vulnerabilities or shares | Yes — user must run it |
| **Example** | ILOVEYOU (2000) — email attachment that infected files when opened | WannaCry (2017) — spread via EternalBlue (SMB exploit), no user action needed | Zeus (banking trojan) — disguised in software downloads, then stole banking credentials |

---

## Section C: Python Security Scripting (Questions 18-22)

**Q18.** Write a Python function that checks if a given IP address appears in common threat intelligence blocklists using the AbuseIPDB API (free tier available).

**Answer:**
```python
import requests

def check_ip_reputation(ip: str, api_key: str) -> dict:
    """Query AbuseIPDB for IP reputation. Returns dict with abuse confidence score."""
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": api_key
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90,
        "verbose": True
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()['data']
        return {
            "ip": data['ipAddress'],
            "abuse_score": data['abuseConfidenceScore'],  # 0-100
            "total_reports": data['totalReports'],
            "country": data['countryCode'],
            "isp": data['isp'],
            "is_tor": data.get('isTor', False)
        }
    else:
        raise Exception(f"API error: {response.status_code}")

# Usage (sign up at abuseipdb.com for free API key)
# result = check_ip_reputation("185.220.101.100", "YOUR_API_KEY")
# if result['abuse_score'] > 80:
#     print(f"HIGH RISK IP: {result['ip']} - Score: {result['abuse_score']}")
```

---

**Q19.** Write a Python script that reads a list of file paths from a text file and checks each file's hash against VirusTotal using their hash search API.

**Answer:**
```python
import hashlib, requests, time

def hash_file_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def check_vt_hash(file_hash: str, api_key: str) -> dict:
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": api_key}
    
    resp = requests.get(url, headers=headers)
    
    if resp.status_code == 404:
        return {"status": "not_found", "detections": 0, "total": 0}
    
    if resp.status_code == 200:
        stats = resp.json()['data']['attributes']['last_analysis_stats']
        return {
            "status": "found",
            "detections": stats.get('malicious', 0),
            "total": sum(stats.values())
        }
    
    return {"status": "error", "code": resp.status_code}

def scan_filelist(filelist_path: str, api_key: str):
    with open(filelist_path) as f:
        files = [line.strip() for line in f if line.strip()]
    
    for filepath in files:
        try:
            fhash = hash_file_sha256(filepath)
            result = check_vt_hash(fhash, api_key)
            status = f"{result['detections']}/{result['total']} detections"
            flag = "⚠ MALICIOUS" if result.get('detections', 0) > 3 else "✓ Clean"
            print(f"{flag} | {filepath} | {fhash[:16]}... | {status}")
        except FileNotFoundError:
            print(f"NOT FOUND: {filepath}")
        except Exception as e:
            print(f"ERROR: {filepath}: {e}")
        
        time.sleep(15)  # VT free API: 4 requests/minute
```

---

**Q20.** Explain what HMAC is and when you would use it instead of a plain hash. Write a Python implementation.

**Answer:** HMAC (Hash-based Message Authentication Code) is a hash computed with a secret key mixed in. A plain hash verifies that data is unchanged but anyone can compute it. HMAC verifies data integrity AND authenticates the sender (only someone who knows the key can produce the correct HMAC).

Use cases: API request signing (sender signs the request with their API secret), verifying webhook payloads (GitHub uses HMAC-SHA256 to sign webhook deliveries), JWT signature verification, cookie integrity protection.

```python
import hmac, hashlib, secrets

def generate_hmac(message: bytes, key: bytes) -> str:
    return hmac.new(key, message, hashlib.sha256).hexdigest()

def verify_hmac(message: bytes, key: bytes, received_hmac: str) -> bool:
    expected = generate_hmac(message, key)
    # Use compare_digest to prevent timing attacks
    return hmac.compare_digest(expected, received_hmac)

# Generate a shared secret key
secret_key = secrets.token_bytes(32)

# Sender signs the message
message = b"Transfer $1000 to account 12345"
signature = generate_hmac(message, secret_key)
print(f"Signature: {signature}")

# Receiver verifies
is_valid = verify_hmac(message, secret_key, signature)
print(f"Valid: {is_valid}")

# Tampered message fails
tampered = b"Transfer $10000 to account 99999"
is_valid_tampered = verify_hmac(tampered, secret_key, signature)
print(f"Tampered valid: {is_valid_tampered}")  # False
```

---

**Q21.** Write a Python function that generates a cryptographically secure random password of configurable length and character set.

**Answer:**
```python
import secrets
import string

def generate_password(
    length: int = 20,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = True  # excludes 0, O, l, 1, I
) -> str:
    alphabet = ""
    if use_upper:
        chars = string.ascii_uppercase
        if exclude_ambiguous:
            chars = chars.replace('O', '').replace('I', '')
        alphabet += chars
    if use_lower:
        chars = string.ascii_lowercase
        if exclude_ambiguous:
            chars = chars.replace('l', '')
        alphabet += chars
    if use_digits:
        chars = string.digits
        if exclude_ambiguous:
            chars = chars.replace('0', '').replace('1', '')
        alphabet += chars
    if use_symbols:
        alphabet += "!@#$%^&*-_=+"
    
    if not alphabet:
        raise ValueError("At least one character type must be selected")
    
    # Ensure at least one of each required type appears
    password = []
    if use_upper: password.append(secrets.choice(string.ascii_uppercase))
    if use_lower: password.append(secrets.choice(string.ascii_lowercase))
    if use_digits: password.append(secrets.choice(string.digits))
    if use_symbols: password.append(secrets.choice("!@#$%^&*-_=+"))
    
    # Fill the rest randomly
    password += [secrets.choice(alphabet) for _ in range(length - len(password))]
    
    # Shuffle (secrets.SystemRandom is CSPRNG)
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

# Generate several passwords
for i in range(5):
    print(generate_password(24))
```

---

**Q22.** What is the difference between encoding, encryption, and hashing? Give an example of each and explain when each is appropriate.

**Answer:**
| | Encoding | Encryption | Hashing |
|-|----------|-----------|---------|
| **Reversible?** | Yes — always | Yes — with key | No — one-way |
| **Secret key?** | No | Yes | No (or HMAC) |
| **Purpose** | Data format conversion | Confidentiality | Integrity verification |
| **Example** | Base64 | AES-256 | SHA-256 |

- **Base64 encoding:** Converts binary data to ASCII text for transmission in email/URLs. Anyone can decode it — it provides zero security. Example: MIME email attachments, JWT header/payload.
- **AES-256 encryption:** Protects data confidentiality. Only those with the key can decrypt. Example: encrypted database field for PAN numbers, file encryption.
- **SHA-256 hashing:** Verifies integrity without storing the original data. Example: password storage (store hash, not password), file integrity (verify download wasn't tampered).

Common mistake: "we Base64-encode passwords for security" — Base64 is NOT security. It's trivially reversible.

---

## Section D: Security Architecture (Questions 23-25)

**Q23.** A startup is designing their first authentication system. They ask you to recommend whether to use TOTP (authenticator app), SMS OTP, or hardware security keys as their MFA second factor. Evaluate each option.

**Answer:**
| Factor | Security | UX | Cost | Recommendation |
|--------|---------|-----|------|---------------|
| **SMS OTP** | LOW — SIM swapping, SS7 attacks allow interception. Deprecated by NIST. | Medium — works on any phone | Low | Avoid for high-value accounts. Acceptable for low-risk consumer use. |
| **TOTP (Authenticator app)** | HIGH — not interruptible by telco attacks, codes are time-limited | Good — any smartphone | Free | Recommend for most business accounts. Better than SMS. |
| **Hardware key (FIDO2/WebAuthn)** | VERY HIGH — phishing-resistant (key is bound to the specific domain, so phishing sites can't use captured codes) | Excellent — one tap | $25-50/user | Best for privileged admin accounts, executives, high-value users |

**Recommendation:** Deploy TOTP for all employees immediately (zero cost). For privileged accounts (domain admins, finance, executives), require FIDO2 hardware keys (YubiKey). Never use SMS OTP for anything important.

---

**Q24.** Explain what the Zero Trust security model is. Write 8 specific technical controls that implement Zero Trust principles in an enterprise environment.

**Answer:** Zero Trust: "Never trust, always verify." Replaces the perimeter/castle-and-moat model where everything inside the network is trusted. In Zero Trust, every request (even from inside the network) is authenticated, authorised, and encrypted — every time.

8 technical controls:
1. **Multi-factor authentication on every access** — identity is verified continuously, not just at login
2. **Microsegmentation** — network divided into tiny zones; access between zones requires explicit authorisation. Even if an attacker compromises one segment, they can't move laterally
3. **Device health checks** — only compliant devices (patched OS, AV enabled, screen lock) get access; evaluated at each connection, not just enrollment
4. **Just-in-time (JIT) access** — privileged access is granted for a specific time window and task, then removed (Privileged Access Workstations/PAM solutions)
5. **Encrypt all internal traffic** — no "trusted" internal HTTP; mTLS between all services
6. **Continuous monitoring and anomaly detection** — SIEM watches all east-west traffic, not just perimeter
7. **Identity-based access (not IP-based)** — access decisions based on user identity + device health, not "is this IP on the corporate network?"
8. **Software-Defined Perimeter / ZTNA** — replace VPN with Zero Trust Network Access; users connect directly to specific applications, never to the entire network

---

**Q25.** A small company with 50 employees asks you to design a password policy. What 8 rules would your policy include and why (include the NIST SP 800-63B rationale for any rules that contradict common myths)?

**Answer:**
1. **Minimum 15 characters** (NIST: focus on length over complexity — passphrases are stronger and more memorable)
2. **No maximum length under 64 characters** (NIST: artificial caps force users to shorter passwords)
3. **Check against known-breached password lists** (NIST: reject passwords from breach databases like HaveIBeenPwned)
4. **No mandatory character complexity rules** (NIST: complexity rules lead to predictable patterns: Password1!, Passw0rd! — length beats complexity)
5. **No mandatory periodic changes** (NIST: forced rotation leads to Password1! → Password2! — weak incremental changes. Only change when compromise suspected.)
6. **No security question prompts** (NIST: mother's maiden name, first pet etc. are guessable/social-engineered/findable on social media)
7. **Require MFA for all accounts** — even a long password is compromised if it's in a breach database
8. **Allow paste from password managers** — blocking paste forces memorised (weaker) passwords; password managers generate strong unique passwords per site

This policy follows modern NIST SP 800-63B guidelines which differ significantly from older, still-common "must have uppercase + number + symbol + change every 90 days" advice.

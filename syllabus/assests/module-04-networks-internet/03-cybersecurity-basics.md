# Cybersecurity Basics

**Module 04 — Networks & Internet | Topic 3**

---

## What is Cybersecurity?

**Cybersecurity** means protecting your computer, data, and online accounts from attackers (hackers, viruses, scams).

> **Think of it like:** Locking your house, putting valuables in a safe, and not telling strangers your house keys.

---

## Common Cyber Threats

| Threat | What It Is | Example |
|--------|-----------|---------|
| **Virus** | Program that copies itself and damages files | Deletes files, slows computer |
| **Malware** | Any harmful software (virus, worm, trojan, spyware) | Steals data, shows ads |
| **Phishing** | Fake email/website that tricks you into giving password | "Your bank account is locked, click here" |
| **Ransomware** | Locks your files and demands money to unlock | WannaCry attack (2017) |
| **Spyware** | Secretly watches what you do | Records your passwords, browsing |
| **Trojan** | Looks like normal software but is harmful | Free game that steals data |
| **Worm** | Spreads automatically across networks | No user action needed to spread |
| **Man-in-the-Middle** | Attacker intercepts communication between two people | On public WiFi, hacker reads your data |
| **Brute Force** | Trying every possible password until one works | Automated password guessing |
| **Social Engineering** | Tricking a person (not technology) to give access | Phone call pretending to be IT support |

---

## How to Stay Safe — 10 Rules

### 1. Strong Passwords

| Weak Password | Strong Password | Why |
|--------------|----------------|-----|
| password123 | Tp@$s2026!xK | Has uppercase, lowercase, numbers, symbols |
| rahul2000 | R@hul_Net#2k26 | Not a simple dictionary word |
| 12345678 | j7$Km9#pL2 | Random, hard to guess |

**Password rules:**
- At least **12 characters**
- Mix of **uppercase + lowercase + numbers + symbols**
- **Different password** for each account
- Use a **password manager** (Bitwarden, LastPass)

### 2. Two-Factor Authentication (2FA)

Even if someone gets your password, 2FA stops them.

```
Step 1: Enter password (something you know)
Step 2: Enter OTP from phone (something you have)
→ Both needed to login
```

**Enable 2FA on:** Gmail, Instagram, WhatsApp, bank accounts, UPI apps

### 3. Spot Phishing Emails

| Sign of Phishing | Example |
|-----------------|---------|
| Urgent language | "Your account will be DELETED in 24 hours!" |
| Suspicious sender | support@g00gle-security.com (notice fake domain) |
| Grammar mistakes | "Dear valued customer, we has detected..." |
| Asks for password | No real company ever asks for your password via email |
| Strange link | Hover over link — URL goes somewhere unexpected |

> **Rule:** Never click links in unexpected emails. Go directly to the website by typing the URL yourself.

### 4. HTTPS Always

- Only enter passwords/card numbers on **HTTPS** websites (lock icon in browser)
- HTTP websites can be read by anyone in between

### 5. Public WiFi Safety

| Danger | Protection |
|--------|-----------|
| Anyone can see your data on public WiFi | Use **VPN** (Virtual Private Network) |
| Fake WiFi hotspots | Verify WiFi name with staff |
| Session hijacking | Don't log into bank/email on public WiFi |

### 6. Software Updates

- Always install **Windows updates** and **app updates**
- Updates fix security holes that hackers can exploit
- Enable auto-update wherever possible

### 7. Antivirus

- Windows 11 has built-in **Windows Defender** (good enough for most)
- Keep it turned on and updated
- Don't install two antivirus programs (they conflict)

### 8. Backup Your Data

- **3-2-1 Rule:** 3 copies, 2 different media, 1 offsite (cloud)
- Use Google Drive / OneDrive for important files
- If ransomware hits, you can restore from backup

### 9. Don't Download from Unknown Sources

- Only download from official websites and app stores
- Pirated software often contains malware
- Don't open email attachments from unknown senders

### 10. Privacy Settings

- Check privacy settings on social media (Instagram, Facebook)
- Don't share personal info (phone number, address) publicly
- Cover your webcam when not in use

---

## VPN — Virtual Private Network

| Feature | Without VPN | With VPN |
|---------|-----------|---------|
| **Your IP visible?** | Yes, everyone sees your real IP | No, they see VPN server's IP |
| **Data encrypted?** | Only on HTTPS sites | All traffic encrypted |
| **ISP can see browsing?** | Yes | No |
| **Location** | Your real location | VPN server's location |

> **When to use VPN:** Public WiFi, accessing blocked content, privacy on unsecured networks.

---

## Firewall — Network Security Guard

A **firewall** monitors all incoming and outgoing network traffic and blocks anything suspicious.

| Type | Where | Example |
|------|-------|---------|
| **Software Firewall** | Inside your computer | Windows Firewall (built-in) |
| **Hardware Firewall** | In network equipment | In business routers |

**Keep Windows Firewall ON** — it blocks unauthorized connections.

---

## Summary

- **Cybersecurity** = protecting your data from hackers and viruses
- Top threats: **Phishing, Malware, Ransomware**
- Use **strong passwords** (12+ chars, mixed) + **2FA**
- Check for **HTTPS** before entering sensitive data
- **Never click** suspicious links in emails
- Use **VPN** on public WiFi
- Keep software **updated** and antivirus **on**
- **Backup** important files (3-2-1 rule)

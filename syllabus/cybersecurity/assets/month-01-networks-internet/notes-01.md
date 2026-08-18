# Month 1: Networks & Internet — Revision Notes

## 1. The CIA Triad

| Property | Definition | Example Controls |
|----------|-----------|-----------------|
| **Confidentiality** | Only authorised parties access data | Encryption (AES, TLS), ACLs, IAM |
| **Integrity** | Data has not been tampered with | Hashing (SHA-256), digital signatures |
| **Availability** | Systems accessible when needed | Redundancy, DDoS protection, RAID |

### Threat Vocabulary
- **Threat**: Potential cause of harm (attacker, ransomware group, hurricane)
- **Vulnerability**: A weakness that can be exploited (unpatched CVE, default credentials)
- **Exploit**: Code or technique that leverages a vulnerability (e.g., EternalBlue / MS17-010)
- **Risk**: Threat × Vulnerability × Impact — what security teams manage and accept/transfer/mitigate

---

## 2. OSI Model — 7 Layers

| # | Layer | PDU | Key Protocols | Device |
|---|-------|-----|--------------|--------|
| 7 | Application | Data | HTTP, HTTPS, DNS, FTP, SMTP, SSH | — |
| 6 | Presentation | Data | TLS/SSL, JPEG, MPEG, ASCII | — |
| 5 | Session | Data | NetBIOS, RPC, PPTP | — |
| 4 | Transport | Segment | TCP, UDP, SCTP | — |
| 3 | Network | Packet | IP, ICMP, ARP, OSPF, BGP | Router |
| 2 | Data Link | Frame | Ethernet (802.3), Wi-Fi (802.11) | Switch |
| 1 | Physical | Bits | Cat5/6, Fiber, RF, DSL | Hub |

**Mnemonic (top→bottom):** All People Seem To Need Data Processing
**Mnemonic (bottom→top):** Please Do Not Throw Sausage Pizza Away

---

## 3. TCP vs UDP

### TCP — Reliable, Connection-Oriented
- 3-way handshake: `SYN → SYN-ACK → ACK`
- Retransmits lost packets; guarantees ordering
- Use: HTTP, SSH, SMTP, IMAP, HTTPS

### UDP — Fast, Connectionless
- No handshake; fire-and-forget; low latency
- No delivery guarantee or ordering
- Use: DNS, DHCP, VoIP, video streaming, gaming, QUIC/HTTP3

---

## 4. Critical Port Numbers

| Port | Protocol | Service | Security Note |
|------|----------|---------|--------------|
| 21 | TCP | FTP | Plaintext — use SFTP instead |
| 22 | TCP | SSH | Encrypted remote shell |
| 23 | TCP | Telnet | Plaintext — deprecated |
| 25 | TCP | SMTP | Email relay |
| 53 | TCP/UDP | DNS | UDP for queries; TCP for zone transfers |
| 80 | TCP | HTTP | Unencrypted — redirect to 443 |
| 110 | TCP | POP3 | Email download (legacy) |
| 143 | TCP | IMAP | Email access |
| 443 | TCP | HTTPS | TLS-encrypted web |
| 445 | TCP | SMB | File sharing — high-value attack target |
| 3306 | TCP | MySQL | Database — never expose externally |
| 3389 | TCP | RDP | Remote Desktop — frequently brute-forced |

---

## 5. DNS Resolution — Step by Step

1. Browser checks **local DNS cache** (TTL-based expiry)
2. Query sent to **Recursive Resolver** (ISP or 8.8.8.8/1.1.1.1)
3. Resolver queries **Root Name Server** (13 root server clusters globally)
4. Root refers to **TLD server** (.com, .org, .uk)
5. TLD refers to domain's **Authoritative Name Server**
6. Authoritative returns **A record** (IPv4) or **AAAA record** (IPv6)
7. Resolver caches the result and returns it to the client

**DNS Record Types**: A, AAAA, CNAME (alias), MX (mail), TXT (SPF/DKIM), NS, PTR (reverse), SOA

---

## 6. Subnetting Essentials

- **CIDR notation**: `192.168.1.0/24` (prefix length = network bits)
- **Usable hosts** = 2^(32 − prefix) − 2

| CIDR | Mask | Usable Hosts | Common Use |
|------|------|-------------|-----------|
| /8 | 255.0.0.0 | 16,777,214 | ISPs |
| /16 | 255.255.0.0 | 65,534 | Large enterprise |
| /24 | 255.255.255.0 | 254 | Office LAN |
| /25 | 255.255.255.128 | 126 | Half a class C |
| /30 | 255.255.255.252 | 2 | Point-to-point links |

**Private ranges (RFC 1918)**: 10.0.0.0/8 | 172.16.0.0/12 | 192.168.0.0/16

---

## 7. Firewalls, NAT & VPN

- **Packet filter**: Inspects IP/port headers statically
- **Stateful firewall**: Tracks active connection table — knows if packet belongs to established session
- **NGFW**: Deep Packet Inspection, app awareness, integrated IPS
- **NAT**: Maps private IPs → public IP; hides internal network topology
- **VPN protocols**: WireGuard (modern, fast), OpenVPN, IPsec/IKEv2, L2TP
  - Remote-access VPN: single user → corporate network
  - Site-to-site VPN: office ↔ office over encrypted tunnel

---

## 8. TLS/SSL & PKI

### TLS Handshake (TLS 1.3 simplified)
1. Client Hello — TLS version, supported cipher suites, random nonce
2. Server Hello — chosen cipher + **certificate** (public key + identity)
3. Client validates certificate chain against trusted Root CA
4. Key exchange via ECDHE (forward secrecy)
5. Session keys derived — encrypted communication begins

### PKI Trust Chain
```
Root CA (self-signed, embedded in OS/browser trust store)
  └── Intermediate CA (signed by Root)
        └── End-Entity Cert (your domain — signed by Intermediate)
```

### Certificate Contains
- Subject CN / Subject Alternative Names (SANs)
- Validity: Not Before / Not After dates
- Public key (RSA 2048-bit, ECDSA P-256)
- Issuer name + CA digital signature
- Serial number + revocation URL (CRL / OCSP)

---

## 9. Wireshark Quick Reference

```
http                      All HTTP traffic
tls                       TLS handshakes and records
dns                       DNS queries and responses
tcp.port == 22            SSH connections
ip.addr == 192.168.1.10   Traffic to/from one host
tcp.flags.syn == 1        TCP SYN packets (new connections)
!(arp or icmp)            Remove background noise
frame contains "password" Search packet payloads
```

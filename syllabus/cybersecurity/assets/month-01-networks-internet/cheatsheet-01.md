# Month 1 Cheatsheet — Networks & Internet

## OSI Model Quick Reference

| # | Layer | Function | Protocols | PDU | Device |
|---|-------|----------|-----------|-----|--------|
| 7 | Application | User-facing services | HTTP, HTTPS, DNS, FTP, SMTP, SSH, SNMP | Data | — |
| 6 | Presentation | Encoding, encryption, compression | TLS/SSL, JPEG, MPEG, ASCII, Unicode | Data | — |
| 5 | Session | Session setup/teardown | NetBIOS, RPC, PPTP, NFS | Data | — |
| 4 | Transport | End-to-end reliable delivery | TCP, UDP, SCTP | Segment | — |
| 3 | Network | Logical addressing & routing | IP, ICMP, ARP, OSPF, BGP, IPsec | Packet | Router |
| 2 | Data Link | Physical addressing (MAC) | Ethernet 802.3, Wi-Fi 802.11, PPP | Frame | Switch |
| 1 | Physical | Bit transmission | Cat5e/6, Fiber, RF, DSL, Coax | Bits | Hub |

## TCP/IP Model vs OSI
| TCP/IP Layer | OSI Equivalent | Key Protocols |
|--------------|---------------|--------------|
| Application | Layers 5, 6, 7 | HTTP, DNS, SMTP, SSH |
| Transport | Layer 4 | TCP, UDP |
| Internet | Layer 3 | IP, ICMP, ARP |
| Network Access | Layers 1, 2 | Ethernet, Wi-Fi |

## Critical Port Numbers
| Port | Protocol | Service | Risk Level |
|------|----------|---------|-----------|
| 21 | TCP | FTP | HIGH — cleartext credentials |
| 22 | TCP | SSH | Low if hardened |
| 23 | TCP | Telnet | CRITICAL — fully cleartext |
| 25 | TCP | SMTP | Medium |
| 53 | UDP/TCP | DNS | Medium — cache poisoning risk |
| 80 | TCP | HTTP | Medium — no encryption |
| 110 | TCP | POP3 | High — cleartext |
| 143 | TCP | IMAP | High — cleartext |
| 443 | TCP | HTTPS | Low |
| 445 | TCP | SMB | CRITICAL — ransomware vector |
| 1433 | TCP | MS SQL | High — never expose externally |
| 3306 | TCP | MySQL | High — never expose externally |
| 3389 | TCP | RDP | HIGH — brute-force target |
| 5900 | TCP | VNC | HIGH — often unencrypted |
| 8080 | TCP | HTTP-alt | Medium |

## Subnet Quick Reference
| CIDR | Subnet Mask | Total IPs | Usable Hosts | Network Bits |
|------|------------|-----------|-------------|-------------|
| /8 | 255.0.0.0 | 16,777,216 | 16,777,214 | 8 |
| /16 | 255.255.0.0 | 65,536 | 65,534 | 16 |
| /24 | 255.255.255.0 | 256 | 254 | 24 |
| /25 | 255.255.255.128 | 128 | 126 | 25 |
| /26 | 255.255.255.192 | 64 | 62 | 26 |
| /27 | 255.255.255.224 | 32 | 30 | 27 |
| /28 | 255.255.255.240 | 16 | 14 | 28 |
| /29 | 255.255.255.248 | 8 | 6 | 29 |
| /30 | 255.255.255.252 | 4 | 2 | 30 |

**Formula:** Usable = 2^(32 − prefix) − 2

## Private IP Ranges (RFC 1918)
| Range | CIDR | Typical Use |
|-------|------|------------|
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | Large enterprise |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | Medium networks |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | Home / small office |

## DNS Record Types
| Record | Maps | Example |
|--------|------|---------|
| A | Hostname → IPv4 | `example.com → 93.184.216.34` |
| AAAA | Hostname → IPv6 | `example.com → 2606:2800::1` |
| CNAME | Alias → canonical name | `www → example.com` |
| MX | Domain → mail server | `Priority 10 mail.example.com` |
| TXT | Domain → text | `v=spf1 include:...` (SPF, DKIM) |
| NS | Domain → name server | `ns1.registrar.com` |
| PTR | IP → hostname (reverse) | `34.216.184.93.in-addr.arpa` |
| SOA | Zone authority record | Serial, refresh, retry times |

## TLS Handshake Steps (TLS 1.3)
| Step | Who | What |
|------|-----|------|
| 1 | Client | Client Hello (TLS ver, cipher suites, random) |
| 2 | Server | Server Hello (chosen cipher, cert, random) |
| 3 | Client | Validate cert chain via PKI |
| 4 | Both | ECDHE key exchange → derive session keys |
| 5 | Both | Finished messages — encrypted channel open |

## Wireshark Filters
| Filter | Purpose |
|--------|---------|
| `http` | All HTTP traffic |
| `tls` | TLS records and handshakes |
| `dns` | DNS queries and responses |
| `tcp.port == 22` | SSH connections |
| `ip.addr == 10.0.0.1` | Traffic for specific host |
| `tcp.flags.syn == 1` | New TCP connections |
| `tcp.flags.rst == 1` | TCP resets (refused connections) |
| `!(arp or icmp or dns)` | Remove background noise |
| `frame contains "GET"` | HTTP GET requests |

## Firewall Types
| Type | Inspects | Stateful | Use Case |
|------|---------|---------|---------|
| Packet Filter | IP/port headers | No | Basic ACLs |
| Stateful | Connection table | Yes | Most firewalls |
| NGFW | Payload / app | Yes | Enterprise |
| WAF | HTTP layer 7 | Yes | Web apps |

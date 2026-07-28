# Module 04 — Networks & Internet — Quick Revision Notes

---

## Network Types
| Type | Range | Example |
|------|-------|---------|
| **PAN** | ~1m | Bluetooth earbuds |
| **LAN** | Building | Office WiFi |
| **MAN** | City | Cable TV network |
| **WAN** | Global | The Internet |

## OSI Model (7 Layers)
| # | Layer | What It Does | Protocol | Device |
|---|-------|-------------|----------|--------|
| 7 | Application | User interface | HTTP, FTP, SMTP, DNS | Browser |
| 6 | Presentation | Encryption, compression | SSL/TLS, JPEG | — |
| 5 | Session | Manages connections | NetBIOS | — |
| 4 | Transport | Reliable delivery | TCP (reliable), UDP (fast) | — |
| 3 | Network | Routing, IP addresses | IP, ICMP | Router |
| 2 | Data Link | MAC addresses, frames | Ethernet, WiFi | Switch |
| 1 | Physical | Cables, signals | — | Hub, cables |

**Memory trick:** "All People Seem To Need Data Processing" (top to bottom)

## TCP vs UDP
- **TCP** = Reliable, ordered, slower (web pages, email, file transfer)
- **UDP** = Fast, no guarantee (video streaming, gaming, DNS)

## IP Addresses
- **IPv4**: 192.168.1.1 (4 numbers, 0-255 each, total ~4 billion addresses)
- **IPv6**: 2001:0db8:85a3::8a2e:0370:7334 (much larger)
- **Private IPs**: 192.168.x.x, 10.x.x.x, 172.16-31.x.x (inside your network)
- **Public IP**: Your router's address on the internet (shared by all devices in your home)
- **Static**: Fixed, doesn't change (servers)
- **Dynamic**: Changes periodically (your home connection, via DHCP)

## DNS (Domain Name System)
- Converts domain names to IP addresses
- `techpath.biz` → DNS → `143.198.45.67`
- Like a phone book for the internet

## How a Website Loads (Key Steps)
1. Type URL → Browser checks cache
2. DNS lookup → find server IP
3. TCP connection (3-way handshake)
4. HTTP request sent
5. Server processes → sends HTML/CSS/JS
6. Browser renders the page

## Common Ports
| Port | Service | Protocol |
|------|---------|----------|
| 80 | HTTP | TCP |
| 443 | HTTPS | TCP |
| 22 | SSH | TCP |
| 21 | FTP | TCP |
| 25 | SMTP (email send) | TCP |
| 53 | DNS | TCP/UDP |
| 3306 | MySQL | TCP |
| 5432 | PostgreSQL | TCP |
| 8000 | Dev servers | TCP |

## WiFi Standards
| Standard | Name | Speed | Band |
|----------|------|-------|------|
| 802.11n | WiFi 4 | 600 Mbps | 2.4/5 GHz |
| 802.11ac | WiFi 5 | 3.5 Gbps | 5 GHz |
| 802.11ax | WiFi 6 | 9.6 Gbps | 2.4/5/6 GHz |

## Cybersecurity Basics
- **Malware** = Virus, Worm, Trojan, Ransomware, Spyware
- **Phishing** = Fake emails/sites that steal credentials
- **Firewall** = Filters network traffic (blocks unauthorized access)
- **HTTPS** = Encrypted connection (look for 🔒 in browser)
- **VPN** = Encrypted tunnel (hides your traffic from ISP)
- **2FA** = Two-Factor Authentication (password + phone code)

## Network Commands
| Command | Purpose |
|---------|---------|
| `ping host` | Test if server is reachable |
| `tracert host` | Show route to server |
| `ipconfig` | Show your IP (Windows) |
| `ifconfig` | Show your IP (Linux) |
| `nslookup domain` | DNS lookup |
| `netstat -an` | Show active connections |

# TCP/IP and the OSI Model: How Data Travels Across Networks

## Why This Matters

Every time you load a web page, send an email, or connect to a remote server, your data passes through a precisely orchestrated stack of protocols. Understanding this stack is the foundation of network defence — you cannot detect or block malicious traffic if you don't understand what normal traffic looks like.

Security tools operate at specific layers: Wireshark captures at Layer 2, firewalls filter at Layers 3 and 4, WAFs operate at Layer 7. Knowing the layers tells you which tool to reach for.

---

## The OSI Model: A Conceptual Framework

The Open Systems Interconnection (OSI) model, published by ISO in 1984, divides network communication into **7 abstract layers**. Each layer provides services to the layer above it and relies on services from the layer below.

| # | Layer | Data Unit | Key Protocols & Standards | Real-World Example |
|---|-------|-----------|--------------------------|-------------------|
| 7 | Application | Data | HTTP, HTTPS, DNS, FTP, SMTP, SSH, SNMP | Your browser making a GET request |
| 6 | Presentation | Data | TLS/SSL, ASCII, Unicode, JPEG, MPEG | TLS encrypting the HTTP payload |
| 5 | Session | Data | NetBIOS, RPC, SQL sessions | Opening a persistent DB connection |
| 4 | Transport | Segment | TCP, UDP, SCTP | TCP port 443 connection to a web server |
| 3 | Network | Packet | IPv4, IPv6, ICMP, ARP, OSPF, BGP | Router deciding next hop for a packet |
| 2 | Data Link | Frame | Ethernet 802.3, Wi-Fi 802.11, PPP | Switch forwarding frame by MAC address |
| 1 | Physical | Bits | Cat5e/Cat6, Fiber, Coaxial, RF (Wi-Fi) | Electrical signals on copper cable |

### Encapsulation: How Data Travels Down the Stack

When you send an HTTP request, each layer **wraps** the data from the layer above with its own header (and sometimes a trailer):

```
Application:   [HTTP Request: GET /index.html]
Presentation:  [TLS Header][Encrypted HTTP Data]
Transport:     [TCP Header: SRC:52341 DST:443][TLS+HTTP Data]
Network:       [IP Header: SRC:192.168.1.5 DST:93.184.216.34][TCP+TLS+HTTP]
Data Link:     [Ethernet Header: SRC MAC DST MAC][IP+TCP+TLS+HTTP][FCS]
Physical:      ----voltage pulses / light pulses / radio waves---->
```

At the destination, this process reverses: each layer strips its header and passes the payload up.

---

## TCP in Depth

### The Three-Way Handshake

Before any data flows, TCP establishes a connection:

```
Client                          Server
  |------- SYN (seq=1000) ------->|   "I want to connect"
  |<-- SYN-ACK (seq=5000,ack=1001)-|   "OK, I'm ready, here's my seq"
  |------- ACK (ack=5001) -------->|   "Got it, connection open"
  |===== DATA TRANSFER BEGINS =====|
```

- **SYN**: Synchronise — establishes initial sequence numbers
- **SYN-ACK**: Both SYN and ACK flags set — server acknowledges and sends its own sequence
- **ACK**: Acknowledgement — confirms receipt

### TCP Connection Termination (4-way)

```
Client                          Server
  |------- FIN ------------------>|   "I'm done sending"
  |<------ ACK -------------------|   "Acknowledged"
  |<------ FIN -------------------|   "I'm done too"
  |------- ACK ------------------>|   "Confirmed, connection closed"
```

### Why Attackers Care About TCP

- **SYN Flood**: Send millions of SYN packets without completing the handshake — exhausts server connection table (half-open connections)
- **TCP Session Hijacking**: Predict sequence numbers to inject data into an established session
- **Port scanning**: Send SYN to probe which ports are open; an open port replies SYN-ACK, a closed port replies RST

### TCP Flags

| Flag | Meaning | Attack Context |
|------|---------|---------------|
| SYN | Synchronise | Port scanning, SYN flood |
| ACK | Acknowledge | Session tracking |
| FIN | Finish | Clean termination |
| RST | Reset | Force-close connection |
| PSH | Push | Deliver data immediately |
| URG | Urgent | Rarely used |

---

## UDP in Practice

UDP discards the overhead of TCP in exchange for speed. It has no handshake, no ACKs, no sequence numbers.

```
Client                          DNS Server
  |------- DNS Query (UDP:53) --->|
  |<------ DNS Response ----------|   (or lost, client retries)
```

**UDP services:** DNS (53), DHCP (67/68), TFTP (69), NTP (123), SNMP (161), QUIC/HTTP3 (443 UDP), gaming, VoIP, video streaming

**Security note:** UDP is commonly used in **amplification attacks** — an attacker sends a small spoofed UDP request to a DNS/NTP server, which responds with a large reply sent to the victim. A 50-byte DNS request can generate a 3000-byte response — 60× amplification factor.

---

## The TCP/IP Stack: Production Reality

The OSI model is conceptual; actual internet software uses the 4-layer TCP/IP model:

| TCP/IP Layer | OSI Equivalent | Protocols |
|--------------|---------------|-----------|
| Application | Layers 5–7 | HTTP, DNS, TLS, SSH, SMTP |
| Transport | Layer 4 | TCP, UDP |
| Internet | Layer 3 | IPv4, IPv6, ICMP |
| Network Access | Layers 1–2 | Ethernet, Wi-Fi, ARP |

---

## IP Addressing

### IPv4 Header Fields That Matter for Security

- **TTL (Time to Live)**: Decremented at each router hop; prevents infinite routing loops. OS fingerprinting uses default TTL values (Linux: 64, Windows: 128, Cisco: 255).
- **Protocol**: Identifies Layer 4 protocol (6=TCP, 17=UDP, 1=ICMP)
- **Source IP**: Can be spoofed in UDP packets (returns won't reach the attacker — used in amplification attacks)
- **Fragmentation flags**: Fragment packets can be used to evade some IDS signatures

### ICMP — The Network Diagnostic Protocol

ICMP is used by ping (`echo request`/`echo reply`) and traceroute. It has no port numbers — it operates directly above IP.

```bash
ping -c 4 8.8.8.8         # Send 4 echo requests
traceroute google.com      # Map the hop-by-hop path (Linux)
tracert google.com         # Same on Windows
```

ICMP can be weaponised: ICMP tunnelling sends data in ping payloads to exfiltrate information through firewalls that allow ICMP but block other traffic.

---

## ARP — The Link Between Layer 3 and Layer 2

Before an IP packet can be placed in an Ethernet frame, the sender needs the **MAC address** of the next-hop device. ARP (Address Resolution Protocol) resolves IP → MAC:

```
Host A broadcasts: "Who has 192.168.1.1? Tell 192.168.1.100"
Router replies:    "192.168.1.1 is at AA:BB:CC:DD:EE:FF"
Host A caches this in its ARP table (arp -a to view)
```

**ARP is unauthenticated** — any host can broadcast a false ARP reply. This is the basis of **ARP spoofing** (ARP poisoning), where an attacker inserts their MAC address into victims' ARP tables to perform a Man-in-the-Middle attack.

---

## Real-World Network Stack: Putting It Together

**What happens when you visit https://example.com:**

1. **DNS** (Layer 7/UDP 53): Resolve `example.com` → `93.184.216.34`
2. **TCP SYN** (Layer 4): Open connection to `93.184.216.34:443`
3. **TLS Handshake** (Layer 6): Negotiate cipher, verify cert, derive session key
4. **HTTP GET** (Layer 7): `GET / HTTP/2` sent inside encrypted TLS record
5. **TCP ACKs** (Layer 4): Delivery confirmed for each segment
6. **Server response**: 200 OK + HTML content arrives
7. **TCP FIN** (Layer 4): Connection gracefully closed

# Month 1 — Practice Exercises: Networks & The Internet

**25 exercises with worked answers. Complete without notes first, then check.**

---

## Section A: Conceptual Understanding (Questions 1-8)

**Q1.** A web browser requests `https://api.example.com/users`. List every protocol involved in this transaction, in the order they are used, from the user pressing Enter to receiving the response.

**Answer:** DNS (UDP/53) → TCP three-way handshake (SYN/SYN-ACK/ACK) → TLS handshake (ClientHello, ServerHello, Certificate, Finished) → HTTP/2 GET request → HTTP/2 200 response → TLS close_notify → TCP FIN/ACK teardown. Each lower layer wraps the higher layer: HTTP data → inside TLS record → inside TCP segment → inside IP packet → inside Ethernet frame.

---

**Q2.** Explain why UDP is used for DNS queries rather than TCP. Give two scenarios where DNS would use TCP instead of UDP.

**Answer:** UDP is connectionless — a DNS query and response fit in a single UDP datagram with no connection overhead, making it much faster for simple lookups. DNS uses TCP when: (1) the response exceeds 512 bytes (EDNS0 raised this to 4096 bytes, but large responses like zone transfers still use TCP), (2) DNS zone transfers (AXFR/IXFR) between authoritative servers use TCP because they transfer large volumes of data.

---

**Q3.** What is the purpose of the TTL (Time to Live) field in an IP packet? What happens when TTL reaches zero?

**Answer:** TTL prevents packets from circulating forever in routing loops. Each router that forwards the packet decrements TTL by 1. When TTL reaches 0, the router drops the packet and sends an ICMP "Time Exceeded" message back to the source. This is how `traceroute` works — it sends packets with TTL=1 (gets response from first hop), TTL=2 (gets response from second hop), etc., mapping the route.

---

**Q4.** A company uses RFC 1918 private IP addresses (10.0.0.0/8) internally. How do employees access the internet if their IPs are not routable on the public internet?

**Answer:** NAT (Network Address Translation). The firewall/router maintains a NAT table mapping internal IP:port to a single (or few) public IP addresses. When an internal host sends traffic out, the firewall rewrites the source IP to the public IP and records the mapping. Return traffic comes in to the public IP, and the firewall looks up the table to forward it to the correct internal host. This is why a home router with one public IP can serve many internal devices.

---

**Q5.** What is a TCP SYN flood attack and why is it effective? What is the defence (SYN cookies) and how does it work?

**Answer:** A SYN flood sends many SYN packets (connection requests) without completing the three-way handshake (never sends the ACK). The server allocates memory for each half-open connection in a backlog queue. If the queue fills up, legitimate connections are refused. SYN cookies defend against this: instead of allocating state immediately, the server generates a cryptographic cookie as the initial sequence number in the SYN-ACK. If the client completes the handshake (sends ACK with the expected value), the server can reconstruct the connection without having stored anything, so the backlog queue never fills.

---

**Q6.** Compare symmetric encryption (AES) and asymmetric encryption (RSA/ECC). How does TLS use BOTH in the same session?

**Answer:** Symmetric: same key to encrypt and decrypt — fast, can encrypt bulk data. Problem: how do you share the key securely? Asymmetric: public key encrypts (anyone can), private key decrypts (only the owner). Slow — impractical for bulk data. TLS uses both: asymmetric during the handshake to authenticate the server (certificate) and to establish a shared secret (ECDHE key exchange). Once the shared secret is established, symmetric AES is used for all session data — fast and secure.

---

**Q7.** What is DNSSEC and what problem does it solve? What is one limitation of DNSSEC?

**Answer:** DNSSEC (DNS Security Extensions) adds digital signatures to DNS records, allowing resolvers to verify that a DNS response came from the authoritative server and was not tampered with in transit. This prevents DNS spoofing/cache poisoning attacks. Limitation: DNSSEC does NOT encrypt DNS queries — anyone intercepting the network can still see what domains you are querying. (DNS over HTTPS/TLS solves the privacy problem; DNSSEC solves the integrity problem.)

---

**Q8.** What is the difference between a hub, a switch, and a router? At which OSI layer does each operate?

**Answer:**
- **Hub (Layer 1 — Physical):** Broadcasts all traffic to all ports. Every device sees every packet. Obsolete for security — a single promiscuous mode adapter captures all traffic.
- **Switch (Layer 2 — Data Link):** Builds a MAC address table and forwards frames only to the correct port. Devices don't see each other's traffic. Security improvement over hub, but still vulnerable to MAC flooding/ARP spoofing.
- **Router (Layer 3 — Network):** Connects different networks, makes forwarding decisions based on IP addresses. Can segment networks with different subnets, apply ACLs, and perform NAT.

---

## Section B: Packet Analysis (Questions 9-13)

**Q9.** You see the following Wireshark capture. What is happening?
```
192.168.1.100 → 192.168.1.1   TCP  SYN   port 80
192.168.1.100 → 192.168.1.1   TCP  SYN   port 443
192.168.1.100 → 192.168.1.1   TCP  SYN   port 22
192.168.1.100 → 192.168.1.1   TCP  SYN   port 8080
192.168.1.100 → 192.168.1.1   TCP  SYN   port 3389
[No SYN-ACK responses, just the SYNs repeating...]
```

**Answer:** This is a TCP SYN scan (nmap `-sS` or similar). The attacker at 192.168.1.100 is scanning the target at 192.168.1.1 to discover which ports are open. The lack of SYN-ACK suggests either: the ports are closed (RST response), firewalled (no response), or the attacker is moving too fast to see the responses in this capture window. Detection: port scan detection rules in IDS/SIEM (many SYNs to different ports from one source in a short time).

---

**Q10.** Calculate: A packet leaves host A with TTL=64. It traverses 15 routers before reaching host B. What TTL value arrives at host B?

**Answer:** TTL=64−15=49. Each router decrements TTL by 1. If the TTL had been only 14, the packet would be dropped at the 15th router (TTL would hit 0), and host A would receive an ICMP Time Exceeded message.

---

**Q11.** You capture a DNS response for `evil.example.com` that returns `192.168.1.1` (an internal IP). You know this is wrong — the real IP should be `203.0.113.10`. What attack might be occurring?

**Answer:** DNS cache poisoning (DNS spoofing). An attacker has injected a false DNS record, redirecting users to a malicious/unintended IP. This could be used for: phishing (attacker controls 192.168.1.1 and hosts a fake login page), man-in-the-middle (intercepting credentials), or denial of service (sending users to a non-existent server). Defences: DNSSEC, DNS over HTTPS, monitoring for unexpected DNS response changes.

---

**Q12.** A web application sends this HTTP response header:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```
What does this header do and what attack does it prevent?

**Answer:** HTTP Strict Transport Security (HSTS) tells the browser to ALWAYS use HTTPS for this domain (and all subdomains due to `includeSubDomains`) for the next 31,536,000 seconds (1 year). `preload` means this domain can be submitted to browser HSTS preload lists (hardcoded into browsers). It prevents SSL stripping attacks — where a man-in-the-middle downgrades an HTTPS connection to HTTP before the browser connects. Even if an attacker strips HTTPS from the initial request, a browser with HSTS cached for this domain will refuse to connect over HTTP.

---

**Q13.** Identify the OSI layer for each of these:
a) MAC address collision on a switch  
b) TCP port 443 being blocked by a firewall  
c) A router choosing which path to forward a packet  
d) Bit errors on a cable due to interference  
e) HTTP GET request failing with 404

**Answer:**
a) Layer 2 (Data Link) — MAC addresses operate at Layer 2
b) Layer 4 (Transport) — port numbers are a Layer 4 concept
c) Layer 3 (Network) — routing decisions are based on IP (Layer 3)
d) Layer 1 (Physical) — electrical interference is a physical layer problem
e) Layer 7 (Application) — HTTP is an application layer protocol; 404 is an HTTP status code

---

## Section C: Subnetting (Questions 14-17)

**Q14.** For the network `172.16.50.0/23`, calculate:
a) The subnet mask in dotted decimal  
b) The number of usable host addresses  
c) The broadcast address  
d) The first and last usable host addresses

**Answer:**
a) /23 = 255.255.254.0 (23 ones in binary: 11111111.11111111.11111110.00000000)
b) 2^9 - 2 = 510 usable hosts (/23 leaves 9 host bits, 2^9=512, minus network and broadcast)
c) 172.16.51.255
d) First: 172.16.50.1 / Last: 172.16.51.254

---

**Q15.** A company has 5 departments: Sales (50 hosts), Engineering (100 hosts), Finance (25 hosts), HR (12 hosts), Management (5 hosts). Design a subnetting scheme using 192.168.0.0/24. Assign the smallest appropriate subnet to each department (to minimise IP waste).

**Answer:**
- Engineering (100 hosts): needs /25 (126 hosts) → 192.168.0.0/25 (hosts .1-.126)
- Sales (50 hosts): needs /26 (62 hosts) → 192.168.0.128/26 (hosts .129-.190)
- Finance (25 hosts): needs /27 (30 hosts) → 192.168.0.192/27 (hosts .193-.222)
- HR (12 hosts): needs /28 (14 hosts) → 192.168.0.224/28 (hosts .225-.238)
- Management (5 hosts): needs /29 (6 hosts) → 192.168.0.240/29 (hosts .241-.246)
- Remaining: 192.168.0.248/29 (spare)

---

**Q16.** Is `10.10.128.50` in the same subnet as `10.10.192.100` if the subnet mask is 255.255.128.0 (/17)?

**Answer:**
- 10.10.128.50 with /17: network = 10.10.128.0 (128 in binary is 10000000; the /17 mask covers the first 17 bits)
- 10.10.192.100 with /17: network = 10.10.128.0 (192 in binary is 11000000; both 128 and 192 have the same first bit set, so same /17 network)
- **Yes, they are in the same /17 subnet (10.10.128.0/17)**

---

**Q17.** Explain the difference between a public IP address and a private IP address. List the three RFC 1918 private address ranges.

**Answer:** Public IPs are globally routable on the internet — assigned by IANA through ISPs. Private IPs are reserved for internal/local networks — not routable on the public internet (ISPs filter them). NAT translates between private and public. RFC 1918 private ranges:
- 10.0.0.0/8 (10.0.0.0 – 10.255.255.255)
- 172.16.0.0/12 (172.16.0.0 – 172.31.255.255)
- 192.168.0.0/16 (192.168.0.0 – 192.168.255.255)

---

## Section D: Applied Security Scenarios (Questions 18-22)

**Q18.** A user reports their browser shows a certificate error when visiting your company's internal website. The error says "Certificate issued for: *.evil-corp.com". What is happening and what should the user do?

**Answer:** This is likely a man-in-the-middle (MITM) attack or corporate proxy interception. The attacker/proxy is intercepting the HTTPS traffic and presenting their own certificate. The user should: (1) NOT proceed past the warning — do NOT click "Accept Risk" or "Proceed Anyway", (2) immediately disconnect from the network, (3) report to the security team, (4) not enter any credentials. The security team should investigate the network route between the user's machine and the server.

---

**Q19.** You are analysing logs and see thousands of ICMP echo requests per second from a single external IP to your web server. What type of attack is this? What are two mitigations?

**Answer:** This is an ICMP flood (a type of DoS/DDoS attack). The attacker is attempting to overwhelm your server's processing capacity. Mitigations: (1) Rate limit or block ICMP at the firewall/router — most web servers don't need to respond to external pings, (2) Contact your ISP or DDoS mitigation provider (Cloudflare, Akamai) to filter traffic upstream before it reaches your network, (3) If available, enable cloud-based DDoS scrubbing services.

---

**Q20.** Write a simple firewall policy for a web server that should only serve HTTP (80) and HTTPS (443) traffic from the internet, and allow SSH (22) only from the admin network `10.0.1.0/24`.

**Answer:**
```
# Default policy: DROP everything
iptables -P INPUT DROP
iptables -P FORWARD DROP

# Allow established/related connections (return traffic)
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow web traffic from anywhere
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow SSH ONLY from admin network
iptables -A INPUT -p tcp --dport 22 -s 10.0.1.0/24 -j ACCEPT

# Everything else: DROP (already covered by default policy)
```

---

**Q21.** What is a "man-in-the-middle" (MITM) attack at the network layer? Describe an ARP spoofing MITM attack step by step, then describe three defences.

**Answer:** MITM: the attacker positions themselves between two communicating parties, intercepting and potentially modifying communications. ARP Spoofing MITM: (1) Attacker sends unsolicited ARP replies claiming "I have the IP of the gateway, here's my MAC". (2) Victim updates ARP cache to point gateway IP → attacker's MAC. (3) Victim sends traffic meant for gateway to attacker instead. (4) Attacker forwards traffic (so nothing seems broken) while reading/modifying it. (5) Attacker repeats to the gateway, spoofing the victim's IP.

Defences: (1) Dynamic ARP Inspection (DAI) on managed switches — validates ARP packets against a DHCP snooping table, (2) Static ARP entries for critical servers, (3) Encrypt all sensitive communications (HTTPS/TLS) so even if traffic is intercepted, it's unreadable.

---

**Q22.** A Wireshark filter `tcp.flags.push==1 && tcp.flags.ack==1 && tcp.len > 1000` matches packets. Explain what these packets are and give a real-world example of when you'd see them.

**Answer:** These are TCP data transfer packets — PSH flag means "deliver this data to the application immediately" (don't buffer), ACK acknowledges previous data, and `tcp.len > 1000` means they contain more than 1000 bytes of payload. Real-world example: a large HTTP response body being delivered from a web server to a browser. Each segment has PSH+ACK set (push the data up to the HTTP layer), and carries a chunk of the web page content (>1000 bytes = real data, not just a handshake or keepalive).

---

## Section E: Design and Analysis (Questions 23-25)

**Q23.** Design a secure DNS architecture for a company that needs: internal DNS (for `corp.local`), external DNS (for `example.com`), and protection against DNS-based data exfiltration.

**Answer:** Architecture: (1) **Split-horizon DNS** — internal DNS server (Windows DNS or BIND) that knows about `corp.local` addresses and is not accessible from the internet. (2) **External authoritative DNS** — hosted at DNS provider (Cloudflare, Route53) for `example.com`. (3) **Internal recursive resolver** — forwards external lookups to internal server → internet-facing forwarder → upstream (Cloudflare 1.1.1.1 or 8.8.8.8). (4) **DNS filtering** for data exfiltration protection: deploy Cisco Umbrella, Cloudflare Gateway, or internal DNS RPZ rules that (a) block known malicious domains, (b) alert on unusually long DNS queries (exfiltration often encodes data in subdomains: `data.AAAAABBBBCCCC.malicious.com`), (c) rate-limit DNS queries per host, (d) block DNS queries to external resolvers (all DNS must go through the company's DNS servers).

---

**Q24.** Explain what happens at the network level during a TLS 1.3 handshake. Why is TLS 1.3 faster and more secure than TLS 1.2?

**Answer:** TLS 1.3 handshake (1-RTT):
1. Client → Server: ClientHello (including key_share with Diffie-Hellman public key)
2. Server → Client: ServerHello + Certificate + CertificateVerify (signature) + Finished. Server can already derive session keys from the DH key exchange.
3. Client → Server: Finished. Client verifies the certificate and signature.
4. Encrypted application data flows immediately.

**Why faster:** TLS 1.2 required 2 round trips before data could flow. TLS 1.3 achieves key exchange and authentication in 1 round trip. TLS 1.3 also supports 0-RTT resumption for returning visitors (data sent with the first packet).

**Why more secure:** TLS 1.3 removed all weak cipher suites (RC4, MD5, SHA-1, RSA key exchange without forward secrecy, 3DES). It mandates Perfect Forward Secrecy (ECDHE) — compromising the server's private key later cannot decrypt past sessions. It encrypts more of the handshake, hiding certificate information from passive observers.

---

**Q25.** A security analyst sees this in their SIEM:
```
Source IP: 10.0.5.100 (internal workstation)
DNS queries in 10 minutes:
  aHR0cHM6Ly9ld.malware-c2.com
  aHR0cHM6Ly9lb.malware-c2.com  
  aHR0cHM6Ly9lc.malware-c2.com
  aHR0cHM6Ly9ld.malware-c2.com
  [48 more similar queries...]
```
What technique is the attacker using? What data is likely being exfiltrated? How should the analyst respond?

**Answer:** This is **DNS tunnelling / data exfiltration via DNS**. The attacker is encoding data in subdomain labels (the prefixes before `malware-c2.com` look like Base64 — `aHR0cHM6Ly9l` decodes to `https://e`, which might be the start of a URL or other stolen data). Each DNS query carries a small chunk of data to the attacker's DNS server, which logs all queries and reassembles the data.

**Response:** (1) Immediately isolate workstation `10.0.5.100` from the network, (2) Block all DNS queries to `malware-c2.com` at the DNS resolver, (3) Capture memory of the workstation (volatile evidence), (4) Search all other workstations for DNS queries to the same C2 domain (lateral spread?), (5) Investigate what malware on `10.0.5.100` is making these queries — what process is calling DNS? (6) Determine what data was exfiltrated — Base64 decode as many subdomains as possible, (7) Report incident per your IR procedure.

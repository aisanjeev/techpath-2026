# Month 8 — Web Application Security: Tools & Resources

## Core Tools

| Tool | Purpose | Download |
|---|---|---|
| Burp Suite Community | Web proxy, scanner, intruder | https://portswigger.net/burp/communitydownload |
| Burp Suite Pro | Full scanner + advanced intruder | https://portswigger.net/burp/pro |
| OWASP ZAP | Free web app scanner | https://www.zaproxy.org/download/ |
| SQLMap | Automated SQL injection | https://sqlmap.org/ |
| Nikto | Web server scanner | https://github.com/sullo/nikto |
| Gobuster | Directory/DNS brute-forcing | https://github.com/OJ/gobuster/releases |
| ffuf | Fast web fuzzer | https://github.com/ffuf/ffuf/releases |
| Postman | API testing and documentation | https://www.postman.com/downloads/ |
| Insomnia | REST/GraphQL API client | https://insomnia.rest/download |

## Vulnerable Practice Applications

| App | Description | Setup |
|---|---|---|
| DVWA | PHP app with configurable vuln levels | `docker run -p 80:80 vulnerables/web-dvwa` |
| OWASP Juice Shop | Modern Node.js app (100+ challenges) | `docker run -p 3000:3000 bkimminich/juice-shop` |
| WebGoat | Java-based OWASP training app | `docker run -p 8080:8080 webgoat/goatandwolf` |
| HackTheBox Web Challenges | CTF-style web challenges | https://www.hackthebox.com/challenges |
| PortSwigger Labs | Free browser-based web security labs | https://portswigger.net/web-security |
| PentesterLab | Structured web security exercises | https://pentesterlab.com/ |

## Learning Resources

| Resource | Type | URL |
|---|---|---|
| PortSwigger Web Security Academy | Free labs + theory | https://portswigger.net/web-security |
| OWASP Top 10 (2021) | Official reference | https://owasp.org/Top10/ |
| OWASP Testing Guide v4.2 | Comprehensive methodology | https://owasp.org/www-project-web-security-testing-guide/ |
| OWASP API Security Top 10 | API-specific reference | https://owasp.org/www-project-api-security/ |
| HackTricks — Web Attacks | Attack techniques wiki | https://book.hacktricks.xyz/pentesting-web |
| PayloadsAllTheThings | Payload reference library | https://github.com/swisskyrepo/PayloadsAllTheThings |
| JWT.io | JWT decoder/debugger | https://jwt.io |
| CyberChef | Data encode/decode/transform | https://gchq.github.io/CyberChef/ |

## Browser Extensions

| Extension | Purpose | Browser |
|---|---|---|
| FoxyProxy | Switch proxy on/off easily | Firefox / Chrome |
| Wappalyzer | Technology fingerprinting | Firefox / Chrome |
| Cookie-Editor | Inspect and modify cookies | Firefox / Chrome |
| HackBar | Quick payload injection bar | Firefox |

## Certifications

| Cert | Provider | URL |
|---|---|---|
| BSCP (Burp Suite Certified Practitioner) | PortSwigger | https://portswigger.net/web-security/certification |
| GWAPT (Web App Pen Tester) | GIAC | https://www.giac.org/certifications/web-application-penetration-tester-gwapt/ |
| eWPT (Web Penetration Tester) | INE Security | https://ine.com/certifications/ewpt-certification |
| OSWE | Offensive Security | https://www.offsec.com/certifications/exp-312/ |

## YouTube / Video Resources

- **LiveOverflow** — Deep web security research: https://www.youtube.com/@LiveOverflow
- **STÖK** — Bug bounty methodology: https://www.youtube.com/@STOKfredrik
- **NahamSec** — Bug bounty and web hacking: https://www.youtube.com/@NahamSec
- **PortSwigger** — Official labs walkthroughs: https://www.youtube.com/@PortSwiggerTV

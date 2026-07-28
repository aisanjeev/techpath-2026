# Assignment: Computer Communication and Internet

**Module 05 — CCC Exam Preparation**

---

## Instructions

Complete all four tasks below. For each task, write down your observations and take screenshots where indicated. Submit your completed assignment to your trainer.

---

## Task 1: Connect to WiFi and Check Your IP Address

**Objective:** Learn how to connect to a WiFi network and find your device's IP address.

### Steps:

1. **Connect to WiFi:**
   - On your computer, click the WiFi icon in the taskbar (bottom-right corner)
   - Find the WiFi network name (SSID) of the classroom/lab WiFi
   - Click on it and enter the password
   - Confirm you are connected (the WiFi icon should show connected)

2. **Find your IP Address (Method 1 — Settings):**
   - Open **Settings** > **Network & Internet** > **WiFi**
   - Click on the connected network name
   - Scroll down to find your **IPv4 address**
   - Write it down: _______________

3. **Find your IP Address (Method 2 — Command Prompt):**
   - Open **Command Prompt** (search "cmd" in Start menu)
   - Type: `ipconfig` and press Enter
   - Find the line that says **IPv4 Address**
   - Write it down: _______________

4. **Find your Default Gateway (Router IP):**
   - In the same ipconfig output, find **Default Gateway**
   - Write it down: _______________
   - This is the IP address of the WiFi router you are connected to

5. **Find your Public IP Address:**
   - Open your web browser (Chrome)
   - Go to: https://www.whatismyip.com
   - Write down the public IP shown: _______________

### Questions to Answer:
- Is your private IP (IPv4) the same as your public IP? Why or why not?
- How many other devices are connected to the same WiFi? (Ask your trainer or classmates for their IPs)
- What is the difference between a private IP and a public IP?

---

## Task 2: Identify Parts of a URL

**Objective:** Understand the structure of a URL by examining real websites.

### Steps:

1. **Open Chrome** and visit: `https://www.irctc.co.in/nget/train-search`

2. **Break down the URL into parts:**

   ```
   https://www.irctc.co.in/nget/train-search
   |_____|  |______________|  |_____________|
   Protocol    Domain Name       Path
   ```

   - **Protocol:** _______________
   - **Subdomain:** _______________
   - **Domain Name:** _______________
   - **Country Code:** _______________
   - **Path:** _______________

3. **Now visit these websites and break down each URL:**

   | Website URL | Protocol | Domain | Path |
   |-------------|----------|--------|------|
   | https://www.google.com/search?q=CCC+exam | | | |
   | https://www.digilocker.gov.in/dashboard | | | |
   | https://student.nielit.gov.in | | | |
   | http://example.com/page.html | | | |

4. **Security Check:**
   - Which of the above URLs use HTTPS (secure)? _____________
   - Which uses HTTP (not secure)? _____________
   - How can you tell if a website is secure? (Hint: look at the address bar)

### Questions to Answer:
- What does the padlock icon in the address bar mean?
- What is the difference between HTTP and HTTPS?
- What does ".gov.in" mean in a URL? What does ".co.in" mean?

---

## Task 3: Explore Network Settings on Your Computer

**Objective:** Understand the network configuration of your computer.

### Steps:

1. **Open Network Settings:**
   - Right-click the WiFi/Network icon in the taskbar
   - Select **Network and Internet settings**
   - Click on **Properties** of your connected network

2. **Record the following information:**
   | Setting | Value |
   |---------|-------|
   | Network Name (SSID) | |
   | Status (Connected/Disconnected) | |
   | IPv4 Address | |
   | IPv6 Address | |
   | DNS Server | |
   | Network Type (Private/Public) | |

3. **Open Command Prompt and run these commands:**

   a) `ipconfig /all` — Record the following:
   - Physical Address (MAC Address): _______________
   - DHCP Enabled (Yes/No): _______________
   - DNS Servers: _______________

   b) `ping google.com` — Record the following:
   - Did you get a reply? (Yes/No): _______________
   - Average response time: _______________
   - This tells you: your internet is working and how fast the connection is

   c) `nslookup google.com` — Record the following:
   - IP Address of google.com: _______________
   - This demonstrates DNS in action — converting a name to an IP address

   d) `tracert google.com` — Record the following:
   - Number of hops: _______________
   - This shows all the routers between your computer and Google's server

### Questions to Answer:
- What is a MAC address? How is it different from an IP address?
- What does DHCP do?
- Why does `tracert` show multiple hops? What are these hops?

---

## Task 4: Explore Digital India Services

**Objective:** Familiarize yourself with important e-governance services covered in the CCC exam.

### Steps:

1. **Explore DigiLocker:**
   - Open Chrome and go to: https://www.digilocker.gov.in
   - Look at the homepage and note what services are offered
   - List 3 types of documents you can store in DigiLocker:
     1. _______________
     2. _______________
     3. _______________

2. **Explore UMANG:**
   - Go to: https://web.umang.gov.in
   - Browse the available services
   - List 5 government services available on UMANG:
     1. _______________
     2. _______________
     3. _______________
     4. _______________
     5. _______________

3. **Explore Cyber Crime Reporting:**
   - Go to: https://cybercrime.gov.in
   - Note what types of crimes can be reported:
     - _______________
     - _______________
     - _______________
   - What is the helpline number for financial fraud? _______________

4. **Internet Security Self-Assessment:**
   - Check if your passwords are strong using these criteria:
     | Criteria | Your Gmail Password | Your Bank App Password |
     |----------|-------------------|----------------------|
     | At least 8 characters? | Yes/No | Yes/No |
     | Has uppercase letters? | Yes/No | Yes/No |
     | Has lowercase letters? | Yes/No | Yes/No |
     | Has numbers? | Yes/No | Yes/No |
     | Has special characters? | Yes/No | Yes/No |
     | Is it unique (not used elsewhere)? | Yes/No | Yes/No |
   - If any answer is "No," consider updating your passwords to be stronger

### Questions to Answer:
- What is the full form of UMANG?
- Why is DigiLocker useful? Give two practical benefits.
- If someone steals money from your bank account online, where should you report it?
- Name two Digital India initiatives that help rural India.

---

## Submission Guidelines

- Complete all 4 tasks
- Write answers clearly in your notebook or type them in a document
- Take screenshots where indicated
- Submit to your trainer by the end of the class

**Marks Distribution:**
| Task | Marks |
|------|-------|
| Task 1: WiFi and IP Address | 10 |
| Task 2: URL Parts | 10 |
| Task 3: Network Settings | 10 |
| Task 4: Digital India Services | 10 |
| **Total** | **40** |

---

*TechPath Institute — CCC Exam Preparation*

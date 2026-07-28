# Module 07 — Communication & Collaboration: Email

**Comprehensive Notes — CCC Exam Preparation**

**Expected Exam Weight: 6-8 MCQs out of 100**

---

## 1. Introduction to Email

**Email (Electronic Mail)** is a method of exchanging digital messages over the internet. It was one of the first services on the internet and remains one of the most important tools for both personal and professional communication.

Email allows users to:
- Send and receive text messages instantly
- Attach files (documents, images, videos)
- Communicate with one person or hundreds simultaneously
- Maintain a written record of conversations
- Access messages from any device with internet

### Email Address Format
Every email address follows the format: `username@domain.com`

**Three components:**
1. **Username** (local part) — Unique identifier chosen by the user (e.g., `rahul.sharma`)
2. **@ symbol** — Separator between username and domain. Pronounced "at"
3. **Domain name** — The email service provider (e.g., `gmail.com`, `yahoo.com`)

**Example:** In `priya@techpath.biz`, "priya" is the username, "@" is the separator, and "techpath.biz" is the domain.

### Popular Email Services in India
| Service | Domain | Free Storage |
|---------|--------|-------------|
| Gmail (Google) | @gmail.com | 15 GB |
| Yahoo Mail | @yahoo.com | 1 TB |
| Outlook (Microsoft) | @outlook.com | 15 GB |
| Rediffmail | @rediffmail.com | 1 GB |

---

## 2. Email Operations

### Composing an Email
The compose window in Gmail contains these fields:

| Field | Purpose |
|-------|---------|
| To | Primary recipient (mandatory) |
| CC (Carbon Copy) | Additional recipients (visible to all) |
| BCC (Blind Carbon Copy) | Hidden recipients (invisible to others) |
| Subject | Brief topic description |
| Body | Main message content |
| Attach (paperclip icon) | Add files to the email |

### To vs CC vs BCC

| Feature | To | CC | BCC |
|---------|----|----|-----|
| Full form | (Direct recipient) | Carbon Copy | Blind Carbon Copy |
| Visibility | Visible to all | Visible to all | Hidden from all |
| Purpose | Primary audience | For information | Privacy/mass mail |
| Who sees them | Everyone | Everyone | Only sender |

**Key exam fact:** BCC recipients are hidden — no other recipient can see who was added in BCC.

### Reply, Reply All, and Forward

| Action | What It Does | Subject Prefix |
|--------|-------------|----------------|
| Reply | Sends response to original sender only | Re: |
| Reply All | Sends response to sender + all CC recipients | Re: |
| Forward | Sends the email to a new person | Fwd: |

### Attachments
- Files sent along with an email
- **Gmail maximum attachment size: 25 MB** (extremely frequently asked)
- Files larger than 25 MB are shared via Google Drive automatically
- Gmail blocks executable files (.exe, .bat) for security
- Common attachment types: PDF, DOCX, XLSX, PPTX, JPG, PNG, ZIP

---

## 3. Mailbox Folders

Every email account has standard folders for organizing messages:

| Folder | Contains | Auto-delete? |
|--------|----------|-------------|
| **Inbox** | All received emails | No |
| **Sent Mail** | Copies of sent emails | No |
| **Drafts** | Unsent/incomplete emails | No |
| **Spam/Junk** | Unwanted/suspicious emails | Yes — after 30 days |
| **Trash/Bin** | Deleted emails | Yes — after 30 days |
| **Starred** | Emails marked with a star | No |
| **All Mail** | Every email (including archived) | No |

**Key exam facts:**
- Drafts = emails saved but not sent
- Spam and Trash are auto-cleared after **30 days** in Gmail
- Sent folder stores a copy of every email you send

### Gmail Inbox Categories
Gmail organizes the Inbox into tabs:
- **Primary** — Important personal emails
- **Social** — Social media notifications
- **Promotions** — Marketing and offers
- **Updates** — Bills, receipts, notifications

### Labels and Filters
- **Labels** are tags/categories for organizing emails (like colored stickers)
- One email can have multiple labels
- **Filters** automatically sort incoming emails based on rules (sender, subject, keywords)
- **Archiving** removes an email from Inbox without deleting it (goes to All Mail)

### Contacts (Address Book)
- Stores names, email addresses, and phone numbers
- Enables auto-complete when typing email addresses
- Can create contact groups for sending emails to multiple people
- Accessible at contacts.google.com

---

## 4. Email Protocols

Email uses three main protocols:

### SMTP (Simple Mail Transfer Protocol)
- **Purpose:** Sending emails
- **Port:** 25 (default), 587 (secure)
- **Direction:** Outgoing
- **Memory trick:** **S**MTP = **S**ending

### POP3 (Post Office Protocol version 3)
- **Purpose:** Downloading/receiving emails
- **Port:** 110 (default), 995 (secure)
- **Behavior:** Downloads emails to local device and deletes from server (by default)
- **Best for:** Single-device users
- **Offline access:** Full (emails are local)

### IMAP (Internet Message Access Protocol)
- **Purpose:** Syncing emails across devices
- **Port:** 143 (default), 993 (secure)
- **Behavior:** Keeps emails on server, syncs across all devices
- **Best for:** Multi-device users (phone + laptop + tablet)
- **Offline access:** Limited

### POP3 vs IMAP — Key Differences

| Feature | POP3 | IMAP |
|---------|------|------|
| Emails stored | Local device | Server |
| After access | Deleted from server | Kept on server |
| Multi-device | No sync | Synced |
| Offline access | Full | Limited |
| Storage used | Local disk | Server space |

### Store-and-Forward Model
Email delivery follows the Store-and-Forward model:
1. Sender composes email → SMTP sends to sender's mail server
2. Sender's server → SMTP forwards to recipient's mail server
3. Recipient's server stores the email
4. Recipient retrieves via POP3 or IMAP

Each server **stores** the email temporarily before **forwarding** it to the next hop. If the next server is unavailable, the email is queued and retried.

---

## 5. Netiquette (Network Etiquette)

**Netiquette** = Network + Etiquette = Rules of polite behavior on the internet.

### Important Netiquette Rules
1. **ALL CAPS = SHOUTING** — Never type entire messages in capitals
2. Be polite and respectful
3. Think before posting — content is hard to remove once shared
4. Respect others' privacy
5. Do not spam
6. Give credit to original content creators
7. Use proper grammar in professional communication
8. Respond to emails within 24-48 hours
9. Avoid forwarding chain emails

---

## 6. Spam and Phishing

### Spam
- **Definition:** Unsolicited bulk emails sent without consent
- **Types:** Advertising, chain emails, scams, malware
- **Handling:** Mark as spam, do not click links, do not reply, do not open attachments

### Phishing
- **Definition:** Fake emails impersonating trusted organizations to steal personal information
- **Warning signs:**
  - Suspicious sender address
  - Generic greeting ("Dear Customer")
  - Urgent language ("Account will be closed!")
  - Spelling/grammar mistakes
  - Requests for passwords, PINs, OTPs
  - Suspicious links (hover to check real URL)
- **Protection:** Never share passwords via email, verify sender, enable 2FA

**Key exam fact:** Banks and government agencies **never** request passwords, PINs, or OTPs via email.

---

## 7. Instant Messaging

**Instant Messaging (IM)** is real-time text communication over the internet.

### Popular IM Apps in India
- WhatsApp, Telegram, Signal, Google Chat, Facebook Messenger

### Email vs Instant Messaging
| Feature | Email | Instant Messaging |
|---------|-------|-------------------|
| Speed | Fast | Instant (real-time) |
| Formality | Formal | Informal |
| Best for | Official records | Quick conversations |

### Emoticons vs Emojis
- **Emoticons:** Text-based expressions using keyboard characters (e.g., `:-) :-(`)
- **Emojis:** Graphical icons representing emotions, objects, etc.
- Use in informal communication only — avoid in professional emails

---

## Exam Tips — Most Frequently Asked Questions

| Question Pattern | Answer |
|-----------------|--------|
| Email stands for | Electronic Mail |
| CC stands for | Carbon Copy |
| BCC stands for | Blind Carbon Copy |
| BCC recipients are visible to | No one (except the sender) |
| The @ symbol separates | Username from domain name |
| Maximum Gmail attachment size | 25 MB |
| SMTP is used to | Send emails |
| POP3 is used to | Download/receive emails |
| IMAP is used to | Sync emails across devices |
| POP3 deletes email from | Server (after downloading) |
| IMAP keeps email on | Server |
| Drafts folder contains | Unsent/incomplete emails |
| Spam is auto-deleted after | 30 days |
| Trash is auto-deleted after | 30 days |
| ALL CAPS on internet means | Shouting |
| Netiquette means | Network etiquette / Internet manners |
| Spam is | Unsolicited bulk email |
| Phishing is | Fake email to steal personal info |
| Default SMTP port | 25 |
| Default POP3 port | 110 |
| Default IMAP port | 143 |
| Store-and-Forward means | Email is stored at each server before forwarding |

---

## Summary Table

| Topic | Key Points |
|-------|-----------|
| Email Basics | Electronic mail, username@domain format, free services (Gmail) |
| Email Operations | Compose, To/CC/BCC, Reply/Reply All/Forward, 25 MB attachment limit |
| Mailbox Folders | Inbox, Sent, Drafts, Spam, Trash — Spam & Trash cleared after 30 days |
| Protocols | SMTP (send), POP3 (download), IMAP (sync), Store-and-Forward model |
| Netiquette | Internet manners, ALL CAPS = shouting, respect privacy |
| Spam & Phishing | Spam = junk mail, Phishing = fake emails for stealing info |
| Instant Messaging | Real-time chat (WhatsApp), emoticons vs emojis |

---

*TechPath Institute — CCC Exam Preparation Course*
*Module 07: Communication & Collaboration — Email*
*Total expected questions: 6-8 out of 100 MCQs*

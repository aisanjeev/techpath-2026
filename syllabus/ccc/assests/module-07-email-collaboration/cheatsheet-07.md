# Cheatsheet — Module 07: Communication & Collaboration (Email)

**CCC Exam Quick Revision**

---

## Email Address Format

```
username  @  domain.com
   |      |      |
 Local  Separator  Service Provider
 Part    ("at")    (gmail.com, yahoo.com)
```

**Rule:** Every email must have exactly ONE @ symbol.

---

## To vs CC vs BCC

| Field | Full Form | Visible to Others? | Use When |
|-------|-----------|-------------------|----------|
| **To** | (Direct recipient) | Yes | Primary audience |
| **CC** | Carbon Copy | Yes | Keeping someone informed |
| **BCC** | Blind Carbon Copy | **No** (hidden) | Mass emails / privacy |

**Quick rule:** CC = everyone sees. BCC = no one sees.

---

## Email Actions

| Action | What Happens | Subject Prefix |
|--------|-------------|----------------|
| **Reply** | Sends to original sender only | Re: |
| **Reply All** | Sends to sender + all CC | Re: |
| **Forward** | Sends to a new recipient | Fwd: |

---

## Mailbox Folders

| Folder | Purpose | Auto-Delete? |
|--------|---------|-------------|
| **Inbox** | Received emails | No |
| **Sent** | Copies of sent emails | No |
| **Drafts** | Unsent emails | No |
| **Spam** | Junk/unwanted mail | **30 days** |
| **Trash** | Deleted emails | **30 days** |
| **Starred** | Important (starred) emails | No |
| **All Mail** | Everything (including archived) | No |

---

## Email Protocol Comparison

| Protocol | Full Form | Purpose | Default Port | Secure Port |
|----------|-----------|---------|-------------|-------------|
| **SMTP** | Simple Mail Transfer Protocol | **Sending** | 25 | 587 |
| **POP3** | Post Office Protocol v3 | **Downloading** | 110 | 995 |
| **IMAP** | Internet Message Access Protocol | **Syncing** | 143 | 993 |

**Memory tricks:**
- **S**MTP = **S**ending
- **P**OP3 = **P**ulling (downloading) to local device
- **I**MAP = **I**nternet syncing across devices

---

## POP3 vs IMAP

| Feature | POP3 | IMAP |
|---------|------|------|
| Emails stored | Local device | Server |
| After reading | Deleted from server | Kept on server |
| Multi-device sync | No | Yes |
| Offline access | Full | Limited |
| Best for | One device | Multiple devices |

---

## Gmail Attachment Limits

| Service | Max Attachment Size |
|---------|-------------------|
| **Gmail** | **25 MB** |
| Yahoo | 25 MB |
| Outlook | 20 MB |

**If file > 25 MB:** Gmail auto-shares via Google Drive.

**Blocked file types:** .exe, .bat, .cmd (security risk)

---

## Gmail Search Operators

| Operator | Example | Finds |
|----------|---------|-------|
| `from:` | `from:priya@gmail.com` | Emails from Priya |
| `to:` | `to:amit@gmail.com` | Emails sent to Amit |
| `subject:` | `subject:meeting` | "meeting" in subject |
| `has:attachment` | `has:attachment` | All emails with files |
| `is:unread` | `is:unread` | Unread emails |
| `is:starred` | `is:starred` | Starred emails |
| `before:` | `before:2026/07/01` | Before July 1 |
| `after:` | `after:2026/06/01` | After June 1 |
| `label:` | `label:work` | Emails with "work" label |

---

## Gmail Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **C** | Compose new email |
| **R** | Reply |
| **A** | Reply All |
| **F** | Forward |
| **E** | Archive |
| **#** | Delete (move to Trash) |
| **S** | Star/unstar |
| **Ctrl + Enter** | Send email |
| **Ctrl + K** | Insert link |
| **Ctrl + B** | Bold |
| **Ctrl + I** | Italic |
| **Ctrl + U** | Underline |
| **/** | Search |

**Note:** Enable keyboard shortcuts in Gmail Settings first.

---

## Netiquette Quick Rules

| Rule | Explanation |
|------|-------------|
| No ALL CAPS | ALL CAPS = SHOUTING |
| Be polite | Use "please", "thank you" |
| Think before posting | Hard to undo once sent |
| Respect privacy | Don't share others' info without consent |
| No spam | Don't send bulk unwanted messages |
| Timely replies | Respond within 24-48 hours |
| Professional format | Greeting + Body + Closing + Signature |

---

## Spam vs Phishing

| Feature | Spam | Phishing |
|---------|------|----------|
| **What** | Junk/unwanted bulk email | Fake email impersonating trusted source |
| **Goal** | Advertising, nuisance | Steal passwords, bank details, PINs |
| **Danger level** | Annoying | Dangerous |
| **Action** | Mark as spam, delete | Report, never click links |

---

## Phishing Red Flags

1. Suspicious sender domain (e.g., bank-secure.xyz instead of sbi.co.in)
2. Generic greeting ("Dear Customer" not your name)
3. Urgent threats ("Account closed in 24 hours!")
4. Spelling/grammar mistakes
5. Requests for passwords, PINs, OTPs
6. Suspicious links (hover to check real URL)
7. "Too good to be true" offers

**Golden rule:** Banks NEVER ask for passwords or PINs via email.

---

## Emoticons vs Emojis

| Type | Made Of | Example |
|------|---------|---------|
| Emoticon | Keyboard characters | :-) :-( ;-) |
| Emoji | Graphical icons | Images/pictographs |

**Use in:** Casual messages only. **Avoid in:** Professional/formal emails.

---

## Email Store-and-Forward Flow

```
Sender → SMTP → Sender's Server → SMTP → Recipient's Server → POP3/IMAP → Recipient
```

---

## Top CCC Exam Questions — Quick Answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Email stands for? | Electronic Mail |
| 2 | CC stands for? | Carbon Copy |
| 3 | BCC stands for? | Blind Carbon Copy |
| 4 | @ symbol separates? | Username from domain |
| 5 | Gmail max attachment? | 25 MB |
| 6 | SMTP is used for? | Sending email |
| 7 | POP3 is used for? | Downloading email |
| 8 | IMAP is used for? | Syncing email |
| 9 | Drafts folder stores? | Unsent emails |
| 10 | Spam auto-deletes after? | 30 days |
| 11 | ALL CAPS means? | Shouting |
| 12 | Netiquette means? | Internet etiquette |
| 13 | Phishing goal? | Steal personal info |
| 14 | Default SMTP port? | 25 |
| 15 | POP3 vs IMAP key diff? | POP3 downloads locally; IMAP syncs on server |

---

*TechPath Institute — CCC Exam Quick Revision*
*Module 07: Communication & Collaboration — Email*

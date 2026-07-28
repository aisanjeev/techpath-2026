# Email Protocols

**Module 07 — CCC Exam Preparation | Topic 4**

---

## What are Email Protocols?

A **protocol** is a set of rules that computers follow to communicate with each other. Email protocols are the rules that govern how emails are sent, received, and stored on the internet.

Think of protocols like traffic rules — just as vehicles follow traffic rules to move safely on roads, computers follow protocols to exchange emails correctly.

There are three main email protocols you need to know for the CCC exam:

1. **SMTP** — For sending emails
2. **POP3** — For downloading/receiving emails
3. **IMAP** — For syncing/accessing emails

**CCC Exam Tip:** You must remember which protocol does what. A very common question format is: "SMTP is used for ___" (sending email) or "POP3 is used for ___" (receiving/downloading email).

---

## SMTP (Simple Mail Transfer Protocol)

### What is SMTP?
**SMTP** stands for **Simple Mail Transfer Protocol**. It is the protocol used for **sending** emails from your computer to the mail server and between mail servers.

### How SMTP Works
1. You compose an email and click **Send**
2. Your email client (Gmail, Outlook) connects to the SMTP server
3. The SMTP server checks the recipient's domain (e.g., yahoo.com)
4. The SMTP server transfers the email to the recipient's mail server
5. The email is stored in the recipient's mailbox

### Key Facts about SMTP
| Feature | Detail |
|---------|--------|
| Full form | Simple Mail Transfer Protocol |
| Purpose | **Sending** emails |
| Port number | 25 (default), 587 (secure/TLS) |
| Direction | Outgoing mail |
| Model | Push protocol (pushes mail to server) |

**CCC Exam Tip:** SMTP = **Sending** mail. Remember: **S** in SMTP = **S**ending. This memory trick helps in the exam.

---

## POP3 (Post Office Protocol version 3)

### What is POP3?
**POP3** stands for **Post Office Protocol version 3**. It is used for **downloading** (receiving) emails from the mail server to your local computer.

### How POP3 Works
1. Your email client connects to the POP3 mail server
2. It **downloads** all new emails to your computer
3. By default, the emails are **deleted from the server** after downloading
4. You can read emails **offline** (without internet) after downloading

### Key Facts about POP3
| Feature | Detail |
|---------|--------|
| Full form | Post Office Protocol version 3 |
| Purpose | **Downloading/receiving** emails |
| Port number | 110 (default), 995 (secure/SSL) |
| Direction | Incoming mail |
| Storage | Downloads to local device |
| Server copy | Deleted from server (by default) |
| Offline access | Yes — emails are stored locally |

### POP3 Analogy
POP3 works like a **physical post office** — you go to the post office, collect your letters, and take them home. The post office no longer has your letters once you pick them up.

**CCC Exam Tip:** POP3 **downloads** emails and (by default) **removes them from the server**. This means if you check email on your phone using POP3, those emails may not appear on your computer later.

---

## IMAP (Internet Message Access Protocol)

### What is IMAP?
**IMAP** stands for **Internet Message Access Protocol**. It is used for **accessing and syncing** emails across multiple devices without downloading them permanently.

### How IMAP Works
1. Your email client connects to the IMAP server
2. It shows you the emails that are **stored on the server**
3. Emails remain on the server — they are **not deleted** after reading
4. Any changes (read, delete, move) are **synced across all devices**

### Key Facts about IMAP
| Feature | Detail |
|---------|--------|
| Full form | Internet Message Access Protocol |
| Purpose | **Syncing/accessing** emails on server |
| Port number | 143 (default), 993 (secure/SSL) |
| Direction | Incoming mail |
| Storage | Emails stay on server |
| Server copy | Kept on server |
| Offline access | Limited — needs internet for full access |
| Multi-device | Yes — synced across all devices |

### IMAP Analogy
IMAP works like a **library** — you go to the library to read books, but the books stay in the library. You can visit from different locations and always find the same books available.

**CCC Exam Tip:** IMAP keeps emails on the server and syncs across devices. Most modern email services (Gmail, Outlook) use IMAP by default because people check email on multiple devices.

---

## POP3 vs IMAP — Comparison

This comparison is extremely important for the CCC exam.

| Feature | POP3 | IMAP |
|---------|------|------|
| Full form | Post Office Protocol v3 | Internet Message Access Protocol |
| Purpose | Download emails to device | Access emails on server |
| Emails stored | On local device | On server |
| Server copy after access | Deleted (by default) | Kept on server |
| Multi-device access | Difficult (email on one device only) | Easy (synced across all devices) |
| Offline access | Full access (emails are local) | Limited (needs internet) |
| Storage space used | Uses local storage | Uses server storage |
| Speed | Faster (emails are local) | Depends on internet speed |
| Best for | Single device users | Multiple device users |
| Port (default) | 110 | 143 |
| Port (secure) | 995 | 993 |

**CCC Exam Tip:** The POP3 vs IMAP comparison is one of the most commonly tested topics. Key difference: **POP3 downloads and deletes from server; IMAP keeps on server and syncs**.

---

## Store-and-Forward Model

The **Store-and-Forward** model is how email works on the internet. Here is the process:

### How Email Travels from Sender to Receiver

```
Sender (Rahul)
    |
    v
Rahul's Email Client (Gmail)
    |
    v  [SMTP - Sending]
Rahul's SMTP Server (smtp.gmail.com)
    |
    v  [SMTP - Forwarding between servers]
Priya's Mail Server (mail.yahoo.com)
    |
    v  [POP3/IMAP - Receiving]
Priya's Email Client (Yahoo Mail)
    |
    v
Receiver (Priya)
```

### Steps Explained:
1. **Rahul composes** an email to priya@yahoo.com and clicks Send
2. The email is sent via **SMTP** to Gmail's SMTP server
3. Gmail's SMTP server looks up Yahoo's mail server address
4. The email is **forwarded** via SMTP to Yahoo's mail server
5. Yahoo's mail server **stores** the email in Priya's mailbox
6. When Priya opens Yahoo Mail, her client uses **POP3 or IMAP** to retrieve the email

### Why "Store-and-Forward"?
- **Store:** Each server along the way temporarily stores the email before passing it on
- **Forward:** The email is forwarded from one server to the next until it reaches the destination
- If the recipient's server is temporarily unavailable, the sending server **stores** the email and **retries** later

**CCC Exam Tip:** Email uses the **Store-and-Forward** model. The email is stored at each intermediate server before being forwarded to the next one.

---

## Email Protocols Summary Table

| Protocol | Full Form | Purpose | Port | Secure Port |
|----------|-----------|---------|------|-------------|
| SMTP | Simple Mail Transfer Protocol | Sending emails | 25 | 587 |
| POP3 | Post Office Protocol v3 | Downloading emails | 110 | 995 |
| IMAP | Internet Message Access Protocol | Syncing emails | 143 | 993 |

---

## All Three Protocols Working Together

When you use Gmail or any email service, all three protocols work together:

| Action | Protocol Used |
|--------|--------------|
| You send an email | **SMTP** |
| Your friend receives (downloads) your email | **POP3** |
| Your friend reads email on phone and laptop (synced) | **IMAP** |
| Email travels between Gmail server and Yahoo server | **SMTP** |

---

## Key Terms to Remember

| Term | Meaning |
|------|---------|
| Protocol | Set of rules for computer communication |
| SMTP | Protocol for sending emails |
| POP3 | Protocol for downloading/receiving emails |
| IMAP | Protocol for syncing emails across devices |
| Store-and-Forward | Email delivery model — store at each hop, then forward |
| Port | A numbered channel on a server for specific services |
| Mail server | Computer that handles sending/receiving emails |
| Push protocol | Actively sends data (SMTP pushes emails) |

---

## Practice Questions

1. What does SMTP stand for and what is it used for?
2. How is POP3 different from IMAP?
3. Which protocol keeps emails on the server after reading?
4. Explain the Store-and-Forward model of email.
5. What is the default port number for SMTP?
6. Why is IMAP better for users with multiple devices?

---

*TechPath Institute — CCC Exam Preparation Course*
*Module 07: Communication & Collaboration — Email*

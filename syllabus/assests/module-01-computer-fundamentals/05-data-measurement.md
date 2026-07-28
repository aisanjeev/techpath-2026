# Data Measurement — Bits, Bytes, KB, MB, GB, TB

**Module 01 — Computer Fundamentals | Topic 5**

---

## The Smallest Unit: Bit

A **bit** is the smallest piece of data a computer can store. It can only be:
- **0** (off / no / false)
- **1** (on / yes / true)

Everything in a computer — text, photos, videos, music — is stored as billions of 0s and 1s.

---

## Bit to Byte

| Unit | How Much | Example |
|------|----------|---------|
| **1 Bit** | Single 0 or 1 | Like one light switch (on/off) |
| **1 Byte** | 8 Bits | One letter or number (like "A" or "5") |

> **Remember:** 1 Byte = 8 Bits. Always.

With 1 byte (8 bits), you can make **256 different combinations** (2^8 = 256). That's enough for all English letters (A-Z, a-z), numbers (0-9), and special characters (!@#$%).

---

## Full Data Size Table

| Unit | Short | Equal To | Real Life Example |
|------|-------|----------|-------------------|
| 1 Bit | b | 0 or 1 | One switch on/off |
| 1 Byte | B | 8 Bits | One typed letter |
| 1 Kilobyte | KB | 1,024 Bytes | A short text message |
| 1 Megabyte | MB | 1,024 KB | One MP3 song (~3-5 MB) |
| 1 Gigabyte | GB | 1,024 MB | A movie (~1-2 GB) |
| 1 Terabyte | TB | 1,024 GB | ~500 hours of video |
| 1 Petabyte | PB | 1,024 TB | All photos on Facebook (approx) |

> **Memory trick:** The order is: **B → KB → MB → GB → TB → PB**
> Each one is **1,024 times** the previous one.

---

## Why 1024 and Not 1000?

Computers work in **binary** (base 2), not decimal (base 10).

- 2^10 = **1,024** (closest power of 2 to 1000)
- So 1 KB = 1,024 Bytes, not 1,000 Bytes
- In daily life, companies sometimes round to 1000 (that's why a "500 GB" hard disk shows ~465 GB in Windows)

---

## Common File Sizes

| File Type | Typical Size |
|-----------|-------------|
| Text message (WhatsApp) | 1-5 KB |
| Word document (few pages) | 50-500 KB |
| One photo (phone camera) | 2-5 MB |
| One MP3 song | 3-5 MB |
| One HD video (1 min) | 100-200 MB |
| One movie (Full HD) | 1-3 GB |
| Windows 11 installation | ~25 GB |
| GTA V game | ~100 GB |

---

## ASCII and Unicode — How Text is Stored

### ASCII (Old System)
- Uses **7 bits** per character
- Can store **128 characters** (English letters, numbers, basic symbols)
- Example: A = 65, B = 66, a = 97, 0 = 48

### Unicode (Modern System)
- Uses **8 to 32 bits** per character
- Can store **150,000+ characters**
- Supports: Hindi, Chinese, Arabic, Japanese, emoji, and all world languages
- Example: "namaste" in Hindi = "नमस्ते" — each letter uses Unicode

> **Why Unicode matters:** Without Unicode, you couldn't type in Hindi, send emoji, or read Chinese text on your computer.

---

## Quick Quiz Yourself

1. How many bits in 1 byte? → **8**
2. How many bytes in 1 KB? → **1,024**
3. What's bigger: 1 GB or 1 MB? → **1 GB** (1 GB = 1,024 MB)
4. A photo is usually measured in? → **MB** (megabytes)
5. ASCII or Unicode supports Hindi? → **Unicode**

---

## Summary

- **Bit** = smallest unit (0 or 1)
- **Byte** = 8 bits (one character)
- Order: Bit → Byte → KB → MB → GB → TB → PB
- Each step = **1,024 times** bigger
- **ASCII** = English only (128 chars), **Unicode** = all languages (150,000+ chars)

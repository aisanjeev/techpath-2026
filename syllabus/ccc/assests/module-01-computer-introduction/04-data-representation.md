# Data Representation in Computers

**Module 01 — CCC Exam Preparation | Topic 4**

---

## How Computers Store Data

Computers understand only two things: **0** and **1**. Everything — text, images, videos, music — is stored as combinations of 0s and 1s inside the computer. This is because computers use electrical signals, and a signal can be either **ON (1)** or **OFF (0)**.

---

## Bits and Bytes

### Bit (Binary Digit)
- The **smallest unit of data** in a computer
- A bit can hold only one of two values: **0** or **1**
- "Bit" comes from **Bi**nary Digi**t**

### Byte
- A group of **8 bits** = 1 Byte
- A byte can represent a single character (letter, number, or symbol)
- **Example:** The letter "A" is stored as `01000001` (8 bits = 1 byte)

**CCC Exam Tip:** "How many bits are in one byte?" — Answer: **8 bits = 1 byte**. This is one of the most frequently asked questions in the CCC exam.

### Nibble
- A group of **4 bits** = 1 Nibble
- Half a byte

---

## Memory Size Units

Computer memory is measured in bytes. As data gets larger, we use bigger units:

| Unit | Full Form | Size | Equivalent |
|------|-----------|------|------------|
| **Bit** | Binary Digit | Smallest unit | 0 or 1 |
| **Byte** | — | 8 bits | 1 character |
| **KB** | Kilobyte | 1,024 Bytes | About half a page of text |
| **MB** | Megabyte | 1,024 KB | About 1 photo or 1 MP3 song |
| **GB** | Gigabyte | 1,024 MB | About 1 movie or 250 songs |
| **TB** | Terabyte | 1,024 GB | About 250 movies |
| **PB** | Petabyte | 1,024 TB | Massive data centres |
| **EB** | Exabyte | 1,024 PB | Global-scale data |
| **ZB** | Zettabyte | 1,024 EB | All data on the internet |

**CCC Exam Tip:** The conversion factor is always **1,024** (not 1,000):
- 1 KB = 1,024 Bytes
- 1 MB = 1,024 KB
- 1 GB = 1,024 MB
- 1 TB = 1,024 GB

This conversion is asked in almost every exam. Remember: 1024 = 2^10.

### Quick Conversion Examples

**Example 1:** How many bytes are in 2 KB?
- 2 KB = 2 × 1,024 = **2,048 Bytes**

**Example 2:** How many KB are in 5 MB?
- 5 MB = 5 × 1,024 = **5,120 KB**

**Example 3:** How many MB are in 2 GB?
- 2 GB = 2 × 1,024 = **2,048 MB**

---

## ASCII Code

### What is ASCII?

**ASCII** stands for **American Standard Code for Information Interchange**. It is a coding system that assigns a unique number to each character (letter, digit, symbol) so that computers can store and exchange text.

- ASCII uses **7 bits** to represent each character
- Total characters: **128** (0 to 127)
- Extended ASCII uses **8 bits** and can represent **256** characters

### Important ASCII Values

| Character | ASCII Value | Binary |
|-----------|-------------|--------|
| A | 65 | 01000001 |
| B | 66 | 01000010 |
| Z | 90 | 01011010 |
| a | 97 | 01100001 |
| b | 98 | 01100010 |
| z | 122 | 01111010 |
| 0 | 48 | 00110000 |
| 9 | 57 | 00111001 |
| Space | 32 | 00100000 |

**CCC Exam Tip:** Remember these key ASCII values:
- A = 65, Z = 90 (uppercase letters: 65–90)
- a = 97, z = 122 (lowercase letters: 97–122)
- 0 = 48, 9 = 57 (digits: 48–57)

### Unicode

- ASCII can only represent English characters
- **Unicode** was created to support ALL languages in the world — Hindi, Tamil, Arabic, Chinese, etc.
- Unicode uses **16 bits** (or more) per character
- Can represent over **1,00,000** characters
- Hindi text on your computer and phone is possible because of Unicode

---

## Number Systems

Computers primarily use the binary number system, but humans use decimal. Understanding different number systems helps us understand how computers work internally.

### 1. Decimal Number System (Base 10)

- The system we use in everyday life
- Uses **10 digits**: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- Base = 10 (each position is a power of 10)

**Example:** 253 in decimal
- 2 × 10² + 5 × 10¹ + 3 × 10⁰
- = 200 + 50 + 3
- = 253

### 2. Binary Number System (Base 2)

- The language of computers
- Uses only **2 digits**: 0 and 1
- Base = 2 (each position is a power of 2)

**Example:** Binary 1011 in decimal
- 1 × 2³ + 0 × 2² + 1 × 2¹ + 1 × 2⁰
- = 8 + 0 + 2 + 1
- = **11** in decimal

### 3. Octal Number System (Base 8)

- Uses **8 digits**: 0, 1, 2, 3, 4, 5, 6, 7
- Base = 8 (each position is a power of 8)
- Used as a shorthand for binary (3 binary digits = 1 octal digit)

**Example:** Octal 25 in decimal
- 2 × 8¹ + 5 × 8⁰
- = 16 + 5
- = **21** in decimal

### 4. Hexadecimal Number System (Base 16)

- Uses **16 symbols**: 0–9 and A–F
- A = 10, B = 11, C = 12, D = 13, E = 14, F = 15
- Base = 16
- Used in computing for memory addresses, colour codes, MAC addresses

**Example:** Hex 1A in decimal
- 1 × 16¹ + A × 16⁰
- = 16 + 10
- = **26** in decimal

---

## Number System Comparison

| Feature | Decimal | Binary | Octal | Hexadecimal |
|---------|---------|--------|-------|-------------|
| Base | 10 | 2 | 8 | 16 |
| Digits used | 0–9 | 0–1 | 0–7 | 0–9, A–F |
| Used by | Humans | Computers | Programmers | Programmers |
| Example | 255 | 11111111 | 377 | FF |

---

## Decimal to Binary Conversion

**Method:** Divide by 2 repeatedly and note the remainders from bottom to top.

**Example:** Convert 13 to binary

| Step | Division | Quotient | Remainder |
|------|----------|----------|-----------|
| 1 | 13 ÷ 2 | 6 | **1** |
| 2 | 6 ÷ 2 | 3 | **0** |
| 3 | 3 ÷ 2 | 1 | **1** |
| 4 | 1 ÷ 2 | 0 | **1** |

Read remainders from bottom to top: **1101**

So, 13 in decimal = **1101** in binary.

---

## Binary to Decimal Conversion

**Method:** Multiply each bit by its positional power of 2 and add.

**Example:** Convert binary 10110 to decimal

| Position | 4 | 3 | 2 | 1 | 0 |
|----------|---|---|---|---|---|
| Binary digit | 1 | 0 | 1 | 1 | 0 |
| Power of 2 | 2⁴=16 | 2³=8 | 2²=4 | 2¹=2 | 2⁰=1 |
| Value | 16 | 0 | 4 | 2 | 0 |

Total = 16 + 0 + 4 + 2 + 0 = **22**

So, binary 10110 = **22** in decimal.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Bit | Smallest unit of data (0 or 1) |
| Byte | 8 bits = 1 character |
| 1 KB | 1,024 Bytes |
| 1 MB | 1,024 KB |
| 1 GB | 1,024 MB |
| 1 TB | 1,024 GB |
| ASCII | Character encoding (A=65, a=97, 0=48) |
| Binary | Base 2 (0, 1) — computer's language |
| Decimal | Base 10 (0–9) — human system |
| Octal | Base 8 (0–7) |
| Hexadecimal | Base 16 (0–9, A–F) |
| Unicode | Supports all world languages |

---

*TechPath Institute — CCC Exam Preparation*

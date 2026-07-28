# Module 01 — Computer Fundamentals — Quick Revision Notes

---

## What is a Computer?
- Electronic device that takes **Input**, **Processes** it, **Outputs** result, and **Stores** data (IPOS cycle)
- Works on **binary** (0s and 1s) — every image, video, text is just binary

## Hardware vs Software
- **Hardware** = Physical parts you can touch (CPU, RAM, keyboard, monitor)
- **Software** = Programs/instructions that run on hardware
  - **System software** = OS (Windows, Linux), drivers, BIOS
  - **Application software** = Chrome, Word, VS Code, games

## CPU (Central Processing Unit)
- The **brain** of the computer
- Two parts: **ALU** (math & logic) and **CU** (control unit — directs operations)
- Speed measured in **GHz** (e.g., 3.5 GHz = 3.5 billion operations/second)
- **Cores**: More cores = handle more tasks simultaneously (dual-core, quad-core, octa-core)
- **Generations**: Higher = better (Intel 12th Gen > 10th Gen)

## Memory Types
| Type | Speed | Size | Persistent? | Purpose |
|------|-------|------|-------------|---------|
| **Register** | Fastest | Bytes | No | Inside CPU, holds current instruction |
| **Cache** (L1/L2/L3) | Very fast | KB-MB | No | Frequently used data near CPU |
| **RAM** | Fast | 4-64 GB | No | Currently running programs |
| **SSD** | Medium | 128 GB-4 TB | Yes | Permanent storage (fast) |
| **HDD** | Slow | 500 GB-10 TB | Yes | Permanent storage (cheap, large) |

## RAM vs ROM
- **RAM** (Random Access Memory) = Temporary, loses data when power off, fast, read/write
- **ROM** (Read Only Memory) = Permanent, keeps data without power, stores BIOS/firmware

## Storage Units
```
1 Bit = 0 or 1
8 Bits = 1 Byte
1024 Bytes = 1 KB
1024 KB = 1 MB
1024 MB = 1 GB
1024 GB = 1 TB
```

## Number Systems
| System | Base | Digits | Used For |
|--------|------|--------|----------|
| **Binary** | 2 | 0, 1 | How computers think |
| **Decimal** | 10 | 0-9 | Human counting |
| **Octal** | 8 | 0-7 | Unix file permissions |
| **Hexadecimal** | 16 | 0-9, A-F | Colors (#FF5733), memory addresses |

## Logic Gates
| Gate | Symbol | Rule | Example |
|------|--------|------|---------|
| AND | A · B | Both 1 → 1 | 1 AND 1 = 1 |
| OR | A + B | Any 1 → 1 | 1 OR 0 = 1 |
| NOT | Ā | Flip | NOT 1 = 0 |
| XOR | A ⊕ B | Different → 1 | 1 XOR 0 = 1 |

## Ports & Connectors
- **USB-A** = Standard rectangular (peripherals)
- **USB-C** = Reversible, modern (charging + data)
- **HDMI** = Video + audio (monitors, TVs)
- **VGA** = Old video only (blue connector)
- **Ethernet (RJ45)** = Wired internet
- **3.5mm Jack** = Audio (headphones, speakers)

## Troubleshooting Basics
1. **Restart** — fixes 50% of problems
2. **Check connections** — cables, WiFi, Bluetooth
3. **Task Manager** (`Ctrl+Shift+Esc`) — find resource hogs
4. **Safe Mode** — boot with minimal drivers
5. **Google the error message** — someone has had this problem before

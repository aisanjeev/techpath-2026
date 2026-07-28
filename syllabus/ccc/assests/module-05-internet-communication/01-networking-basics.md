# Networking Basics

**Module 05 — CCC Exam Preparation | Topic 1**

---

## What is a Computer Network?

A **computer network** is a group of two or more computers that are connected together so they can share data, files, and resources (like printers and internet connections).

Think of it like this: In your home, you have one WiFi router. Your phone, laptop, and smart TV are all connected to the same router. They can share the internet connection and even share files with each other. This is a computer network.

**Simple Definition:** A computer network is a collection of interconnected devices that communicate with each other to share information and resources.

**CCC Exam Tip:** The exam often asks "What is a computer network?" Remember: two or more computers connected to share data and resources.

---

## Why Do We Need Networks?

Before networks existed, if Priya in the Accounts department wanted to send a file to Rahul in the Sales department, she had to copy the file onto a floppy disk (or pen drive) and physically walk to his desk. This was called **sneakernet** — because you used your sneakers (shoes) to carry data!

Networks solve this problem. With a network, Priya can instantly share the file from her computer, and Rahul can access it from his.

### Benefits of Computer Networks:

| Benefit | Example |
|---------|---------|
| **Resource Sharing** | One printer shared by 20 computers in an office |
| **Data Sharing** | Sharing files instantly between departments |
| **Communication** | Email, video calls, instant messaging |
| **Internet Access** | One internet connection shared by all devices |
| **Cost Saving** | Instead of buying 20 printers, buy 1 and share it |
| **Backup & Storage** | Central server stores all data safely |

---

## Types of Computer Networks

Networks are classified based on how large an area they cover.

### 1. LAN (Local Area Network)

A **LAN** connects computers in a **small area** such as one room, one building, or a group of nearby buildings.

- **Coverage:** Within a building or campus (up to a few kilometers)
- **Speed:** Very fast (100 Mbps to 10 Gbps)
- **Ownership:** Privately owned by the organization
- **Cost:** Low setup cost
- **Examples:**
  - Computers in a school computer lab in Bhopal
  - All PCs in a TechPath Institute classroom
  - Devices connected to your home WiFi router

**CCC Exam Tip:** "LAN covers which area?" is a very common question. Answer: A single building or office. LAN is the smallest type of network after PAN (Personal Area Network).

### 2. MAN (Metropolitan Area Network)

A **MAN** covers a **city or a large town**. It connects multiple LANs within a city.

- **Coverage:** A city or metropolitan area (up to 50-100 km)
- **Speed:** Moderate to fast
- **Ownership:** Can be private or public
- **Cost:** Higher than LAN
- **Examples:**
  - Cable TV network across Delhi
  - A bank connecting all its branches in Pune
  - Government offices connected across Bhopal city

**Easy way to remember:** MAN = City-sized network.

### 3. WAN (Wide Area Network)

A **WAN** covers a **very large area** — it can span across countries or even the entire world.

- **Coverage:** Countries, continents, or worldwide
- **Speed:** Slower than LAN (depends on connection type)
- **Ownership:** Usually operated by telecom companies
- **Cost:** Very high
- **Examples:**
  - The **Internet** is the largest WAN in the world
  - Indian Railways network connecting stations across India
  - A company like TCS connecting offices in Delhi, Pune, and New York

**CCC Exam Tip:** "What is the largest network?" — The Internet (it is the world's largest WAN).

### Comparison Table

| Feature | LAN | MAN | WAN |
|---------|-----|-----|-----|
| **Full Form** | Local Area Network | Metropolitan Area Network | Wide Area Network |
| **Area** | Room, building, campus | City or town | Country or worldwide |
| **Speed** | Very fast | Moderate | Slower |
| **Example** | Office, school lab | City cable TV | Internet |
| **Cost** | Low | Medium | High |
| **Ownership** | Private | Private or public | Telecom companies |

---

## Network Topologies

**Topology** means the arrangement or layout of computers in a network. It describes how computers are connected to each other.

Think of topology as the "map" of a network — it shows which computer is connected to which.

### 1. Star Topology

In a **Star topology**, all computers are connected to one central device (called a **hub** or **switch**). No computer is directly connected to another computer — all communication goes through the central device.

**How it looks:** Imagine a star shape — the hub is in the center, and each computer is at the tip of a ray.

```
    PC1
     |
PC2--HUB--PC3
     |
    PC4
```

**Features:**
- All devices connect to a central hub/switch
- If one computer fails, the rest of the network keeps working
- If the central hub fails, the entire network goes down
- Easy to add or remove computers
- Most commonly used topology today

**Real-life example:** Your home WiFi — all devices (phone, laptop, TV) connect to one router (central device).

**CCC Exam Tip:** Star topology is the most commonly used topology. Remember: one central device, failure of hub = entire network fails.

### 2. Bus Topology

In a **Bus topology**, all computers are connected to a single main cable called the **backbone** or **bus**. Data travels along this cable in both directions.

**How it looks:** Imagine a straight road (the cable) with houses (computers) on both sides.

```
PC1---PC2---PC3---PC4---PC5
|_________________________|
         (Bus/Cable)
```

**Features:**
- All devices share one single cable
- Cheap and easy to set up for small networks
- If the main cable breaks, the entire network fails
- As more computers are added, the network becomes slower
- Difficult to troubleshoot problems

**Real-life example:** Old cable TV networks where one cable ran through the entire building.

### 3. Ring Topology

In a **Ring topology**, each computer is connected to exactly two other computers, forming a closed circle (ring). Data travels in one direction around the ring.

**How it looks:** Imagine computers sitting in a circle, each connected to the next.

```
    PC1
   /   \
PC4     PC2
   \   /
    PC3
```

**Features:**
- Data travels in one direction (unidirectional) around the ring
- Each computer acts as a repeater — it receives data and passes it to the next
- If one computer fails, the entire ring can break (unless it is a dual ring)
- Equal access for all computers — no single computer dominates
- Used less frequently today

**Real-life example:** Token Ring networks (older technology, mostly replaced by Star topology).

### Topology Comparison

| Feature | Star | Bus | Ring |
|---------|------|-----|------|
| **Central Device** | Yes (hub/switch) | No | No |
| **Cable Used** | Separate cable for each PC | One shared cable | Circular cable |
| **Failure Impact** | Only one PC affected | Whole network fails | Ring breaks |
| **Hub Failure** | Whole network fails | N/A | N/A |
| **Speed** | Fast | Slows with more PCs | Moderate |
| **Cost** | Medium | Low | Medium |
| **Common Today?** | Yes (most common) | Rarely used | Rarely used |
| **Easy to Add PCs** | Yes | Difficult | Difficult |

---

## Other Network Terms to Know

### PAN (Personal Area Network)
- Covers a very small area — around one person (up to 10 meters)
- Example: Bluetooth connection between your phone and earphones, or your phone and smartwatch

### Network Devices

| Device | Function |
|--------|----------|
| **Hub** | Sends data to all connected devices (not smart) |
| **Switch** | Sends data only to the intended device (smarter than hub) |
| **Router** | Connects your network to the internet, directs traffic |
| **Modem** | Converts digital signals to analog and vice versa |

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Computer Network | Two or more computers connected to share data/resources |
| LAN | Covers a building or campus — fastest |
| MAN | Covers a city — medium speed |
| WAN | Covers countries/world — Internet is the largest WAN |
| Star Topology | Central hub, most common, hub failure = network down |
| Bus Topology | Single cable, cheap, cable break = network down |
| Ring Topology | Circular, data flows one way, one PC failure = ring breaks |

---

*TechPath Institute — CCC Exam Preparation*

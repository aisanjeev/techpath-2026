# Linux Fundamentals for Security Practitioners

## Why Linux Matters in Security

Linux powers roughly 96% of the world's web servers, the majority of cloud infrastructure, and virtually every penetration testing and SIEM platform. Whether you're defending servers or operating offensive tools (Kali, Metasploit, Burp Suite), Linux fluency is non-negotiable. Understanding the system you're defending means understanding how attackers move through it.

---

## The Linux Filesystem

Linux uses a unified hierarchy rooted at `/` — everything is a file or directory under this root.

```
/
├── bin/        Essential user binaries (ls, cat, bash)
├── boot/       Kernel and bootloader
├── dev/        Device files (/dev/sda = first disk, /dev/null = black hole)
├── etc/        System-wide configuration files
├── home/       User home directories (/home/alice, /home/bob)
├── lib/        Shared libraries
├── opt/        Optional third-party software
├── proc/       Virtual filesystem — live kernel/process data
├── root/       Root user's home directory
├── sbin/       System admin binaries (fdisk, iptables)
├── tmp/        Temporary files (world-writable — persistence risk)
├── usr/        User programs and data
│   ├── bin/   Additional user binaries
│   ├── sbin/  Additional admin binaries
│   └── share/ Documentation, icons
├── var/        Variable data — logs, mail, databases
│   ├── log/   System and service logs
│   └── www/   Web server files (often Apache/nginx root)
└── srv/        Service data (FTP, web)
```

### Security-Critical Files

| File | Contents | Risk if Compromised |
|------|---------|---------------------|
| `/etc/passwd` | User accounts (world-readable) | Account enumeration |
| `/etc/shadow` | Password hashes (root-only) | Offline cracking |
| `/etc/sudoers` | Sudo privileges | Privilege escalation |
| `/etc/ssh/sshd_config` | SSH server config | Remote access weakening |
| `/etc/crontab` | System cron jobs | Persistence |
| `/root/.bash_history` | Root command history | Credential disclosure |
| `~/.ssh/authorized_keys` | Trusted SSH public keys | Backdoor persistence |
| `/tmp` | Temporary files — world-writable | Malware staging |

---

## Users, Groups, and the Privilege Model

### User Types
- **Root (UID 0)**: Unrestricted — can read, write, or delete any file
- **System users (UID 1–999)**: Service accounts (www-data, nobody, daemon) — no interactive shell
- **Regular users (UID ≥ 1000)**: Human users — limited to their own files and group-shared resources

```bash
id                     # Show current UID, GID, and group memberships
whoami                 # Show current username
cat /etc/passwd        # View all accounts
# Format: username:x:UID:GID:comment:home:shell
# 'x' means password hash is in /etc/shadow

sudo cat /etc/shadow   # View hashed passwords (requires sudo/root)
# Format: username:$6$salt$hash:last_changed:min:max:warn:inactive:expire
# $6$ = SHA-512 | $5$ = SHA-256 | $y$ = yescrypt (modern) | $1$ = MD5 (weak)
```

### The sudo System

`sudo` (Substitute User DO) allows specific users to run commands as root or other users, with logging.

```bash
sudo command              # Run as root (requires user's own password)
sudo -u alice command     # Run as alice
sudo -l                   # List what the current user can sudo
sudo su -                 # Open a full root shell

# /etc/sudoers controls who can sudo what:
# Format: user  host=(runas) command
# alice ALL=(ALL:ALL) ALL     -- alice can sudo anything
# bob ALL=(ALL) NOPASSWD: /bin/systemctl restart nginx  -- passwordless specific cmd
```

**Security note:** `/etc/sudoers` is a critical persistence target. Attackers who achieve code execution often add themselves to sudoers or add a new NOPASSWD rule.

```bash
# Audit sudoers:
sudo cat /etc/sudoers
sudo ls /etc/sudoers.d/
```

---

## Linux Processes

### Process Hierarchy

Every process except `init` (PID 1) has a parent process. This parent-child relationship is critical for detecting malicious activity — `nginx` spawning `bash` is suspicious.

```bash
ps aux                    # All processes: USER, PID, %CPU, %MEM, COMMAND
ps -ef                    # Full format with PPID (parent PID)
pstree                    # Visual tree of process hierarchy
top                       # Real-time sorted view (press 'k' to kill, 'q' to quit)
htop                      # Better real-time view (install: sudo apt install htop)

# Kill processes
kill PID                  # Send SIGTERM (graceful shutdown)
kill -9 PID               # Send SIGKILL (immediate, force)
killall nginx             # Kill all processes named nginx

# Who started a process?
ls -la /proc/PID/exe      # Executable path
cat /proc/PID/cmdline     # Full command line
```

### Cron Jobs — Scheduled Tasks (and Persistence)

```bash
crontab -l                     # List current user's cron jobs
sudo crontab -l                # Root's cron jobs
cat /etc/crontab               # System cron
ls /etc/cron.d/                # Drop-in cron files
ls /etc/cron.hourly/           # Hourly scripts

# Cron syntax: minute hour day month weekday command
# 0 * * * * /usr/bin/backup.sh     -- runs at :00 every hour
# */5 * * * * /opt/check.sh        -- every 5 minutes
```

**Forensic tip:** `find /etc/cron* /var/spool/cron -type f 2>/dev/null` shows all cron job files. Attackers add cron jobs for persistence — compare against a known-good baseline.

---

## Linux Logging

### Log Files

| Log File | Content | Monitor For |
|----------|---------|------------|
| `/var/log/auth.log` | SSH, sudo, su, PAM | Failed logins, sudo abuse |
| `/var/log/syslog` | General system messages | Service crashes, errors |
| `/var/log/kern.log` | Kernel messages | Rootkit activity, hardware errors |
| `/var/log/apache2/access.log` | Web requests | SQLi, path traversal, scanning |
| `/var/log/apache2/error.log` | Web errors | Attack failures |
| `/var/log/dpkg.log` | Package installs/removes | Unauthorised software |
| `/var/log/wtmp` | Login records (binary) | Use `last` to read |
| `/var/log/btmp` | Failed login records (binary) | Use `lastb` to read |

### Log Analysis Commands

```bash
# Real-time monitoring
tail -f /var/log/auth.log

# Find failed SSH attempts
grep "Failed password" /var/log/auth.log | tail -50

# Count failed logins by IP
grep "Failed password" /var/log/auth.log | \
  grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | \
  sort | uniq -c | sort -rn | head -10

# Find successful logins
grep "Accepted" /var/log/auth.log | tail -20

# Find sudo usage
grep "sudo" /var/log/auth.log | grep -v "pam_unix"

# systemd journal (modern systems)
journalctl -u ssh                    # SSH service logs
journalctl -p err --since "1 hour ago"   # Recent errors
journalctl -f                        # Follow live
```

---

## Essential CLI Toolkit for Security

### Text Processing Pipeline

```bash
# Structure of a pipeline:
grep "pattern" file.log | awk '{print $3}' | sort | uniq -c | sort -rn

# grep: find matching lines
grep -i "error" /var/log/syslog          # Case-insensitive
grep -v "DEBUG" app.log                  # Exclude lines
grep -E "error|warning" app.log          # Regex OR
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' # Extract IPs only (-o = only match)

# awk: field processing
awk '{print $1, $4}' access.log          # Print columns 1 and 4
awk -F: '{print $1}' /etc/passwd         # Colon-delimited: print field 1
awk '$9 == 404' access.log               # Print lines where column 9 is 404

# sed: stream editing
sed 's/oldword/newword/g' file           # Replace all occurrences
sed '/^#/d' config.txt                   # Delete comment lines
sed -n '10,20p' file                     # Print lines 10-20

# cut: extract columns
cut -d: -f1,3 /etc/passwd                # Print fields 1 and 3

# sort + uniq: count and deduplicate
sort file.txt | uniq -c | sort -rn       # Most common lines first
```

### Network Investigation

```bash
# What's listening?
ss -tlnp                    # TCP listeners with PIDs
netstat -tlnp               # Older but widely available

# Who's connected right now?
ss -tnp state established
netstat -tnp

# Which process owns a port?
lsof -i :80
lsof -i :443

# Firewall status
sudo iptables -L -n -v      # iptables rules
sudo ufw status verbose     # UFW (Uncomplicated Firewall)

# Test connectivity
curl -I https://example.com  # HTTP headers only
wget -q -O /dev/null url     # Download and discard (test speed)
nc -zv 192.168.1.1 22        # Test if port 22 is open (netcat)
```

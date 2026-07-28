#!/bin/bash
# system-info.sh — Display system information
# Run: chmod +x system-info.sh && ./system-info.sh

echo "=========================================="
echo "         SYSTEM INFORMATION REPORT        "
echo "=========================================="
echo ""
echo "Date & Time : $(date)"
echo "Username    : $(whoami)"
echo "Hostname    : $(hostname)"
echo ""

echo "--- Operating System ---"
if [ -f /etc/os-release ]; then
    grep -E "^(NAME|VERSION)=" /etc/os-release
else
    echo "OS info not available"
fi
echo ""

echo "--- CPU Info ---"
grep -E "^(model name|cpu cores)" /proc/cpuinfo | head -4
echo ""

echo "--- Memory (RAM) ---"
free -h
echo ""

echo "--- Disk Usage ---"
df -h | head -5
echo ""

echo "--- Network ---"
echo "IP Address:"
hostname -I 2>/dev/null || echo "Not available"
echo ""

echo "--- Uptime ---"
uptime
echo ""
echo "=========================================="
echo "          Report generated at $(date +%H:%M)"
echo "=========================================="

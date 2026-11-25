#!/usr/bin/env bash
set -euo pipefail

echo "=== Memory ==="
free -h

echo ""
echo "=== Disk (ext4) ==="
df -hT -t ext4 || df -hT

echo ""
echo "=== Top 5 Memory Processes ==="
ps aux --sort=-%mem | head -n 6

echo ""
echo "=== Listening Ports ==="
ss -tulnp || true

echo ""
echo "=== Recent Journal Errors (last 10m) ==="
journalctl --since "10 minutes ago" -p err --no-pager || true

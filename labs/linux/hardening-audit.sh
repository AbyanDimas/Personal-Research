#!/usr/bin/env bash
set -euo pipefail

echo "=== Enabled Boot Services ==="
systemctl list-unit-files --type=service --state=enabled --no-pager | head -n 20

echo ""
echo "=== Local TCP Port Scan ==="
if command -v nmap >/dev/null 2>&1; then
  nmap -v -sT localhost | grep -E "PORT|open" || true
else
  ss -tlpn
fi

echo ""
echo "=== Mandatory Access Control ==="
if command -v aa-status >/dev/null 2>&1; then
  aa-status | head -n 4 || true
elif command -v getenforce >/dev/null 2>&1; then
  getenforce || true
else
  echo "Neither AppArmor nor SELinux CLI found"
fi

---
layout: default
title: Linux Lab Scripts - Personal Research Journal
permalink: /labs/linux/
---

# Linux Lab Scripts

Script bash latihan untuk monitoring, manajemen user/group, permission, dan hardening

## health-check.sh

Ambil snapshot kondisi server dalam satu kali jalan (memory, disk ext4, top 5 proses memory, listening ports, dan error journal 10 menit terakhir)

    chmod +x labs/linux/health-check.sh
    sudo ./labs/linux/health-check.sh

    === Memory ===
                   total        used        free      shared  buff/cache   available
    Mem:           3.8Gi       984Mi       1.1Gi        12Mi       1.7Gi       2.6Gi
    Swap:          2.0Gi          0B       2.0Gi

    === Disk (ext4) ===
    Filesystem     Type  Size  Used Avail Use% Mounted on
    /dev/sda1      ext4   58G   18G   38G  32% /

    === Top 5 Memory Processes ===
    USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    mysql        845  0.7  7.8 1420312 312450 ?      Sl   Nov21   8:45 mysqld
    www-data    1142  1.3  0.6 214520 24680 ?        S    Nov21   1:12 nginx

    === Listening Ports ===
    Netid  State   Recv-Q  Send-Q   Local Address:Port   Peer Address:Port  Process
    tcp    LISTEN  0       128            0.0.0.0:22          0.0.0.0:*      users:(("sshd",pid=790,fd=3))

## user-group-lab.sh

Otomatisasi latihan pembuatan group secret-group, user jane, usermod -a -G, chmod 750 /var/secret, dan symlink myscript.sh

    chmod +x labs/linux/user-group-lab.sh
    sudo ./labs/linux/user-group-lab.sh

    Setup complete:
    uid=1001(jane) gid=1001(jane) groups=1001(jane),1002(secret-group)
    drwxr-x--- 2 root secret-group 4096 Nov 25 20:48 /var/secret

## hardening-audit.sh

Pengecekan read-only untuk service yang aktif saat boot, port TCP lokal (nmap atau fallback ss), dan status AppArmor/SELinux

    chmod +x labs/linux/hardening-audit.sh
    sudo ./labs/linux/hardening-audit.sh

    === Enabled Boot Services ===
    UNIT FILE                              STATE           PRESET
    cron.service                           enabled         enabled
    ssh.service                            enabled         enabled
    ufw.service                            enabled         enabled

    === Local TCP Port Scan ===
    PORT   STATE SERVICE
    22/tcp open  ssh
    80/tcp open  http

    === Mandatory Access Control ===
    apparmor module is loaded.
    42 profiles are loaded.
    40 profiles are in enforce mode.

<div class="page-nav-box">
  <a href="{{ '/docs/linux/encryption/' | relative_url }}" class="page-nav-btn">&larr; Data Encryption</a>
  <a href="{{ '/' | relative_url }}" class="page-nav-btn">Back to Home &rarr;</a>
</div>

---
layout: default
title: Managing System Processes - Linux Administration
permalink: /docs/linux/processes/
---

# Managing System Processes

Catatan materi dari bootstrap-it.com/linux-admin

## Inspecting Processes

Cek proses yang jalan di shell saat ini

```bash
ps
```

```text
  PID TTY          TIME CMD
 2410 pts/0    00:00:00 bash
 2488 pts/0    00:00:00 ps
```

Cek seluruh proses dari semua user lalu filter service ssh

```bash
ps aux | grep ssh
```

```text
root         790  0.0  0.1  15428  5820 ?        Ss   Nov21   0:02 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root        2395  0.0  0.2  17840  9124 ?        Ss   20:10   0:00 sshd: ubuntu [priv]
ubuntu      2409  0.0  0.1  17972  6340 ?        S    20:10   0:00 sshd: ubuntu@pts/0
```

Cari PID dan command lengkap tanpa memunculkan proses grep

```bash
pgrep -a sshd
```

```text
790 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
2395 sshd: ubuntu [priv]
2409 sshd: ubuntu@pts/0
```

## Monitoring Log dan Event Data

Cek log systemd dalam 10 menit terakhir

```bash
journalctl --since "10 minutes ago"
```

```text
Nov 25 20:10:02 web01 sshd[2395]: Accepted publickey for ubuntu from 10.0.1.5 port 54122 ssh2
Nov 25 20:10:02 web01 systemd-logind[612]: New session 14 of user ubuntu.
Nov 25 20:12:41 web01 sudo[2450]:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; COMMAND=/usr/bin/apt update
```

Masuk ke /var/log dan lihat daftar file log yang tersedia

```bash
cd /var/log && ll
```

```text
total 19432
-rw-r----- 1 syslog adm   421840 Nov 25 20:10 auth.log
-rw-r----- 1 syslog adm  1240120 Nov 25 20:12 syslog
-rw-r----- 1 syslog adm   184320 Nov 25 19:45 kern.log
```

Filter log interface eno1 dari syslog

```bash
grep eno1 < /var/log/syslog | tail -n 3
```

```text
Nov 25 19:40:11 web01 systemd-networkd[482]: eno1: Gained carrier
Nov 25 19:40:13 web01 systemd-networkd[482]: eno1: DHCPv4 address 192.168.1.10/24 via 192.168.1.1
Nov 25 19:40:13 web01 systemd-networkd[482]: eno1: Configured
```

Cek pesan kernel (hardware, driver, atau OOM killer) lewat dmesg

```bash
sudo dmesg | tail -n 4
```

```text
[    4.120411] e1000e 0000:00:1f.6 eno1: NIC Link is Up 1000 Mbps Full Duplex, Flow Control: Rx/Tx
[    4.120892] IPv6: ADDRCONF(NETDEV_CHANGE): eno1: link becomes ready
[   12.884120] EXT4-fs (sda1): re-mounted. Quota mode: none.
```

## Simulasi dan Terminasi Proses

Jalankan proses dummy yes ke /dev/null di background untuk tes load CPU, lalu hentikan dengan kill memakai PID

```bash
yes > /dev/null &
ps -p $!
kill $!
```

```text
  PID TTY          TIME CMD
 2615 pts/0    00:00:04 yes
[1]+  Terminated              yes > /dev/null
```

Jika ingin langsung menembak nama proses tanpa mencari PID, gunakan killall (perintah kill butuh PID, bukan nama proses)

```bash
yes > /dev/null &
killall yes
```

```text
[1]+  Terminated              yes > /dev/null
```

- Gunakan kill -9 PID hanya jika proses tidak merespons SIGTERM biasa

## Enable / Disable Service dengan systemd

Cek daftar unit service yang aktif saat boot

```bash
systemctl list-unit-files | grep enabled
```

```text
cron.service                           enabled         enabled
nginx.service                          enabled         enabled
ssh.service                            enabled         enabled
ufw.service                            enabled         enabled
```

Cek status service apache2

```bash
systemctl status apache2
```

```text
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; preset: enabled)
     Active: active (running) since Mon 2026-11-21 16:53:01 WIB; 4 days ago
```

Matikan sekaligus cabut apache2 dari startup

```bash
sudo systemctl disable --now apache2
```

```text
Synchronizing state of apache2.service with SysV service script with /lib/systemd/systemd-sysv-install.
Removed "/etc/systemd/system/multi-user.target.wants/apache2.service".
```

<div class="page-nav-box">
  <a href="{{ '/docs/linux/monitoring/' | relative_url }}" class="page-nav-btn">&larr; Monitoring System</a>
  <a href="{{ '/docs/linux/users-and-groups/' | relative_url }}" class="page-nav-btn">Next: Users &amp; Groups &rarr;</a>
</div>

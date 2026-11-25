---
layout: default
title: Hardening Your Server - Linux Administration
permalink: /docs/linux/hardening/
---

# Hardening Your Server

Catatan materi dari bootstrap-it.com/linux-admin dan dokumentasi keamanan AWS EC2

## Patching Sistem

Update daftar paket dan upgrade sistem di Debian/Ubuntu

Command:

    sudo apt update && sudo apt upgrade -y

Output:

    Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease
    Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]
    Reading package lists... Done
    0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.

Update paket di RHEL, Amazon Linux, atau Fedora

Command:

    sudo dnf update -y

Output:

    Last metadata expiration check: 0:04:12 ago on Wed 25 Nov 2026 08:20:00 PM WIB.
    Dependencies resolved.
    Nothing to do.
    Complete!

## Port dan Service Access Control

Scan port TCP yang terbuka secara lokal dengan nmap

Command:

    nmap -v -sT localhost

Output:

    Starting Nmap 7.94 ( https://nmap.org ) at 2026-11-25 20:30 WIB
    Initiating Connect Scan at 20:30
    Scanning localhost (127.0.0.1) [1000 ports]
    Discovered open port 22/tcp on 127.0.0.1
    Discovered open port 80/tcp on 127.0.0.1
    PORT   STATE SERVICE
    22/tcp open  ssh
    80/tcp open  http

Scan port TCP dari luar ke host target

Command:

    nmap -v -sT bootstrap-it.com

Output:

    Starting Nmap 7.94 ( https://nmap.org ) at 2026-11-25 20:31 WIB
    PORT    STATE SERVICE
    80/tcp  open  http
    443/tcp open  https

Matikan dan disable service yang tidak terpakai seperti apache2

Command:

    sudo systemctl disable --now apache2

Output:

    Removed "/etc/systemd/system/multi-user.target.wants/apache2.service".

- Di AWS EC2, jangan buka port 22 ke 0.0.0.0/0 pada Security Group; batasi ke IP VPN/bastion atau gunakan SSM Session Manager

## Mandatory Access Control dan Audit

Cek status AppArmor (Ubuntu/Debian)

Command:

    sudo aa-status | head -n 4

Output:

    apparmor module is loaded.
    42 profiles are loaded.
    40 profiles are in enforce mode.

Cek status SELinux (RHEL/Amazon Linux)

Command:

    getenforce

Output:

    Enforcing

- Tambahan hardening host: mount /tmp, /var, /home dengan nodev, nosuid, noexec di /etc/fstab jika workload mendukung, aktifkan auditd, dan jalankan sudo lynis audit system untuk baseline check

<div class="page-nav-box">
  <a href="{{ '/docs/linux/permissions-and-links/' | relative_url }}" class="page-nav-btn">&larr; Permissions &amp; Symlinks</a>
  <a href="{{ '/docs/linux/encryption/' | relative_url }}" class="page-nav-btn">Next: Data Encryption &rarr;</a>
</div>

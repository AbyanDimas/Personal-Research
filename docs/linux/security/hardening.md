---
layout: default
title: Hardening Your Server - Linux Administration
permalink: /docs/linux/hardening/
---

# Hardening Your Server

Catatan belajar pribadi dari bootstrap-it.com/linux-admin dan dokumentasi keamanan AWS EC2

## Patching and Package Hygiene

Langkah paling dasar untuk memperkecil celah keamanan adalah rutin memperbarui paket sistem dan membuang atau mematikan service yang tidak dipakai. Di Debian atau Ubuntu kita jalankan apt update dan apt upgrade

    $ sudo apt update && sudo apt upgrade -y
    Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease
    Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]
    Reading package lists... Done
    0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.

Sementara di keluarga RHEL, Amazon Linux, atau Fedora perintahnya memakai dnf update

    $ sudo dnf update -y
    Last metadata expiration check: 0:04:12 ago on Wed 25 Nov 2026 08:20:00 PM WIB.
    Dependencies resolved.
    Nothing to do.
    Complete!

## Port and Network Control

Supaya tahu port mana saja yang terbuka dan menerima koneksi dari lokal, jalankan TCP connect scan ke localhost memakai nmap

    $ nmap -v -sT localhost
    Starting Nmap 7.94 ( https://nmap.org ) at 2026-11-25 20:30 WIB
    Initiating Connect Scan at 20:30
    Scanning localhost (127.0.0.1) [1000 ports]
    Discovered open port 22/tcp on 127.0.0.1
    Discovered open port 80/tcp on 127.0.0.1
    PORT   STATE SERVICE
    22/tcp open  ssh
    80/tcp open  http

Kita juga bisa mengetes dari sisi luar ke domain atau IP target untuk memastikan firewall atau Security Group memang hanya meloloskan port yang semestinya terbuka

    $ nmap -v -sT bootstrap-it.com
    Starting Nmap 7.94 ( https://nmap.org ) at 2026-11-25 20:31 WIB
    PORT    STATE SERVICE
    80/tcp  open  http
    443/tcp open  https

Kalau ketemu service yang tidak dibutuhkan seperti apache2, langsung matikan dan cabut dari boot supaya port-nya tertutup

    $ sudo systemctl disable --now apache2
    Removed "/etc/systemd/system/multi-user.target.wants/apache2.service".

Di AWS EC2, jangan pernah membuka port 22 ke 0.0.0.0/0 pada Security Group; batasi hanya untuk IP VPN, bastion, atau IP kantor tertentu, atau tutup port 22 sama sekali dan pakai SSM Session Manager

## Host-Level Hardening Extras

Pastikan sistem Mandatory Access Control bawaan distro tetap aktif, yaitu AppArmor di Ubuntu/Debian atau SELinux dalam mode enforcing di RHEL/Amazon Linux

    $ sudo aa-status | head -n 4
    apparmor module is loaded.
    42 profiles are loaded.
    40 profiles are in enforce mode.

    $ getenforce
    Enforcing

Sebagai tambahan di sisi host, partisi seperti /tmp, /var, dan /home bisa dipasang dengan opsi nodev, nosuid, dan noexec di /etc/fstab kalau workload-nya mendukung. Untuk pencatatan perubahan file sensitif atau eskalasi hak akses, aktifkan auditd dan sesekali jalankan Lynis (sudo lynis audit system) untuk mengecek kesiapan sistem terhadap standar baseline CIS

<div class="page-nav-box">
  <a href="{{ '/docs/linux/permissions-and-links/' | relative_url }}" class="page-nav-btn">&larr; Permissions &amp; Symlinks</a>
  <a href="{{ '/docs/linux/encryption/' | relative_url }}" class="page-nav-btn">Next: Data Encryption &rarr;</a>
</div>

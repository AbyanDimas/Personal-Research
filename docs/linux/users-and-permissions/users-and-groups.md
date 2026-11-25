---
layout: default
title: Working with Users and Groups - Linux Administration
permalink: /docs/linux/users-and-groups/
---

# Working with Users and Groups

Catatan materi dari bootstrap-it.com/linux-admin dan dokumentasi keamanan AWS EC2

## Best Practices Admin Power

- Hindari login atau bekerja langsung memakai akun root
- Buat akun unik untuk tiap user, jangan share akun default seperti ubuntu atau ec2-user
- Berikan authority seperlunya saja sesuai kebutuhan user (least privilege)
- Jalankan privilege admin hanya lewat sudo supaya tercatat di log

## Account Data dan Group Files

Cek daftar user di /etc/passwd (bisa dibaca semua user) dan hash password di /etc/shadow (khusus root/shadow)

    tail -n 3 /etc/passwd

    systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
    ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
    jane:x:1001:1001::/home/jane:/bin/bash

    sudo tail -n 2 /etc/shadow

    ubuntu:$y$j9T$abc123.../:19850:0:99999:7:::
    jane:$y$j9T$xyz789.../:20052:0:99999:7:::

Cek daftar group di /etc/group dan file template default di /etc/skel

    tail -n 3 /etc/group

    ubuntu:x:1000:
    jane:x:1001:
    secret-group:x:1002:jane

    ls -a /etc/skel

    .  ..  .bash_logout  .bashrc  .profile

## Account Activity Data

Cek UID, GID, dan group milik user ubuntu, lalu cek sesi login aktif dan riwayat login

    id ubuntu

    uid=1000(ubuntu) gid=1000(ubuntu) groups=1000(ubuntu),4(adm),27(sudo)

    who

    ubuntu   pts/0        2026-11-25 20:10 (10.0.1.5)

    w

     20:22:14 up 4 days,  3:29,  1 user,  load average: 0.08, 0.10, 0.09
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
    ubuntu   pts/0    10.0.1.5         20:10    0.00s  0.04s  0.00s w

    last -n 3

    ubuntu   pts/0        10.0.1.5         Wed Nov 25 20:10   still logged in
    ubuntu   pts/0        10.0.1.5         Tue Nov 24 09:14 - 11:42  (02:28)
    reboot   system boot  6.8.0-45-generic Fri Nov 21 16:53   still running

## Managing Accounts dan Groups

Buat user jane dengan home directory, pasang password, buat group secret-group, ubah group ownership /var/secret, lalu masukkan jane ke group tersebut

    sudo useradd -m jane
    sudo passwd jane
    sudo groupadd secret-group
    sudo mkdir -p /var/secret
    sudo chown :secret-group /var/secret
    sudo usermod -a -G secret-group jane

    id jane

    uid=1001(jane) gid=1001(jane) groups=1001(jane),1002(secret-group)

- Flag -a pada usermod -a -G wajib dipakai supaya group lama milik user tidak terhapus

## SSH Access per User (AWS EC2 Best Practices)

Matikan login password dan blokir root login di /etc/ssh/sshd_config

    PasswordAuthentication no
    PubkeyAuthentication yes
    PermitRootLogin no

Gunakan key Ed25519 atau RSA 2048-bit+ dan jaga permission folder .ssh tiap user

    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/authorized_keys

- Di AWS EC2, alternatif tanpa membuka port 22 dan mengelola static key adalah AWS Systems Manager Session Manager (via IAM) atau EC2 Instance Connect (short-lived SSH key)

<div class="page-nav-box">
  <a href="{{ '/docs/linux/processes/' | relative_url }}" class="page-nav-btn">&larr; Managing Processes</a>
  <a href="{{ '/docs/linux/permissions-and-links/' | relative_url }}" class="page-nav-btn">Next: Permissions &amp; Symlinks &rarr;</a>
</div>

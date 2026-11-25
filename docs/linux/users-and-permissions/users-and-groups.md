---
layout: default
title: Working with Users and Groups - Linux Administration
permalink: /docs/linux/users-and-groups/
---

# Working with Users and Groups

Catatan belajar pribadi dari bootstrap-it.com/linux-admin dan dokumentasi keamanan AWS EC2

## Admin Power Best Practices

Saat mengelola server, sebisa mungkin hindari login atau kerja langsung memakai akun root. Setiap admin atau operator sebaiknya punya akun unik masing-masing daripada berbagi satu akun bawaan seperti ubuntu atau ec2-user, dan setiap akun hanya diberi hak akses seperlunya saja. Kalau butuh menjalankan perintah administratif, lakukan lewat sudo supaya aktivitasnya tercatat dan bisa dibatasi di /etc/sudoers.d/

## Account and Group Files

Data akun user tersimpan di /etc/passwd dalam format yang bisa dibaca semua user, sedangkan hash password dan aturan masa berlaku password disimpan terpisah di /etc/shadow yang hanya bisa dibuka dengan akses root atau group shadow

    $ tail -n 3 /etc/passwd
    systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
    ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
    jane:x:1001:1001::/home/jane:/bin/bash

    $ sudo tail -n 2 /etc/shadow
    ubuntu:$y$j9T$abc123.../:19850:0:99999:7:::
    jane:$y$j9T$xyz789.../:20052:0:99999:7:::

Daftar group dan anggotanya ada di /etc/group, sementara isi folder /etc/skel menjadi template file bawaan yang otomatis disalin ke home directory setiap kali kita membuat user baru

    $ tail -n 3 /etc/group
    ubuntu:x:1000:
    jane:x:1001:
    secret-group:x:1002:jane

    $ ls -a /etc/skel
    .  ..  .bash_logout  .bashrc  .profile

## Account Activity Data

Untuk melihat UID, GID, dan daftar group milik seorang user pakai perintah id. Kalau mau mengecek siapa yang sedang login sekarang, apa yang lagi mereka kerjakan, dan riwayat login sebelumnya, pakai who, w, dan last

    $ id ubuntu
    uid=1000(ubuntu) gid=1000(ubuntu) groups=1000(ubuntu),4(adm),27(sudo)

    $ who
    ubuntu   pts/0        2026-11-25 20:10 (10.0.1.5)

    $ w
     20:22:14 up 4 days,  3:29,  1 user,  load average: 0.08, 0.10, 0.09
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
    ubuntu   pts/0    10.0.1.5         20:10    0.00s  0.04s  0.00s w

    $ last -n 3
    ubuntu   pts/0        10.0.1.5         Wed Nov 25 20:10   still logged in
    ubuntu   pts/0        10.0.1.5         Tue Nov 24 09:14 - 11:42  (02:28)
    reboot   system boot  6.8.0-45-generic Fri Nov 21 16:53   still running

## Managing Accounts and Groups

Contoh alur lengkap membuat user baru bernama jane sekalian home directory-nya, memasang password, membuat group secret-group, mengubah kepemilikan group folder /var/secret, lalu memasukkan jane ke dalam group tersebut. Saat memakai usermod, flag -a wajib disertakan bersama -G supaya group lama milik user tidak ikut terhapus

    $ sudo useradd -m jane
    $ sudo passwd jane
    New password:
    Retype new password:
    passwd: password updated successfully

    $ sudo groupadd secret-group
    $ sudo mkdir -p /var/secret
    $ sudo chown :secret-group /var/secret
    $ sudo usermod -a -G secret-group jane

    $ id jane
    uid=1001(jane) gid=1001(jane) groups=1001(jane),1002(secret-group)

## SSH Access per User (AWS EC2 Best Practices)

Di server production maupun AWS EC2, login SSH berbasis password sebaiknya dimatikan dan akses langsung ke root lewat SSH harus diblokir di /etc/ssh/sshd_config

    PasswordAuthentication no
    PubkeyAuthentication yes
    PermitRootLogin no

Gunakan key modern seperti Ed25519 atau RSA minimal 2048-bit dan hindari algoritma lama seperti DSA. Public key masing-masing user ditaruh di /home/username/.ssh/authorized_keys dengan permission yang ketat supaya tidak bisa dibaca atau diubah sembarang user

    $ chmod 700 ~/.ssh
    $ chmod 600 ~/.ssh/authorized_keys

Khusus di AWS, alternatif yang lebih aman daripada membuka port 22 dan mengelola static key adalah memakai AWS Systems Manager Session Manager yang mengandalkan IAM, atau EC2 Instance Connect yang memakai SSH key berumur pendek

<div class="page-nav-box">
  <a href="{{ '/docs/linux/processes/' | relative_url }}" class="page-nav-btn">&larr; Managing Processes</a>
  <a href="{{ '/docs/linux/permissions-and-links/' | relative_url }}" class="page-nav-btn">Next: Permissions &amp; Symlinks &rarr;</a>
</div>

---
layout: default
title: Data Encryption - Linux Administration
permalink: /docs/linux/encryption/
---

# Data Encryption

Catatan belajar pribadi dari dokumentasi AWS EBS/KMS dan referensi Linux LUKS/GPG

Enkripsi data at rest di Linux dan AWS bekerja di dua layer yang berbeda: layer infrastruktur yang ditangani oleh cloud hypervisor, dan layer OS di dalam Linux itu sendiri

## Infrastructure Layer: Amazon EBS Encryption

Di AWS, enkripsi volume EBS ditangani secara transparan oleh hardware AWS Nitro atau hypervisor menggunakan AES-256. Yang terenkripsi bukan hanya data yang tersimpan di volume, tapi juga lalu lintas data antara instance EC2 dan EBS serta seluruh snapshot atau volume turunan yang dibuat darinya. Pengelolaan kuncinya memakai AWS KMS lewat mekanisme envelope encryption, jadi sistem operasi Linux di dalam EC2 tidak perlu mengatur passphrase atau menjalankan cryptsetup sama sekali

## OS Layer: Linux Unified Key Setup (LUKS)

Kalau ada kebutuhan kepatuhan yang mewajibkan double encryption di level infrastruktur dan level OS, atau ketika memakai ephemeral instance store di EC2 yang tidak didukung enkripsi EBS, kita bisa mengenkripsi block device langsung dari dalam Linux menggunakan LUKS dan cryptsetup

Alur lengkapnya dimulai dari memformat partisi sebagai container LUKS (ini akan menghapus seluruh isi partisi), membukanya menjadi device mapper, membuat filesystem ext4 di atasnya, lalu me-mount ke direktori tujuan

    $ sudo cryptsetup luksFormat /dev/sdb1

    WARNING!
    ========
    This will overwrite data on /dev/sdb1 irrevocably.

    Are you sure? (Type 'yes' in capital letters): YES
    Enter passphrase for /dev/sdb1:
    Verify passphrase:

    $ sudo cryptsetup open /dev/sdb1 secure_data
    Enter passphrase for /dev/sdb1:

    $ sudo mkfs.ext4 /dev/mapper/secure_data
    mke2fs 1.47.0 (5-Feb-2023)
    Creating filesystem with 2620928 4k blocks and 655360 inodes
    Writing superblocks and filesystem accounting information: done

    $ sudo mkdir -p /mnt/secure
    $ sudo mount /dev/mapper/secure_data /mnt/secure

    $ lsblk /dev/sdb
    NAME          MAJ:MIN RM SIZE RO TYPE  MOUNTPOINTS
    sdb             8:16   0  10G  0 disk
    └─sdb1          8:17   0  10G  0 part
      └─secure_data 253:0  0  10G  0 crypt /mnt/secure

Untuk server tanpa layar (headless) yang harus bisa unlock otomatis saat reboot, biasanya dipakai dropbear SSH di dalam initramfs atau pengambilan kunci dari AWS KMS saat proses boot seperti yang diterapkan di Amazon EMR dan AWS ParallelCluster

## File and Artifact Encryption with GPG

Untuk kebutuhan enkripsi per file, misalnya sebelum menaruh file rahasia ke backup atau repositori, kita bisa pakai GnuPG (gpg) dengan enkripsi simetris memakai passphrase lalu mendekripsinya kembali saat dibutuhkan

    $ gpg -c secret.txt
    (prompts for passphrase and writes secret.txt.gpg)

    $ ls -l secret.txt*
    -rw-r--r-- 1 ubuntu ubuntu 24 Nov 25 20:35 secret.txt
    -rw-r--r-- 1 ubuntu ubuntu 78 Nov 25 20:35 secret.txt.gpg

    $ gpg -d secret.txt.gpg
    gpg: AES256.CFB encrypted data
    gpg: encrypted with 1 passphrase
    my-db-password-123

<div class="page-nav-box">
  <a href="{{ '/docs/linux/hardening/' | relative_url }}" class="page-nav-btn">&larr; Server Hardening</a>
  <a href="{{ '/labs/linux/' | relative_url }}" class="page-nav-btn">Next: Linux Lab Scripts &rarr;</a>
</div>

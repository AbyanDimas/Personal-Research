---
layout: default
title: Data Encryption - Linux Administration
permalink: /docs/linux/encryption/
---

# Data Encryption

Catatan materi dari dokumentasi AWS EBS/KMS dan referensi Linux LUKS/GPG

## Layer Infrastruktur: Amazon EBS Encryption

- Enkripsi berjalan di level hardware AWS Nitro/hypervisor dengan AES-256
- Mencakup data di volume, traffic antara EC2 dan EBS, serta snapshot dan volume turunannya
- Key dikelola oleh AWS KMS lewat envelope encryption, transparan bagi OS Linux di dalam guest

## Layer OS: Linux Unified Key Setup (LUKS)

Dipakai saat butuh double encryption (layer infrastruktur + OS) atau untuk volume ephemeral EC2 instance store

Format partisi /dev/sdb1 dengan LUKS, buka mapper, buat filesystem ext4, lalu mount

    sudo cryptsetup luksFormat /dev/sdb1
    sudo cryptsetup open /dev/sdb1 secure_data
    sudo mkfs.ext4 /dev/mapper/secure_data
    sudo mkdir -p /mnt/secure
    sudo mount /dev/mapper/secure_data /mnt/secure

Cek hasil mapping block device dengan lsblk

    lsblk /dev/sdb

    NAME          MAJ:MIN RM SIZE RO TYPE  MOUNTPOINTS
    sdb             8:16   0  10G  0 disk
    └─sdb1          8:17   0  10G  0 part
      └─secure_data 253:0  0  10G  0 crypt /mnt/secure

- Untuk server headless saat reboot, unlock bisa memakai dropbear SSH di initramfs atau fetch key dari AWS KMS saat boot (seperti di Amazon EMR dan AWS ParallelCluster)

## Enkripsi File dengan GPG

Enkripsi simetris file memakai passphrase lalu dekripsi kembali

    gpg -c secret.txt
    ls -l secret.txt*

    -rw-r--r-- 1 ubuntu ubuntu 24 Nov 25 20:35 secret.txt
    -rw-r--r-- 1 ubuntu ubuntu 78 Nov 25 20:35 secret.txt.gpg

    gpg -d secret.txt.gpg

    gpg: AES256.CFB encrypted data
    gpg: encrypted with 1 passphrase
    my-db-password-123

<div class="page-nav-box">
  <a href="{{ '/docs/linux/hardening/' | relative_url }}" class="page-nav-btn">&larr; Server Hardening</a>
  <a href="{{ '/labs/linux/' | relative_url }}" class="page-nav-btn">Next: Linux Lab Scripts &rarr;</a>
</div>

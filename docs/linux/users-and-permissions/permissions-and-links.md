---
layout: default
title: Object Permissions and Symlinks - Linux Administration
permalink: /docs/linux/permissions-and-links/
---

# Object Permissions and Extending Usability

Catatan belajar pribadi dari bootstrap-it.com/linux-admin

## Applying Object Permissions

Di Linux, permission file dan folder bisa diatur dengan notasi angka yang berasal dari penjumlahan tiga nilai dasar: read (r) bernilai 4, write (w) bernilai 2, dan execute (x) bernilai 1. Jadi kalau pemilik diberi akses penuh (rwx), angkanya adalah 7 dari 4 + 2 + 1

Dalam praktiknya ada beberapa kombinasi angka yang paling sering dipakai. Angka 755 (rwxr-xr-x) umum untuk folder dan script bersama karena pemilik bisa mengubah sementara user lain hanya bisa membaca dan menjalankan. Angka 700 (rwx------) mengunci folder agar hanya pemilik yang bisa masuk, misalnya untuk ~/.ssh. Untuk file konfigurasi biasa dipakai 644 (rw-r--r--), sedangkan file sensitif seperti private key atau authorized_keys wajib memakai 600 (rw-------)

Berikut contoh mengubah permission folder /var/secret agar user lain di luar group tidak bisa masuk, lalu membuat file dan memindahkan kepemilikannya ke jane dan secret-group

    $ ls -ld /var/secret
    drwxr-xr-x 2 root secret-group 4096 Nov 25 20:25 /var/secret

    $ sudo chmod 750 /var/secret
    $ ls -ld /var/secret
    drwxr-x--- 2 root secret-group 4096 Nov 25 20:25 /var/secret

    $ sudo touch /var/secret/note.txt
    $ sudo chown jane:secret-group /var/secret/note.txt
    $ ls -l /var/secret/note.txt
    -rw-r--r-- 1 jane secret-group 0 Nov 25 20:26 /var/secret/note.txt

## Extending Object Usability

Symbolic link atau symlink dipakai untuk memunculkan shortcut ke script, binary, atau file konfigurasi di lokasi lain tanpa harus menduplikasi file aslinya. Sebaiknya selalu pakai absolute path saat membuat symlink supaya link-nya tidak putus ketika dipanggil dari direktori lain, dan berbeda dengan hard link, symlink bisa menunjuk ke folder maupun melintasi filesystem yang berbeda

    $ sudo ln -s /home/ubuntu/scripts/myscript.sh /var/secret
    $ ls -l /var/secret
    total 0
    lrwxrwxrwx 1 root root         32 Nov 25 20:28 myscript.sh -> /home/ubuntu/scripts/myscript.sh
    -rw-r--r-- 1 jane secret-group  0 Nov 25 20:26 note.txt

<div class="page-nav-box">
  <a href="{{ '/docs/linux/users-and-groups/' | relative_url }}" class="page-nav-btn">&larr; Users &amp; Groups</a>
  <a href="{{ '/docs/linux/hardening/' | relative_url }}" class="page-nav-btn">Next: Server Hardening &rarr;</a>
</div>

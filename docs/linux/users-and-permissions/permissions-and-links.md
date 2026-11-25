---
layout: default
title: Object Permissions and Symlinks - Linux Administration
permalink: /docs/linux/permissions-and-links/
---

# Object Permissions and Extending Usability

Catatan materi dari bootstrap-it.com/linux-admin

## Numeric Notation

- Read: r = 4
- Write: w = 2
- Execute: x = 1
- Full permissions: 7 (4 + 2 + 1)

Kombinasi umum yang sering dipakai
- 755 (rwxr-xr-x) untuk direktori dan script bersama
- 700 (rwx------) untuk folder private seperti ~/.ssh
- 644 (rw-r--r--) untuk file konfigurasi biasa
- 600 (rw-------) untuk private key dan authorized_keys

Ubah permission /var/secret menjadi 750

Command:

    ls -ld /var/secret
    sudo chmod 750 /var/secret
    ls -ld /var/secret

Output:

    drwxr-xr-x 2 root secret-group 4096 Nov 25 20:25 /var/secret
    drwxr-x--- 2 root secret-group 4096 Nov 25 20:25 /var/secret

Buat file dan atur owner menjadi jane:secret-group

Command:

    sudo touch /var/secret/note.txt
    sudo chown jane:secret-group /var/secret/note.txt
    ls -l /var/secret/note.txt

Output:

    -rw-r--r-- 1 jane secret-group 0 Nov 25 20:26 /var/secret/note.txt

## Extending Object Usability

Buat symbolic link ke /home/ubuntu/scripts/myscript.sh di dalam /var/secret

Command:

    sudo ln -s /home/ubuntu/scripts/myscript.sh /var/secret
    ls -l /var/secret

Output:

    total 0
    lrwxrwxrwx 1 root root         32 Nov 25 20:28 myscript.sh -> /home/ubuntu/scripts/myscript.sh
    -rw-r--r-- 1 jane secret-group  0 Nov 25 20:26 note.txt

- Selalu pakai absolute path saat membuat symlink supaya link tidak putus ketika dipanggil dari direktori lain
- Symlink bisa menunjuk ke direktori dan melintasi filesystem berbeda (berbeda dengan hard link)

<div class="page-nav-box">
  <a href="{{ '/docs/linux/users-and-groups/' | relative_url }}" class="page-nav-btn">&larr; Users &amp; Groups</a>
  <a href="{{ '/docs/linux/hardening/' | relative_url }}" class="page-nav-btn">Next: Server Hardening &rarr;</a>
</div>

---
layout: default
title: Monitoring System - Linux Administration
permalink: /docs/linux/monitoring/
---

# Monitoring System

Catatan belajar pribadi dari bootstrap-it.com/linux-admin ditambah beberapa referensi dari dokumentasi AWS EC2

## Why Monitor

Alasan utama memantau server adalah supaya kita tahu kapasitas yang sedang terpakai sebelum service tiba-tiba mati kehabisan CPU, RAM, disk, atau bandwidth. Selain itu, monitoring membantu kita menangkap proses yang lagi nyangkut atau makan resource berlebihan supaya bisa langsung dihentikan. Kalau sudah terbiasa melihat kondisi normalnya, lonjakan traffic atau load yang aneh juga bakal langsung kelihatan

## CPU and Memory

Untuk melihat kondisi CPU, memory, dan load average secara live, biasanya langsung buka top. Di dalamnya kita bisa tekan M untuk urutkan berdasarkan pemakaian memory, P berdasarkan CPU, dan q kalau mau keluar

    $ top
    top - 20:15:04 up 4 days,  3:22,  1 user,  load average: 0.18, 0.12, 0.09
    Tasks: 112 total,   1 running, 111 sleeping,   0 stopped,   0 zombie
    %Cpu(s):  2.4 us,  0.7 sy,  0.0 ni, 96.6 id,  0.3 wa,  0.0 hi,  0.0 si,  0.0 st
    MiB Mem :   3912.5 total,   1142.8 free,    984.2 used,   1785.5 buff/cache
    MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   2640.1 avail Mem

      PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
     1142 www-data  20   0  214520  24680  11200 S   1.3   0.6   1:12.40 nginx
      845 mysql     20   0 1420312 312450  34120 S   0.7   7.8   8:45.11 mysqld

Kalau cuma butuh cek cepat sisa RAM dan swap tanpa tampilan interaktif, pakai free -h saja biar angkanya langsung kebaca dalam satuan GiB atau MiB

    $ free -h
                   total        used        free      shared  buff/cache   available
    Mem:           3.8Gi       984Mi       1.1Gi        12Mi       1.7Gi       2.6Gi
    Swap:          2.0Gi          0B       2.0Gi

Kalau mau lihat detail mentah dari kernel soal pemakaian memory seperti MemAvailable, Cached, dan SwapCached, bisa langsung baca /proc/meminfo pakai less atau head

    $ head -n 6 /proc/meminfo
    MemTotal:        4006420 kB
    MemFree:         1170232 kB
    MemAvailable:    2703480 kB
    Buffers:          142120 kB
    Cached:          1524100 kB
    SwapCached:            0 kB

## Disk Space

Untuk cek kapasitas disk yang terpasang sekalian tipe filesystem-nya, jalankan df -hT

    $ df -hT
    Filesystem     Type      Size  Used Avail Use% Mounted on
    tmpfs          tmpfs     392M  1.2M  391M   1% /run
    /dev/sda1      ext4       58G   18G   38G  32% /
    tmpfs          tmpfs     2.0G     0  2.0G   0% /dev/shm

Kalau cuma ingin fokus ke partisi ext4 dan menyembunyikan tmpfs yang banyak, tambahkan flag -t ext4

    $ df -h -t ext4
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda1        58G   18G   38G  32% /

Waktu disk mulai penuh dan mau cari folder mana yang paling boros, biasanya langsung cek pakai du -sh di folder yang dicurigai seperti /var/log

    $ sudo du -sh /var/log/*
    4.2M    /var/log/auth.log
    180M    /var/log/journal
    12M     /var/log/syslog

## Network Traffic

Untuk memantau traffic jaringan secara real-time per koneksi di interface tertentu, misalnya eno1, bisa jalankan iftop -i eno1

    $ sudo iftop -i eno1
                     12.5Kb          25.0Kb          37.5Kb          50.0Kb
    +----------------+---------------+---------------+---------------+---------
    192.168.1.10            => 192.168.1.50                  18.4Kb  14.2Kb  12.1Kb
                            <=                                2.1Kb   1.8Kb   1.5Kb
    ---------------------------------------------------------------------------
    TX:             cum:   412KB   peak:   24.1Kb        rates:   18.4Kb  14.2Kb
    RX:                    108KB            5.2Kb                  2.1Kb   1.8Kb

Sedangkan untuk melihat port TCP atau UDP mana saja yang lagi listening beserta proses pemiliknya, ss -tulnp jauh lebih praktis

    $ sudo ss -tulnp
    Netid  State   Recv-Q  Send-Q   Local Address:Port   Peer Address:Port  Process
    udp    UNCONN  0       0        127.0.0.53%lo:53          0.0.0.0:*      users:(("systemd-resolve",pid=512,fd=13))
    tcp    LISTEN  0       128            0.0.0.0:22          0.0.0.0:*      users:(("sshd",pid=790,fd=3))
    tcp    LISTEN  0       511            0.0.0.0:80          0.0.0.0:*      users:(("nginx",pid=1142,fd=6))

## AWS EC2 Note

Di lingkungan AWS EC2, command seperti top dan free -h cuma menampilkan apa yang dilihat kernel di dalam VM, sedangkan metrik di sisi hypervisor seperti CPUCreditBalance pada instance t3 atau t4g dan antrean disk EBS dipantau lewat Amazon CloudWatch

<div class="page-nav-box">
  <a href="{{ '/' | relative_url }}" class="page-nav-btn">&larr; Home</a>
  <a href="{{ '/docs/linux/processes/' | relative_url }}" class="page-nav-btn">Next: Managing Processes &rarr;</a>
</div>

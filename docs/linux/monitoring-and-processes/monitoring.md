---
layout: default
title: Monitoring System - Linux Administration
permalink: /docs/linux/monitoring/
---

# Monitoring System

Catatan materi dari bootstrap-it.com/linux-admin dan dokumentasi AWS EC2

## Kenapa Perlu Monitoring

- Mengetahui kapasitas CPU, memory, disk, dan network yang sedang terpakai sebelum service down
- Menemukan proses yang nyangkut atau makan resource berlebihan supaya bisa langsung dihentikan
- Punya baseline kondisi normal server sehingga lonjakan traffic atau load langsung ketahuan

## CPU dan Memory

Pengecekan proses, load average, dan pemakaian CPU/memory secara live dengan top

    top

    top - 20:15:04 up 4 days,  3:22,  1 user,  load average: 0.18, 0.12, 0.09
    Tasks: 112 total,   1 running, 111 sleeping,   0 stopped,   0 zombie
    %Cpu(s):  2.4 us,  0.7 sy,  0.0 ni, 96.6 id,  0.3 wa,  0.0 hi,  0.0 si,  0.0 st
    MiB Mem :   3912.5 total,   1142.8 free,    984.2 used,   1785.5 buff/cache
    MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   2640.1 avail Mem

      PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
     1142 www-data  20   0  214520  24680  11200 S   1.3   0.6   1:12.40 nginx
      845 mysql     20   0 1420312 312450  34120 S   0.7   7.8   8:45.11 mysqld

- Tekan P untuk urutkan berdasarkan CPU, M berdasarkan memory, q untuk keluar
- Perhatikan nilai avail Mem dan wa (iowait), bukan hanya free

Cek ringkasan RAM dan swap tanpa tampilan interaktif

    free -h

                   total        used        free      shared  buff/cache   available
    Mem:           3.8Gi       984Mi       1.1Gi        12Mi       1.7Gi       2.6Gi
    Swap:          2.0Gi          0B       2.0Gi

- Total RAM: 3.8 GiB, terpakai 984 MiB, available 2.6 GiB
- Swap 2.0 GiB masih kosong (0B used)

Cek detail counter memory langsung dari kernel di /proc/meminfo

    head -n 6 /proc/meminfo

    MemTotal:        4006420 kB
    MemFree:         1170232 kB
    MemAvailable:    2703480 kB
    Buffers:          142120 kB
    Cached:          1524100 kB
    SwapCached:            0 kB

## Disk Space

Pengecekan partisi, kapasitas filesystem, dan tipe filesystem

    df -hT

    Filesystem     Type      Size  Used Avail Use% Mounted on
    tmpfs          tmpfs     392M  1.2M  391M   1% /run
    /dev/sda1      ext4       58G   18G   38G  32% /
    tmpfs          tmpfs     2.0G     0  2.0G   0% /dev/shm

Filter output df khusus filesystem ext4 supaya tmpfs tidak ikut tampil

    df -t ext4 -h

    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda1        58G   18G   38G  32% /

- Total kapasitas root (/dev/sda1): 58G, terpakai 18G (32%), sisa 38G

Cek folder mana yang paling banyak memakan storage di /var/log

    sudo du -sh /var/log/*

    4.2M    /var/log/auth.log
    180M    /var/log/journal
    12M     /var/log/syslog

## Network Traffic

Pantau traffic jaringan secara live per koneksi pada interface eno1

    sudo iftop -i eno1

                     12.5Kb          25.0Kb          37.5Kb          50.0Kb
    +----------------+---------------+---------------+---------------+---------
    192.168.1.10            => 192.168.1.50                  18.4Kb  14.2Kb  12.1Kb
                            <=                                2.1Kb   1.8Kb   1.5Kb
    ---------------------------------------------------------------------------
    TX:             cum:   412KB   peak:   24.1Kb        rates:   18.4Kb  14.2Kb
    RX:                    108KB            5.2Kb                  2.1Kb   1.8Kb

Cek daftar port TCP/UDP yang sedang listening beserta PID pemiliknya

    sudo ss -tulnp

    Netid  State   Recv-Q  Send-Q   Local Address:Port   Peer Address:Port  Process
    udp    UNCONN  0       0        127.0.0.53%lo:53          0.0.0.0:*      users:(("systemd-resolve",pid=512,fd=13))
    tcp    LISTEN  0       128            0.0.0.0:22          0.0.0.0:*      users:(("sshd",pid=790,fd=3))
    tcp    LISTEN  0       511            0.0.0.0:80          0.0.0.0:*      users:(("nginx",pid=1142,fd=6))

## Catatan AWS EC2

- top dan free -h hanya membaca metrik di dalam guest OS
- Metrik sisi hypervisor seperti CPUCreditBalance pada instance t3/t4g dan antrean disk EBS dipantau lewat Amazon CloudWatch

<div class="page-nav-box">
  <a href="{{ '/' | relative_url }}" class="page-nav-btn">&larr; Home</a>
  <a href="{{ '/docs/linux/processes/' | relative_url }}" class="page-nav-btn">Next: Managing Processes &rarr;</a>
</div>

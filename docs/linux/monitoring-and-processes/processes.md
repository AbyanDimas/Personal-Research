---
layout: default
title: Managing System Processes - Linux Administration
permalink: /docs/linux/processes/
---

# Managing System Processes

Catatan belajar pribadi dari bootstrap-it.com/linux-admin

## Inspecting Processes

Saat mau cek proses apa saja yang lagi jalan di terminal sekarang, cukup ketik ps. Kalau mau lihat semua proses dari seluruh user lengkap dengan PID dan penggunaan CPU atau RAM-nya, pakai ps aux lalu bisa disaring pakai grep misalnya untuk mencari ssh

    $ ps
      PID TTY          TIME CMD
     2410 pts/0    00:00:00 bash
     2488 pts/0    00:00:00 ps

    $ ps aux | grep ssh
    root         790  0.0  0.1  15428  5820 ?        Ss   Nov21   0:02 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
    root        2395  0.0  0.2  17840  9124 ?        Ss   20:10   0:00 sshd: ubuntu [priv]
    ubuntu      2409  0.0  0.1  17972  6340 ?        S    20:10   0:00 sshd: ubuntu@pts/0

Cara lain yang lebih ringkas tanpa memunculkan proses grep itu sendiri adalah pgrep -a

    $ pgrep -a sshd
    790 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
    2395 sshd: ubuntu [priv]
    2409 sshd: ubuntu@pts/0

## Reading Event Data and Logs

Untuk melacak kejadian terbaru di sistem, journalctl --since "10 minutes ago" sangat berguna karena langsung menampilkan log systemd dalam 10 menit terakhir

    $ journalctl --since "10 minutes ago"
    Nov 25 20:10:02 web01 sshd[2395]: Accepted publickey for ubuntu from 10.0.1.5 port 54122 ssh2
    Nov 25 20:10:02 web01 systemd-logind[612]: New session 14 of user ubuntu.
    Nov 25 20:12:41 web01 sudo[2450]:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; COMMAND=/usr/bin/apt update

Kita juga bisa masuk ke /var/log dan lihat daftar file log yang ada di sana, lalu mencari kata kunci tertentu di syslog seperti nama interface jaringan eno1

    $ cd /var/log && ll
    total 19432
    -rw-r----- 1 syslog adm   421840 Nov 25 20:10 auth.log
    -rw-r----- 1 syslog adm  1240120 Nov 25 20:12 syslog
    -rw-r----- 1 syslog adm   184320 Nov 25 19:45 kern.log

    $ grep eno1 < /var/log/syslog | tail -n 3
    Nov 25 19:40:11 web01 systemd-networkd[482]: eno1: Gained carrier
    Nov 25 19:40:13 web01 systemd-networkd[482]: eno1: DHCPv4 address 192.168.1.10/24 via 192.168.1.1
    Nov 25 19:40:13 web01 systemd-networkd[482]: eno1: Configured

Kalau masalahnya berkaitan dengan hardware, driver, atau OOM killer, cek ring buffer kernel lewat dmesg

    $ sudo dmesg | tail -n 4
    [    4.120411] e1000e 0000:00:1f.6 eno1: NIC Link is Up 1000 Mbps Full Duplex, Flow Control: Rx/Tx
    [    4.120892] IPv6: ADDRCONF(NETDEV_CHANGE): eno1: link becomes ready
    [   12.884120] EXT4-fs (sda1): re-mounted. Quota mode: none.

## Testing and Terminating Processes

Untuk latihan mematikan proses yang bikin CPU penuh, kita bisa jalankan yes > /dev/null di background lalu hentikan memakai kill dengan PID-nya

    $ yes > /dev/null &
    [1] 2615

    $ ps -p 2615
      PID TTY          TIME CMD
     2615 pts/0    00:00:04 yes

    $ kill 2615
    [1]+  Terminated              yes > /dev/null

Perlu diingat kalau kill butuh nomor PID, jadi kalau mau langsung menembak nama prosesnya tanpa cari PID dulu, pakai killall atau pkill. Gunakan kill -9 PID hanya kalau proses benar-benar bandel dan tidak mempan dikirimi SIGTERM biasa

    $ yes > /dev/null &
    [1] 2640

    $ killall yes
    [1]+  Terminated              yes > /dev/null

## Managing Services with systemd

Untuk melihat service apa saja yang otomatis jalan setiap kali server boot, gabungkan systemctl list-unit-files dengan grep enabled

    $ systemctl list-unit-files | grep enabled
    cron.service                           enabled         enabled
    nginx.service                          enabled         enabled
    ssh.service                            enabled         enabled
    ufw.service                            enabled         enabled

Kalau ada service yang tidak dipakai seperti apache2, kita bisa cek dulu statusnya lalu matikan sekaligus cabut dari daftar startup memakai systemctl disable --now

    $ systemctl status apache2
    ● apache2.service - The Apache HTTP Server
         Loaded: loaded (/lib/systemd/system/apache2.service; enabled; preset: enabled)
         Active: active (running) since Mon 2026-11-21 16:53:01 WIB; 4 days ago

    $ sudo systemctl disable --now apache2
    Synchronizing state of apache2.service with SysV service script with /lib/systemd/systemd-sysv-install.
    Removed "/etc/systemd/system/multi-user.target.wants/apache2.service".

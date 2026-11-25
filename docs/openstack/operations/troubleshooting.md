---
layout: default
title: Troubleshooting - OpenStack Research Documentation
permalink: /docs/operations/troubleshooting/
---

# Troubleshooting and Diagnostic Guide

Catatan diagnosa dan perbaikan masalah saat menjalankan DevStack multi-node dengan batas RAM 4GB per VM

## 1. Out-Of-Memory (OOM Killer)

Gejala: daemon utama seperti mysqld, beam.smp (RabbitMQ), atau nova-conductor tiba-tiba mati tanpa pesan error di log service

Cek kernel ring buffer untuk memastikan apakah OOM killer yang menembak proses

```bash
sudo dmesg -T | grep -i oom
```

```text
[Wed Nov 25 18:10:04 2026] Out of memory: Killed process 1842 (mysqld) total-vm:1920412kB, anon-rss:512400kB
```

Langkah perbaikan
- Pastikan swapfile 8GB sampai 10GB sudah terpasang dan aktif
- Batasi ukuran buffer pool di /etc/mysql/mariadb.conf.d/50-server.cnf dan pastikan service telemetry (Ceilometer, Aodh, Heat) dimatikan di local.conf

```text
[mysqld]
innodb_buffer_pool_size = 256M
max_connections = 100
```

## 2. Timeout Koneksi AMQP dan Heartbeat Loss

Gejala: nova-compute di Node 2 melaporkan AMQP server on 192.168.101.142:5672 is unreachable atau Heartbeat timeout on AMQP connection

Cek port 5672, status RabbitMQ, dan daftar user/permission di Node 1

```text
sudo ss -tulpn | grep 5672
sudo rabbitmqctl status
sudo rabbitmqctl list_users
sudo rabbitmqctl list_permissions -p /
```

Perpanjang batas heartbeat di /etc/nova/nova.conf jika VM sering mengalami CPU steal atau swap delay

```text
[oslo_messaging_rabbit]
heartbeat_timeout_threshold = 60
heartbeat_rate = 2
```

## 3. Gagal DHCP dan Metadata di OVN

Gejala: instance berstatus ACTIVE tapi gagal mendapat IP dari cloud-init

Cek logical flow di Northbound/Southbound DB, lakukan resync, lalu cek target Southbound DB di Node 2

```text
sudo ovn-nbctl show
sudo ovn-sbctl show

neutron-ovn-db-sync-util \
  --config-file /etc/neutron/neutron.conf \
  --config-file /etc/neutron/plugins/ml2/ml2_conf.ini
```

Cek target Southbound DB di Node 2

```bash
sudo ovs-vsctl get open . external_ids:ovn-remote
```

```text
"tcp:192.168.101.142:6642"
```

## 4. Pengecekan Service systemd di DevStack

Di DevStack modern, seluruh daemon berjalan sebagai systemd user unit di bawah akun stack

```text
systemctl --user list-units "devstack@*"
journalctl --user -u devstack@n-cpu.service -f --no-tail
journalctl --user -u devstack@q-svc.service -f --no-tail
systemctl --user restart devstack@n-cpu.service
```

<div class="page-nav-box">
  <a class="page-nav-btn" href="{{ '/docs/core-services/storage/' | relative_url }}">&larr; Glance & Cinder</a>
  <a class="page-nav-btn" href="{{ '/' | relative_url }}">Return to Overview &rarr;</a>
</div>

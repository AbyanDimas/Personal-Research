---
layout: default
title: DevStack Homelab Overview & Practical Notes
permalink: /docs/overview/devstack-lab-notes/
---

# OpenStack DevStack Lab: Practical Notes

Catatan hasil eksperimen menjalankan OpenStack multi-node di dua VM Ubuntu 24.04.4 LTS dengan RAM 4GB dan disk 60GB per node

## Kenapa Pakai Hardware Terbatas

Kebanyakan tutorial mengasumsikan server 16GB RAM ke atas. Menjalankan lab di VM 4GB justru memaksa kita paham alur kerja aslinya—misalnya kenapa openstack server list memicu Nova Conductor kirim pesan RPC ke RabbitMQ sebelum query ke MySQL, dan berapa besar memory yang dimakan tiap daemon saat tidak ada headroom

## Setup Node

Dua node berada di subnet LAN yang sama dengan satu NIC fisik (ens3) dan tanpa interface terpisah untuk provider network

| Node | Hostname | IP | Role |
|---|---|---|---|
| Node 1 | ab-lab-research-01 | 192.168.101.142 | Controller & Network node |
| Node 2 | ab-lab-research-02 | 192.168.101.143 | Compute node |

Pilihan deployment jatuh ke DevStack karena service dipasang langsung dari source git dan pip. Saat terjadi error, traceback Python dari kode service langsung terlihat tanpa terhalang layer container

## Pembagian Role

- Node 1 menjalankan seluruh control-plane: Keystone, Nova API, Neutron server, Glance, MySQL, RabbitMQ, dan bridge br-ex
- Node 2 dibiarkan ramping hanya menjalankan nova-compute dan OVN controller / Neutron L2 agent
- Pemisahan ini untuk menghindari dua node sama-sama berebut RAM 4GB untuk API dan database

## Networking Tanpa NIC Cadangan

Karena hanya tersedia ens3, external network menumpang di jalur fisik yang sama dengan traffic management. Caranya dengan menyisihkan blok kecil /28 yang tidak terpakai di subnet LAN untuk FLOATING_RANGE dan mengarahkan PUBLIC_INTERFACE ke ens3 agar br-ex dibangun di atasnya

<div class="page-nav-box">
  <a class="page-nav-btn" href="{{ '/docs/overview/architecture/' | relative_url }}">&larr; Architecture & Topology</a>
  <a class="page-nav-btn" href="{{ '/docs/overview/environment-setup/' | relative_url }}">Next: Environment & Setup &rarr;</a>
</div>

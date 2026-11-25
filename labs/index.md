---
layout: default
title: Lab Scripts & Automation - Personal Research Journal
permalink: /labs/
---

# Lab Automation Scripts & Configurations

Kumpulan script bootstrap dan template konfigurasi untuk lab Linux dan OpenStack

## Struktur Direktori

    labs/
    ├── devstack/
    │   ├── bootstrap.sh       # Setup OS, user stack, dan clone devstack
    │   └── local.conf         # Template DevStack (OVN + Placement) untuk RAM 4GB
    ├── linux/
    │   ├── health-check.sh    # Snapshot memory, disk, proses, port, dan journal
    │   ├── user-group-lab.sh  # Latihan user, group, permission, dan symlink
    │   ├── hardening-audit.sh # Audit read-only service boot, port, dan MAC
    │   └── index.md           # Dokumentasi script lab Linux
    └── README.md              # Panduan quickstart

Untuk script lab Linux, lihat [Linux Lab Scripts]({{ '/labs/linux/' | relative_url }})

## DevStack Lab Automation

### 1. bootstrap.sh

Menyiapkan VM Ubuntu 22.04 LTS atau 24.04 LTS untuk DevStack: install git/sudo/curl/bridge-utils, buat user stack dengan passwordless sudo, aktifkan net.ipv4.ip_forward = 1, dan clone repo DevStack

    curl -fsSL https://raw.githubusercontent.com/AbyanDimas/Personal-Research/pages/labs/devstack/bootstrap.sh | sudo bash

### 2. local.conf

Konfigurasi untuk environment RAM 4GB dengan OVN/OVS, Keystone, Glance, Nova, Placement, Neutron, dan worker dibatasi (API_WORKERS=2, CONDUCTOR_WORKERS=2) agar tidak OOM

    su - stack
    cd /opt/stack/devstack
    cp /path/to/Personal-Research/labs/devstack/local.conf ./local.conf
    ./stack.sh

## Kolla-Ansible Assets

Untuk deployment multi-node berbasis container, lihat panduan di [Kolla-Ansible Multi-Node Deployment]({{ '/docs/operations/kolla-ansible/' | relative_url }})

<div class="page-nav-box">
  <a href="{{ '/docs/operations/kolla-ansible/' | relative_url }}" class="page-nav-btn">&larr; Kolla-Ansible Guide</a>
  <a href="{{ '/' | relative_url }}" class="page-nav-btn">Back to Home &rarr;</a>
</div>

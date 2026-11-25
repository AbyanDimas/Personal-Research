---
layout: default
title: Environment & Setup - OpenStack Research Documentation
permalink: /docs/overview/environment-setup/
---

# Prerequisites and Environment Setup

Langkah persiapan OS Ubuntu 24.04 LTS dan konfigurasi dual local.conf untuk deploy DevStack di Node 1 (Controller) dan Node 2 (Compute) dengan RAM 4GB

## 1. Persiapan Sistem Operasi

Jalankan langkah ini di Node 1 dan Node 2

Buat swapfile 8GB supaya proses kompilasi Python, instalasi dependensi, dan inisialisasi database tidak kehabisan RAM 4GB

    sudo fallocate -l 8G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

Buat user non-root stack dengan akses passwordless sudo, lalu clone repository DevStack

    sudo useradd -s /bin/bash -d /opt/stack -m stack
    echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
    sudo chmod 0440 /etc/sudoers.d/stack

    sudo su - stack
    git clone https://opendev.org/openstack/devstack.git
    cd devstack

## 2. Konfigurasi Controller (Node 1)

Buat file /opt/stack/devstack/local.conf di Node 1 (192.168.101.142)

    [[local|localrc]]
    HOST_IP=192.168.101.142
    SERVICE_HOST=192.168.101.142
    MYSQL_HOST=192.168.101.142
    RABBIT_HOST=192.168.101.142
    GLANCE_HOSTPORT=192.168.101.142:9292

    ADMIN_PASSWORD=SecretPassword123
    DATABASE_PASSWORD=$ADMIN_PASSWORD
    RABBIT_PASSWORD=$ADMIN_PASSWORD
    SERVICE_PASSWORD=$ADMIN_PASSWORD

    # Matikan service non-esensial yang boros RAM
    disable_service horizon
    disable_service tempest
    disable_service heat

    # Aktifkan Neutron dengan driver OVN
    enable_plugin neutron https://opendev.org/openstack/neutron
    Q_AGENT=ovn
    Q_ML2_PLUGIN_MECHANISM_DRIVERS=ovn,logger
    Q_ML2_TENANT_NETWORK_TYPE=geneve

    # Mapping external bridge pada single NIC
    PUBLIC_INTERFACE=ens3
    FLOATING_RANGE=192.168.101.224/28
    Q_FLOATING_ALLOCATION_METHOD=continuous
    PUBLIC_NETWORK_GATEWAY=192.168.101.1

## 3. Konfigurasi Compute Node (Node 2)

Buat file /opt/stack/devstack/local.conf di Node 2 (192.168.101.143)

    [[local|localrc]]
    HOST_IP=192.168.101.143
    SERVICE_HOST=192.168.101.142
    MYSQL_HOST=192.168.101.142
    RABBIT_HOST=192.168.101.142
    GLANCE_HOSTPORT=192.168.101.142:9292

    ADMIN_PASSWORD=SecretPassword123
    DATABASE_PASSWORD=$ADMIN_PASSWORD
    RABBIT_PASSWORD=$ADMIN_PASSWORD
    SERVICE_PASSWORD=$ADMIN_PASSWORD

    # Hanya jalankan service compute dan agent OVN di Node 2
    ENABLED_SERVICES=n-cpu,ovn-controller,ovs-vswitchd,ovsdb-server,placement-client
    NOVA_VNC_ENABLED=True
    NOVNCPROXY_URL="http://192.168.101.142:6080/vnc_auto.html"
    VNCSERVER_LISTEN=192.168.101.143
    VNCSERVER_PROXYCLIENT_ADDRESS=192.168.101.143

## 4. Eksekusi dan Verifikasi

Jalankan ./stack.sh secara berurutan: selesaikan Node 1 dulu baru jalankan ./stack.sh di Node 2

Verifikasi registrasi hypervisor dan service compute dari Node 1

Command:

    source openrc admin admin
    openstack hypervisor list
    openstack compute service list

Output:

    +----+---------------------+-----------------+----------------+-------+
    | ID | Hypervisor Hostname | Hypervisor Type | Host IP        | State |
    +----+---------------------+-----------------+----------------+-------+
    |  1 | ab-lab-research-02  | QEMU            | 192.168.101.143| up    |
    +----+---------------------+-----------------+----------------+-------+

<div class="page-nav-box">
  <a class="page-nav-btn" href="{{ '/docs/overview/architecture/' | relative_url }}">&larr; Architecture & Topology</a>
  <a class="page-nav-btn" href="{{ '/docs/core-services/keystone/' | relative_url }}">Next: Keystone (Identity) &rarr;</a>
</div>

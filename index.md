---
layout: default
title: Personal Research Journal
---

# Personal Research Journal

Just a place for my personal study notes, commands, and random technical experiments

## Linux

### Monitoring & Processes

- [Monitoring System]({{ '/docs/linux/monitoring/' | relative_url }}) - CPU, RAM, disk, network traffic, and CloudWatch vs OS metrics
- [Managing System Processes]({{ '/docs/linux/processes/' | relative_url }}) - ps, journalctl, dmesg, kill/killall, and systemd units

### Users, Permissions & Links

- [Working with Users and Groups]({{ '/docs/linux/users-and-groups/' | relative_url }}) - /etc/passwd, sudo best practices, useradd, groupadd, and EC2 SSH access
- [Object Permissions & Symlinks]({{ '/docs/linux/permissions-and-links/' | relative_url }}) - numeric chmod notation, chown, and symbolic links

### Security

- [Hardening Your Server]({{ '/docs/linux/hardening/' | relative_url }}) - patching, nmap port checks, Security Groups, AppArmor/SELinux, and auditd
- [Data Encryption]({{ '/docs/linux/encryption/' | relative_url }}) - AWS EBS/KMS encryption, LUKS cryptsetup, and GPG

### Labs

- [Linux Lab Scripts]({{ '/labs/linux/' | relative_url }}) - bash scripts for health checks, user/group setup, and hardening audits

## OpenStack

### Overview

- [Architecture & Topology]({{ '/docs/overview/architecture/' | relative_url }}) - multi-node DevStack topology, control-plane vs compute split, and AMQP/SQL RPC flow
- [Environment & Setup]({{ '/docs/overview/environment-setup/' | relative_url }}) - Ubuntu 24.04 LTS prep, 8GB swap sizing, stack user permissions, and local.conf specs
- [DevStack Lab Notes]({{ '/docs/overview/devstack-lab-notes/' | relative_url }}) - real-world homelab notes on constrained hardware

### Core Services

- [Keystone]({{ '/docs/core-services/keystone/' | relative_url }}) - Fernet tokens, key rotation, system-scoped vs project-scoped RBAC, and service tokens
- [Nova & Placement]({{ '/docs/core-services/nova-placement/' | relative_url }}) - instance boot workflow, scheduler filters, and Placement resource providers
- [Neutron & OVN]({{ '/docs/core-services/neutron-ovn/' | relative_url }}) - OVN software-defined networking, Geneve encapsulation, distributed routing, and single-NIC br-ex
- [Glance & Cinder]({{ '/docs/core-services/storage/' | relative_url }}) - image formats (RAW vs QCOW2), block storage lifecycle, and LVM loopback driver

### Operations & Labs

- [Troubleshooting & Diagnostics]({{ '/docs/operations/troubleshooting/' | relative_url }}) - OOM prevention, AMQP heartbeat tuning, systemd services, and OVN DB sync
- [Kolla-Ansible]({{ '/docs/operations/kolla-ansible/' | relative_url }}) - containerized multi-node deployment with Docker/Podman, HAProxy VIP, and Ansible
- [Lab Scripts & Configs]({{ '/labs/' | relative_url }}) - DevStack bootstrap scripts and low-memory local.conf recipes

(function () {
  const searchInput = document.getElementById('wiki-search-input');
  const dropdown = document.getElementById('search-dropdown');
  if (!searchInput || !dropdown) return;

  const baseUrl = (searchInput.getAttribute('data-baseurl') || '').replace(/\/$/, '');

  const searchIndex = [
    {
      title: "Home",
      url: baseUrl + "/",
      category: "Journal",
      description: "Personal research journal index and study notes.",
      keywords: "home index research journal notes"
    },
    {
      title: "Monitoring System",
      url: baseUrl + "/docs/linux/monitoring/",
      category: "Linux - System & Processes",
      description: "CPU, memory, disk, network traffic monitoring, and CloudWatch vs OS metrics.",
      keywords: "linux monitoring top free df du iftop ss meminfo cloudwatch cpucreditbalance"
    },
    {
      title: "Managing System Processes",
      url: baseUrl + "/docs/linux/processes/",
      category: "Linux - System & Processes",
      description: "Process trees, journalctl, dmesg, kill/killall, and systemd service management.",
      keywords: "linux processes ps pgrep journalctl syslog dmesg yes kill killall systemctl"
    },
    {
      title: "Working with Users and Groups",
      url: baseUrl + "/docs/linux/users-and-groups/",
      category: "Linux - Access & Security",
      description: "Account files, sudo best practices, useradd, groupadd, usermod, and EC2 SSH access.",
      keywords: "linux users groups passwd shadow skel id who w last useradd groupadd chown usermod ssh ssm"
    },
    {
      title: "Object Permissions & Symlinks",
      url: baseUrl + "/docs/linux/permissions-and-links/",
      category: "Linux - Access & Security",
      description: "Numeric chmod notation, chown ownership, and extending object usability with symlinks.",
      keywords: "linux permissions numeric 755 700 644 600 chmod chown symlink ln -s"
    },
    {
      title: "Hardening Your Server",
      url: baseUrl + "/docs/linux/hardening/",
      category: "Linux - Access & Security",
      description: "Patching, nmap port scans, AWS Security Groups, AppArmor/SELinux, and auditd.",
      keywords: "linux hardening apt dnf nmap security group apparmor selinux auditd lynis"
    },
    {
      title: "Data Encryption",
      url: baseUrl + "/docs/linux/encryption/",
      category: "Linux - Access & Security",
      description: "Amazon EBS and AWS KMS encryption, LUKS cryptsetup, and GPG file encryption.",
      keywords: "linux encryption ebs kms aes256 luks cryptsetup gpg"
    },
    {
      title: "Linux Lab Scripts",
      url: baseUrl + "/labs/linux/",
      category: "Linux - Labs",
      description: "Bash scripts for Linux health checks, user/group/permission labs, and hardening audits.",
      keywords: "linux labs bash scripts health-check user-group-lab hardening-audit"
    },
    {
      title: "Architecture & Topology",
      url: baseUrl + "/docs/overview/architecture/",
      category: "OpenStack - Overview",
      description: "Two-node DevStack topology on 4GB RAM VMs. Controller vs Compute role split, AMQP RPC, single NIC design.",
      keywords: "devstack multi-node 4gb ram homelab topology controller compute rabbitmq mysql amqp rpc single nic br-ex ens3 floating ip"
    },
    {
      title: "Environment & Setup (local.conf)",
      url: baseUrl + "/docs/overview/environment-setup/",
      category: "OpenStack - Overview",
      description: "Ubuntu 24.04 LTS host configuration, 8GB swap sizing, non-root stack user, local.conf for Node 1 and Node 2.",
      keywords: "ubuntu 24.04 swap 8gb stack user sudo local.conf controller compute stacking devstack ovn geneve"
    },
    {
      title: "DevStack Lab Practical Notes",
      url: baseUrl + "/docs/overview/devstack-lab-notes/",
      category: "OpenStack - Overview",
      description: "Real-world observations running DevStack on two 4GB VMs without dedicated provider NICs.",
      keywords: "homelab devstack notes lessons survival split single nic br-ex ens3 floating range underpowered"
    },
    {
      title: "Keystone: Identity Service",
      url: baseUrl + "/docs/core-services/keystone/",
      category: "OpenStack - Core Services",
      description: "Fernet token architecture, key rotation, system-scoped and project-scoped RBAC, service catalog and service tokens.",
      keywords: "keystone identity auth authentication fernet token rotation rbac system scope project scope service catalog service token"
    },
    {
      title: "Nova & Placement: Compute",
      url: baseUrl + "/docs/core-services/nova-placement/",
      category: "OpenStack - Core Services",
      description: "Placement API decoupling, Resource Providers, Traits, instance boot lifecycle, Nova Conductor, libvirt/KVM tuning.",
      keywords: "nova compute placement api resource provider inventory traits allocation instance boot lifecycle scheduler libvirt kvm"
    },
    {
      title: "Neutron & OVN: Networking",
      url: baseUrl + "/docs/core-services/neutron-ovn/",
      category: "OpenStack - Core Services",
      description: "OVN SDN backend, Geneve encapsulation, Northbound/Southbound DB, Distributed Virtual Routing (DVR), br-ex single NIC.",
      keywords: "neutron sdn ovn open virtual network geneve vxlan dvr distributed virtual routing floating ip br-ex bridge ip_forward"
    },
    {
      title: "Glance & Cinder: Storage",
      url: baseUrl + "/docs/core-services/storage/",
      category: "OpenStack - Core Services",
      description: "Image management (RAW vs QCOW2), Cinder persistent block storage, LVM loopback driver, volume attachment workflow.",
      keywords: "glance cinder image raw qcow2 block storage persistent volume iscsi lvm loopback ceph rbd"
    },
    {
      title: "Troubleshooting & Diagnostics",
      url: baseUrl + "/docs/operations/troubleshooting/",
      category: "OpenStack - Operations",
      description: "Solving OOM kills on MySQL and RabbitMQ, AMQP heartbeat tuning, OVN DB synchronization, systemd service management.",
      keywords: "troubleshooting diagnostic oom killer mysqld memory out of memory rabbitmq heartbeat timeout ovn db sync systemd journalctl"
    },
    {
      title: "Kolla-Ansible (Multi-Node)",
      url: baseUrl + "/docs/operations/kolla-ansible/",
      category: "OpenStack - Operations",
      description: "Containerized OpenStack deployment with Docker/Podman microservices, HAProxy Keepalived VIP, and Ansible automation.",
      keywords: "kolla ansible multinode containerized docker podman haproxy keepalived vip globals.yml inventory deployment production"
    },
    {
      title: "Lab Automation Assets",
      url: baseUrl + "/labs/",
      category: "OpenStack - Labs",
      description: "Ready-to-use DevStack bootstrap scripts, low-memory local.conf recipes, and operational configs.",
      keywords: "labs devstack scripts automation bootstrap local.conf shell bash config templates recipes"
    }
  ];

  let selectedIndex = -1;

  function renderResults(results) {
    if (results.length === 0) {
      dropdown.innerHTML = '<div class="search-empty">No matching documents found</div>';
      dropdown.style.display = 'block';
      return;
    }

    dropdown.innerHTML = results.map((item, idx) => `
      <a href="${item.url}" class="search-result-item" data-index="${idx}">
        <div class="search-result-header">
          <span class="search-result-title">${item.title}</span>
          <span class="search-result-category">${item.category}</span>
        </div>
        <div class="search-result-desc">${item.description}</div>
      </a>
    `).join('');

    dropdown.style.display = 'block';
    selectedIndex = -1;
  }

  function handleSearch() {
    const query = searchInput.value.trim().toLowerCase();
    if (!query) {
      dropdown.style.display = 'none';
      dropdown.innerHTML = '';
      return;
    }

    const matches = searchIndex.filter(item => {
      return item.title.toLowerCase().includes(query) ||
             item.description.toLowerCase().includes(query) ||
             item.keywords.toLowerCase().includes(query) ||
             item.category.toLowerCase().includes(query);
    });

    renderResults(matches);
  }

  searchInput.addEventListener('input', handleSearch);

  searchInput.addEventListener('keydown', function (e) {
    const items = dropdown.querySelectorAll('.search-result-item');
    if (!items.length || dropdown.style.display === 'none') return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = (selectedIndex + 1) % items.length;
      updateActiveItem(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = (selectedIndex - 1 + items.length) % items.length;
      updateActiveItem(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && items[selectedIndex]) {
        items[selectedIndex].click();
      } else if (items.length > 0) {
        items[0].click();
      }
    } else if (e.key === 'Escape') {
      dropdown.style.display = 'none';
      searchInput.blur();
    }
  });

  function updateActiveItem(items) {
    items.forEach((item, idx) => {
      if (idx === selectedIndex) {
        item.classList.add('selected');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('selected');
      }
    });
  }

  // Keyboard shortcut '/' to focus search
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.dinky-search')) {
      dropdown.style.display = 'none';
    }
  });
})();

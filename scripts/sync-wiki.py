#!/usr/bin/env python3
"""
Automated GitHub Wiki Synchronizer.
Converts repository documentation into GitHub Wiki format and pushes to
https://github.com/<owner>/<repo>.wiki.git.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Mapping from repo path to GitHub Wiki page name
DOCS_MAP = {
    "index.md": "Home.md",
    "docs/linux/monitoring-and-processes/monitoring.md": "Linux-Monitoring-System.md",
    "docs/linux/monitoring-and-processes/processes.md": "Linux-Managing-Processes.md",
    "docs/linux/users-and-permissions/users-and-groups.md": "Linux-Users-and-Groups.md",
    "docs/linux/users-and-permissions/permissions-and-links.md": "Linux-Permissions-and-Symlinks.md",
    "docs/linux/security/hardening.md": "Linux-Server-Hardening.md",
    "docs/linux/security/encryption.md": "Linux-Data-Encryption.md",
    "labs/linux/index.md": "Linux-Lab-Scripts.md",
    "docs/openstack/overview/architecture.md": "Architecture-and-Topology.md",
    "docs/openstack/overview/environment-setup.md": "Environment-and-Setup.md",
    "docs/openstack/overview/devstack-lab-notes.md": "DevStack-Lab-Notes.md",
    "docs/openstack/core-services/keystone.md": "Keystone-Identity.md",
    "docs/openstack/core-services/nova-placement.md": "Nova-and-Placement-Compute.md",
    "docs/openstack/core-services/neutron-ovn.md": "Neutron-and-OVN-Networking.md",
    "docs/openstack/core-services/storage.md": "Glance-and-Cinder-Storage.md",
    "docs/openstack/operations/troubleshooting.md": "Troubleshooting-and-Diagnostics.md",
    "docs/openstack/operations/kolla-ansible.md": "Kolla-Ansible-Multi-Node.md",
    "labs/index.md": "Lab-Automation-Assets.md",
}

LINK_REPLACEMENTS = {
    r"/docs/linux/monitoring/?": "Linux-Monitoring-System",
    r"/docs/linux/processes/?": "Linux-Managing-Processes",
    r"/docs/linux/users-and-groups/?": "Linux-Users-and-Groups",
    r"/docs/linux/permissions-and-links/?": "Linux-Permissions-and-Symlinks",
    r"/docs/linux/hardening/?": "Linux-Server-Hardening",
    r"/docs/linux/encryption/?": "Linux-Data-Encryption",
    r"/labs/linux/?": "Linux-Lab-Scripts",
    r"/docs/overview/architecture/?": "Architecture-and-Topology",
    r"\./docs/overview/architecture/?": "Architecture-and-Topology",
    r"/docs/overview/environment-setup/?": "Environment-and-Setup",
    r"\./docs/overview/environment-setup/?": "Environment-and-Setup",
    r"/docs/overview/devstack-lab-notes/?": "DevStack-Lab-Notes",
    r"\./docs/overview/devstack-lab-notes/?": "DevStack-Lab-Notes",
    r"/docs/core-services/keystone/?": "Keystone-Identity",
    r"\./docs/core-services/keystone/?": "Keystone-Identity",
    r"/docs/core-services/nova-placement/?": "Nova-and-Placement-Compute",
    r"\./docs/core-services/nova-placement/?": "Nova-and-Placement-Compute",
    r"/docs/core-services/neutron-ovn/?": "Neutron-and-OVN-Networking",
    r"\./docs/core-services/neutron-ovn/?": "Neutron-and-OVN-Networking",
    r"/docs/core-services/storage/?": "Glance-and-Cinder-Storage",
    r"\./docs/core-services/storage/?": "Glance-and-Cinder-Storage",
    r"/docs/operations/troubleshooting/?": "Troubleshooting-and-Diagnostics",
    r"\./docs/operations/troubleshooting/?": "Troubleshooting-and-Diagnostics",
    r"/docs/operations/kolla-ansible/?": "Kolla-Ansible-Multi-Node",
    r"\./docs/operations/kolla-ansible/?": "Kolla-Ansible-Multi-Node",
    r"/labs/?": "Lab-Automation-Assets",
    r"\./labs/?": "Lab-Automation-Assets",
}

SIDEBAR_CONTENT = """[[Home]]

### Linux
* [[Monitoring System|Linux-Monitoring-System]]
* [[Managing Processes|Linux-Managing-Processes]]
* [[Users & Groups|Linux-Users-and-Groups]]
* [[Permissions & Symlinks|Linux-Permissions-and-Symlinks]]
* [[Server Hardening|Linux-Server-Hardening]]
* [[Data Encryption|Linux-Data-Encryption]]
* [[Linux Lab Scripts|Linux-Lab-Scripts]]

### OpenStack - Overview
* [[Architecture & Topology|Architecture-and-Topology]]
* [[Environment & Setup|Environment-and-Setup]]
* [[DevStack Lab Notes|DevStack-Lab-Notes]]

### OpenStack - Core Services
* [[Keystone (Identity)|Keystone-Identity]]
* [[Nova & Placement (Compute)|Nova-and-Placement-Compute]]
* [[Neutron & OVN (Networking)|Neutron-and-OVN-Networking]]
* [[Glance & Cinder (Storage)|Glance-and-Cinder-Storage]]

### OpenStack - Operations & Labs
* [[Troubleshooting & Diagnostics|Troubleshooting-and-Diagnostics]]
* [[Kolla-Ansible (Multi-Node)|Kolla-Ansible-Multi-Node]]
* [[Lab Scripts & Configs|Lab-Automation-Assets]]
"""

FOOTER_CONTENT = """---
*Synced automatically from the main repository via GitHub Actions.* [View Source on GitHub](https://github.com/AbyanDimas/Personal-Research)
"""

def clean_frontmatter(content):
    # Strip Jekyll frontmatter
    content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)
    # Strip page-nav-box div
    content = re.sub(r'<div class="page-nav-box">.*?</div>', "", content, flags=re.DOTALL)
    # Unwrap Jekyll relative_url filter
    content = re.sub(r"\{\{\s*['\"]([^'\"]+)['\"]\s*\|\s*relative_url\s*\}\}", r"\1", content)
    # Replace relative links with wiki page names
    for pattern, target in LINK_REPLACEMENTS.items():
        content = re.sub(r'\]\(' + pattern + r'\)', f']({target})', content)
        content = re.sub(r'href=[\'"]' + pattern + r'[\'"]', f'href="{target}"', content)
    return content.strip() + "\n"

def run_cmd(cmd, cwd=None, check=True):
    res = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {cmd}\n{res.stderr.strip()}")
    return res.stdout.strip()

def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        try:
            token = run_cmd("gh auth token")
        except Exception:
            token = ""

    repo = os.environ.get("GITHUB_REPOSITORY", "AbyanDimas/Personal-Research")

    if not token:
        wiki_url = f"https://github.com/{repo}.wiki.git"
    else:
        wiki_url = f"https://x-access-token:{token}@github.com/{repo}.wiki.git"

    temp_wiki_dir = Path("/tmp/wiki-sync-repo")
    if temp_wiki_dir.exists():
        shutil.rmtree(temp_wiki_dir)

    print(f"==> Cloning wiki repository: https://github.com/{repo}.wiki.git")
    try:
        run_cmd(f"git clone {wiki_url} {temp_wiki_dir}")
    except Exception as e:
        print(f"❌ Could not clone wiki repository: {e}")
        sys.exit(1)

    print("==> Converting documentation for GitHub Wiki...")
    repo_root = Path(__file__).resolve().parent.parent

    for src_rel, dest_name in DOCS_MAP.items():
        src_path = repo_root / src_rel
        dest_path = temp_wiki_dir / dest_name

        if not src_path.exists():
            print(f"Warning: {src_rel} does not exist. Skipping.")
            continue

        raw_content = src_path.read_text(encoding="utf-8")
        converted_content = clean_frontmatter(raw_content)
        dest_path.write_text(converted_content, encoding="utf-8")
        print(f"  ✓ Processed: {src_rel} -> {dest_name}")

    # Write Sidebar and Footer
    (temp_wiki_dir / "_Sidebar.md").write_text(SIDEBAR_CONTENT.strip() + "\n", encoding="utf-8")
    (temp_wiki_dir / "_Footer.md").write_text(FOOTER_CONTENT.strip() + "\n", encoding="utf-8")
    print("  ✓ Created _Sidebar.md and _Footer.md")

    # Configure Git in wiki clone
    run_cmd('git config user.name "github-actions[bot]"', cwd=temp_wiki_dir)
    run_cmd('git config user.email "41898282+github-actions[bot]@users.noreply.github.com"', cwd=temp_wiki_dir)

    status = run_cmd("git status --porcelain", cwd=temp_wiki_dir)
    if not status:
        print("==> Wiki is already up-to-date with latest docs. No changes to push.")
        sys.exit(0)

    print("==> Changes detected. Committing to wiki...")
    run_cmd("git add -A", cwd=temp_wiki_dir)
    run_cmd('git commit -m "docs: synchronize wiki with latest repository documentation [skip ci]"', cwd=temp_wiki_dir)

    print("==> Pushing changes to GitHub Wiki...")
    run_cmd("git push origin master", cwd=temp_wiki_dir)
    print("✅ Successfully synchronized GitHub Wiki!")

if __name__ == "__main__":
    main()

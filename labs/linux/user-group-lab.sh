#!/usr/bin/env bash
set -euo pipefail

# Requires root/sudo. Demonstrates user, group, permission, and symlink setup.
GROUP_NAME="secret-group"
USER_NAME="jane"
TARGET_DIR="/var/secret"
SCRIPT_SRC="/home/ubuntu/scripts/myscript.sh"

if ! getent group "${GROUP_NAME}" >/dev/null; then
  groupadd "${GROUP_NAME}"
fi

if ! id "${USER_NAME}" >/dev/null 2>&1; then
  useradd -m "${USER_NAME}"
fi

usermod -a -G "${GROUP_NAME}" "${USER_NAME}"

mkdir -p "${TARGET_DIR}"
chown :"${GROUP_NAME}" "${TARGET_DIR}"
chmod 750 "${TARGET_DIR}"

if [ -f "${SCRIPT_SRC}" ] && [ ! -L "${TARGET_DIR}/myscript.sh" ]; then
  ln -s "${SCRIPT_SRC}" "${TARGET_DIR}/myscript.sh"
fi

echo "Setup complete:"
id "${USER_NAME}"
ls -ld "${TARGET_DIR}"

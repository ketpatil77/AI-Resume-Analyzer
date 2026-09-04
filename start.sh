#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

APP_NAME="AI Resume Analyser"
CLIENT_PORT="${CLIENT_PORT:-5173}"
STAMP_FILE="node_modules/.install-stamp"

echo
echo "$APP_NAME"
echo "=========================="

need_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: $2" >&2
    exit 1
  fi
}

find_port() {
  local port="$1"
  while [ "$port" -le 8999 ]; do
    if ! (ss -ltn 2>/dev/null || netstat -ltn 2>/dev/null || true) | grep -q ":$port "; then
      echo "$port"
      return
    fi
    port=$((port + 1))
  done
  echo "ERROR: No free port found." >&2
  exit 1
}

package_hash() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum package.json | awk '{print $1}'
  else
    shasum -a 256 package.json | awk '{print $1}'
  fi
}

need_command node "Node.js is required. Install Node.js LTS from https://nodejs.org/"
need_command npm "npm is required. Reinstall Node.js LTS from https://nodejs.org/"

HASH="$(package_hash)"
OLD_HASH=""
if [ -f "$STAMP_FILE" ]; then
  OLD_HASH="$(sed -n 's/^PACKAGE_HASH=//p' "$STAMP_FILE")"
fi

if [ ! -d node_modules ] || [ "$HASH" != "$OLD_HASH" ]; then
  echo "Installing dependencies..."
  npm install
  mkdir -p node_modules
  printf "PACKAGE_HASH=%s\n" "$HASH" > "$STAMP_FILE"
else
  echo "Dependencies already ready."
fi

CLIENT_PORT="$(find_port "$CLIENT_PORT")"
export TMPDIR="${TMPDIR:-/tmp}" TEMP="${TEMP:-/tmp}" TMP="${TMP:-/tmp}"

echo "App:    http://127.0.0.1:$CLIENT_PORT"
echo "Local analysis mode. No API key needed."
echo

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "http://127.0.0.1:$CLIENT_PORT" >/dev/null 2>&1 || true
fi

npm run client -- --host 127.0.0.1 --port "$CLIENT_PORT"

#!/usr/bin/env bash
# Turnkey launcher for the NIGHTJAR CTF.
# Creates a local venv, installs deps, prints the LAN URL, and serves the game.
set -euo pipefail
cd "$(dirname "$0")"

PORT="${PORT:-8000}"

if [ ! -d .venv ]; then
  echo "[*] creating virtual environment..."
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[*] installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo "[*] running self-test on the puzzle chain..."
python3 app.py --selftest

# Best-effort LAN IP for macOS.
LAN_IP="$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo '127.0.0.1')"

echo
echo "=================================================================="
echo "  OPERATION NIGHTJAR is live."
echo "  On this machine : http://localhost:${PORT}"
echo "  On your network : http://${LAN_IP}:${PORT}"
echo "  Share the network URL with players on the same Wi-Fi/LAN."
echo "  Stop the server : Ctrl-C"
echo "=================================================================="
echo

PORT="${PORT}" python3 app.py

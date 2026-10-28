#!/usr/bin/env bash
# ContestPusher — Linux/macOS starter
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT="${CONTESTPUSHER_PORT:-8090}"

# ── Kleuren ──
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

# ── Python check ──
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}✗ Python 3 niet gevonden.${NC}"
  echo "  Installeer via: https://www.python.org/downloads/"
  exit 1
fi

PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✓${NC} Python $PY_VER gevonden"

# ── Virtualenv aanmaken als die er niet is ──
if [ ! -d ".venv" ]; then
  echo -e "${YELLOW}→${NC} Virtuele omgeving aanmaken…"
  python3 -m venv .venv
fi

# ── Activeren ──
# shellcheck disable=SC1091
source .venv/bin/activate

# ── Dependencies installeren ──
echo -e "${YELLOW}→${NC} Dependencies controleren / installeren…"
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo -e "${GREEN}✓${NC} Dependencies gereed"

# ── Starten via GUI launcher ──
CONTESTPUSHER_PORT="$PORT" python3 tray.py

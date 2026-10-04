#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/init_db.py
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q -r requirements.txt
python3 app/app.py

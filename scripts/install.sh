#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m pip install -r requirements.txt
python3 scripts/extract_sources.py
python3 scripts/sync_app_data.py
python3 scripts/build_workbook.py
test -f workspace-app/data/index.json
test -f workbook/BMGT8044_Amalgamated_Research_Workspace.xlsx
echo "install complete"

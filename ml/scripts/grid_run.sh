#!/usr/bin/env bash
# One grid job (scripts/grid_job.py), from ml/ on the shared disk:
#   task submit -g 0 -H grid -C ml -- bash scripts/grid_run.sh threshold/deberta-v3-small-open/0.1
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/grid_env.sh
python scripts/grid_job.py run "$1"

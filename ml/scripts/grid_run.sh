#!/usr/bin/env bash
# One job from scripts/jobs.py on an ECS Grid machine, from ml/ on the shared disk:
#   task submit -g 0 -H grid -C ml -- bash scripts/grid_run.sh threshold/deberta-v3-small-open/0.1
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/grid_env.sh
python scripts/jobs.py run "$1"

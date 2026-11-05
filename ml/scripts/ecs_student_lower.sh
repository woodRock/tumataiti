#!/usr/bin/env bash
# Train a student on the deployed recipe (NZ data v2 + open English) with a share
# of the training documents lowercased, because the deployed students fail on
# lowercase text (ml/results/m3open_robust_lower_*). The other arguments and all
# evaluation sets are as ecs_student.sh. Build data/robust first on the shared
# disk (grid_job.py run gold/lower). One GPU, a few hours:
#   task submit -t "RTX A5000" -C ml -n lower-deberta -- ./scripts/ecs_student_lower.sh microsoft/deberta-v3-small deberta-v3-small-open-lower
#   task fetch ml/runs/m3-v2/deberta-v3-small-open-lower
# LOWER_FRACTION sets the share (default 0.25).
set -euo pipefail
cd "$(dirname "$0")/.."
BACKBONE=$1 NAME=$2
shift 2
exec env DATA=v2 EXTRA=open ./scripts/ecs_student.sh "$BACKBONE" "$NAME" --lr 5e-5 \
  --lower-fraction "${LOWER_FRACTION:-0.25}" "$@"

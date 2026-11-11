#!/usr/bin/env bash
# Train a student on the deployed recipe (NZ data v4 + open English) with a share
# of the training documents lowercased, because the deployed students fail on
# lowercase text (ml/results/m3open_robust_lower_*). The other arguments and all
# evaluation sets are as ecs_student.sh. Build data/robust-v4 first on the shared
# disk (jobs.py run gold/lower), or re-predict afterwards with PREDICT_ONLY=1. One GPU, a few hours:
#   task submit -t "RTX A5000" -C ml -n lower-deberta -- ./scripts/ecs_student_lower.sh microsoft/deberta-v3-small deberta-v3-small-open-lower
#   task fetch ml/runs/m3-v4/deberta-v3-small-open-lower
# LOWER_FRACTION sets the share (default 0.25).
set -euo pipefail
cd "$(dirname "$0")/.."
BACKBONE=$1 NAME=$2
shift 2
exec env DATA=v4 EXTRA=open ./scripts/ecs_student.sh "$BACKBONE" "$NAME" --lr 5e-5 \
  --lower-fraction "${LOWER_FRACTION:-0.25}" "$@"

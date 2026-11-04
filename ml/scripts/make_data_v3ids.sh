#!/usr/bin/env bash
# Build the v3ids training data: v3 plus unlabelled order and booking codes
# shaped like IRD numbers and NHIs (SPEC §9.8). Compared against v3.
# Usage: scripts/make_data_v3ids.sh [path-to-tumataiti-ml]
set -euo pipefail
cd "$(dirname "$0")/.."
CLI="${1:-tumataiti-ml}"
V=data/v3ids
[ -f data/v1/nz_test_false_alarm.jsonl ] || ./scripts/make_data_v3.sh "$CLI"
"$CLI" generate --split train_v3ids --n 8000 --seed 1 --out $V/nz_train.jsonl
"$CLI" generate --split dev_v3ids --n 800  --seed 2 --out $V/nz_dev.jsonl

#!/usr/bin/env bash
# Build the held-out false-alarm test set, and the v3 training data (rejected,
# SPEC §9.8): v2 plus templates for false alarms
# (kinship words, ID-shaped order and booking codes), and the held-out
# false-alarm test set. Other evaluation sets are unchanged (data/v1).
# Usage: scripts/make_data_v3.sh [path-to-tumataiti-ml]
set -euo pipefail
cd "$(dirname "$0")/.."
CLI="${1:-tumataiti-ml}"
V=data/v3
[ -f data/v1/pii300k_en_val.jsonl ] || ./scripts/make_data_v1.sh "$CLI"
"$CLI" generate --split train_v3 --n 8000 --seed 1 --out $V/nz_train.jsonl
"$CLI" generate --split dev_v3   --n 800  --seed 2 --out $V/nz_dev.jsonl
"$CLI" generate --split test_false_alarm --n 600 --seed 6 --out data/v1/nz_test_false_alarm.jsonl

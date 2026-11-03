#!/usr/bin/env bash
# Build every M3 dataset (SPEC §9.1). Deterministic: the same files on any machine.
# The evaluation sets still regenerate from HEAD; nz_train and nz_dev are v1
# only at commit 5f1b73f (HEAD's generator writes v2 training data).
# Usage: scripts/make_data_v1.sh [path-to-tumataiti-ml]
set -euo pipefail
cd "$(dirname "$0")/.."
CLI="${1:-tumataiti-ml}"
V=data/v1
"$CLI" generate --split train      --n 8000 --seed 1 --out $V/nz_train.jsonl
"$CLI" generate --split dev        --n 800  --seed 2 --out $V/nz_dev.jsonl
"$CLI" generate --split test_names --n 1600 --seed 3 --out $V/nz_test_names.jsonl
"$CLI" generate --split test_full  --n 1750 --seed 4 --out $V/nz_test_full.jsonl
for pair in "Māori:maori" "Pākehā:pakeha" "Pasifika:pasifika" "Asian NZ:asian_nz"; do
  "$CLI" generate --split test_full --group "${pair%%:*}" --n 1400 --seed 5 --out "$V/nz_cf_${pair##*:}.jsonl"
done
"$CLI" prepare-pii300k --split train      --out $V/pii300k_en_train.jsonl
"$CLI" prepare-pii300k --split validation --out $V/pii300k_en_val.jsonl

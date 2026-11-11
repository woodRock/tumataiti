#!/usr/bin/env bash
# Data v4 (SPEC §9.1): v2 plus pepeha and the other places affiliation appears,
# with every affiliation (maunga, awa, moana, waka, iwi, hapū, marae, wharenui,
# tupuna) split into training and held-out lists like the names. From v4 the
# NZ evaluation sets are data/v4 too, because affiliation is scored: test_names
# and test_full add held-out pepeha templates and affiliations, and the name
# audit regenerates test_full per community. The false-alarm set is the v1 one
# (same split and seed, so the file is identical). Also builds the v4 ablation
# training data: v4kin (+ kinship templates) and v4ids (+ ID look-alikes).
# The v1-v3 files are unchanged; v2-era results are reproducible from commit 3437c11.
# Usage: scripts/make_data_v4.sh [path-to-tumataiti-ml]
set -euo pipefail
cd "$(dirname "$0")/.."
CLI="${1:-tumataiti-ml}"
V=data/v4
[ -f data/v1/pii300k_en_val.jsonl ] || ./scripts/make_data_v1.sh "$CLI"
"$CLI" generate --split train_v4      --n 8000 --seed 1 --out $V/nz_train.jsonl
"$CLI" generate --split dev_v4        --n 800  --seed 2 --out $V/nz_dev.jsonl
"$CLI" generate --split test_names_v4 --n 2300 --seed 3 --out $V/nz_test_names.jsonl  # 100 per template
"$CLI" generate --split test_full_v4  --n 2750 --seed 4 --out $V/nz_test_full.jsonl   # 250 per template
for pair in "Māori:maori" "Pākehā:pakeha" "Pasifika:pasifika" "Asian NZ:asian_nz"; do
  "$CLI" generate --split test_full_v4 --group "${pair%%:*}" --n 2200 --seed 5 --out "$V/nz_cf_${pair##*:}.jsonl"
done
"$CLI" generate --split test_false_alarm --n 600 --seed 6 --out $V/nz_test_false_alarm.jsonl
for a in kin ids; do
  "$CLI" generate --split train_v4$a --n 8000 --seed 1 --out data/v4$a/nz_train.jsonl
  "$CLI" generate --split dev_v4$a   --n 800  --seed 2 --out data/v4$a/nz_dev.jsonl
done

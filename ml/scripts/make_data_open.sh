#!/usr/bin/env bash
# Openly licensed English PII data (datasets/open_pii.py), replacing
# PII-Masking-300k for models that will be published. Deterministic.
#   train: 20,000 Nemotron-PII + 10,000 Gretel-en documents (PII-300k had 29,908)
#   test:  1,000 + 1,000 from their test/validation splits, an English set
#          that none of the students trained on
# Gretel's finance set is left out: its post-hoc labels miss addresses and
# account numbers, and unlabelled PII would train the model to skip it.
# Usage: scripts/make_data_open.sh [path-to-tumataiti-ml]
set -euo pipefail
cd "$(dirname "$0")/.."
CLI="${1:-tumataiti-ml}"
O=data/open
"$CLI" prepare-open --source nemotron  --split train --n 20000 --seed 1 --out $O/nemotron_train.jsonl
"$CLI" prepare-open --source gretel-en --split train --n 10000 --seed 1 --out $O/gretel_en_train.jsonl
"$CLI" prepare-open --source nemotron  --split test  --n 1000  --seed 2 --out $O/nemotron_test.jsonl
"$CLI" prepare-open --source gretel-en --split test  --n 1000  --seed 2 --out $O/gretel_en_test.jsonl
cat $O/nemotron_train.jsonl $O/gretel_en_train.jsonl > $O/open_en_train.jsonl
cat $O/nemotron_test.jsonl $O/gretel_en_test.jsonl > $O/open_en_test.jsonl
wc -l $O/open_en_train.jsonl $O/open_en_test.jsonl

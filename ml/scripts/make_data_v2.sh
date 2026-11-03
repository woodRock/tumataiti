#!/usr/bin/env bash
# Build the v2 training data (SPEC §9.1): balanced community names and the v2
# templates. Evaluation sets are unchanged, so v2 runs score against data/v1.
# Usage: scripts/make_data_v2.sh [path-to-tumataiti-ml]
set -euo pipefail
cd "$(dirname "$0")/.."
CLI="${1:-tumataiti-ml}"
V=data/v2
[ -f data/v1/pii300k_en_val.jsonl ] || ./scripts/make_data_v1.sh "$CLI"
"$CLI" generate --split train --n 8000 --seed 1 --out $V/nz_train.jsonl
"$CLI" generate --split dev   --n 800  --seed 2 --out $V/nz_dev.jsonl

#!/usr/bin/env bash
# Train one student backbone and predict on every M3 evaluation set.
#
#   task submit -t "RTX A5000" -n m3-deberta-small -- ./scripts/ecs_student.sh microsoft/deberta-v3-small deberta-v3-small --lr 5e-5
#   task fetch runs/m3/deberta-v3-small
#
# Extra arguments after NAME go to `tumataiti-ml train` (e.g. --max-steps 30 for a smoke test).
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/ecs_env.sh
BACKBONE=$1 NAME=$2
shift 2
OUT=runs/m3/$NAME
V=data/v1

[ -f $V/pii300k_en_val.jsonl ] || ./scripts/make_data_v1.sh "$CLI"
"$CLI" train --backbone "$BACKBONE" --train $V/nz_train.jsonl $V/pii300k_en_train.jsonl --dev $V/nz_dev.jsonl --out "$OUT" "$@"

LIMIT=()
[[ " $* " == *" --max-steps "* ]] && LIMIT=(--limit 50)
for ds in nz_test_names nz_test_full nz_cf_maori nz_cf_pakeha nz_cf_pasifika nz_cf_asian_nz pii300k_en_val; do
  "$CLI" predict --detector student --model "$OUT/model" --device cuda "${LIMIT[@]}" \
    --gold "$V/$ds.jsonl" --out "$OUT/pred/$ds.jsonl" > /dev/null
done
echo "done: $OUT"

#!/usr/bin/env bash
# Train one student backbone and predict on every M3 evaluation set.
#
#   task submit -t "RTX A5000" -n m3-deberta-small -- ./scripts/ecs_student.sh microsoft/deberta-v3-small deberta-v3-small --lr 5e-5
#   task fetch runs/m3/deberta-v3-small
#
# Extra arguments after NAME go to `tumataiti-ml train` (e.g. --max-steps 30 for a smoke test).
# PREDICT_ONLY=1 skips training and re-predicts with the existing model (e.g. after a decoder change).
# DATA=v2, v3 or v4 trains on data/DATA and writes runs/m3-DATA/NAME. The NZ evaluation
# sets are data/v4 (affiliation is scored from v4; v2-era runs used data/v1, commit 3437c11);
# PII-Masking-300k validation is data/v1.
# EXTRA picks the English data trained alongside the NZ set: open (default:
# Nemotron-PII + Gretel, scripts/make_data_open.sh), none, or pii300k. pii300k
# only reproduces the M3 v1/v2 results: PII-Masking-300k's licence forbids
# distributing derivative works such as trained weights (SPEC §9.1).
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/ecs_env.sh
BACKBONE=$1 NAME=$2
shift 2
DATA=${DATA:-v1}
V=data/v1
E=data/v4
T=data/$DATA
OUT=runs/m3$([ "$DATA" = v1 ] || echo "-$DATA")/$NAME

[ -f $V/pii300k_en_val.jsonl ] || ./scripts/make_data_v1.sh "$CLI"
( flock 9; [ -f $E/nz_test_false_alarm.jsonl ] || ./scripts/make_data_v4.sh "$CLI" ) 9>"$STORE/venvs/.tumataiti-data.lock"
# Jobs submitted together would race to write the same files.
( flock 9; [ -f $T/nz_dev.jsonl ] || "./scripts/make_data_$DATA.sh" "$CLI" ) 9>"$STORE/venvs/.tumataiti-data.lock"
TRAIN=($T/nz_train.jsonl)
case "${EXTRA:-open}" in
  pii300k) TRAIN+=($V/pii300k_en_train.jsonl) ;;
  open)
    ( flock 9; [ -f data/open/open_en_train.jsonl ] || ./scripts/make_data_open.sh "$CLI" ) 9>"$STORE/venvs/.tumataiti-data.lock"
    TRAIN+=(data/open/open_en_train.jsonl) ;;
  none) ;;
  *) echo "EXTRA must be pii300k, open or none" >&2; exit 2 ;;
esac
[ -n "${PREDICT_ONLY:-}" ] || "$CLI" train --backbone "$BACKBONE" --train "${TRAIN[@]}" --dev $T/nz_dev.jsonl --out "$OUT" "$@"

LIMIT=()
[[ " $* " == *" --max-steps "* ]] && LIMIT=(--limit 50)
for ds in nz_test_names nz_test_full nz_cf_maori nz_cf_pakeha nz_cf_pasifika nz_cf_asian_nz nz_test_false_alarm pii300k_en_val open_en_test; do
  gold=$E/$ds.jsonl
  [ "$ds" = pii300k_en_val ] && gold=$V/$ds.jsonl
  [ "$ds" = open_en_test ] && gold=data/open/$ds.jsonl
  [ -f "$gold" ] || continue
  "$CLI" predict --detector student --model "$OUT/model" --device cuda "${LIMIT[@]}" \
    --gold "$gold" --out "$OUT/pred/$ds.jsonl" > /dev/null
done
# Typing variants of the v4 sets (robustness.py builds them in data/robust-v4), when
# built; score_lower.py uses these for the students trained with lowercased text.
for v in nomacron lower; do
  for gold in data/robust-v4/$v/*.jsonl; do
    [ -f "$gold" ] || continue
    "$CLI" predict --detector student --model "$OUT/model" --device cuda "${LIMIT[@]}" \
      --gold "$gold" --out "$OUT/pred/robust/$v/$(basename "$gold")" > /dev/null
  done
done
echo "done: $OUT"

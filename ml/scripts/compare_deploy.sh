#!/usr/bin/env bash
# Before shipping a new student to the demo: compare it with the shipped one,
# both int4 ONNX on this machine's CPU, alone and merged with the rules (what
# the demo runs), on every evaluation set. Not a paper result; a deploy check.
#   taura run -- ml/scripts/compare_deploy.sh OLD.onnx NEW.onnx [OUT]
# The model directories need tokenizer.json and config.json beside the .onnx.
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$PWD/.venv/bin:$PATH"
OLD=$1 NEW=$2 OUT=${3:-runs/deploy-check}
gold_of() {
  case $1 in
    pii300k_en_val) echo data/v1/$1.jsonl ;;
    open_en_test) echo data/open/$1.jsonl ;;
    *) echo data/v4/$1.jsonl ;;
  esac
}
SETS="nz_test_full nz_test_names nz_cf_maori nz_cf_pakeha nz_cf_pasifika nz_cf_asian_nz nz_test_false_alarm pii300k_en_val open_en_test"
mkdir -p "$OUT/results"
for ds in $SETS; do
  G=$(gold_of $ds)
  [ -f "$OUT/rules/$ds.jsonl" ] || tumataiti-ml predict --detector rules --gold "$G" --out "$OUT/rules/$ds.jsonl" > /dev/null
  for m in old:$OLD new:$NEW; do
    name=${m%%:*} model=${m#*:}
    [ -f "$OUT/$name/$ds.jsonl" ] ||
      tumataiti-ml predict --detector student-onnx --model "$model" --gold "$G" --out "$OUT/$name/$ds.jsonl" > /dev/null
    tumataiti-ml combine --primary "$OUT/rules/$ds.jsonl" --secondary "$OUT/$name/$ds.jsonl" \
      --out "$OUT/rules+$name/$ds.jsonl" > /dev/null
  done
  if [ $ds = nz_test_false_alarm ]; then
    tumataiti-ml false-alarms --gold "$G" --pred "$OUT"/{old,new,rules+old,rules+new}/$ds.jsonl \
      --json "$OUT/results/$ds.json" --markdown "$OUT/results/$ds.md" > /dev/null
  else
    tumataiti-ml score --gold "$G" --pred "$OUT"/{old,new,rules+old,rules+new}/$ds.jsonl --title "$ds" \
      --json "$OUT/results/$ds.json" --markdown "$OUT/results/$ds.md" > /dev/null
  fi
  echo "scored $ds"
done
echo "old: $OLD" > "$OUT/results/models.txt"
echo "new: $NEW" >> "$OUT/results/models.txt"

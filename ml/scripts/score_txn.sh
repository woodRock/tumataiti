#!/usr/bin/env bash
# The review layer without and with transaction labels (relabelling model
# identifiers that fail every NZ checksum), for the fp32 DeBERTa-v3-small open
# student merged with the rules. Was an inline command in the v2 era.
#   taura run -- bash ml/scripts/score_txn.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$PWD/.venv/bin:$PATH"
R=${RUNS:-runs/m3-v4}
M=${MODEL:-deberta-v3-small-open}
for ds in nz_test_full open_en_test pii300k_en_val nz_test_false_alarm; do
  G=data/v4/$ds.jsonl
  [ $ds = open_en_test ] && G=data/open/$ds.jsonl
  [ $ds = pii300k_en_val ] && G=data/v1/$ds.jsonl
  [ -f "$R/$M/$ds.jsonl" ] || cp "$R/$M/pred/$ds.jsonl" "$R/$M/pred/$ds.meta.json" "$R/$M/"
  tumataiti-ml review --gold "$G" --pred "$R/$M/$ds.jsonl" --out "$R/$M+review/$ds.jsonl" > /dev/null
  tumataiti-ml review --transaction-labels --gold "$G" --pred "$R/$M/$ds.jsonl" --out "$R/$M+review+txn/$ds.jsonl" > /dev/null
  for v in "$M+review" "$M+review+txn"; do
    tumataiti-ml combine --primary "$R/rules/$ds.jsonl" --secondary "$R/$v/$ds.jsonl" --out "$R/rules+$v/$ds.jsonl" > /dev/null
  done
  tumataiti-ml score --gold "$G" --pred "$R/rules+$M+review/$ds.jsonl" "$R/rules+$M+review+txn/$ds.jsonl" \
    --title "$ds: review layer without and with transaction labels" \
    --markdown "results/txn_$ds.md" --json "results/txn_$ds.json" > /dev/null
done
tumataiti-ml false-alarms --gold data/v4/nz_test_false_alarm.jsonl \
  --pred "$R/rules+$M+review/nz_test_false_alarm.jsonl" "$R/rules+$M+review+txn/nz_test_false_alarm.jsonl" \
  --markdown results/txn_false_alarms.md --json results/txn_false_alarms.json > /dev/null
echo "wrote results/txn_*"

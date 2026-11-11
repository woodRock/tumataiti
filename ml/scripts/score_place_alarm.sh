#!/usr/bin/env bash
# False alarms on place names outside a pepeha (synth/place_alarm.py): the
# shipped int4 students of data v2 and v4, alone and with the rules, on this
# machine's CPU. Not yet a paper result.
#   taura run -- ml/scripts/score_place_alarm.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$PWD/.venv/bin:$PATH"
G=data/v4/nz_test_place_alarm.jsonl
O=runs/place-alarm
[ -f $G ] || python -m tumataiti_ml.synth.place_alarm --n 1000 --seed 7 --out $G
tumataiti-ml predict --detector rules --gold $G --out $O/rules/nz_test_place_alarm.jsonl > /dev/null
for v in v2 v4; do
  tumataiti-ml predict --detector student-onnx --gold $G --out $O/$v/nz_test_place_alarm.jsonl \
    --model runs/m3-$v/deberta-v3-small-open/onnx/model_int8_int4-block.onnx > /dev/null
  tumataiti-ml combine --primary $O/rules/nz_test_place_alarm.jsonl --secondary $O/$v/nz_test_place_alarm.jsonl \
    --out $O/rules+$v/nz_test_place_alarm.jsonl > /dev/null
done
mkdir -p $O/results
tumataiti-ml false-alarms --gold $G --pred $O/{rules,v2,v4,rules+v2,rules+v4}/nz_test_place_alarm.jsonl \
  --json $O/results/place_alarm.json --markdown $O/results/place_alarm.md > /dev/null
cat $O/results/place_alarm.md

#!/usr/bin/env bash
# Score false alarms (SPEC §9.8) for each model on data/v4/nz_test_false_alarm.jsonl (the v1 file, regenerated):
# the model alone, after the review layer (`tumataiti-ml review`), and each
# merged with the rules. Model predictions must exist (ecs_student.sh or local_int8.sh).
#   RUNS=runs/m3-v4 TAG=fa MODELS="deberta-v3-small-open-int8-int4-block" uv run ./scripts/score_false_alarms.sh
set -euo pipefail
cd "$(dirname "$0")/.."
R=${RUNS:-runs/m3-v4}
TAG=${TAG:-fa}
DS=nz_test_false_alarm
GOLD=data/v4/$DS.jsonl
[ -f "$GOLD" ] || tumataiti-ml generate --split test_false_alarm --n 600 --seed 6 --out "$GOLD"
[ -f "$R/rules/$DS.jsonl" ] || tumataiti-ml predict --detector rules --gold "$GOLD" --out "$R/rules/$DS.jsonl" > /dev/null
preds=("$R/rules/$DS.jsonl")
for m in $MODELS; do
  [ -f "$R/$m/pred/$DS.jsonl" ] && cp "$R/$m/pred/$DS.jsonl" "$R/$m/pred/$DS.meta.json" "$R/$m/" 2>/dev/null || true
  tumataiti-ml review --gold "$GOLD" --pred "$R/$m/$DS.jsonl" --out "$R/$m+review/$DS.jsonl" > /dev/null
  for v in "$m" "$m+review"; do
    tumataiti-ml combine --primary "$R/rules/$DS.jsonl" --secondary "$R/$v/$DS.jsonl" --out "$R/rules+$v/$DS.jsonl" > /dev/null
  done
  preds+=("$R/$m/$DS.jsonl" "$R/$m+review/$DS.jsonl" "$R/rules+$m/$DS.jsonl" "$R/rules+$m+review/$DS.jsonl")
done
tumataiti-ml false-alarms --gold "$GOLD" --pred "${preds[@]}" --title "False-alarm set (600 documents)" \
  --markdown "results/${TAG}_false_alarms.md" --json "results/${TAG}_false_alarms.json" > /dev/null
tumataiti-ml score --gold "$GOLD" --pred "${preds[@]}" --title "False-alarm set (600 documents)" \
  --markdown "results/${TAG}_$DS.md" --json "results/${TAG}_$DS.json" > /dev/null
echo "wrote results/${TAG}_*"

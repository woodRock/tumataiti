#!/usr/bin/env bash
# GPU timings for the paper, all from one GPU: re-predict test_full with the
# teacher and the three fp32 open students, one after another, in one job, so
# every GPU time in the main table comes from the same card. Training and the
# other predictions may run on any GPU (ecs_student.sh, ecs_teacher.sh); this
# overwrites their test_full predictions, so the leak rates and times in the
# main table come from this run. Run after the three students have trained:
#   task submit -C ml -n v4-timing -- ./scripts/ecs_time.sh
#   task fetch ml/runs/m3-v4/timing_gpu.txt ml/runs/m3-v4/openai-privacy-filter ...
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/ecs_env.sh
R=runs/m3-v4
GOLD=data/v4/nz_test_full.jsonl
STUDENTS="deberta-v3-small-open modernbert-base-open mdeberta-v3-base-open"
for m in $STUDENTS; do
  [ -f "$R/$m/model/config.json" ] || { echo "$R/$m/model is missing: train it first" >&2; exit 1; }
done
nvidia-smi --query-gpu=name --format=csv,noheader -i "${CUDA_VISIBLE_DEVICES:-0}" | head -1 > $R/timing_gpu.txt
echo "timing on: $(cat $R/timing_gpu.txt)"
"$CLI" predict --detector openai-privacy-filter --device cuda --gold $GOLD \
  --out $R/openai-privacy-filter/nz_test_full.jsonl > /dev/null
for m in $STUDENTS; do
  "$CLI" predict --detector student --model "$R/$m/model" --device cuda --gold $GOLD \
    --out "$R/$m/pred/nz_test_full.jsonl" > /dev/null
done
echo "done"

#!/usr/bin/env bash
# Quantise a student with each encoder option (embeddings always int8) and
# predict test_full on this machine's CPU:
#   taura run -- ml/scripts/int8_variants.sh runs/m3-v2 mdeberta-v3-base [encoder ...]
set -euo pipefail
cd "$(dirname "$0")/.."
R=$1 NAME=$2
shift 2
D=$R/$NAME/onnx
for enc in "${@:-fp16 int8-block int4-block}"; do
  for e in $enc; do
    uv run tumataiti-ml quantise --onnx "$D/model.onnx" --encoder "$e"
    uv run tumataiti-ml predict --detector student-onnx --model "$D/model_int8_$e.onnx" \
      --gold data/v1/nz_test_full.jsonl --out "$R/$NAME-int8-$e/nz_test_full.jsonl" > /dev/null
  done
done

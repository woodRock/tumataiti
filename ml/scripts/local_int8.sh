#!/usr/bin/env bash
# Quantise an exported student to int8 and predict every M3 evaluation set on
# this machine's CPU (the latency target). Run under taura so it gets a record:
#   taura run -- ml/scripts/local_int8.sh runs/m3-v4 deberta-v3-small-open [ENCODER]
# ENCODER is a `tumataiti-ml quantise --encoder` option (default dynamic).
set -euo pipefail
cd "$(dirname "$0")/.."
R=$1 NAME=$2 ENC=${3:-dynamic}
V=data/v4  # NZ sets; PII-Masking-300k is data/v1
uv run tumataiti-ml quantise --onnx "$R/$NAME/onnx/model.onnx" --encoder "$ENC"
if [ "$ENC" = dynamic ]; then MODEL=model_int8.onnx OUT=$NAME-int8; else MODEL=model_int8_$ENC.onnx OUT=$NAME-int8-$ENC; fi
for ds in nz_test_names nz_test_full nz_cf_maori nz_cf_pakeha nz_cf_pasifika nz_cf_asian_nz nz_test_false_alarm pii300k_en_val open_en_test; do
  gold=$V/$ds.jsonl
  [ "$ds" = pii300k_en_val ] && gold=data/v1/$ds.jsonl
  [ "$ds" = open_en_test ] && gold=data/open/$ds.jsonl
  uv run tumataiti-ml predict --detector student-onnx --model "$R/$NAME/onnx/$MODEL" \
    --gold "$gold" --out "$R/$OUT/$ds.jsonl" > /dev/null
done
echo "done: $R/$OUT"

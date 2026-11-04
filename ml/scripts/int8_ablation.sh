#!/usr/bin/env bash
# Which quantised ops break a student? Quantise only the embedding lookup
# (Gather) or only the matrix multiplies (MatMul, Gemm), then predict test_full.
#   taura run -- ml/scripts/int8_ablation.sh runs/m3-v2 mdeberta-v3-base
set -euo pipefail
cd "$(dirname "$0")/.."
R=$1 NAME=$2
D=$R/$NAME/onnx
for variant in gather matmul; do
  ops=$([ $variant = gather ] && echo '["Gather"]' || echo '["MatMul", "Gemm"]')
  uv run python -c "
from onnxruntime.quantization import QuantType, quantize_dynamic
quantize_dynamic('$D/model.onnx', '$D/model_int8_$variant.onnx', weight_type=QuantType.QInt8,
                 op_types_to_quantize=$ops, per_channel=True)"
  ls -l "$D/model_int8_$variant.onnx"
  uv run tumataiti-ml predict --detector student-onnx --model "$D/model_int8_$variant.onnx" \
    --gold data/v1/nz_test_full.jsonl --out "$R/$NAME-int8-$variant/nz_test_full.jsonl" > /dev/null
done

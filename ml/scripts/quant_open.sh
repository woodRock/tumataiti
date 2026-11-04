#!/usr/bin/env bash
# Quantisation comparison for the published (open-data) students, so the paper's
# quantisation results describe models trained only on openly licensed data.
# For each student: dynamic int8, and int8 embeddings with an fp16 encoder
# (the int4 encoder already exists: m3open_int4_*). For mDeBERTa-v3-base: int8
# on the embedding Gather only and on MatMul/Gemm only. Each predicts test_full
# on this machine's CPU; everything is merged with the rules and scored. Run
# from the repo root:
#   taura run -- bash ml/scripts/quant_open.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$PWD/.venv/bin:$PATH"
R=runs/m3-v2
ds=nz_test_full
GOLD=data/v1/$ds.jsonl
STUDENTS="deberta-v3-small-open modernbert-base-open mdeberta-v3-base-open"

predict() {  # model file, output run name
  tumataiti-ml predict --detector student-onnx --model "$1" --gold "$GOLD" --out "$R/$2/$ds.jsonl" > /dev/null
}

for m in $STUDENTS; do
  D=$R/$m/onnx
  tumataiti-ml quantise --onnx "$D/model.onnx" --encoder dynamic
  predict "$D/model_int8.onnx" "$m-int8"
  tumataiti-ml quantise --onnx "$D/model.onnx" --encoder fp16
  predict "$D/model_int8_fp16.onnx" "$m-int8-fp16"
done

# Which quantised ops break mDeBERTa (as int8_ablation.sh, for the open student).
m=mdeberta-v3-base-open
D=$R/$m/onnx
for variant in gather matmul; do
  ops=$([ $variant = gather ] && echo '["Gather"]' || echo '["MatMul", "Gemm"]')
  python -c "
from onnxruntime.quantization import QuantType, quantize_dynamic
quantize_dynamic('$D/model.onnx', '$D/model_int8_$variant.onnx', weight_type=QuantType.QInt8,
                 op_types_to_quantize=$ops, per_channel=True)"
  predict "$D/model_int8_$variant.onnx" "$m-int8-$variant"
done

MODELS=""
for m in $STUDENTS; do MODELS="$MODELS $m $m-int8 $m-int8-fp16 $m-int8-int4-block"; done
MODELS="$MODELS mdeberta-v3-base-open-int8-gather mdeberta-v3-base-open-int8-matmul"
preds=()
for m in $MODELS; do
  tumataiti-ml combine --primary "$R/rules/$ds.jsonl" --secondary "$R/$m/$ds.jsonl" --out "$R/rules+$m/$ds.jsonl" > /dev/null
  preds+=("$R/rules+$m/$ds.jsonl")
done
tumataiti-ml score --gold "$GOLD" --pred "${preds[@]}" \
  --title "Open-data students, quantised: held-out templates and names (fp32 on GPU, others on laptop CPU)" \
  --markdown results/m3open_quant_$ds.md --json results/m3open_quant_$ds.json > /dev/null
echo "wrote results/m3open_quant_$ds.*"

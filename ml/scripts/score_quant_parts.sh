#!/usr/bin/env bash
# Score the mDeBERTa (data v2) quantisation ablation on the held-out NZ set:
# dynamic int8 on the embedding Gather only, on MatMul and Gemm only, and on
# both, each alone and merged with the rules (SPEC §9.6, finding 7). Run from ml/:
#   uv run ./scripts/score_quant_parts.sh
set -euo pipefail
cd "$(dirname "$0")/.."
R=runs/m3-v2
ds=nz_test_full
MODELS="mdeberta-v3-base mdeberta-v3-base-int8-gather mdeberta-v3-base-int8-matmul mdeberta-v3-base-int8"
preds=()
for m in $MODELS; do
  tumataiti-ml combine --primary "$R/rules/$ds.jsonl" --secondary "$R/$m/$ds.jsonl" --out "$R/rules+$m/$ds.jsonl" > /dev/null
  preds+=("$R/rules+$m/$ds.jsonl")
done
tumataiti-ml score --gold data/v1/$ds.jsonl --pred "${preds[@]}" \
  --title "mDeBERTa-v3-base (data v2), which ops are quantised: held-out templates and names" \
  --markdown results/m3v2_quantparts_$ds.md --json results/m3v2_quantparts_$ds.json > /dev/null
echo "wrote results/m3v2_quantparts_$ds.*"

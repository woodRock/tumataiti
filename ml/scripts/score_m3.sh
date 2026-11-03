#!/usr/bin/env bash
# Score every M3 detector, alone and merged with the rules, on every evaluation
# set. Run from ml/ after fetching runs/m3/<detector>/ from ECS:
#   uv run ./scripts/score_m3.sh
set -euo pipefail
cd "$(dirname "$0")/.."
V=data/v1
R=runs/m3
OUT=results
SETS="nz_test_names nz_test_full nz_cf_maori nz_cf_pakeha nz_cf_pasifika nz_cf_asian_nz pii300k_en_val"
MODELS="${MODELS:-openai-privacy-filter deberta-v3-small deberta-v3-small-int8 modernbert-base mdeberta-v3-base}"

# Flatten student predictions (runs/m3/<name>/pred/) next to the others.
for m in $MODELS; do
  [ -d "$R/$m/pred" ] && cp "$R/$m/pred/"* "$R/$m/"
done
# The teacher's PII-Masking-300k predictions carry over from M1 (same data and model).
cp -n runs/openai-privacy-filter/pii300k_en_val.jsonl runs/openai-privacy-filter/pii300k_en_val.meta.json "$R/openai-privacy-filter/" 2>/dev/null || true

for m in $MODELS; do
  for ds in $SETS; do
    tumataiti-ml combine --primary "$R/rules/$ds.jsonl" --secondary "$R/$m/$ds.jsonl" --out "$R/rules+$m/$ds.jsonl" > /dev/null
  done
done

score() {  # dataset, title
  local preds=("$R/rules/$1.jsonl")
  for m in $MODELS; do preds+=("$R/$m/$1.jsonl"); done
  for m in $MODELS; do preds+=("$R/rules+$m/$1.jsonl"); done
  tumataiti-ml score --gold "$V/$1.jsonl" --pred "${preds[@]}" --title "$2" \
    --markdown "$OUT/m3_$1.md" --json "$OUT/m3_$1.json" > /dev/null
}
score nz_test_full "NZ synthetic v1, held-out templates and names (1,750 documents)"
score nz_test_names "NZ synthetic v1, training templates with held-out names (1,600 documents)"
score pii300k_en_val "PII-Masking-300k, English validation (7,946 documents)"

runs=()
for m in $MODELS; do runs+=("$R/$m"); done
for m in $MODELS; do runs+=("$R/rules+$m"); done
tumataiti-ml counterfactual --data "$V" --runs "${runs[@]}" --markdown "$OUT/m3_names_counterfactual.md" --json "$OUT/m3_names_counterfactual.json" > /dev/null
echo "wrote $OUT/m3_*.md"

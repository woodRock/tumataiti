#!/usr/bin/env bash
# Score every detector, alone and merged with the rules, on every evaluation
# set. Run from ml/ after fetching the students' and teacher's predictions:
#   RUNS=runs/m3-v4 TAG=m3open MODELS="openai-privacy-filter deberta-v3-small-open ..." uv run ./scripts/score_m3.sh
# The NZ sets are data/v4 (affiliation is scored from v4); v2-era results
# (data/v1, runs/m3-v2) are reproducible from commit 3437c11.
set -euo pipefail
cd "$(dirname "$0")/.."
V=data/v4
R=${RUNS:-runs/m3-v4}
TAG=${TAG:-m3}
OUT=results
SETS="nz_test_names nz_test_full nz_cf_maori nz_cf_pakeha nz_cf_pasifika nz_cf_asian_nz pii300k_en_val"
MODELS="${MODELS:-openai-privacy-filter deberta-v3-small-open modernbert-base-open mdeberta-v3-base-open}"

gold_of() {
  case $1 in
    pii300k_en_val) echo data/v1/$1.jsonl ;;
    open_en_test) echo data/open/$1.jsonl ;;
    *) echo $V/$1.jsonl ;;
  esac
}

# Rules predictions, made here when missing (CPU, seconds).
for ds in $SETS nz_test_false_alarm open_en_test; do
  [ -f "$R/rules/$ds.jsonl" ] || tumataiti-ml predict --detector rules --gold "$(gold_of $ds)" --out "$R/rules/$ds.jsonl" > /dev/null
done
# Flatten student predictions (runs/.../<name>/pred/) next to the others.
for m in $MODELS; do
  [ -d "$R/$m/pred" ] && cp "$R/$m/pred/"* "$R/$m/" 2>/dev/null || true
done
# The English sets did not change, so the teacher's predictions on them carry
# over (PII-Masking-300k from M1, the open set from the v2-era run).
if [[ " $MODELS " == *" openai-privacy-filter "* ]]; then
  cp -n runs/openai-privacy-filter/pii300k_en_val.jsonl runs/openai-privacy-filter/pii300k_en_val.meta.json "$R/openai-privacy-filter/" 2>/dev/null || true
  cp -n runs/m3/openai-privacy-filter/open_en_test.jsonl runs/m3/openai-privacy-filter/open_en_test.meta.json "$R/openai-privacy-filter/" 2>/dev/null || true
fi

# The open English test set (scripts/make_data_open.sh) is scored only when the
# rules and every model have predictions on it.
OPEN=1
for m in rules $MODELS; do [ -f "$R/$m/open_en_test.jsonl" ] || OPEN=; done
[ -n "$OPEN" ] && SETS="$SETS open_en_test"

for m in $MODELS; do
  for ds in $SETS; do
    tumataiti-ml combine --primary "$R/rules/$ds.jsonl" --secondary "$R/$m/$ds.jsonl" --out "$R/rules+$m/$ds.jsonl" > /dev/null
  done
done

score() {  # dataset, title
  local gold; gold=$(gold_of "$1")
  local preds=("$R/rules/$1.jsonl")
  for m in $MODELS; do preds+=("$R/$m/$1.jsonl"); done
  for m in $MODELS; do preds+=("$R/rules+$m/$1.jsonl"); done
  tumataiti-ml score --gold "$gold" --pred "${preds[@]}" --title "$2" \
    --markdown "$OUT/${TAG}_$1.md" --json "$OUT/${TAG}_$1.json" > /dev/null
}
score nz_test_full "NZ synthetic v4, held-out templates, names and affiliations"
score nz_test_names "NZ synthetic v4, training templates with held-out names and affiliations"
score pii300k_en_val "PII-Masking-300k, English validation"
[ -n "$OPEN" ] && score open_en_test "Open English PII test set: Nemotron-PII + Gretel-en"

runs=()
for m in $MODELS; do runs+=("$R/$m"); done
for m in $MODELS; do runs+=("$R/rules+$m"); done
tumataiti-ml counterfactual --data "$V" --runs "${runs[@]}" --markdown "$OUT/${TAG}_names_counterfactual.md" --json "$OUT/${TAG}_names_counterfactual.json" > /dev/null
echo "wrote $OUT/${TAG}_*.md"

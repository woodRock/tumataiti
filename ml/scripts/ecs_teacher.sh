#!/usr/bin/env bash
# Run the openai/privacy-filter teacher over evaluation sets on one ECS GPU.
#
#   task submit -t "RTX A5000" -n teacher-eval -- ./scripts/ecs_teacher.sh
#   task fetch runs/m3/openai-privacy-filter
#
# SETS=open_en_test runs only the open English test set (data/open/).
#
# M1's runs (nz_synth_v0) came from commit b9d1dd8; the generator has changed since.
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/ecs_env.sh

V=data/v1
[ -f $V/pii300k_en_val.jsonl ] || ./scripts/make_data_v1.sh "$CLI"
# PII-Masking-300k validation predictions carry over from M1 (same data, same model).
for ds in ${SETS:-nz_test_names nz_test_full nz_cf_maori nz_cf_pakeha nz_cf_pasifika nz_cf_asian_nz}; do
  gold=$V/$ds.jsonl
  [ "$ds" = open_en_test ] && gold=data/open/open_en_test.jsonl
  "$CLI" predict --detector openai-privacy-filter --device cuda \
    --gold "$gold" --out "runs/m3/openai-privacy-filter/$ds.jsonl"
done

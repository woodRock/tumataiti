#!/usr/bin/env bash
# The false-alarm ablation (SPEC §9.8) on data v4: DeBERTa-v3-small trained on
# v4 (3 epochs, 1 epoch, 1 epoch with seed 1), v4kin (v4 + kinship templates,
# 1 epoch, two seeds) and v4ids (v4kin + ID look-alikes), gathered in
# runs/m3-v4fa and scored on every set, on false alarms and per kinship word.
# Needs the students' predictions fetched from ECS (ecs_student.sh) and the
# rules and teacher in runs/m3-v4 (score_m3.sh).
#   taura run -- bash ml/scripts/score_fa.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$PWD/.venv/bin:$PATH"
R=runs/m3-v4fa
mkdir -p $R
link() { [ -e "$R/$1" ] || ln -s "../$2" "$R/$1"; }
link rules m3-v4/rules
link openai-privacy-filter m3-v4/openai-privacy-filter
link deberta-small-open-v4 m3-v4/deberta-v3-small-open
link deberta-small-open-v4-1ep m3-v4/deberta-v3-small-open-1ep
link deberta-small-open-v4-1ep-s1 m3-v4/deberta-v3-small-open-1ep-s1
link deberta-small-open-v4kin m3-v4kin/deberta-v3-small-open
link deberta-small-open-v4kin-s1 m3-v4kin/deberta-v3-small-open-s1
link deberta-small-open-v4ids m3-v4ids/deberta-v3-small-open
M="deberta-small-open-v4 deberta-small-open-v4-1ep deberta-small-open-v4-1ep-s1 deberta-small-open-v4kin deberta-small-open-v4kin-s1 deberta-small-open-v4ids"
RUNS=$R TAG=m3fa MODELS="$M" ./scripts/score_m3.sh
RUNS=$R TAG=m3fa MODELS="$M" ./scripts/score_false_alarms.sh
python scripts/score_kinship_words.py

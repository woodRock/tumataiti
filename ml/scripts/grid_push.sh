#!/usr/bin/env bash
# Copy what grid jobs read but `task sync` doesn't carry (ml/runs isn't in git)
# from this machine to the shared disk: the rules' and teacher's predictions and
# the deployed int4 models' predictions and files. Run from the repo root:
#   ml/scripts/grid_push.sh
set -euo pipefail
cd "$(dirname "$0")/.."
DEST=/vol/ecrg-solar/woodj4/tūmataiti/ml/
R=runs/m3-v4
paths=("$R/rules" "$R/rules+openai-privacy-filter" "$R/deberta-v3-small-open-int8-int4-block")
for m in deberta-v3-small modernbert-base mdeberta-v3-base; do
  paths+=("$R/rules+$m-open-int8-int4-block" "$R/$m-open/onnx/model_int8_int4-block.onnx")
done
rsync -aLR -e "ssh -J woodj4@entry.ecs.vuw.ac.nz" "${paths[@]}" "woodj4@barretts.ecs.vuw.ac.nz:$DEST"

#!/usr/bin/env bash
# Copy an exported, quantised student into the demo (not committed: see
# .gitignore). Usage: scripts/copy-model.sh <onnx dir> <model file> <precision>
#   scripts/copy-model.sh ml/runs/m3-v2/deberta-v3-small/onnx model_int8_int4-block.onnx "int8 embeddings, int4 encoder"
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=$1 MODEL=$2 PRECISION=$3
OUT=demo/public/models/student
mkdir -p $OUT
cp "$SRC/$MODEL" $OUT/model.onnx
cp "$SRC/tokenizer.json" "$SRC/config.json" $OUT/
NAME=$(basename "$(dirname "$(cd "$SRC" && pwd)")")
BYTES=$(cat $OUT/model.onnx $OUT/tokenizer.json $OUT/config.json | wc -c | tr -d ' ')
printf '{"name": "%s", "precision": "%s", "bytes": %s}\n' "$NAME" "$PRECISION" "$BYTES" > $OUT/manifest.json
cat $OUT/manifest.json

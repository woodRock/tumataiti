#!/usr/bin/env bash
# Copy an exported, quantised student into the demo (not committed: see
# .gitignore). Usage: scripts/copy-model.sh <onnx dir> <model file> <precision> [name]
# REPO=<owner/name> records the model's Hugging Face repo, for the attribution link.
#   scripts/copy-model.sh ml/runs/m3-v2/deberta-v3-small/onnx model_int8_int4-block.onnx "int8 embeddings, int4 encoder"
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=$1 MODEL=$2 PRECISION=$3
OUT=demo/public/models/student
mkdir -p $OUT
cp "$SRC/$MODEL" $OUT/model.onnx
cp "$SRC/tokenizer.json" "$SRC/config.json" $OUT/
NAME=${4:-$(basename "$(dirname "$(cd "$SRC" && pwd)")")}
BYTES=$(cat $OUT/model.onnx $OUT/tokenizer.json $OUT/config.json | wc -c | tr -d ' ')
# GitHub refuses files over 100 MB, so the site (docs/, served by GitHub Pages)
# holds the model in parts; the page downloads them and joins them in order.
rm -f $OUT/model.onnx.part-*
split -b 45m $OUT/model.onnx $OUT/model.onnx.part-
rm $OUT/model.onnx
PARTS=$(cd $OUT && ls model.onnx.part-* | sed 's/.*/"&"/' | paste -sd, -)
printf '{"name": "%s", "precision": "%s", "bytes": %s, "repo": %s, "parts": [%s]}\n' "$NAME" "$PRECISION" "$BYTES" \
  "$([ -n "${REPO:-}" ] && echo "\"$REPO\"" || echo null)" "$PARTS" > $OUT/manifest.json
cat $OUT/manifest.json

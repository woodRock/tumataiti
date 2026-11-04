#!/usr/bin/env bash
# Publish an open-data student to the Hugging Face Hub: the fp32 checkpoint,
# the int4 ONNX file and the model card (model_cards/NAME.md).
#   ml/scripts/hf_upload.sh deberta-v3-small-open woodrock/tumataiti-deberta-v3-small-open
# Only models trained without PII-Masking-300k may be published (SPEC §9.1).
# Prints the Hub commit; pin it in demo/model.lock (scripts/lock-model.sh).
set -euo pipefail
cd "$(dirname "$0")/.."
NAME=$1 REPO=$2
R=runs/m3-v2/$NAME
grep -q data/open/ "$R/config.json" && ! grep -q pii300k "$R/config.json" \
  || { echo "$R was not trained on the open data only" >&2; exit 1; }
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
mkdir "$STAGE/onnx"
cp "$R/model/config.json" "$R/model/model.safetensors" "$R/model/tokenizer.json" "$R/model/tokenizer_config.json" "$STAGE/"
cp "$R/onnx/model_int8_int4-block.onnx" "$STAGE/onnx/model_int4.onnx"
cp "model_cards/$NAME.md" "$STAGE/README.md"
hf upload "$REPO" "$STAGE" . --commit-message "Upload $NAME from tūmataiti $(git rev-parse --short HEAD)"

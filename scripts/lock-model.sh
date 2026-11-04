#!/usr/bin/env bash
# Pin a published student for the demo: writes demo/model.lock with the Hub
# commit and the SHA-256 of each file the demo downloads.
#   scripts/lock-model.sh woodrock/tumataiti-deberta-v3-small-open <commit> deberta-v3-small-open
set -euo pipefail
cd "$(dirname "$0")/.."
REPO=$1 REVISION=$2 NAME=$3
MODEL_FILE=onnx/model_int4.onnx
DIR=$(mktemp -d)
trap 'rm -rf "$DIR"' EXIT
sha() { curl -fsSL --retry 3 "https://huggingface.co/$REPO/resolve/$REVISION/$1" | shasum -a 256 | cut -d' ' -f1; }
cat > demo/model.lock <<LOCK
# The student the demo ships, pinned to a Hub commit (scripts/lock-model.sh).
REPO=$REPO
REVISION=$REVISION
NAME=$NAME
PRECISION="int8 embeddings, int4 encoder"
MODEL_FILE=$MODEL_FILE
MODEL_SHA256=$(sha $MODEL_FILE)
TOKENIZER_SHA256=$(sha tokenizer.json)
CONFIG_SHA256=$(sha config.json)
LOCK
cat demo/model.lock

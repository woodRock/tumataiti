#!/usr/bin/env bash
# Download the student pinned in demo/model.lock from the Hugging Face Hub,
# check every file against its pinned SHA-256, and install it in the demo.
# The Pages build runs this, so visitors download the model from the site
# itself, never from a third party.
set -euo pipefail
cd "$(dirname "$0")/.."
source demo/model.lock
DIR=$(mktemp -d)
trap 'rm -rf "$DIR"' EXIT
fetch() {  # path in repo, expected sha256
  curl -fsSL --retry 3 -o "$DIR/$(basename "$1")" "https://huggingface.co/$REPO/resolve/$REVISION/$1"
  echo "$2  $DIR/$(basename "$1")" | shasum -a 256 -c --quiet
}
fetch "$MODEL_FILE" "$MODEL_SHA256"
fetch tokenizer.json "$TOKENIZER_SHA256"
fetch config.json "$CONFIG_SHA256"
REPO=$REPO scripts/copy-model.sh "$DIR" "$(basename "$MODEL_FILE")" "$PRECISION" "$NAME"

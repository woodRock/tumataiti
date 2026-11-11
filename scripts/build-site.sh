#!/usr/bin/env bash
# Build the demo into docs/, which GitHub Pages serves from the main branch
# (Settings > Pages > Deploy from a branch: main, /docs). Replaces the Actions
# workflow (.github/workflows/pages.yml), so the site deploys without Actions:
#   scripts/build-site.sh && git add docs && git commit -m "Rebuild the site" && git push
# Tests the Rust crates, installs the student pinned in demo/model.lock (checked
# against its SHA-256; stored in parts under 100 MB, GitHub's file limit) and
# builds for https://woodrock.github.io/tumataiti/.
set -euo pipefail
cd "$(dirname "$0")/.."
cargo test -q -p tumataiti-rules -p tumataiti-wasm -p tumataiti-student
[ ! -f demo/model.lock ] || scripts/fetch-model.sh
(cd demo && npm ci && npm run build -- --base=/tumataiti/ --outDir ../docs --emptyOutDir)
touch docs/.nojekyll  # serve files as they are, without Jekyll
find docs -size +95M | grep . && { echo "a file in docs/ is over GitHub's limit" >&2; exit 1; } || true
du -sh docs

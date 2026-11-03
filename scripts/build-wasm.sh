#!/usr/bin/env bash
# Compile tumataiti-rules to WebAssembly and generate JS bindings for the demo.
set -euo pipefail
cd "$(dirname "$0")/.."
cargo build -p tumataiti-wasm --target wasm32-unknown-unknown --release
wasm-bindgen target/wasm32-unknown-unknown/release/tumataiti_wasm.wasm \
  --target web --out-dir demo/src/wasm

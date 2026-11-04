#!/usr/bin/env bash
# Compile the Rust crates to WebAssembly and generate JS bindings for the demo:
# the rules (always loaded) and the student model's tokeniser and decoder
# (loaded only when the model is switched on).
set -euo pipefail
cd "$(dirname "$0")/.."
cargo build -p tumataiti-wasm --target wasm32-unknown-unknown --release
wasm-bindgen target/wasm32-unknown-unknown/release/tumataiti_wasm.wasm \
  --target web --out-dir demo/src/wasm
# tokenizers needs getrandom's browser backend, selected by a cfg flag.
RUSTFLAGS='--cfg getrandom_backend="wasm_js"' \
  cargo build -p tumataiti-student --target wasm32-unknown-unknown --release
wasm-bindgen target/wasm32-unknown-unknown/release/tumataiti_student.wasm \
  --target web --out-dir demo/src/wasm-student

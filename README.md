# Tūmataiti

Local redaction for the Atamai AI portal: strip personal information from text on the user's own device before anything reaches a cloud model. See [SPEC.md](SPEC.md) for the full design.

Live demo: https://woodrock.github.io/tumataiti/

Done so far: milestone 0 (deterministic rules for NZ identifiers, compiled from Rust to WebAssembly, and a browser demo that runs them with no server) milestone 1 (synthetic NZ data, an evaluation harness and baseline results for the rules and the `openai/privacy-filter` teacher), and milestone 3 so far (small student models evaluated on held-out NZ templates and names; with the v2 training data, rules + mDeBERTa-v3-base leaks 1.1% of held-out NZ documents and rules + DeBERTa-v3-small 4.9%, against 44.2% for rules + teacher). See [ml/results](ml/results/README.md).

## Layout

```
crates/tumataiti-rules   Rust rules, checksums, span merging, policy, pseudonymisation
crates/tumataiti-wasm    WebAssembly bindings for the browser
crates/tumataiti-student Student model tokeniser and span decoder for the browser (WebAssembly)
crates/tumataiti-py      Python bindings (PyO3), used for evaluation and training labels
demo/                    React + Vite demo site (static, no backend)
ml/                      Python: synthetic NZ data, detectors, evaluation (uv project)
scripts/build-wasm.sh    Builds the WebAssembly modules into demo/src/wasm and demo/src/wasm-student
scripts/copy-model.sh    Copies an exported student model into the demo
```

## Requirements

- Rust with the `wasm32-unknown-unknown` target: `rustup target add wasm32-unknown-unknown`
- `wasm-bindgen` CLI matching the crate version: `cargo install wasm-bindgen-cli --version 0.2.130 --locked`
- Node 20 or later

## Run

```bash
cargo test
```

```bash
./scripts/build-wasm.sh
```

```bash
npm --prefix demo install
```

```bash
npm --prefix demo run dev
```

For the ML side, from `ml/` (needs uv):

```bash
uv sync --extra rules && uv run pytest
```

`npm --prefix demo run build` produces a static site in `demo/dist`, with a Content-Security-Policy that stops the page contacting any other origin.

### The student model in the demo

The demo runs the rules on their own unless a student model is copied in. The model is not committed or published yet. With an exported model (see [ml/results](ml/results/README.md)):

```bash
./scripts/copy-model.sh ml/runs/m3-v2/deberta-v3-small/onnx model_int8_int4-block.onnx "int8 embeddings, int4 encoder"
```

Then restart `npm --prefix demo run dev`. The page offers an "Add the name model" button. It downloads the model from the page's own origin, runs it with ONNX Runtime Web (WebAssembly, one thread), and merges its spans with the rules in Rust. The tokeniser is the Hugging Face `tokenizers` crate compiled to WebAssembly. It matches the Python tokeniser exactly (`cargo test -p tumataiti-student -- --ignored`, with `TUMATAITI_TOKENIZER` and `TUMATAITI_EXPECTED` set; see the test).

## What the rules detect

IRD numbers (mod-11 check digit), NHI numbers (old and new formats), payment cards (Luhn), NZ bank accounts (format), NZ phone numbers, passports and driver licences (by label), emails, URLs, IPv4 addresses, dates of birth or death (by label, including Māori month names), and API keys and passwords. Names, addresses, iwi and hapū affiliation and health details need the model (milestone 3).

## Licence

Apache 2.0.

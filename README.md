# Tūmataiti

Local redaction for the Atamai AI portal: strip personal information from text on the user's own device before anything reaches a cloud model. See [SPEC.md](SPEC.md) for the full design.

This is milestone 0: deterministic rules for NZ identifiers, compiled from Rust to WebAssembly, and a browser demo that runs them with no server.

## Layout

```
crates/tumataiti-rules   Rust rules, checksums, span merging, policy, pseudonymisation
crates/tumataiti-wasm    WebAssembly bindings for the browser
demo/                    React + Vite demo site (static, no backend)
scripts/build-wasm.sh    Builds the WebAssembly module into demo/src/wasm
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

`npm --prefix demo run build` produces a static site in `demo/dist`, with a Content-Security-Policy that stops the page contacting any other origin.

## What the rules detect

IRD numbers (mod-11 check digit), NHI numbers (old and new formats), payment cards (Luhn), NZ bank accounts (format), NZ phone numbers, passports and driver licences (by label), emails, URLs, IPv4 addresses, dates of birth or death (by label, including Māori month names), and API keys and passwords. Names, addresses, iwi and hapū affiliation and health details need the model (milestone 3).

## Licence

Apache 2.0.

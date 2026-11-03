# Tūmataiti — Local Redaction Gateway for Atamai

**Status:** Draft v0.2 (prototype spec) · **Author:** Jesse Wood · **Date:** 2026-11-03
**Context:** Hiringa Te Mahara AI portal (Atamai) — privacy workstream (differential privacy & federated learning)

---

## 1. Summary

Tūmataiti is a small, open-source redaction layer that runs **on the user's own machine** and strips or pseudonymises personally identifiable information (PII) and culturally sensitive details from text **before** it is sent to cloud-hosted models behind Atamai (Anthropic, Qwen, DeepSeek, Meta, etc.). Responses come back containing placeholders, which are restored locally so the user sees a natural answer while the cloud provider never sees the original identifiers.

It is conceptually similar to OpenAI's [Privacy Filter](https://openai.com/index/introducing-openai-privacy-filter/) (an open-weight, Apache-2.0 token-classification model for PII detection), but is:

- tuned for **Aotearoa New Zealand** identifiers and **te reo Māori** names, places and kinship terms;
- governed by **Māori data sovereignty** principles (Te Mana Raraunga, CARE), not just generic PII rules;
- designed as a **research platform** for differential privacy (DP) and federated learning (FL) within Atamai.

## 2. Problem

Atamai routes prompts and retrieved documents (RAG context) to third-party, offshore model providers. Those inputs can contain:

- personal details of whānau, participants, and staff;
- NZ-specific identifiers (IRD, NHI, driver licence, passport numbers);
- whakapapa, iwi/hapū/marae affiliation and other details that are identifying in small communities even without a name;
- mātauranga that a community may not want leaving its control at all.

Once sent, that data is outside the community's governance. Redaction needs to happen *before* the network boundary, on infrastructure the user or iwi controls.

## 3. Goals and non-goals

### Goals (prototype)

1. Detect and redact PII in English and te reo Māori text, locally, on a standard laptop (no GPU required).
2. Reversible pseudonymisation: consistent placeholders (`[PERSON_1]`) mapped in a local-only vault, restored in responses.
3. A drop-in local proxy that sits between Atamai (or any client) and a cloud LLM API.
4. A human-in-the-loop review step so the user can see and correct what will be sent.
5. A reproducible evaluation harness with an NZ / te reo test set.
6. A clear path to DP fine-tuning and federated improvement of the detector.
7. A public, in-browser live demo where anyone can paste text and watch it redacted, with no text sent to any server (§7).

### Non-goals (prototype)

- Guaranteed anonymisation or legal compliance. Redaction reduces risk; it does not remove it.
- Redacting images, audio or scanned PDFs (text only for v0; OCR later).
- Making governance decisions about mātauranga. The tool flags; people decide.
- Production hardening, multi-tenant deployment, or SLA.

## 4. Users and scenarios

| User | Scenario |
|---|---|
| Researcher | Pastes interview notes into Atamai to summarise themes; names, places and dates are pseudonymised first. |
| Kaitiaki / data steward | Sets the redaction policy for a project (e.g. "always redact marae names", "block anything tagged tapu"). |
| Atamai backend | Calls the gateway programmatically to sanitise RAG chunks before they are added to a cloud prompt. |
| Tech team | Runs the evaluation suite, compares detectors, ships updated model weights. |

## 5. System overview

```
 ┌──────────────────────── user / iwi-controlled device ────────────────────────┐
 │                                                                               │
 │  Atamai client ──► Tūmataiti gateway                                          │
 │                     1. normalise (Unicode NFC, macron variants)               │
 │                     2. detect   (rules + local model → spans)                 │
 │                     3. policy   (per-project: redact / mask / allow / block)  │
 │                     4. review   (optional UI diff, user edits spans)          │
 │                     5. pseudonymise → placeholders, vault stores mapping       │
 │                              │                                ▲               │
 │                              ▼                                │ 7. rehydrate  │
 └──────────────────────────────┼────────────────────────────────┼───────────────┘
                                ▼                                │
                     Cloud LLM (Anthropic / Qwen / DeepSeek / Meta)
                                └─────── 6. response with placeholders ─┘
```

Raw text and the vault never leave the device. The cloud sees only sanitised text.

### 5.1 Technology stack

| Layer | Language and tools | Why |
|---|---|---|
| Rules, merge, policy, pseudonymisation | Rust library (`crates/tumataiti-rules`) | One implementation of every checksum and policy decision |
| ↳ in the browser | Same library compiled to WebAssembly (`crates/tumataiti-wasm`, `wasm-bindgen`) | The demo runs exactly the rules the proxy runs |
| ↳ in training and evaluation | Same library through Python bindings (PyO3, planned) | Rule-generated labels match production behaviour |
| Local proxy (M5) | Rust | Single binary, memory safety around sensitive text, good streaming support; runs the same ONNX model via ONNX Runtime |
| Training, data generation, evaluation | Python (PyTorch, Hugging Face), on the ECS GPU cluster | Standard ML tooling |
| Demo frontend | React + TypeScript, built with Vite as a static site | Fits the static-hosting privacy model (§7.1); Transformers.js runs the model in a Web Worker |

## 6. Functional requirements

### 6.1 Detection

**Decision: hybrid, model-led.** The model does most of the work. Deterministic rules cover structured identifiers that a checksum can verify, and a merge step reconciles the two. All-model detection (OpenAI's approach) suits generic worldwide formats, but a model cannot verify an IRD or NHI check digit and gives no explanation beyond a confidence score. Rules are near-perfect and explainable for exactly these NZ identifiers.

| | Rules | Model |
|---|---|---|
| IRD, NHI, bank account, card | Checksum-verified, near-zero false positives | Cannot verify check digits; confuses them with any same-length number |
| Email, URL, phone, secrets | Precise and explainable | Workable but less reliable |
| Names, addresses, affiliation, health in context | Cannot handle | Primary detector |
| Explaining a redaction | Names the rule that fired | Confidence score only |

Components:

1. **Deterministic rules** (high precision, checksum-validated where possible)
   - IRD number (mod-11 checksum), NHI (old and new formats with check digit), payment card (Luhn), NZ phone (landline, mobile `02x`, `+64`), NZ driver licence and passport (told apart by a label on the same line), bank account (`BB-bbbb-AAAAAAA-SS`, format only until per-bank checksums are added), email (including macrons in the local part), URL, IPv4 address, and dates of birth or death (only next to a birth/death label, including Māori month names).
   - API keys / secrets (common provider prefixes, private keys, `password=` style assignments).
   - A format match that fails its checksum is only reported when a label such as "IRD" sits nearby. It is then redacted by default (confidence 0.7), because it is most likely a mistyped real ID, which still identifies the person; the failed check is shown for review. Random numbers that happen to share the format are ignored, and an ID-shaped code with no label is flagged, not redacted. (Decided 2026-11-04 after the M1 evaluation.)
   - Implemented once in Rust and compiled to WebAssembly for the browser (§5.1), so the demo (§7) and the proxy run identical code.
   - *Not yet:* NZ postcodes in address context, high-entropy secret detection, per-bank account checksums.
2. **Model-based span detection** for open-ended categories (names, addresses, affiliation, health in context).
   - **Teacher / baseline:** `openai/privacy-filter` (Apache 2.0; bidirectional token classifier with span decoding; ~1.5B total / ~50M active params). It is too large to ship to a browser (all experts must be downloaded, ~1–3 GB), so it is used on ECS to label training data and as the comparison baseline. Check its category list against the model card.
   - **Comparators:** GLiNER-based PII models, Microsoft Presidio + spaCy.
   - **Tūmataiti model (student):** a small encoder (~100–150M params, e.g. DeBERTa-v3-small or ModernBERT-base) fine-tuned for token classification (BIO tags over the §6.2 categories) on NZ / te reo data. Exported to ONNX and int8-quantised to ~70–150 MB so it runs in a browser and on a laptop CPU. Training pipeline in §10.0.
3. **Gazetteers** (optional, per project): known participant names, marae, hapū, local place names supplied by the data steward. Stored locally only.
4. **Merge step:** each detection outputs `{start, end, text, category, confidence, source: rule|model|gazetteer}`. Overlapping spans merge into one span covering all of them, so no overlapping text is left exposed; it takes the label of the best-ranked span (checksum-verified first, then confidence at or above 0.5, then category priority, then width). A checksum-verified rule match therefore always wins over a model span on the same characters. (M1 found that dropping the losing span instead leaked the model span's extra characters.) Rule matches also serve as weak labels for model training.

### 6.2 Categories (v0)

| Category | Examples | Default action |
|---|---|---|
| `PERSON` | Hēmi Te Rangi, Aunty Mere | Pseudonymise |
| `ADDRESS` | 12 Kōwhai St, Ōtaki 5512 | Pseudonymise |
| `EMAIL`, `PHONE`, `URL`, `IP_ADDRESS` | | Pseudonymise |
| `DATE` (personal) | DOB, date of death | Generalise (year or month) |
| `NZ_GOV_ID` | IRD, NHI, licence, passport | Mask (no restore needed) |
| `FINANCIAL` | bank account, card | Mask |
| `SECRET` | API keys, passwords | Block request |
| `AFFILIATION` | iwi, hapū, marae, whānau name | Policy-defined (default: flag for review) |
| `HEALTH` | diagnoses linked to a person | Flag for review |
| `CULTURAL_RESTRICTED` | content the steward marks tapu / restricted | Block request |

`AFFILIATION`, `HEALTH` and `CULTURAL_RESTRICTED` are deliberately conservative. Combined, they re-identify people in small communities. Policy for them is set with the kaitiaki/legal workstream, not by the tech team alone.

**Public figures and tūpuna:** names of public figures or ancestors discussed in a research capacity (e.g. a rangatira's published work) may be allow-listed per project so research questions remain answerable.

### 6.3 Policy engine

- YAML policy per project: action per category (`allow | flag | pseudonymise | generalise | mask | block`), confidence thresholds, allow-lists, gazetteers.
- Default policy is **recall-first**: low threshold, over-redact rather than under-redact.
- Policies are versioned and their hash is recorded in each audit entry.

### 6.4 Pseudonymisation and rehydration

- Consistent placeholders within a session: every mention of the same entity gets the same token (`[PERSON_1]`), including simple variants (with or without macrons, first name only once full name is known).
- Placeholders are typed so the LLM can still reason ("[PERSON_1] is the mother of [PERSON_2]").
- Optional **surrogate mode**: replace with realistic fake values (fake NZ names/addresses) for tasks where placeholders hurt quality. Surrogates are drawn so they never match a real gazetteer entry.
- Vault: local encrypted store (SQLite + OS keychain key), scoped per session, auto-expiring (default 24h). Never synced.
- Rehydration replaces placeholders in the streamed response before display. Unknown or hallucinated placeholders are left visible and flagged.

### 6.5 Human review

- Side-by-side diff of original vs. outbound text, with highlighted spans and category labels.
- User can add a span, remove a span, or change its category; edits are logged as (non-PII) feedback for model improvement (§10.2).
- Review can be required, optional, or off per policy (e.g. required for `flag` categories).

### 6.6 Interfaces

1. **Rust crate and Python bindings**: `redact(text, policy) -> RedactionResult`, `restore(text, session) -> str`.
2. **CLI**: `tumataiti redact file.txt --policy project.yaml`, `tumataiti eval --dataset nz-test`.
3. **Local proxy** (core prototype deliverable): an HTTP server on `localhost` that exposes Anthropic- and OpenAI-compatible endpoints, sanitises request messages (including tool results and system prompts), forwards upstream, and rehydrates responses, including streaming (SSE).
4. **Review UI**: minimal local web page served by the proxy.
5. **Browser demo**: static website running rules and model entirely in the page (§7).
6. *(Later)* Browser extension for the Atamai web portal, reusing the demo's in-browser detector.

### 6.7 Audit log

Local, append-only log per request: timestamp, policy hash, detector version, counts per category, actions taken, reviewer edits, upstream provider. **No raw PII and no placeholder mappings** in the log.

## 7. Live browser demo

A public web page where anyone (the Atamai team, community, reviewers) can type or paste text and watch it redacted live. It is both an outreach tool and a working proof that local redaction is practical.

### 7.1 Privacy guarantee

**No text typed into the page is sent anywhere.** The only network traffic is the one-time download of the page and the model weights, which are then cached in the browser.

Enforced and made checkable by:

- **Static hosting only** (e.g. Deno Deploy or GitHub Pages): no backend, no API routes, no analytics.
- **Content-Security-Policy** `connect-src 'self'` (plus the weight host if not same-origin) so the page cannot send data to any other origin, even by mistake.
- **Offline mode:** a service worker caches page and weights; the page states "you can turn off your wifi now" and keeps working.
- **"Check it yourself" panel:** short instructions for watching the DevTools Network tab while typing.
- Weights served same-origin and pinned by hash, so the model cannot be swapped silently.

### 7.2 How it runs

- **Runtime:** Transformers.js (ONNX Runtime Web), using WebGPU where available and WebAssembly otherwise. Inference runs in a Web Worker so animations stay smooth.
- **Model:** the int8 student model from §10.0 (~70–150 MB). Until the student is trained, the demo can ship with rules plus an off-the-shelf small PII model to unblock UI work.
- **Rules:** the Rust rule set from §6.1 compiled to WebAssembly (~1.2 MB, ~0.4 MB gzipped), run on every keystroke; the model runs on a short pause in typing.
- **Pseudonymisation:** done in memory in the page; nothing is written to storage.
- **Targets:** first load under 10 s on a typical NZ broadband connection; redaction of a paragraph in under 200 ms on a recent laptop; usable on a modern phone (slower is acceptable).

### 7.3 Interaction and animation

1. **Detect:** spans are highlighted as they are found, coloured by category, with a small badge showing the source (rule or model) and confidence.
2. **Redact:** a black bar sweeps across each span, which then morphs into its placeholder (`Hēmi` → `[PERSON_1]`). Same entity, same placeholder, so linked mentions animate together.
3. **What the cloud sees:** side-by-side toggle of the user's view and the sanitised outbound text.
4. **Round trip:** a simulated (scripted, not real) model response with placeholders, then animated rehydration back to real names. Clearly labelled as simulated so no one thinks text was sent.
5. **Policy controls:** per-category toggles (redact / generalise / allow) and a confidence slider, so people can see the recall/precision trade-off live.
6. **Accessibility:** respects `prefers-reduced-motion` (instant transitions), keyboard usable, screen-reader labels for each redaction.

### 7.4 Preset examples

Each preset shows one feature of the redactor:

| Preset | Shows |
|---|---|
| Interview notes with te reo names, with and without macrons | Model detection of Māori names; consistent placeholders across variants |
| IRD and NHI numbers, one valid and one with a bad check digit | Rules verify checksums; the invalid one is flagged, not treated as a real ID |
| Hui transcript naming a marae, hapū and a whānau member's illness | `AFFILIATION` and `HEALTH` flagged for review, not silently redacted |
| Discussion of a rangatira's published work | Public-figure allow-list: research context kept |
| Email signature with phone, email, address | Structured PII by rules, address by model |
| Text containing an API key | `SECRET` blocks the request entirely |
| A RAG chunk from a long document | Throughput on longer text |

All preset content is synthetic. No real person's details appear in the demo.

### 7.5 Out of scope for the demo

Real calls to cloud models, accounts, saving or sharing of user text, file upload (text box only for v0).

## 8. Non-functional requirements

| Requirement | Prototype target |
|---|---|
| Runs offline | Detection and vault work with no network access |
| Hardware | Apple Silicon or x86 laptop, CPU only, ≤ 8 GB RAM |
| Latency | ≤ 300 ms p50 for a 1k-token prompt on M-series CPU; ≤ 2 s for a 10k-token RAG context |
| Browser | Runs in current Chrome, Edge, Firefox and Safari (WebGPU optional, WebAssembly fallback); model ≤ 150 MB |
| Packaging | Rust crate, `pip install tumataiti` (Python bindings), and a static demo site; model weights downloaded once and pinned by hash |
| Licence | Apache 2.0 (compatible with the baseline model) |
| Fail-safe | If detection fails or times out, **block** the request; never forward unredacted |
| Telemetry | None by default. Any opt-in metrics are aggregated under DP (§10.3) |

## 9. Evaluation

### 9.1 Datasets

- **Public:** PII-Masking-300k (and its corrected version), plus other public NER/PII sets for comparability with the OpenAI baseline.
- **Tūmataiti NZ test set (new):** synthetic and consented documents covering:
  - te reo Māori and Pasifika names, with and without macrons, and code-switched English/te reo text;
  - NZ addresses, place names that are also personal names (e.g. a person and a town sharing a name);
  - NZ identifiers with valid and invalid checksums;
  - research-style text: interview transcripts, hui notes, RAG chunks.
  - Built and labelled with community input; held out from all training.
- **NZ synthetic v0 (built in M1):** 1,600 generated documents from 16 templates (hui notes, referrals, forms, interviews, text messages, tangihanga notices, te reo paragraphs and more), with exact gold spans from the template slots and hard negatives (hui dates, IRD-shaped order references, public government URLs). Generated deterministically (`seed 0`) by `ml/src/tumataiti_ml/synth`. This is a development set for M1–M3, not the held-out community test set above.
- Public data is downloaded at run time and never committed (PII-Masking-300k allows academic use with citation).

All datasets are mapped onto nine evaluation categories (`PERSON`, `ADDRESS`, `EMAIL`, `PHONE`, `URL`, `IP_ADDRESS`, `DATE`, `ID`, `SECRET`) in `ml/src/tumataiti_ml/taxonomy.py`. `ID` merges government IDs, card and bank numbers, and the teacher's `account_number`. Labels that are not personal on their own (generic dates and times, titles, country) are ignored: neither misses nor false positives.

### 9.2 Metrics

- **Document leakage rate (headline):** share of documents with any PII in which at least one gold span leaks. A span leaks if any of its letters or digits is left uncovered by every predicted span, whatever category the prediction has. Partial redaction of a name counts as a leak.
- **Span leak rate**, overall and per category, and per community for names (Māori, Pākehā, Pasifika, Asian NZ) on the synthetic set.
- Character-level precision / recall / F1 over letters and digits, category-agnostic and per category; this is robust to boundary conventions and to names split into given and family parts.
- Exact-span F1 (same start, end and category).
- **Re-identification test:** red-team attempts to identify a person from redacted text plus public information, especially via `AFFILIATION` combinations.
- **Utility:** answer quality of the downstream LLM on redacted vs. original prompts (LLM-judge + human spot checks).
- Latency and memory on reference hardware.

### 9.3 Success criteria for the prototype

- Recall ≥ 0.98 on `PERSON`, `NZ_GOV_ID`, `EMAIL`, `PHONE` on the NZ test set.
- Te reo name recall within 2 points of English name recall (measuring the bias gap is a key result).
- Document leakage rate reported against the OpenAI baseline, showing measurable improvement on NZ data.
- Downstream utility loss ≤ 10% on the research-summarisation tasks.

### 9.4 M1 baseline results (2026-11-04)

Full tables: `ml/results/`. Teacher runs on one RTX A5000 (ECS), rules on a laptop. Lower leak rates are better.

| Detector | PII-Masking-300k doc leak | NZ synthetic v0 doc leak | NZ span leak |
|---|---:|---:|---:|
| Rules only | 95.9% | 93.8% | 45.8% |
| `openai/privacy-filter` (teacher) | 8.2% | 43.2% | 16.8% |
| Rules + teacher (merged) | **7.8%** | **36.2%** | **11.0%** |

Findings:

1. **The teacher is about 5× worse on NZ text than on the public benchmark** (43.2% vs 8.2% of documents leak). It leaks 23% of names, 26% of addresses, 21% of birth/death dates, 14% of phone numbers and 14% of NZ IDs in the synthetic set.
2. **Te reo Māori and Pasifika names leak more:** 25.5% of Māori and 27.8% of Pasifika name mentions leak, against 14.8% for Pākehā names. The gap is about 11 points, so success criterion 9.3 (within 2 points) is far off. Names that are also everyday words leak most (Tūī 71%, Whetū 61%), as do names typed in lowercase without macrons (60%).
3. **Rules and model complement each other.** Merged, phone, email, URL, IP, date and NZ ID leaks on NZ text all drop to 0%, while names and addresses stay at the teacher's level. That is what M3 fine-tuning has to fix.
4. **Typo'd IDs are now redacted.** The first run flagged (sent as-is) IDs with a nearby label but a failed check digit, which leaked 25% of NZ ID spans for the rules alone. These are now redacted by default (§6.1), bringing rule-side ID leakage to 0%.
5. The teacher's median latency is about 0.24–0.28 s per document on an A5000, including a per-token Python Viterbi decoder that is likely a large share (not yet profiled); the rules take under 0.1 ms.

## 10. Research extensions: DP and FL

These are what make Tūmataiti a research project and not only a tool. They map to the DP/FL questions raised for Atamai.

### 10.0 Training pipeline (ECS GPU cluster)

Training runs on the VUW ECS GPU servers through the `task` spooler (one GPU per job, e.g. an RTX A5000; no host pinning; stay within the 5-concurrent-GPU limit).

1. **Data generation:** synthetic NZ / te reo documents from templates, name and place lists, and generated NZ identifiers (valid and invalid checksums). Labels come from the template slots, the rules (§6.1), and `openai/privacy-filter` as a teacher on unlabelled text.
2. **Fine-tune** the student encoder for token classification. Expected cost: a few GPU-hours per run.
3. **Export and compress:** ONNX export, int8 quantisation, then re-run the evaluation (§9) on the quantised model to confirm the accuracy drop is small.
4. **Retrieve** weights with `task fetch` and publish them as static files with a hash recorded in the release.

Every run records its config, data version, seed and metrics so results are reproducible.

### 10.1 Differentially private fine-tuning

Fine-tune the detector on sensitive community text with **DP-SGD** (e.g. Opacus) so the model weights do not memorise specific names or identifiers. Report privacy budget (ε, δ) against detection F1. Run membership-inference and canary-extraction attacks on the fine-tuned weights to check empirically.

### 10.2 Federated improvement

Each organisation or iwi runs Tūmataiti locally. Reviewer corrections (§6.5) become local training signal. Model updates, not data, are aggregated (e.g. with Flower), optionally with:

- secure aggregation, so the coordinator never sees an individual site's update;
- DP noise on updates (user- or site-level DP).

Research questions: how much does federated adaptation close the te reo gap? What is the privacy/utility trade-off at realistic numbers of participating sites (likely few, with non-IID data)? Who governs the aggregated model? That last question goes to the kaitiaki/legal workstream.

### 10.3 DP analytics

Any usage statistics shared back to the Atamai team (e.g. "how often is `HEALTH` flagged") are released with DP noise, so aggregate reporting cannot reveal individual users' content.

**Note:** redaction itself is not differential privacy. DP applies to model training and aggregate statistics. Redaction is a separate, complementary control.

## 11. Threat model (summary)

| Threat | Mitigation |
|---|---|
| Cloud provider logs/retains prompts | Only sanitised text leaves the device |
| Missed PII (false negatives) | Recall-first thresholds, hybrid rules+model, human review, fail-closed |
| Re-identification via quasi-identifiers | `AFFILIATION`/`DATE` generalisation, combination rules, red-team evaluation |
| LLM infers identity from context | Out of scope to fully prevent; measured in re-identification tests |
| Local vault compromise | Encrypted at rest, short expiry, per-session scope |
| Detector weights leak training data | DP-SGD fine-tuning (§10.1) |
| Malicious placeholder injection in responses | Rehydrate only placeholders issued in this session |
| Demo page leaks typed text | Static hosting, no backend, CSP `connect-src 'self'`, offline mode, no analytics (§7.1) |
| Tampered model weights on the demo site | Same-origin weights pinned by hash |

## 12. Prototype milestones

| Phase | Deliverable | Rough effort |
|---|---|---|
| M0 | Repo scaffold, policy schema, NZ rule detectors in Rust with tests, WebAssembly build, initial rules-only demo UI. **Done (prototype), 2026-11-03** | 1–2 weeks |
| M1 | Eval harness; teacher/baseline (`openai/privacy-filter`) on public data; synthetic NZ data generator; Python bindings for the rules. **Done, 2026-11-04** (Presidio and GLiNER comparators still to add; results in §9.4) | 2 weeks |
| M2 | NZ / te reo test set v0 (synthetic), co-designed with community and legal workstream | 3–4 weeks (parallel) |
| M3 | Student model trained on ECS, ONNX int8 export, evaluated against teacher | 2–3 weeks |
| M4 | Live browser demo (§7): animations, presets, offline mode; ships with rules + interim model, then swaps in the M3 student | 2–3 weeks (UI can start after M0) |
| M5 | Local proxy with pseudonymisation, vault, streaming rehydration; minimal review UI | 2–3 weeks |
| M6 | DP-SGD fine-tuning, federated simulation (2–5 synthetic sites), Atamai integration; results report | 4–6 weeks |

## 13. Open questions for the team

1. **Integration point:** does Atamai call cloud models from a server (then the gateway runs on an iwi/HTM-controlled server) or from the client (then it runs on the user's device)? This decides where "local" is.
2. **RAG corpus:** is the retrieval store itself already sanitised, or does redaction need to run on every retrieved chunk at query time?
3. **Governance:** who sets and approves redaction policy for `AFFILIATION`, `HEALTH` and restricted mātauranga? (Legal / community workstreams.)
4. **Data for the NZ test set:** can we use any real (consented) documents, or synthetic only for v0?
5. **Provider agreements:** what retention/zero-data-retention terms do we have with each cloud provider? These affect how conservative the default policy must be.
6. **Reporting:** how should redaction stats appear in Atamai's report outputs (link to the reporting workstream)?
7. **Demo hosting and branding:** where should the public demo live (HTM, VUW, or a project domain), and what design and brand guidance applies (design team)?

## 14. References

- OpenAI, *Introducing OpenAI Privacy Filter* — https://openai.com/index/introducing-openai-privacy-filter/ (model: `openai/privacy-filter` on Hugging Face, Apache 2.0)
- Te Mana Raraunga — Māori Data Sovereignty Principles
- Global Indigenous Data Alliance — CARE Principles for Indigenous Data Governance
- Abadi et al., *Deep Learning with Differential Privacy* (DP-SGD), CCS 2016
- McMahan et al., *Communication-Efficient Learning of Deep Networks from Decentralized Data* (FedAvg), AISTATS 2017
- Microsoft Presidio — https://github.com/microsoft/presidio
- Flower federated learning framework — https://flower.ai
- Opacus — https://opacus.ai
- Transformers.js — https://huggingface.co/docs/transformers.js
- ONNX Runtime Web — https://onnxruntime.ai

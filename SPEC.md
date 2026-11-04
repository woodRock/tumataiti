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
4. **Merge step:** each detection outputs `{start, end, text, category, confidence, source: rule|model|gazetteer}`. Overlapping spans merge into one span covering all of them, so no overlapping text is left exposed; it takes the label of the best-ranked span (checksum-verified first, then confidence at or above 0.5, then a rule over the model, then category priority, then width). A confident rule match therefore keeps its category, detector and checksum note over a model span on the same characters: the model has a single ID label and cannot tell a bank account from a passport, and the demo found it relabelling NZ bank accounts as government IDs before this rule. The model still wins over weak rule matches (e.g. an unlabelled ID-shaped code). The Python evaluation (`analysis.combine`) ranks the same way. (M1 found that dropping the losing span instead leaked the model span's extra characters.) Rule matches also serve as weak labels for model training.

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

- **Public:** PII-Masking-300k, plus other public NER/PII sets for comparability with the OpenAI baseline. PII-Masking-300k is itself synthetic, from a different generator, so it is reported as a cross-generator synthetic test, never as real text. No corrected release exists: OpenAI describe about 10k missing labels in its test split but have not published fixes. Missing gold labels make leakage look *better* than it is, because unlabelled PII cannot count as a leak.
- **Tūmataiti NZ test set (new):** synthetic and consented documents covering:
  - te reo Māori and Pasifika names, with and without macrons, and code-switched English/te reo text;
  - NZ addresses, place names that are also personal names (e.g. a person and a town sharing a name);
  - NZ identifiers with valid and invalid checksums;
  - research-style text: interview transcripts, hui notes, RAG chunks.
  - Built and labelled with community input; held out from all training.
- **NZ synthetic v0 (built in M1):** 1,600 generated documents from 16 templates (hui notes, referrals, forms, interviews, text messages, tangihanga notices, te reo paragraphs and more), with exact gold spans from the template slots and hard negatives (hui dates, IRD-shaped order references, public government URLs). Generated deterministically (`seed 0`) by `ml/src/tumataiti_ml/synth`. This is a development set for M1–M3, not the held-out community test set above.
- **NZ synthetic v1 (built in M3):** the generator split three ways so test numbers are not flattered by memorised templates or names (the literature finds synthetic NER tests easier than human-written ones and sometimes rank models differently):
  - `train` and `dev`: training templates and training name lists;
  - `test_names`: training templates, held-out names (isolates name generalisation);
  - `test_full`: held-out templates (different genres and phrasing) and held-out names (the headline synthetic number);
  - `cf_<group>`: counterfactual name audit, the same `test_full` documents with names drawn from only one community, so groups differ in nothing but the names.
  The generator also mixes in te reo words that are not names in context (tūī the bird, kōwhai the tree, "aroha mai") as hard negatives. The OpenAI teacher never generates or labels any test split. Headline claims still need the small human-annotated set (M2).
- **NZ synthetic v2 training data (M3):** changes `train` and `dev` only; every evaluation split regenerates byte-identical to v1, so v1 and v2 students are scored on the same files. Two changes, both aimed at what v1 students missed on `test_full`:
  - **balanced names:** people are drawn 25% from each community (v1: 50% Māori, 20% Pākehā, 15% Pasifika, 15% Asian NZ), and the Pākehā, Pasifika and Asian NZ training lists are 2–5× longer. The Pākehā surnames now include ones that are also English words (Baker, Hunter, Young, White), the case behind v1 mDeBERTa's reverse name gap;
  - **six new training templates** for the slots that leaked: a name alone on the last line after a closing (v1 DeBERTa-small leaked 90% of these), chat speakers and @-mentions, and names in formal prose with no field label (bare, or after Mr, Ms or Whaea).
  The new templates share genres with some held-out templates but not their wording; the "Nāku noa," closing is kept out of training. So v2's `test_full` gain is partly in-genre and partly phrasing transfer, not wholly unseen genres. Same size as v1 (8,000 training documents), so any change comes from the mix, not the volume.
- Public data is downloaded at run time and never committed.
- **Licences decide which models can be published.** PII-Masking-300k's licence (ai4privacy LICENSE.md) grants academic, non-commercial use with acknowledgement, and requires a written licence for "the creation and dissemination of derivative works". So from 2026-11-04 every student trains only on openly licensed data, and PII-Masking-300k is an evaluation set only. That keeps one model family, whose results describe models that can be deployed, and it makes PII-Masking-300k validation a fair cross-generator test for the students, as it already was for the teacher. The M3 v1 and v2 students in §9.5–9.6 were trained on it; their results stand as findings about data and quantisation, not as deployable models. Students train on the NZ synthetic data plus openly licensed English data (`EXTRA=open` in `ml/scripts/ecs_student.sh`, built by `ml/scripts/make_data_open.sh`):
  - **nvidia/Nemotron-PII** (CC BY 4.0, attribution required): 20,000 of its 100,000 training documents, with character spans;
  - **gretelai/gretel-pii-masking-en-v1** (Apache-2.0): 10,000 of its 49,896 training documents. It lists entity strings without offsets; spans are found by exact word-bounded matching, and the 104 documents with an entity missing from the text are dropped;
  - left out: gretelai/synthetic_pii_finance_multilingual (Apache-2.0). Its spans were added after generation by GLiNER and miss real PII (addresses and account numbers in spot checks), and unlabelled PII would train the student to skip it.
  Their labels map onto the evaluation categories as PII-Masking-300k's do (`taxonomy.OPEN_PII`). 30,000 documents match PII-Masking-300k's 29,908, so a comparison between the two isolates the data source. A held-out **open English test set** (1,000 + 1,000 documents from the two sets' test and validation splits; no overlap with training) gives an English score no student has trained on. Neither set covers NZ IDs or iwi, hapū and marae, which stay with the NZ generator. For further synthetic data, the generator LLM's licence matters too: Llama's terms require a published model trained on its outputs to be named "Llama-…", and Gemma 3 and earlier make it a Gemma derivative, so use Apache-2.0 generators (e.g. Qwen3, Mistral Small, gpt-oss).

All datasets are mapped onto nine evaluation categories (`PERSON`, `ADDRESS`, `EMAIL`, `PHONE`, `URL`, `IP_ADDRESS`, `DATE`, `ID`, `SECRET`) in `ml/src/tumataiti_ml/taxonomy.py`. `ID` merges government IDs, card and bank numbers, and the teacher's `account_number`. Labels that are not personal on their own (generic dates and times, titles, country) are ignored: neither misses nor false positives.

### 9.2 Metrics

- **Document leakage rate (headline):** share of documents with any PII in which at least one gold span leaks. A span leaks if any of its letters or digits is left uncovered by every predicted span, whatever category the prediction has. Partial redaction of a name counts as a leak. This generalises the Text Anonymization Benchmark's entity-level recall (an entity counts as protected only if every mention is masked; Pilán et al. 2022) to whole documents. Report it across operating points (confidence thresholds), not at one threshold only.
- **Span leak rate**, overall and per category, and per community for names (Māori, Pākehā, Pasifika, Asian NZ). The name audit is counterfactual (same documents, only the names swapped) and span-level, because Māori names are often several tokens ("Te Ao", "Ngā…").
- Character-level precision / recall / F1 over letters and digits, category-agnostic and per category; this is robust to boundary conventions and to names split into given and family parts.
- Exact-span F1 (same start, end and category).
- **Re-identification test:** red-team attempts to identify a person from redacted text plus public information, especially via `AFFILIATION` combinations.
- **Utility:** answer quality of the downstream LLM on redacted vs. original prompts (LLM-judge + human spot checks).
- Latency and memory on reference hardware.

### 9.3 Success criteria for the prototype

- Recall ≥ 0.98 on `PERSON`, `NZ_GOV_ID`, `EMAIL`, `PHONE` on the NZ test set (held-out templates and names, and the human-annotated set once it exists).
- Te reo name recall within 2 points of English name recall in the counterfactual audit (measuring the bias gap is a key result).
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

### 9.5 M3 student results (2026-11-04)

Full tables: `ml/results/m3_*`. All numbers are on synthetic data (§9.1); headline claims still need the human-annotated set (M2). Lower leak rates are better. Students ran on one RTX A5000 each; the int8 model on a laptop CPU.

Held-out templates **and** held-out names (`test_full`, 1,750 documents):

| Detector | Doc leak | Name span leak | Median ms / doc | Size |
|---|---:|---:|---:|---:|
| Rules + teacher (`openai/privacy-filter`) | 44.2% | 35.0% | 369 (GPU) | ~2.8 GB |
| Rules + ModernBERT-base | 31.4% | 17.7% | 13 (GPU) | — |
| Rules + DeBERTa-v3-small | 29.9% | 11.8% | 12 (GPU) | 567 MB fp32 |
| Rules + DeBERTa-v3-small, int8 | 32.4% | 15.6% | **15 (laptop CPU)** | **165 MB** |
| **Rules + mDeBERTa-v3-base** | **9.2%** | **3.3%** | 17 (GPU) | not exported yet |

Counterfactual name audit (same documents, only names swapped; name span leak):

| Names | Teacher | DeBERTa-v3-small | mDeBERTa-v3-base |
|---|---:|---:|---:|
| Māori | 52.4% | 11.7% | 0.2% |
| Pākehā | 14.3% | 13.3% | 20.8% |
| Pasifika | 37.4% | 14.3% | 3.2% |
| Asian NZ | 14.7% | 6.4% | 7.0% |
| Māori − Pākehā gap | +38.1 | **−1.5** | −20.6 |

Findings:

1. **Every student beats the teacher on held-out NZ text**, and rules + mDeBERTa-v3-base cuts document leakage from 44.2% to 9.2%. The multilingual backbone matters most for names (3.3% vs 11.8% leaked).
2. **Held-out splits were essential.** On training templates with new names, every student leaks under 1% of documents; on new genres the same models leak 9–46%. Reporting the in-template number would have overstated quality several-fold.
3. **Only DeBERTa-v3-small meets the 2-point name-gap target** (−1.5). mDeBERTa reverses the teacher's bias: it almost never misses Māori names but misses English surnames that are also words (Walker 41%, Campbell 33%), mostly in a held-out tribunal template. The training mix (half Māori names, six Pākehā surnames) is the likely cause; the next data version should balance the name mix and widen the surname lists. The held-out Māori names deliberately include common words (Tūī, Whetū, Kōwhai, Nīkau), which inflates the teacher's gap on this set.
4. **No model over-flags te reo words:** none of 500 te reo filler sentences ("The tūī were singing in the kōwhai") was flagged by any student.
5. **The rules still matter.** Alone, students leak NZ IDs (DeBERTa-small 6.3%, ModernBERT 29.2%) and some phone numbers; merged with the rules, phone, date, email and ID leaks are all 0%. Names remain the whole residual.
6. **Remaining failure modes:** a per-slot breakdown (done for v2, §9.6) located them: a name alone on the last line after "Nāku noa," (DeBERTa-small leaked 90% of these), chat speakers and mentions ("[date] Finn: …"), and names in formal prose with no field label (the tribunal summary). None appears in the training templates. Lowercase voice transcripts, first suspected, leak nothing once merged with the rules.
7. **int8 costs rare classes more than the literature suggests.** Dynamic int8 (with the embedding table quantised, needed to reach 165 MB) raised DeBERTa-small's name leak from 11.8% to 15.6% overall and from 13.3% to 22.7–28.5% on Pākehā names (per-channel to per-tensor). fp16 weights, keeping the embeddings and classifier in higher precision, or quantisation-aware training are next.
8. **PII-Masking-300k is not a fair comparison here:** students trained on its train split (5.0% doc leak for DeBERTa-small) while the teacher did not (8.2%).
9. Two training bugs were found and fixed: Transformers 5 loads DeBERTa-v3 checkpoints in fp16, which made AdamW produce NaN weights (now loaded in fp32); and checkpoint selection by dev leakage would have kept a broken model that redacts everything (now selected by dev F1).

### 9.6 M3 data v2 results (2026-11-04)

Full tables: `ml/results/m3v2_*` (v1 students shown beside v2 as `<model>-v1`). Same backbones, hyperparameters, seed, data size and evaluation files as §9.5; only the training data changed (§9.1, v2: balanced names and six templates for the leaking slots).

Held-out templates and names (`test_full`), each student merged with the rules:

| Detector | Doc leak v1 → v2 | Name span leak v1 → v2 | Any-PII char precision v1 → v2 |
|---|---:|---:|---:|
| Rules + teacher | 44.2% | 35.0% | 85.6 |
| Rules + DeBERTa-v3-small | 29.9% → **4.9%** | 11.8% → **1.6%** | 91.0 → 93.4 |
| Rules + ModernBERT-base | 31.4% → **2.6%** | 17.7% → **1.1%** | 92.8 → 93.3 |
| Rules + mDeBERTa-v3-base | 9.2% → **1.1%** | 3.3% → **0.4%** | 90.3 → 93.7 |

Counterfactual name audit (name span leak, v2 students):

| Names | Teacher | DeBERTa-v3-small | ModernBERT-base | mDeBERTa-v3-base |
|---|---:|---:|---:|---:|
| Māori | 52.4% | 2.1% | 0.2% | 0.1% |
| Pākehā | 14.3% | 1.4% | 6.5% | 7.1% |
| Pasifika | 37.4% | 2.0% | 0.4% | 0.2% |
| Asian NZ | 14.7% | 0.0% | 0.1% | 0.0% |
| Māori − Pākehā gap | +38.1 | **+0.7** (v1 −1.5) | −6.3 (v1 −6.8) | −7.0 (v1 −20.6) |

Findings:

1. **v2 cuts held-out document leakage 4–12× for every backbone**, and precision rises too, so the gain is not from redacting more text. Rules + mDeBERTa leaks 1.1% of documents (19 of 1,750); rules + DeBERTa-small, the browser-sized model, 4.9%.
2. **The targeted slots are mostly fixed.** A name after a closing went from 90% leaked to 0% (DeBERTa-small) and from 28% to 4% (mDeBERTa); chat speakers from up to 32% to 2%. Names in formal prose are the main residual: "Evidence was given by {name}" still leaks 29% for DeBERTa-small and 14% for ModernBERT.
3. **mDeBERTa's reverse name gap shrank from −20.6 to −7.0 points** but still misses the 2-point target. Its remaining Pākehā misses are held-out surnames that are also words or rare as names in multilingual text (Thompson 17%, Clarke 14%, Walker 12%) and the given name Grace (12%). DeBERTa-small is the only model within target (+0.7).
4. **Caveat:** v2 templates share genres (closings, chat, formal prose) with held-out templates, though not their wording, so part of the gain is in-genre rather than transfer to unseen genres. A fresh held-out set with genres absent from both v1 and v2 would measure that; the human-annotated set (M2) is the real check.
5. In-template splits are saturated (dev char F1 is 1.0 from epoch 0 for every run, so checkpoint selection keeps epoch 0) and PII-Masking-300k is unchanged (4.6–5.5% doc leak), as expected for a change that only touches NZ data.

**int8 export of the v2 students** (dynamic per-channel int8 on MatMul, Gemm and the embedding Gather, as in §9.5; ONNX Runtime on a laptop CPU, 4 threads; `ml/results/m3v2_int8_*`). Held-out `test_full`, merged with the rules:

| Student | Doc leak fp32 → int8 | Name leak fp32 → int8 | Māori − Pākehā gap fp32 → int8 | int8 size | int8 ms / doc (CPU) |
|---|---:|---:|---:|---:|---:|
| DeBERTa-v3-small | 4.9% → 11.8% | 1.6% → 4.5% | +0.7 → +3.7 | 165 MB | 15 |
| ModernBERT-base | 2.6% → 25.9% | 1.1% → 11.4% | −6.3 → +4.2 | 153 MB | 45 |
| mDeBERTa-v3-base | 1.1% → 63.7% | 0.4% → 38.8% | −7.0 → −33.1 | 325 MB | 42 |

6. **Dynamic int8 is not usable as-is for any v2 student.** DeBERTa-small degrades least, but more than doubles its leakage and leaves the name-gap target; ModernBERT and mDeBERTa break. (fp32 timings in the tables above are GPU; int8 timings are laptop CPU.)
7. **The matrix multiplies are what break, not the embeddings.** For mDeBERTa, quantising only the embedding table (most of its 278M parameters are the 250k-token vocabulary) leaves leakage at 1.1% and shrinks the file from 1.1 GB to 537 MB; quantising only MatMul and Gemm gives 62.9%. So the next step is int8 embeddings with higher-precision encoder weights (fp16 would put mDeBERTa near 370 MB), or calibrated static quantisation / quantisation-aware training of the encoder.
8. **Weight-only quantisation of the encoder fixes it.** `tumataiti-ml quantise --encoder` keeps the embeddings int8 and either stores the encoder weights as fp16 (computed in fp32) or quantises them block-wise to int8 or int4 (MatMulNBits, 32 weights per scale), with activations left in fp32. On `test_full`, merged with the rules (`ml/results/m3v2_int4_*`, `m3v2_fp16_*`; laptop CPU, 4 threads):

   | Student | fp32 doc leak | int4 encoder: doc leak, size, ms / doc | fp16 encoder: doc leak, size, ms / doc |
   |---|---:|---:|---:|
   | DeBERTa-v3-small | 4.9% | 3.5%, **152 MB**, 40 | 4.6%, 201 MB, 39 |
   | ModernBERT-base | 2.6% | 4.0%, **111 MB**, 110 | 2.6%, 263 MB, 115 |
   | mDeBERTa-v3-base | 1.1% | **0.9%**, 298 MB, 84 | 1.1%, 396 MB, 59 |

   int4 matches fp32 within noise on every set, including the name audit (DeBERTa-small's Māori − Pākehā gap +1.2 points against +0.7 in fp32) and PII-Masking-300k. It is the default for shipping. It is 2–3× slower than the broken dynamic int8 because activations stay fp32, but under 0.1 s per document on a laptop. These students were trained with PII-Masking-300k, so they are timing and method results only (§9.1); latency and size carry over to the open-data students (same architectures and recipe), and their quantised accuracy is re-checked. DeBERTa-small's int4 timing overlapped a few minutes of in-browser testing and may be slightly high.
9. **Spans now widen to whole words** (both decoders: `student/encode.py` and `crates/tumataiti-student`). The demo showed the model splitting words, e.g. redacting only the "I" of "NHI" (tokenised "NH" + "I"). Applied to the stored v2 predictions, widening a span that starts or ends inside a run of letters and digits to the whole run lowered leakage everywhere: held-out document leak, merged with the rules, from 4.9% to 3.0% for DeBERTa-small and from 1.1% to 1.0% for mDeBERTa, and on PII-Masking-300k from 4.7% to 4.2% and 5.5% to 4.9%, with precision within a point. So most partial-word spans were real PII cut short. Trimming spans to whole words instead raised leakage, and so did dropping low-confidence mid-word spans before widening. The cost is that a stray fragment redacts its whole word: in the demo's checksum example the "I" of "NHI" turned the label itself into an ID redaction. So a span that is exactly an identifier field label (NHI, IRD, DOB, DL, SSN and similar; `FIELD_LABELS`) is dropped, which left leakage and precision unchanged on both test sets. Dropping every short span without digits instead was tested and rejected: it raised PII-Masking-300k leakage from 4.2% to 5.5%, because the model there splits IDs such as "ZZ 08 33 44 T" into pieces whose letter-only parts are real PII. Kinship terms tagged as names (Koro, Nan) still need hard negatives in the training data. Results in the tables above predate this change; runs from now on include it.

## 10. Research extensions: DP and FL

These are what make Tūmataiti a research project and not only a tool. They map to the DP/FL questions raised for Atamai.

### 10.0 Training pipeline (ECS GPU cluster)

Training runs on the VUW ECS GPU servers through the `task` spooler (one GPU per job, e.g. an RTX A5000; no host pinning; stay within the 5-concurrent-GPU limit).

1. **Data generation:** synthetic NZ / te reo documents from templates, name and place lists, and generated NZ identifiers (valid and invalid checksums), split by template and by name (§9.1).
2. **Label sources.** Template-slot gold and the rules are the primary supervision, not a safety net: the teacher has no `HEALTH`, `AFFILIATION` or NZ-government-ID category, so it cannot teach those. The teacher labels *unlabelled* text (e.g. real consented NZ text from M2), with checksum-verified rule matches as high-confidence labelling functions that override or filter its pseudo-labels. Where several weak sources disagree, aggregate them with a multi-source HMM (Lison et al. 2020, `skweak`) rather than majority vote, using template gold to estimate each source's accuracy. Self-training rounds on the student's own output are capped, because recursive training erodes rare forms such as macronised Māori names.
3. **Soft and hard labels.** The teacher is a token classifier that exposes per-token posteriors, so distillation can mix soft targets with Viterbi-decoded hard labels (structural KD, since the teacher decodes with constrained Viterbi and the student with softmax).
4. **Backbones compared:** DeBERTa-v3 (best accuracy per parameter), ModernBERT (fastest, English-only) and a multilingual encoder (mDeBERTa-v3 or XLM-R; better coverage of code-switched te reo but a larger download). Fine-tuning the teacher itself on NZ data is the upper bound; at ~0.8 GB in 4-bit it suits the proxy (M5) rather than the browser.
5. **Fine-tune** the student encoder for token classification. Expected cost: a few GPU-hours per run.
6. **Export and compress:** ONNX export and int8 quantisation (dynamic int8, keeping LayerNorm and the classifier in fp32 if static int8 hurts), then re-run the evaluation (§9) on the quantised model, tracking rare classes such as IRD and NHI separately.
4. **Retrieve** weights with `task fetch` and publish them as static files with a hash recorded in the release.

Every run records its config, data version, seed and metrics so results are reproducible.

### 10.1 Differentially private fine-tuning

Fine-tune the detector on sensitive community text with **DP-SGD** (e.g. Opacus) so the model weights do not memorise specific names or identifiers. Report privacy budget (ε, δ) against detection F1, following a standard reporting template (unit of privacy, accountant, δ ≪ 1/n). Run membership-inference (LiRA, reported as TPR at low FPR), canary-exposure (synthetic IRD and NHI numbers inserted as canaries) and one-run audits on the fine-tuned weights to check empirically.

Two caveats: for a token classifier the DP unit is the *example*, not the person, so a person whose details appear in many documents is less protected than ε suggests; and DP tends to cost rare classes most (te reo names, NZ IDs), so report the name-group gap under DP too. Inference latency must not depend on whether a word is in a vocabulary or gazetteer (a timing side-channel has been shown against NER redaction models).

### 10.2 Federated improvement

Each organisation or iwi runs Tūmataiti locally. Reviewer corrections (§6.5) become local training signal. Model updates, not data, are aggregated (e.g. with Flower), optionally with:

- **record-level DP enforced locally at each site** (inter-silo record-level DP, Lowy & Razaviyayn 2023), each site choosing its own ε. User- or site-level DP is not used: with 2–5 iwi it would need noise large enough to hide an entire iwi's contribution, destroying utility or giving little protection;
- a shared encoder with per-site personalised heads or adapters, since federated NER trails centralised training under non-IID label distributions;
- secure aggregation where it helps, noting it offers limited cover with only a handful of parties and that text can be recovered from language-model updates (hence local DP).

Research questions: how much does federated adaptation close the te reo gap? What is the privacy/utility trade-off at realistic numbers of participating sites (likely few, with non-IID data)? Who governs the aggregated model? The aggregated model is itself derived data, so governance must cover who receives it, per-iwi withdrawal and unlearning. That goes to the kaitiaki/legal workstream.

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
| A response echoes a *valid* placeholder into a dangerous context (a URL, markdown image, tool argument or code), so rehydration sends the real value somewhere | Rehydrate for display only; never inside URLs, tool calls or code; tested in M5 (no published work covers this attack) |
| RAG chunks sent to the cloud with inconsistent placeholders across chunks | One placeholder vault per request covering the query and every retrieved chunk |
| Demo page leaks typed text | Static hosting, no backend, CSP `connect-src 'self'`, offline mode, no analytics (§7.1) |
| Tampered model weights on the demo site | Same-origin weights pinned by hash |

## 12. Prototype milestones

| Phase | Deliverable | Rough effort |
|---|---|---|
| M0 | Repo scaffold, policy schema, NZ rule detectors in Rust with tests, WebAssembly build, initial rules-only demo UI. **Done (prototype), 2026-11-03** | 1–2 weeks |
| M1 | Eval harness; teacher/baseline (`openai/privacy-filter`) on public data; synthetic NZ data generator; Python bindings for the rules. **Done, 2026-11-04** (Presidio and GLiNER comparators still to add; results in §9.4) | 2 weeks |
| M2 | NZ / te reo test set, co-designed with community and legal workstream. Brought forward: a small consented, human-annotated set (~200 documents) as early as possible, because fine-tuned encoders overtake the zero-shot teacher with roughly 100–1,000 labelled examples and only human-labelled data supports headline claims | 3–4 weeks (parallel) |
| M3 | Generator v1 with held-out templates and names; three student backbones trained on ECS; evaluated against teacher on held-out splits and the counterfactual name audit; ONNX int8 export. **First pass done, 2026-11-04** (results §9.5); **data v2 done** (balanced names and failure-mode templates; held-out doc leak 1.1–4.9%, §9.6). v2 students exported to ONNX: dynamic int8 doubles DeBERTa-small's leakage and breaks ModernBERT and mDeBERTa, and the encoder MatMuls, not the embeddings, are the cause (§9.6). Open: int8 embeddings with an fp16 or calibrated encoder, a held-out set with genres unseen by v1 and v2, fine-tune the teacher as an upper bound, soft-label distillation once unlabelled real text exists | 2–3 weeks |
| M4 | Live browser demo (§7): animations, presets, offline mode; ships with rules + interim model, then swaps in the M3 student | 2–3 weeks (UI can start after M0) |
| M5 | Local proxy with pseudonymisation, vault, streaming rehydration; minimal review UI; placeholder-echo attack tests; utility ablation of placeholders vs realistic surrogates vs generalisation, including RAG (replacing dates and numbers is known to break reasoning) | 2–3 weeks |
| M6 | DP-SGD fine-tuning, federated simulation (2–5 synthetic sites), Atamai integration; results report | 4–6 weeks |

## 13. Open questions for the team

1. **Integration point:** does Atamai call cloud models from a server (then the gateway runs on an iwi/HTM-controlled server) or from the client (then it runs on the user's device)? This decides where "local" is.
2. **RAG corpus:** is the retrieval store itself already sanitised, or does redaction need to run on every retrieved chunk at query time?
3. **Governance:** who sets and approves redaction policy for `AFFILIATION`, `HEALTH` and restricted mātauranga? (Legal / community workstreams.)
4. **Data for the NZ test set:** can we use any real (consented) documents, or synthetic only for v0?
5. **Provider agreements:** what retention/zero-data-retention terms do we have with each cloud provider? These affect how conservative the default policy must be.
6. **Reporting:** how should redaction stats appear in Atamai's report outputs (link to the reporting workstream)?
7. **Demo hosting and branding:** where should the public demo live (HTM, VUW, or a project domain), and what design and brand guidance applies (design team)?
8. **Te reo data sourcing and release:** te reo lexicons and evaluation data must not come from Kaitiakitanga-licensed resources (e.g. Papa Reo) without agreement. Under what terms should Tūmataiti's own te reo artefacts (name lists, the NZ test set, a te reo-tuned model) be released? The repository is currently public under Apache 2.0.

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

From the literature review (`reports/`; check each against its spot-check table before citing):

- Pilán et al., *The Text Anonymization Benchmark (TAB)*, Computational Linguistics 2022 — entity-level recall over all mentions
- Lison et al., *Named Entity Recognition without Labelled Data: A Weak Supervision Approach*, ACL 2020 — multi-source HMM aggregation
- Lowy & Razaviyayn, *Private Federated Learning Without a Trusted Server*, ICLR 2023 — inter-silo record-level DP
- Mansfield et al., *Behind the Mask: Demographic Bias in Name Detection for PII Masking*, LT-EDI 2022 — name-group audit method
- Staab et al., *Beyond Memorization: Violating Privacy via Inference with LLMs*, ICLR 2024 — redaction is not anonymisation
- Yang & Garibaldi 2015 (i2b2 2014 winner) — rules for formats, models for names, the hybrid precedent

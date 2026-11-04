# Results

## M3: data v2 students (2026-11-04)

Summary and findings are in [SPEC.md §9.6](../../SPEC.md). Same evaluation files as M3 v1; each table shows the v1 student (`<model>-v1`) beside the v2 one.

- [m3v2_nz_test_full.md](m3v2_nz_test_full.md): held-out templates and names
- [m3v2_nz_test_names.md](m3v2_nz_test_names.md): training templates, held-out names
- [m3v2_pii300k_en_val.md](m3v2_pii300k_en_val.md): PII-Masking-300k validation
- [m3v2_names_counterfactual.md](m3v2_names_counterfactual.md): counterfactual name audit
- `m3v2_int8_*`: the same sets for the v2 students against their dynamic int8 ONNX versions (run on a laptop CPU)
- `m3v2_int4_*`: against int8 embeddings with a block-wise int4 encoder (the shipping recipe); `m3v2_fp16_nz_test_full.*`: an fp16 encoder (held-out set only)

Data: `scripts/make_data_v2.sh`. Training: `DATA=v2 scripts/ecs_student.sh` (writes `runs/m3-v2/`). Scoring: `RUNS=runs/m3-v2 TAG=m3v2 MODELS="openai-privacy-filter deberta-v3-small-v1 deberta-v3-small modernbert-base-v1 modernbert-base mdeberta-v3-base-v1 mdeberta-v3-base" scripts/score_m3.sh`. ONNX: `RUNS=runs/m3-v2 scripts/ecs_export.sh NAME` on ECS, then `scripts/local_int8.sh runs/m3-v2 NAME` locally (quantise and predict; scored with `TAG=m3v2_int8`). `scripts/int8_ablation.sh` quantises only the embeddings or only the matrix multiplies.

## M3: student models (2026-11-04)

Summary and findings are in [SPEC.md §9.5](../../SPEC.md).

- [m3_nz_test_full.md](m3_nz_test_full.md): NZ synthetic v1, held-out templates **and** names (the headline synthetic test)
- [m3_nz_test_names.md](m3_nz_test_names.md): training templates, held-out names
- [m3_pii300k_en_val.md](m3_pii300k_en_val.md): PII-Masking-300k validation (students were trained on its train split, so this is in-distribution for them, not for the teacher)
- [m3_names_counterfactual.md](m3_names_counterfactual.md): counterfactual name audit
- `*.json`: full metrics

Students were trained on ECS (one RTX A5000 each, 3 epochs, seed 0, deterministic CUDA, fp32 master weights with bf16 autocast) on `nz_train` (8,000 synthetic documents) plus PII-Masking-300k English train (29,908). Data: `scripts/make_data_v1.sh`. Training: `scripts/ecs_student.sh`. Teacher: `scripts/ecs_teacher.sh`. ONNX: `scripts/ecs_export.sh`, then `tumataiti-ml quantise`. Scoring: `scripts/score_m3.sh`. `deberta-v3-small-int8` was quantised per-tensor; per-channel (now the default) was slightly better and is described in SPEC §9.5.

## M1: baseline results

Generated 2026-11-04 from commit b9d1dd8 (the generator has changed since). Summary and findings are in [SPEC.md §9.4](../../SPEC.md).

- [m1_nz_synth_v0.md](m1_nz_synth_v0.md): NZ synthetic v0, 1,600 documents
- [m1_pii300k.md](m1_pii300k.md): PII-Masking-300k, English validation, 7,946 documents
- [m1_names.md](m1_names.md): name leak rate by community (NZ synthetic v0)
- `*.json`: full metrics, including counts and timings

Detectors:

- `rules`: the Rust rules at the default threshold (0.5); labelled IDs that fail their check digit are redacted, unlabelled ID-shaped codes are not
- `openai-privacy-filter`: the teacher with constrained BIOES Viterbi decoding at the released default operating point (all transition biases zero), bf16 on one RTX A5000
- `rules+openai-privacy-filter`: both, merged as the Rust merge does (overlaps become one span)

## Reproduce

From `ml/`:

```bash
uv sync --extra rules
uv run tumataiti-ml generate --n 1600 --seed 0 --out data/nz_synth_v0.jsonl
uv run tumataiti-ml prepare-pii300k --out data/pii300k_en_val.jsonl
uv run tumataiti-ml predict --detector rules --gold data/nz_synth_v0.jsonl --out runs/rules/nz_synth_v0.jsonl
```

The teacher runs on the ECS GPU cluster:

```bash
task sync && task submit -t "RTX A5000" -n tumataiti-teacher-eval -- ./scripts/ecs_teacher.sh
task fetch runs/openai-privacy-filter
```

Then combine and score:

```bash
uv run tumataiti-ml combine --primary runs/rules/nz_synth_v0.jsonl --secondary runs/openai-privacy-filter/nz_synth_v0.jsonl --out runs/rules+openai-privacy-filter/nz_synth_v0.jsonl
uv run tumataiti-ml score --gold data/nz_synth_v0.jsonl --pred runs/*/nz_synth_v0.jsonl --markdown results/m1_nz_synth_v0.md
uv run tumataiti-ml names --gold data/nz_synth_v0.jsonl --pred runs/*/nz_synth_v0.jsonl
```

Synthetic data is identical on the laptop and the servers (same SHA-256), so offsets line up.

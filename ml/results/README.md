# M1 baseline results

Generated 2026-11-04. Summary and findings are in [SPEC.md §9.4](../../SPEC.md).

- [m1_nz_synth_v0.md](m1_nz_synth_v0.md): NZ synthetic v0, 1,600 documents
- [m1_pii300k.md](m1_pii300k.md): PII-Masking-300k, English validation, 7,946 documents
- [m1_names.md](m1_names.md): name leak rate by community (NZ synthetic v0)
- `*.json`: full metrics, including counts and timings

Detectors:

- `rules`: the Rust rules at the default threshold (0.5), so labelled-but-invalid IDs are flagged and count as leaks
- `rules-incl-flagged`: the same, counting flagged spans as redacted (threshold 0.3)
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

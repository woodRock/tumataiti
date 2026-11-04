## NZ synthetic v1, training templates with held-out names (1,600 documents)

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **93.8%** | **0.0%** | **0.0%** | **1.6%** | **0.0%** | **0.0%** | **1.6%** |
| Span leak rate | 45.8% | 0.0% | 0.0% | 0.3% | 0.0% | 0.0% | 0.3% |
| Any-PII char precision | 89.4 | 100.0 | 100.0 | 100.0 | 93.7 | 93.6 | 93.6 |
| Any-PII char recall | 57.3 | 100.0 | 100.0 | 99.8 | 100.0 | 100.0 | 99.8 |
| Any-PII char F1 | 69.8 | 100.0 | 100.0 | 99.9 | 96.7 | 96.7 | 96.6 |
| Exact-span F1 (all categories) | 67.0 | 99.8 | 99.5 | 68.4 | 96.6 | 96.3 | 79.6 |
| Median ms per document | 0.04 | 27.15 | 96.33 | 59.56 | 27.19 | 96.38 | 59.60 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (3100 spans) | 100.0% | 0.0% | 0.0% | 0.9% | 0.0% | 0.0% | 0.9% |
| ADDRESS (700 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 0.0% | 0.0% | 0.2% | 0.0% | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 99.7 | 100.0 | 99.6 | 99.7 | 100.0 | 99.6 |
| ADDRESS | 0.0 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 99.9 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| URL | 51.0 | 100.0 | 100.0 | 100.0 | 51.0 | 51.0 | 51.0 |
| IP_ADDRESS | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 |
| ID | 96.8 | 100.0 | 99.9 | 100.0 | 96.8 | 96.7 | 96.8 |
| SECRET | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |

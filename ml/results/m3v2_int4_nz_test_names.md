## NZ synthetic v1, training templates with held-out names (1,600 documents)

| Metric | rules | deberta-v3-small | deberta-v3-small-int8-int4-block | modernbert-base | modernbert-base-int8-int4-block | mdeberta-v3-base | mdeberta-v3-base-int8-int4-block | rules+deberta-v3-small | rules+deberta-v3-small-int8-int4-block | rules+modernbert-base | rules+modernbert-base-int8-int4-block | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **93.8%** | **0.0%** | **0.0%** | **0.1%** | **0.9%** | **0.1%** | **0.0%** | **0.0%** | **0.0%** | **0.1%** | **0.2%** | **0.1%** | **0.0%** |
| Span leak rate | 45.8% | 0.0% | 0.0% | 0.0% | 0.2% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Any-PII char precision | 89.4 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 93.7 | 93.7 | 93.7 | 93.7 | 93.7 | 93.7 |
| Any-PII char recall | 57.3 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| Any-PII char F1 | 69.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 96.7 | 96.7 | 96.7 | 96.7 | 96.7 | 96.7 |
| Exact-span F1 (all categories) | 67.0 | 100.0 | 100.0 | 99.7 | 98.2 | 68.6 | 68.7 | 96.7 | 96.7 | 96.5 | 95.3 | 79.8 | 79.8 |
| Median ms per document | 0.04 | 8.89 | 33.30 | 13.47 | 98.83 | 17.19 | 80.49 | 8.93 | 33.35 | 13.52 | 98.87 | 17.23 | 80.53 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8-int4-block | modernbert-base | modernbert-base-int8-int4-block | mdeberta-v3-base | mdeberta-v3-base-int8-int4-block | rules+deberta-v3-small | rules+deberta-v3-small-int8-int4-block | rules+modernbert-base | rules+modernbert-base-int8-int4-block | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (3100 spans) | 100.0% | 0.0% | 0.0% | 0.1% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.1% | 0.0% | 0.0% |
| ADDRESS (700 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 11.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8-int4-block | modernbert-base | modernbert-base-int8-int4-block | mdeberta-v3-base | mdeberta-v3-base-int8-int4-block | rules+deberta-v3-small | rules+deberta-v3-small-int8-int4-block | rules+modernbert-base | rules+modernbert-base-int8-int4-block | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 99.9 |
| ADDRESS | 0.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| URL | 51.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 51.0 | 51.0 | 51.0 | 51.0 | 51.0 | 51.0 |
| IP_ADDRESS | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 96.8 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 96.8 | 96.8 | 96.8 | 96.8 | 96.8 | 96.8 |
| SECRET | 100.0 | 100.0 | 100.0 | 100.0 | 99.1 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |

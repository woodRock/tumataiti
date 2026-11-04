## mDeBERTa-v3-base (data v2), which ops are quantised: held-out templates and names

| Metric | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-gather | rules+mdeberta-v3-base-int8-matmul | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **1.1%** | **1.1%** | **62.9%** | **63.7%** |
| Span leak rate | 0.2% | 0.2% | 23.0% | 23.2% |
| Any-PII char precision | 93.7 | 93.7 | 94.2 | 94.3 |
| Any-PII char recall | 99.9 | 99.9 | 88.8 | 88.7 |
| Any-PII char F1 | 96.7 | 96.7 | 91.4 | 91.4 |
| Exact-span F1 (all categories) | 70.9 | 70.9 | 50.5 | 50.5 |
| Median ms per document | 17.26 | 70.88 | 44.19 | 42.04 |

Span leak rate by category (lower is better):

| Metric | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-gather | rules+mdeberta-v3-base-int8-matmul | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|
| PERSON (5250 spans) | 0.4% | 0.4% | 38.9% | 38.8% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 20.3% | 22.1% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-gather | rules+mdeberta-v3-base-int8-matmul | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|
| PERSON | 99.6 | 99.6 | 84.4 | 84.3 |
| ADDRESS | 100.0 | 100.0 | 96.9 | 96.4 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 99.9 | 99.9 | 100.0 | 100.0 |
| DATE | 86.0 | 86.0 | 99.8 | 99.9 |
| ID | 99.9 | 99.9 | 100.0 | 100.0 |

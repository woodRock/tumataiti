## NZ synthetic v1, held-out templates and names (1,750 documents)

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **0.7%** | **7.1%** | **9.3%** | **0.7%** | **2.7%** | **1.4%** |
| Span leak rate | 64.1% | 0.1% | 1.4% | 1.7% | 0.1% | 0.6% | 0.2% |
| Any-PII char precision | 88.8 | 98.9 | 93.1 | 97.8 | 94.4 | 92.4 | 93.8 |
| Any-PII char recall | 38.6 | 99.9 | 99.3 | 99.3 | 99.9 | 99.7 | 99.9 |
| Any-PII char F1 | 53.8 | 99.4 | 96.1 | 98.6 | 97.1 | 95.9 | 96.7 |
| Exact-span F1 (all categories) | 51.9 | 93.3 | 85.7 | 61.9 | 92.2 | 87.1 | 73.0 |
| Median ms per document | 0.05 | 29.44 | 103.71 | 78.23 | 29.48 | 103.76 | 78.27 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 0.2% | 1.0% | 0.5% | 0.2% | 1.0% | 0.5% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.2% | 16.4% | 28.4% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 98.3 | 94.4 | 97.6 | 98.3 | 94.4 | 97.6 |
| ADDRESS | 0.0 | 99.9 | 97.6 | 100.0 | 99.9 | 97.6 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 98.9 | 99.2 | 100.0 | 99.0 | 99.9 |
| DATE | 100.0 | 100.0 | 93.3 | 94.0 | 100.0 | 98.2 | 100.0 |
| ID | 100.0 | 100.0 | 99.9 | 98.4 | 100.0 | 100.0 | 99.9 |

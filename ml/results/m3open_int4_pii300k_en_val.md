## PII-Masking-300k, English validation

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **33.9%** | **50.8%** | **43.4%** | **32.2%** | **42.3%** | **38.9%** |
| Span leak rate | 85.4% | 12.4% | 21.1% | 14.6% | 11.3% | 17.7% | 12.7% |
| Any-PII char precision | 96.5 | 95.0 | 93.5 | 94.9 | 94.9 | 93.5 | 94.8 |
| Any-PII char recall | 20.1 | 92.3 | 84.1 | 88.8 | 93.0 | 87.2 | 90.6 |
| Any-PII char F1 | 33.2 | 93.6 | 88.5 | 91.8 | 93.9 | 90.2 | 92.6 |
| Exact-span F1 (all categories) | 23.9 | 77.0 | 68.0 | 70.3 | 77.5 | 71.1 | 71.6 |
| Median ms per document | 0.01 | 52.09 | 115.26 | 98.87 | 52.10 | 115.27 | 98.88 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 4.9% | 22.3% | 4.3% | 4.9% | 22.2% | 4.3% |
| ADDRESS (8852 spans) | 100.0% | 18.5% | 28.4% | 17.0% | 18.5% | 28.4% | 17.0% |
| EMAIL (2612 spans) | 0.6% | 1.0% | 18.0% | 2.4% | 0.1% | 0.1% | 0.1% |
| PHONE (1997 spans) | 99.3% | 2.0% | 3.3% | 1.7% | 2.0% | 3.2% | 1.7% |
| IP_ADDRESS (2166 spans) | 50.4% | 0.6% | 1.4% | 0.6% | 0.6% | 0.6% | 0.6% |
| DATE (2317 spans) | 66.0% | 68.6% | 94.6% | 82.6% | 54.2% | 63.6% | 58.4% |
| ID (10054 spans) | 97.0% | 3.6% | 7.7% | 13.0% | 3.6% | 7.6% | 12.4% |
| SECRET (1620 spans) | 76.5% | 26.7% | 8.2% | 5.5% | 26.5% | 8.1% | 5.4% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 91.5 | 82.6 | 93.2 | 91.5 | 82.6 | 93.2 |
| ADDRESS | 0.0 | 89.8 | 83.9 | 92.0 | 89.8 | 83.9 | 92.0 |
| EMAIL | 98.1 | 97.1 | 89.7 | 96.8 | 97.3 | 94.1 | 97.4 |
| PHONE | 2.7 | 86.5 | 86.8 | 84.0 | 83.8 | 84.4 | 82.1 |
| IP_ADDRESS | 39.2 | 93.0 | 95.2 | 93.7 | 93.1 | 95.2 | 93.7 |
| DATE | 49.8 | 61.7 | 20.4 | 47.7 | 69.5 | 53.8 | 67.5 |
| ID | 2.9 | 92.8 | 91.1 | 85.8 | 92.0 | 90.4 | 85.6 |
| SECRET | 40.4 | 79.5 | 80.9 | 85.9 | 78.3 | 79.8 | 84.8 |

## PII-Masking-300k, English validation (7,946 documents)

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **34.2%** | **44.8%** | **42.1%** | **33.2%** | **36.7%** | **37.3%** |
| Span leak rate | 85.4% | 12.5% | 16.8% | 15.3% | 11.8% | 13.8% | 13.2% |
| Any-PII char precision | 96.5 | 95.0 | 94.5 | 94.9 | 94.9 | 94.4 | 94.8 |
| Any-PII char recall | 20.1 | 92.2 | 87.7 | 89.0 | 92.8 | 90.4 | 90.9 |
| Any-PII char F1 | 33.2 | 93.6 | 91.0 | 91.9 | 93.8 | 92.4 | 92.8 |
| Exact-span F1 (all categories) | 23.9 | 76.0 | 72.3 | 69.9 | 76.2 | 74.1 | 71.0 |
| Median ms per document | 0.01 | 49.28 | 131.55 | 98.90 | 49.29 | 131.56 | 98.91 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 8.2% | 12.9% | 5.9% | 8.1% | 12.9% | 5.9% |
| ADDRESS (8852 spans) | 100.0% | 17.0% | 21.1% | 24.6% | 17.0% | 21.1% | 24.6% |
| EMAIL (2612 spans) | 0.6% | 0.1% | 10.1% | 0.5% | 0.1% | 0.1% | 0.2% |
| PHONE (1997 spans) | 99.3% | 1.7% | 3.7% | 2.3% | 1.7% | 3.7% | 2.3% |
| IP_ADDRESS (2166 spans) | 50.4% | 0.7% | 1.5% | 0.7% | 0.6% | 0.8% | 0.6% |
| DATE (2317 spans) | 66.0% | 64.6% | 98.1% | 90.9% | 53.7% | 64.7% | 61.0% |
| ID (10054 spans) | 97.0% | 3.4% | 5.1% | 6.2% | 3.4% | 5.1% | 6.0% |
| SECRET (1620 spans) | 76.5% | 35.2% | 10.6% | 5.2% | 34.8% | 10.6% | 5.2% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 90.1 | 83.5 | 91.1 | 90.1 | 83.4 | 91.1 |
| ADDRESS | 0.0 | 90.3 | 86.0 | 87.6 | 90.3 | 86.0 | 87.6 |
| EMAIL | 98.1 | 97.2 | 95.4 | 97.3 | 97.2 | 97.0 | 97.3 |
| PHONE | 2.7 | 83.7 | 88.1 | 86.4 | 81.3 | 85.2 | 83.3 |
| IP_ADDRESS | 39.2 | 91.8 | 94.6 | 95.7 | 91.7 | 94.6 | 95.6 |
| DATE | 49.8 | 63.9 | 13.5 | 34.3 | 70.8 | 55.6 | 62.6 |
| ID | 2.9 | 91.6 | 93.1 | 91.6 | 90.8 | 92.3 | 90.9 |
| SECRET | 40.4 | 74.1 | 81.1 | 89.2 | 72.5 | 79.7 | 87.5 |

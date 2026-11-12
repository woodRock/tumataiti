## Deployed and retrained, int4: pii300k_en_val

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| **Document leak rate** (lower is better) | **32.2%** | **33.1%** |
| Span leak rate | 11.3% | 11.1% |
| Any-PII char precision | 94.9 | 94.5 |
| Any-PII char recall | 93.0 | 93.3 |
| Any-PII char F1 | 93.9 | 93.9 |
| Exact-span F1 (all categories) | 77.5 | 75.3 |
| Median ms per document | 52.10 | 89.12 |

Span leak rate by category (lower is better):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON (5808 spans) | 4.9% | 7.3% |
| ADDRESS (8852 spans) | 18.5% | 16.6% |
| EMAIL (2612 spans) | 0.1% | 0.1% |
| PHONE (1997 spans) | 2.0% | 1.5% |
| IP_ADDRESS (2166 spans) | 0.6% | 0.6% |
| DATE (2317 spans) | 54.2% | 56.7% |
| ID (10054 spans) | 3.6% | 3.3% |
| SECRET (1620 spans) | 26.5% | 21.1% |

Character-level F1 by category (category must match):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON | 91.5 | 88.3 |
| ADDRESS | 89.8 | 87.7 |
| EMAIL | 97.3 | 97.3 |
| PHONE | 83.8 | 81.0 |
| IP_ADDRESS | 93.1 | 93.9 |
| DATE | 69.5 | 71.4 |
| ID | 92.0 | 91.7 |
| SECRET | 78.3 | 81.5 |

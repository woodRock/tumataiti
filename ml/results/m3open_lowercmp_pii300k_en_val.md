## Deployed and retrained, int4: pii300k_en_val

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| **Document leak rate** (lower is better) | **33.2%** | **39.7%** |
| Span leak rate | 11.8% | 14.0% |
| Any-PII char precision | 94.9 | 94.8 |
| Any-PII char recall | 92.8 | 91.0 |
| Any-PII char F1 | 93.8 | 92.9 |
| Exact-span F1 (all categories) | 76.2 | 75.5 |
| Median ms per document | 49.29 | 80.39 |

Span leak rate by category (lower is better):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON (5808 spans) | 8.1% | 14.1% |
| ADDRESS (8852 spans) | 17.0% | 22.3% |
| EMAIL (2612 spans) | 0.1% | 0.1% |
| PHONE (1997 spans) | 1.7% | 1.3% |
| IP_ADDRESS (2166 spans) | 0.6% | 0.6% |
| DATE (2317 spans) | 53.7% | 63.0% |
| ID (10054 spans) | 3.4% | 3.5% |
| SECRET (1620 spans) | 34.8% | 19.5% |

Character-level F1 by category (category must match):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON | 90.1 | 86.4 |
| ADDRESS | 90.3 | 87.0 |
| EMAIL | 97.2 | 97.3 |
| PHONE | 81.3 | 81.6 |
| IP_ADDRESS | 91.7 | 94.7 |
| DATE | 70.8 | 66.5 |
| ID | 90.8 | 91.9 |
| SECRET | 72.5 | 82.6 |

## pii300k_en_val: review layer without and with transaction labels

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| **Document leak rate** (lower is better) | **32.3%** | **32.3%** |
| Span leak rate | 11.4% | 11.4% |
| Any-PII char precision | 94.9 | 94.9 |
| Any-PII char recall | 93.0 | 93.0 |
| Any-PII char F1 | 93.9 | 93.9 |
| Exact-span F1 (all categories) | 77.9 | 77.9 |
| Median ms per document | 17.09 | 17.09 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON (5808 spans) | 5.4% | 5.4% |
| ADDRESS (8852 spans) | 18.4% | 18.4% |
| EMAIL (2612 spans) | 0.1% | 0.1% |
| PHONE (1997 spans) | 1.9% | 1.9% |
| IP_ADDRESS (2166 spans) | 0.6% | 0.6% |
| DATE (2317 spans) | 56.3% | 56.3% |
| ID (10054 spans) | 3.4% | 3.4% |
| SECRET (1620 spans) | 24.1% | 24.1% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON | 91.3 | 91.3 |
| ADDRESS | 90.1 | 90.1 |
| EMAIL | 97.3 | 97.3 |
| PHONE | 84.6 | 84.6 |
| IP_ADDRESS | 93.4 | 93.4 |
| DATE | 69.0 | 69.0 |
| ID | 92.3 | 92.3 |
| SECRET | 78.7 | 78.7 |

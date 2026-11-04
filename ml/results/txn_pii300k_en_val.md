## pii300k_en_val: review layer without and with transaction labels

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| **Document leak rate** (lower is better) | **31.4%** | **31.4%** |
| Span leak rate | 11.0% | 11.0% |
| Any-PII char precision | 94.9 | 94.9 |
| Any-PII char recall | 93.2 | 93.2 |
| Any-PII char F1 | 94.0 | 94.0 |
| Exact-span F1 (all categories) | 76.8 | 76.8 |
| Median ms per document | 11.91 | 11.91 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON (5808 spans) | 7.4% | 7.4% |
| ADDRESS (8852 spans) | 15.1% | 15.1% |
| EMAIL (2612 spans) | 0.1% | 0.1% |
| PHONE (1997 spans) | 1.8% | 1.8% |
| IP_ADDRESS (2166 spans) | 0.6% | 0.6% |
| DATE (2317 spans) | 54.3% | 54.3% |
| ID (10054 spans) | 3.2% | 3.2% |
| SECRET (1620 spans) | 31.4% | 31.4% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON | 89.9 | 89.9 |
| ADDRESS | 90.6 | 90.6 |
| EMAIL | 97.2 | 97.2 |
| PHONE | 82.1 | 82.1 |
| IP_ADDRESS | 92.1 | 92.1 |
| DATE | 70.9 | 70.9 |
| ID | 91.3 | 91.3 |
| SECRET | 74.4 | 74.4 |

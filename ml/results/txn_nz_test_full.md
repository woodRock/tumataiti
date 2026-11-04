## nz_test_full: review layer without and with transaction labels

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| **Document leak rate** (lower is better) | **0.3%** | **0.3%** |
| Span leak rate | 0.1% | 0.1% |
| Any-PII char precision | 94.4 | 94.4 |
| Any-PII char recall | 100.0 | 100.0 |
| Any-PII char F1 | 97.1 | 97.1 |
| Exact-span F1 (all categories) | 92.2 | 92.2 |
| Median ms per document | 11.43 | 11.43 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON (5250 spans) | 0.1% | 0.1% |
| ADDRESS (1000 spans) | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON | 98.5 | 98.5 |
| ADDRESS | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 |
| ID | 100.0 | 100.0 |

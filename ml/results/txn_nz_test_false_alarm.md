## nz_test_false_alarm: review layer without and with transaction labels

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| **Document leak rate** (lower is better) | **0.0%** | **0.0%** |
| Span leak rate | 0.0% | 0.0% |
| Any-PII char precision | 77.0 | 80.3 |
| Any-PII char recall | 100.0 | 100.0 |
| Any-PII char F1 | 87.0 | 89.1 |
| Exact-span F1 (all categories) | 65.6 | 67.8 |
| Median ms per document | 10.71 | 10.71 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON (800 spans) | 0.0% | 0.0% |
| ADDRESS (100 spans) | 0.0% | 0.0% |
| EMAIL (100 spans) | 0.0% | 0.0% |
| PHONE (200 spans) | 0.0% | 0.0% |
| ID (200 spans) | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON | 91.6 | 91.6 |
| ADDRESS | 97.5 | 97.5 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 99.9 | 99.9 |
| ID | 50.9 | 58.0 |
